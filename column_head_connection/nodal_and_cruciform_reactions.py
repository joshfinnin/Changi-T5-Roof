"""
Script for extracting the member forces at each corner node on the column head connections.
The reactions from each of the beams that are not internal to the column head are summed for each combination in
the global axes.  The resultant forces for each combination are then reported back in two ways; in the global axes,
and in the axes of the cruciform (45 degrees to global).

Target groups:
Leaf 03-07\03-07\1D\G01 PrimaryTop
Leaf 03-07\03-07\1D\G02 PrimaryBot
Leaf 03-07\03-07\1D\G03 PrimaryDiag
Leaf 03-07\03-07\1D\G04 PrimaryVert
Leaf 03-07\03-07\1D\G27 BracingPlanTop
Leaf 03-07\03-07\1D\G28 BracingPlanBot
"""

import duckdb
import csv
from inputs import BF_EXT_ALS_PARQ_FILE_DICT, node_cos_ang_dicts, node_sin_ang_dicts, NODE_DICT, COL_HEAD_LOCATION, CRUCIFORM_OUTPUT_FP, NODAL_OUTPUT_FP, NODAL_FORCE_PARQUET


def get_direction_coefficients(location: str, bp_parq_files: dict) -> str:
    """Function for determining the direction coefficient for each of the cruciform plates.
    This is essentially a rotation of axes for each of the nodes based on their relative position with respect to
    the column head."""
    direction_coefficients = ", ".join(
        f"({node}, '{model}', {node_cos_ang_dicts[location][node]}, {node_sin_ang_dicts[location][node]})"
        for node in list(NODE_DICT[location])
        for model in bp_parq_files.keys())

    return direction_coefficients


def get_differential_sum_query(key: str):
    query_sum_dict = {"Fx_MAX": "SUM(Fx) AS Fx",
                      }

    return query_sum_dict[key]


