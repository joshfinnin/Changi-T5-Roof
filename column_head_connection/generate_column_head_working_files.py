

import duckdb
import logging
import time

from inputs import (FULL_BEAM_FORCES_PARQUET, BEAM_ENDS_PARQUET, NODAL_FORCE_PARQUET, BEAM_PROPERTY_PARQUET)
from inputs import (BF_PERM_PARQ_FILE_DICT, BP_PERM_PARQ_FILE_DICT,
                    BF_EXT_ALS_PARQ_FILE_DICT, BP_EXT_ALS_PARQ_FILE_DICT, NODE_DICT)
from inputs import EXCLUDED_BEAM_DICT, TARGET_GROUPS, RESULT_CASE_FILTER, COL_HEAD_LOCATION, ALS_ONLY


def configure_logging():
    logging.basicConfig(level=logging.INFO)


def process_time(func):

    def wrapper():
        start = time.time()
        func()
        end = time.time()
        duration = end - start
        log.info(f"Duration: {duration:.2f}s")

    return wrapper


def get_perm_beam_end_query(location: str, bp_parq_file: str, node_dict: dict, target_groups: str,
                            excluded_beams: dict) -> str:
    """Gets the SQL write_full_beam_forces_query for finding the relevant ends of the beam.
    Have updated the query to only pull the properties from a single model."""

    nodes = node_dict[location]

    # This query needs to be updated
    beam_end_query = f"""
    SELECT BeamNumber,
    0.0 AS BeamEnd,
    -1 AS Sign,
    FROM '{bp_parq_file}'
    WHERE N1 IN {nodes}
    AND GroupName IN {target_groups}
    AND BeamNumber NOT IN {excluded_beams[location]}

    UNION ALL

    SELECT BeamNumber,
    1.0 AS BeamEnd,
    1 AS Sign,
    FROM '{bp_parq_file}' 
    WHERE N2 IN {nodes}
    AND GroupName IN {target_groups}
    AND BeamNumber NOT IN {excluded_beams[location]}"""

    return beam_end_query


def get_full_beam_properties_query(bp_parq_file: str, target_groups: str) -> str:
    """Function to get the properties corresponding to each and every beam from the different bf_parqs."""

    property_query = f"""SELECT
    BeamNumber, GroupName, N1, N2
    FROM '{bp_parq_file}'
    WHERE GroupName IN {target_groups}"""

    return property_query


def get_full_beam_force_query(bf_perm_parq_files: dict, bf_als_parq_files: dict, bp_als_parq_files: dict,
                              beam_numbers: tuple, target_groups: str, result_case_filter: str, als_only=False) -> str:
    """Gets the full set of beam forces for beams from the series of bf_parqs, using filtering criteria."""

    # First query the permanent models for the end forces that occur for our target beams
    perm_prequery = "\n UNION ALL ".join(f"SELECT "
                                    f"BeamNumber, ResultCaseName, ResultCase, Position, '{model_name}' AS Model, "
                                    f"Fx, Fy, Fz, Mx, My, Mz FROM '{bf_perm_parq_file}' "
                                    f"WHERE Position IN (0.0, 1.0) AND ResultCaseName NOT LIKE '%BIF%'"
                                    f"AND BeamNumber IN {beam_numbers}" for model_name,
                                    bf_perm_parq_file in bf_perm_parq_files.items())

    # Second query the als models for the end forces that occur for our target beams
    # (based on BeamID rather than on BeamNumber)
    als_prequery = "\n UNION ALL ".join(f"""SELECT
                                            BeamIDNumber AS BeamNumber, ResultCaseName, ResultCase, Position, 
                                            '{model_name}' AS Model, Fx, Fy, Fz, Mx, My, Mz 
                                            FROM '{bf_als_parq_file}' AS BF
                                            JOIN '{bp_als_parq_files[model_name]}' 
                                            AS BP ON BP.BeamNumber = BF.BeamNumber
                                            WHERE Position IN (0.0, 1.0) AND ResultCaseName NOT LIKE '%BIF%'
                                            AND BeamIDNumber IN {beam_numbers}""" for model_name,
                                            bf_als_parq_file in bf_als_parq_files.items())

    # Added in this logic to ensure that we can query only the ALS models if we want to, but for the elements
    # that occur in the permanent model at the location we identify
    if als_only:
        prequery = als_prequery
    else:
        prequery = perm_prequery + "\n UNION ALL \n" + als_prequery

    full_beam_force_query = f"""SELECT BF.BeamNumber, ResultCaseName, ResultCase, Position, 
    BF.Model, Fx, Fy, Fz, Mx, My, Mz 
    FROM ({prequery}) AS BF 
    JOIN FULL_BEAM_PROPERTIES AS BP ON BF.BeamNumber = BP.BeamNumber 
    AND ResultCaseName NOT LIKE '%BIF%'
    AND ResultCaseName NOT IN {result_case_filter}
    AND BP.GroupName IN {target_groups}"""

    return full_beam_force_query


