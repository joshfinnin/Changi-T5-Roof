
"""Script to wrangle and organize the data from multiple sources into the end reaction schedule."""
import duckdb
import time
from inputs import (perm_forces_parq_dict, splice_data,
                    als_models, als_force_parq_dict, als_prop_parq_dict, als_summary_parq_folder_dict,
                    perm_beam_forces_filtered_parq, perm_beam_properties_parq)


def get_perm_beam_prop_query(beam_properties_parquet: str):
    """Function to get the beam properties from the permanent model."""

    perm_beam_properties = f"""SELECT DISTINCT BP.BeamNumber, GroupName,
                                CASE
                                WHEN GroupName LIKE '%ColHeadVert%' THEN 'Cruciform'
                                ELSE PropertyName
                                END AS PropertyName
                               FROM '{beam_properties_parquet}' AS BP
                               JOIN SPLICE_TABLE AS SPL ON SPL.BeamNumber = BP.BeamNumber
                               ORDER BY BP.BeamNumber
                               """

    return perm_beam_properties


def get_perm_beam_end_force_query(perm_forces_parq_files: dict):
    """Function for extracting the forces for the permanent model for the beam numbers
    that occur at the target positions.  Uses the values in SPLICE_TABLE
    to get the forces that only occur at the locations of interest."""

    beam_end_force_query = " UNION ALL ".join(f"""SELECT BP.BeamNumber AS BeamNumber, '{model}' AS Model, 
                               ResultCase, ResultCaseName,
                               BF.Position, Fx, Fy, Fz, Mx, My, Mz
                               FROM BEAM_PROPERTIES AS BP
                               JOIN '{perm_parq}' AS BF ON BP.BeamNumber = BF.BeamNumber
                               JOIN SPLICE_TABLE AS SPL ON SPL.BeamNumber = BP.BeamNumber AND SPL.Position = BF.Position
                               """ for model, perm_parq in perm_forces_parq_files.items())

    return beam_end_force_query


def get_initial_als_end_forces(als_force_parq: str, als_prop_parq: str, beam_numbers: tuple) -> str:
    """Function for extracting only the target beams from the ALS model based on SPLICE_TABLE."""

    query = f"""SELECT BF.BeamNumber, ALS_PROP.BeamIDNumber, ResultCase, ResultCaseName, 
    Position, Fx, Fy, Fz, Mx, My, Mz
    FROM '{als_force_parq}' AS BF
    JOIN '{als_prop_parq}' AS ALS_PROP
    ON ALS_PROP.BeamNumber = BF.BeamNumber
    WHERE ALS_PROP.BeamIDNumber IN {beam_numbers}"""
    return query


def get_als_end_forces(model: str):
    """Function for distilling the forces from the ALS parquet files into summary parquet files."""

    # NOTE: Beam properties is not the normal beam properties, I have created a new table above.
    # TODO Fix the above naming so that it uses a convention that is less confusing.
    query = f"""SELECT
    BP.BeamNumber, '{model}' AS Model, ResultCase, ResultCaseName,
    ALS_BF.Position, Fx, Fy, Fz, Mx, My, Mz
    FROM INITIAL_ALS_RESULTS AS ALS_BF
    JOIN BEAM_PROPERTIES AS BP ON BP.BeamNumber = ALS_BF.BeamIDNumber
    JOIN SPLICE_TABLE AS SPL ON SPL.BeamNumber = ALS_BF.BeamIDNumber AND SPL.Position = ALS_BF.Position"""
    return query


if __name__ == '__main__':

    with duckdb.connect() as conn:

        permanent_beam_numbers = tuple(b[0] for b in splice_data)

        splice_locations = ",\n".join(str(t) for t in splice_data)
        splice_table = f"""CREATE TABLE SPLICE_TABLE(BeamNumber, Position) AS (VALUES
                           {splice_locations});"""
        conn.execute(splice_table)

        prop_table = r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\QA\beam_properties.parquet"
        query = f"""CREATE TABLE BEAM_PROPERTIES AS {get_perm_beam_prop_query(perm_beam_properties_parq)};
                    COPY BEAM_PROPERTIES TO '{prop_table}' (FORMAT PARQUET);
                    CREATE TEMP TABLE BEAM_NUMBERS AS (SELECT DISTINCT BeamNumber FROM BEAM_PROPERTIES);"""

        conn.execute(query)

        # Execute query to write permanent results to parquet file
        query = f"""CREATE TABLE PERM AS WITH
                BEAM_END_FORCES AS ({get_perm_beam_end_force_query(perm_forces_parq_dict)})
                SELECT * FROM BEAM_END_FORCES
                ORDER BY BeamNumber, Model, ResultCase;
                COPY PERM TO '{perm_beam_forces_filtered_parq}'
                (FORMAT PARQUET)"""

        print("Writing the permanent beam force results to file...")
        start = time.time()
        results = conn.execute(query).fetchall()
        for result in results:
            print(result)
        end = time.time()
        duration = end - start
        print(f"Duration of query execution: {duration:.2f}s")

        for als_model in als_models:

            # Execute query to write ALS results to parquet files
            query = f"""COPY(WITH INITIAL_ALS_RESULTS AS ({get_initial_als_end_forces(als_force_parq_dict[als_model], als_prop_parq_dict[als_model], permanent_beam_numbers)}),
                        ALS_BEAM_FORCES AS ({get_als_end_forces(als_model)})
                        SELECT BeamNumber,
                        Model, ResultCase, ResultCaseName, Position, Fx, Fy, Fz, Mx, My, Mz
                        FROM ALS_BEAM_FORCES) TO '{als_summary_parq_folder_dict[als_model]}'
                        (FORMAT PARQUET, COMPRESSION ZSTD);"""

            print(f"Writing the ALS beam force results to file for {als_model}...")
            start = time.time()
            results = conn.execute(query).fetchall()
            for result in results:
                print(f"\t{result[0]:,.0f} rows retrieved.")
            end = time.time()
            duration = end - start
            print(f"\tRetrieval time: {duration:.2f}s")