def get_combined_worst_force_envelope(direction_coefficients: str, nodal_force_parquet_fp: str, transform=False):
    """Function for getting the extrema load conditions."""

    if not transform:
        combined_force_envelope_query = f"""
        WITH NODAL_BEAM_FORCES AS
        (SELECT * FROM '{nodal_force_parquet_fp}'),

        COMBO_RESULTS AS
        (
        SELECT 
        Node,
        ResultCaseName,
        Model,
        SUM(Fx) AS Fx, SUM(Fy) AS Fy, SUM(Fz) AS Fz,
        SUM(Mx) AS Mx, SUM(My) AS My, SUM(Mz) AS Mz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2) AS Fxy,
        SQRT(SUM(Fx)**2 + SUM(Fz)**2) AS Fxz,
        SQRT(SUM(Fy)**2 + SUM(Fz)**2) AS Fyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2) AS Mxy,
        SQRT(SUM(Mx)**2 + SUM(Mz)**2) AS Mxz,
        SQRT(SUM(My)**2 + SUM(Mz)**2) AS Myz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2 + SUM(Fz)**2) AS Fxyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2 + SUM(Mz)**2) AS Mxyz
        FROM NODAL_BEAM_FORCES AS BF
        GROUP BY Node, Model, ResultCaseName),

        EXTREMAS AS (SELECT
        Node,
        ResultCaseName,
        Model,
        Fx, Fy, Fz, Mx, My, Mz, Fxy, Fxz, Fyz, Mxy, Mxz, Myz, Fxyz, Mxyz,
        MAX(Fx) OVER() AS Fx_MAX, MIN(Fx) OVER() AS Fx_MIN,
        MAX(Fy) OVER() AS Fy_MAX, MIN(Fy) OVER() AS Fy_MIN,
        MAX(Fz) OVER() AS Fz_MAX, MIN(Fz) OVER() AS Fz_MIN,
        MAX(Mx) OVER() AS Mx_MAX, MIN(Mx) OVER() AS Mx_MIN,
        MAX(My) OVER() AS My_MAX, MIN(My) OVER() AS My_MIN,
        MAX(Mz) OVER() AS Mz_MAX, MIN(Mz) OVER() AS Mz_MIN,
        MAX(Fxy) OVER() AS Fxy_MAX, MAX(Fxz) OVER() AS Fxz_MAX, MAX(Fyz) OVER() AS Fyz_MAX,
        MAX(Mxy) OVER() AS Mxy_MAX, MAX(Mxz) OVER() AS Mxz_MAX, MAX(Myz) OVER() AS Myz_MAX,
        MAX(Fxyz) OVER() AS Fxyz_MAX, MAX(Mxyz) OVER() AS Mxyz_MAX
        FROM COMBO_RESULTS)

        SELECT
        Node,
        ResultCaseName,
        Model,
        Fx, Fy, Fz, Mx, My, Mz, Fxy, Fxz, Fyz, Mxy, Mxz, Myz, Fxyz, Mxyz
        FROM EXTREMAS
        WHERE
        Fx IN (Fx_MAX, Fx_MIN) OR
        Fy IN (Fy_MAX, Fy_MIN) OR
        Fz IN (Fz_MAX, Fz_MIN) OR
        Mx IN (Mx_MAX, Mx_MIN) OR
        My IN (My_MAX, My_MIN) OR
        Mz IN (Mz_MAX, Mz_MIN) OR
        Fxy = Fxy_MAX OR
        Fxz = Fxz_MAX OR
        Fyz = Fyz_MAX OR
        Mxy = Mxy_MAX OR
        Mxz = Mxz_MAX OR
        Myz = Myz_MAX OR
        Fxyz = Fxyz_MAX OR
        Mxyz = Mxyz_MAX
        ORDER BY Node, ResultCaseName"""

    else:

        # The below are multipliers for the transformation of forces to the column head axes.
        # The directional multipliers are based on whether they are to the North or South of the
        # column head, and whether they occur to the East or West of the column head.
        combined_force_envelope_query = f"""
        WITH NODAL_BEAM_FORCES AS (SELECT * FROM '{nodal_force_parquet_fp}'),

        COMBO_RESULTS AS
        (
        SELECT 
        Node,
        ResultCaseName,
        Model,
        SUM(Fx) AS Fx, SUM(Fy) AS Fy, SUM(Fz) AS Fz,
        SUM(Mx) AS Mx, SUM(My) AS My, SUM(Mz) AS Mz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2) AS Fxy,
        SQRT(SUM(Fx)**2 + SUM(Fz)**2) AS Fxz,
        SQRT(SUM(Fy)**2 + SUM(Fz)**2) AS Fyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2) AS Mxy,
        SQRT(SUM(Mx)**2 + SUM(Mz)**2) AS Mxz,
        SQRT(SUM(My)**2 + SUM(Mz)**2) AS Myz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2 + SUM(Fz)**2) AS Fxyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2 + SUM(Mz)**2) AS Mxyz
        FROM NODAL_BEAM_FORCES AS BF
        GROUP BY Node, Model, ResultCaseName),

        DIRECTION_COEFFICIENTS AS (SELECT * FROM (VALUES {direction_coefficients}) AS dc(Node, Model, cos_coeff, sin_coeff)),

        ROTATED_SUMS AS (SELECT
        COMBO_RESULTS.Node,
        COMBO_RESULTS.ResultCaseName,
        COMBO_RESULTS.Model,
        cos_coeff * Fx - sin_coeff * Fy AS N,
        sin_coeff * Fx + cos_coeff * Fy AS Vy,
        Fz AS Vz,
        cos_coeff * Mx - sin_coeff * My AS T,
        sin_coeff * Mx + cos_coeff * My AS Myy,
        Mz AS Mzz,
        Fxy AS Vxy,
        SQRT((cos_coeff * Fx - sin_coeff * Fy)**2 + Fz**2) AS Vxz,
        SQRT((sin_coeff * Fx + cos_coeff * Fy)**2 + Fz**2) AS Vyz,
        SQRT((cos_coeff * Mx - sin_coeff * My)**2 + (sin_coeff * Mx + cos_coeff * My)**2) AS Mxy,
        SQRT((cos_coeff * Mx - sin_coeff * My)**2 + Mz**2) AS Mxz,
        SQRT((sin_coeff * Mx + cos_coeff * My)**2 + Mz**2) AS Myz,
        SQRT((cos_coeff * Fx - sin_coeff * Fy)**2 + (sin_coeff * Fx + cos_coeff * Fy)**2 + Fz**2) AS Vxyz,
        SQRT((cos_coeff * Mx - sin_coeff * My)**2 + (sin_coeff * Mx + cos_coeff * My)**2 + Mz**2) AS Mxyz
        FROM COMBO_RESULTS
        JOIN DIRECTION_COEFFICIENTS AS DC ON DC.Node = COMBO_RESULTS.Node AND DC.Model = COMBO_RESULTS.Model
        ),

        EXTREMAS AS (SELECT
        MAX(N) AS N_MAX, MIN(N) AS N_MIN,
        MAX(Vy) AS Vy_MAX, MIN(Vy) AS Vy_MIN,
        MAX(Vz) AS Vz_MAX, MIN(Vz) AS Vz_MIN,
        MAX(T) AS T_MAX, MIN(T) AS T_MIN,
        MAX(Myy) AS Myy_MAX, MIN(Myy) AS Myy_MIN,
        MAX(Mzz) AS Mzz_MAX, MIN(Mzz) AS Mzz_MIN,
        MAX(Vxy) AS Vxy_MAX,
        MAX(Vxz) AS Vxz_MAX,
        MAX(Vyz) AS Vyz_MAX,
        MAX(Mxy) AS Mxy_MAX,
        MAX(Mxz) AS Mxz_MAX,
        MAX(Myz) AS Myz_MAX,
        MAX(Vxyz) AS Vxyz_MAX,
        MAX(Mxyz) AS Mxyz_MAX
        FROM ROTATED_SUMS)

        SELECT
        ROTATED_SUMS.Node,
        ResultCaseName,
        Model,
        N, Vy, Vz, T, Myy, Mzz, Vxy, Vxz, Vyz, Mxy, Mxz, Myz, Vxyz, Mxyz
        FROM ROTATED_SUMS
        CROSS JOIN EXTREMAS AS EX
        WHERE
        N IN (N_MAX, N_MIN) OR
        Vy IN (Vy_MAX, Vy_MIN) OR
        Vz IN (Vz_MAX, Vz_MIN) OR
        T IN (T_MAX, T_MIN) OR
        Myy IN (Myy_MAX, Myy_MIN) OR
        Mzz IN (Mzz_MAX, Mzz_MIN) OR
        Vxy = Vxy_MAX OR
        Vxz = Vxz_MAX OR
        Vyz = Vyz_MAX OR
        Mxy = Mxy_MAX OR
        Mxz = Mxz_MAX OR
        Myz = Myz_MAX OR
        Vxyz = Vxyz_MAX OR
        Mxyz = Mxyz_MAX
        ORDER BY ROTATED_SUMS.Node, ResultCaseName"""

    return combined_force_envelope_query


