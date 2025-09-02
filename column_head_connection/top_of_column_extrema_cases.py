
"""
Script that finds the extrema combinations for the top of column for the design of the column head connection.
These combinations are only one subset of the combinations needed to design the column head.
Refer to other scripts for the worst case node differential forces, and the worst case individual corner node cases.
"""

import duckdb
import csv
from inputs import bf_ext_als_parq_files, bp_ext_als_parq_files, column_beam_number_dict


def get_column_query(location: str, bf_parq_files: dict) -> str:

    prequery = " UNION ALL ".join(f"""SELECT BeamNumber, ResultCaseName, '{model}' AS Model, Position, 
    Fx, Fy, Fz, Mx, My, Mz FROM '{bf_parq_files[model]}' 
    WHERE BeamNumber = {column_beam_number_dict[model][location]}""" for model in bf_parq_files.keys())

    query = f"""WITH FULL_BEAM_FORCES AS ({prequery}),

    COLUMN_FORCES AS 
    (SELECT BeamNumber, ResultCaseName, Model, Fx, Fy, Fz, Mx, My, Mz, 
    SQRT(Fx**2 + Fy**2) AS Fxy, SQRT(Fx**2 + Fz**2) AS Fxz, SQRT(Fy**2 + Fz**2) AS Fyz, 
    SQRT(Mx**2 + My**2) AS Mxy, SQRT(Mx**2 + Mz**2) AS Mxz, SQRT(My**2 + Mz**2) AS Myz, 
    SQRT(Fx**2 + Fy**2 + Fz**2) AS Fxyz, 
    SQRT(Mx**2 + My**2 + Mz**2) AS Mxyz 
    FROM FULL_BEAM_FORCES
    WHERE Position = 1.0 
    AND ResultCaseName NOT LIKE '%BIF%'),

    COLUMN_MAX_FORCES AS (SELECT
    MAX(Fx) AS Fx_MAX, MIN(Fx) AS Fx_MIN,
    MAX(Fy) AS Fy_MAX, MIN(Fy) AS Fy_MIN,
    MAX(Fz) AS Fz_MAX, MIN(Fz) AS Fz_MIN,
    MAX(Mx) AS Mx_MAX, MIN(Mx) AS Mx_MIN,
    MAX(My) AS My_MAX, MIN(My) AS My_MIN,
    MAX(Mz) AS Mz_MAX, MIN(Mz) AS Mz_MIN,
    MAX(Fxy) AS Fxy_MAX, MAX(Fxz) AS Fxz_MAX, MAX(Fyz) AS Fyz_MAX,
    MAX(Mxy) AS Mxy_MAX, MAX(Mxz) AS Mxz_MAX, MAX(Myz) AS Myz_MAX,
    MAX(Fxyz) AS Fxyz_MAX, MAX(Mxyz) AS Mxyz_MAX
    FROM COLUMN_FORCES)

    SELECT COLUMN_FORCES.BeamNumber, ResultCaseName, Model,
    Fx, Fy, Fz, 
    Mx, My, Mz, 
    Fxy, Fxz, Fyz,
    Mxy, Mxz, Myz,
    Fxyz, Mxyz
    FROM COLUMN_FORCES
    CROSS JOIN COLUMN_MAX_FORCES AS CMF
    WHERE 
    Fx IN (CMF.Fx_MAX, CMF.Fx_MIN) OR
    Fy IN (CMF.Fy_MAX, CMF.Fy_MIN) OR
    Fz IN (CMF.Fz_MAX, CMF.Fz_MIN) OR
    Mx IN (CMF.Mx_MAX, CMF.Mx_MIN) OR
    My IN (CMF.My_MAX, CMF.My_MIN) OR
    Mz IN (CMF.Mz_MAX, CMF.Mz_MIN) OR
    Fxy = CMF.Fxy_MAX OR
    Fxz = CMF.Fxz_MAX OR
    Fyz = CMF.Fyz_MAX OR
    Mxy = CMF.Mxy_MAX OR
    Mxz = CMF.Mxz_MAX OR
    Myz = CMF.Myz_MAX OR
    Fxyz = CMF.Fxyz_MAX OR
    Mxyz = CMF.Mxyz_MAX"""

    return query


if __name__ == '__main__':

    output_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\02 - Connections\Main Leaf Column Head\C1 Loads\2025-08-03 C1 Column Head Connections_Column Worst Combinations_EXT_ALS.csv"

    location = "C1"

    with duckdb.connect() as conn:

        with open(output_fp, 'w+', newline='') as output_file:
            headers = ["BeamNumber", "ResultCaseName", "Model", "Fx", "Fy", "Fz", "Mx", "My", "Mz",
                       "Fxy", "Fxz", "Fyz", "Mxy", "Mxz", "Myz", "Fxyz", "Mxyz"]
            writer = csv.writer(output_file)
            writer.writerow(headers)

            query = get_column_query(location, bf_ext_als_parq_files)

            results = conn.execute(query).fetchall()
            # for result in results:
            #     print(result)
            writer.writerows(results)