def get_nodal_beam_force_query() -> str:
    """Gets the nodal beam forces occurring at a particular location"""

    nodal_beam_force_query = f"""
        SELECT
        BF.BeamNumber,
        BF.ResultCaseName,
        BF.ResultCase,
        BF.Model,
        CASE
            WHEN BE.BeamEnd = 0.0 THEN BP.N1
            WHEN BE.BeamEnd = 1.0 THEN BP.N2
        END AS Node,
        Fx * Sign AS Fx, Fy * Sign AS Fy, Fz * Sign AS Fz, 
        Mx * Sign AS Mx, My * Sign AS My, Mz * Sign AS Mz
        FROM FULL_BEAM_FORCES AS BF
        JOIN FULL_BEAM_PROPERTIES AS BP ON BP.BeamNumber = BF.BeamNumber
        JOIN BEAM_ENDS AS BE ON BE.BeamNumber = BF.BeamNumber
        WHERE BF.Position = BE.BeamEnd"""

    return nodal_beam_force_query


model_element_dict = {model_name: [] for model_name in BP_PERM_PARQ_FILE_DICT.keys()}

if __name__ == '__main__':

    configure_logging()
    log = logging.getLogger(__name__)

    with duckdb.connect() as conn:
        log.info("DuckDB database created.")

        # ----------------------------------------------------------------------
        # SUBQUERY COMPONENTS
        # ----------------------------------------------------------------------
        beam_end_query = get_perm_beam_end_query(COL_HEAD_LOCATION, BP_PERM_PARQ_FILE_DICT["LB_Gmax"], NODE_DICT,
                                                 TARGET_GROUPS, EXCLUDED_BEAM_DICT)

        property_query = get_full_beam_properties_query(BP_PERM_PARQ_FILE_DICT["LB_Gmax"], TARGET_GROUPS)

        full_nodal_beam_force_query = get_nodal_beam_force_query()

        # ----------------------------------------------------------------------
        # MAIN QUERIES
        # ----------------------------------------------------------------------
        log.info("Generating SQL queries...")

        beam_ends_query = f"""CREATE TABLE BEAM_ENDS AS ({beam_end_query});"""

        conn.execute(beam_ends_query)
        # Collect the beam numbers from the beam ends table
        beam_numbers = tuple(b[0] for b in conn.execute("""SELECT BeamNumber FROM BEAM_ENDS;""").fetchall())

        # Querying the beam numbers first facilitates predicate pushdown as I can inject the values as literals
        # So the subsequent queries should execute significantly faster
        full_beam_force_query = get_full_beam_force_query(BF_PERM_PARQ_FILE_DICT, BF_EXT_ALS_PARQ_FILE_DICT,
                                                          BP_EXT_ALS_PARQ_FILE_DICT, beam_numbers, TARGET_GROUPS,
                                                          RESULT_CASE_FILTER)


        write_full_beam_forces_query = f"""CREATE TABLE FULL_BEAM_FORCES AS
                    WITH FULL_BEAM_PROPERTIES AS ({property_query})
                    {full_beam_force_query};

                    COPY FULL_BEAM_FORCES
                    TO '{FULL_BEAM_FORCES_PARQUET}'
                    (FORMAT PARQUET);
                    """

        write_full_beam_properties_query = f"""CREATE TABLE FULL_BEAM_PROPERTIES AS
                    {property_query};

                    COPY FULL_BEAM_PROPERTIES
                    TO '{BEAM_PROPERTY_PARQUET}'
                    (FORMAT PARQUET);"""

        write_beam_ends_query = f"""CREATE TABLE BEAM_ENDS AS 
                    {beam_end_query};

                    COPY BEAM_ENDS
                    TO '{BEAM_ENDS_PARQUET}'
                    (FORMAT PARQUET);"""

        write_nodal_force_query = f"""CREATE TABLE FULL_NODAL_FORCES AS
                    {full_nodal_beam_force_query};

                    COPY FULL_NODAL_FORCES
                    TO '{NODAL_FORCE_PARQUET}'
                    (FORMAT PARQUET);"""

        # ----------------------------------------------------------------------
        # WRITE THE BEAM FORCES TABLE TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing global axis beam forces to parquet...")
        start = time.time()
        conn.execute(write_full_beam_forces_query)
        conn.commit()
        end = time.time()
        duration = end - start
        log.info(f"Duration: {duration:.2f}s")

        # ----------------------------------------------------------------------
        # WRITE THE BEAM PROPERTIES TABLE TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing beam properties to parquet...")
        conn.execute(write_full_beam_properties_query)
        conn.commit()

        # ----------------------------------------------------------------------
        # WRITE THE NODAL FORCE RESULTS TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing beam force data at the nodes to parquet...")
        conn.execute(write_nodal_force_query)
        conn.commit()