def get_differential_load_combinations(bp_parq_files: dict, node_pairs: dict, nodal_force_parquet_fp: str) -> str:
    """Function for getting the maximum differential load combinations for the different conditions."""
    # How do we do this?
    # We start with the nodal results

    query_key = {"Fx_MAX": "MAX(Fx) AS Fx_MAX"}

    fx_diff_query = f"""WITH DIFFS AS (SELECT 
                        ResultCaseName, 
                        Model,
                        SUM(Fx) FILTER (WHERE Node IN ())
                        - 
                        SUM(Fx) FILTER (WHERE Node IN ()) AS Fx_DIFF
                        FROM COMBO_RESULTS
                        GROUP BY ResultCaseName, Model
                        )
                        SELECT ResultCaseName, Model, Fx_DIFF
                        FROM DIFFS 
                        WHERE Fx_DIFF IN (SELECT MAX(Fx_DIFF) FROM DIFFS)
                        OR Fx_DIFF IN (SELECT MIN(Fx_DIFF) FROM DIFFS)"""

    query = f"""WITH NODAL_BEAM_FORCES AS (SELECT * FROM '{nodal_force_parquet_fp}'),
                COMBO_RESULTS AS (
                SELECT
                Node,
                ResultCaseName,
                Model,
                SUM(Fx) AS Fx,
                SUM(Fy) AS Fy,
                SUM(Fz) AS Fz,
                SUM(Mx) AS Mx,
                SUM(My) AS My,
                SUM(Mz) AS Mz
                FROM NODAL_BEAM_FORCES
                GROUP BY Node, Model, ResultCaseName
                )
                """


if __name__ == '__main__':

    direction_coefficients = get_direction_coefficients(COL_HEAD_LOCATION, BF_EXT_ALS_PARQ_FILE_DICT)

    with duckdb.connect() as conn:

        with open(CRUCIFORM_OUTPUT_FP, 'w+', newline='') as cruciform_output_file:

            # Get a writer for the cruciform_output_file and write the headers
            headers = ("Node", "ResultCaseName", "Model",
                           "N", "Vy", "Vz", "T", "Myy", "Mzz",
                           "Vxy", "Vxz", "Vyz", "Mxy", "Mxz", "Myz", "Vxyz", "Mxyz")

            writer = csv.writer(cruciform_output_file)
            writer.writerow(headers)

            # combined_full_nodal_force_query = f"""WITH FULL_BEAM_FORCES AS (SELECT * FROM '{beam_forces_parquet_fp}'),
            #         FULL_BEAM_PROPERTIES AS (SELECT * FROM '{property_parquet_fp}'),
            #         BEAM_ENDS AS (SELECT * FROM '{beam_ends_parquet_fp}'),
            #         NODAL_BEAM_FORCES AS (SELECT * FROM '{nodal_force_parquet_fp}')
            #         SELECT Node, ResultCaseName, Model, SUM(Fx), SUM(Fy), SUM(Fz), SUM(Mx), SUM(My), SUM(Mz)
            #         FROM NODAL_BEAM_FORCES
            #         GROUP BY Node, ResultCaseName, Model"""

            combined_worst_case_forces_query = get_combined_worst_force_envelope(direction_coefficients,
                                                                                 NODAL_FORCE_PARQUET,
                                                                                 transform=True)
            # full_nodal_force_query = get_full_combined_nodal_force_query(location,
            #                                                              bp_parq_files,
            #                                                              NODE_DICT,
            #                                                              target_groups,
            #                                                              excluded_beam_dict)

            # Write the results to cruciform_output_file
            results = conn.execute(combined_worst_case_forces_query).fetchall()
            writer.writerows(results)

        with open(NODAL_OUTPUT_FP, 'w+', newline='') as nodal_output_file:

            headers = ("Node", "ResultCaseName", "Model",
                       "Fx", "Fy", "Fz", "Mx", "My", "Mz",
                       "Fxy", "Fxz", "Fyz", "Mxy", "Mxz", "Myz", "Fxyz", "Mxyz")

            writer = csv.writer(nodal_output_file)
            writer.writerow(headers)

            combined_worst_nodal_force_query = get_combined_worst_force_envelope(direction_coefficients,
                                                                                 NODAL_FORCE_PARQUET,
                                                                                 transform=False)

            results = conn.execute(combined_worst_nodal_force_query).fetchall()
            writer.writerows(results)
