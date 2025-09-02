

import duckdb
import logging
from inputs import bp_parq_files, bf_ext_als_parq_files, bp_ext_als_parq_files, node_dict
from inputs import excluded_beam_dict, target_groups, result_case_filter


def configure_logging():
    logging.basicConfig(level=logging.INFO)


def get_perm_beam_end_query(location: str, bp_parq_files: dict, node_dict: dict, target_groups: str,
                            excluded_beams: dict) -> str:
    """Gets the SQL write_full_beam_forces_query for finding the relevant ends of the beam."""

    models = bp_parq_files.keys()

    nodes = {m_name: node_dict[location] for m_name in models if "ALS" not in m_name}

    # This query needs to be updated
    beam_end_query = " UNION ALL ".join(f"""
    SELECT BeamNumber,
    0.0 AS BeamEnd,
    -1 AS Sign,
    '{model}' as Model
    FROM '{bp_parq}'
    WHERE N1 IN {nodes[model]}
    AND GroupName IN {target_groups}
    AND BeamNumber NOT IN {excluded_beams[model][location]}

    UNION ALL

    SELECT BeamNumber,
    1.0 AS BeamEnd,
    1 AS Sign,
    '{model}' as Model
    FROM '{bp_parq}' 
    WHERE N2 IN {nodes[model]}
    AND GroupName IN {target_groups}
    AND BeamNumber NOT IN {excluded_beams[model][location]}""" for model, bp_parq in bp_parq_files.items())

    return beam_end_query


def get_full_beam_properties_query(bp_parq_files: dict, target_groups: str) -> str:
    """Function to get the properties corresponding to each and every beam from the different bf_parqs."""

    property_query = " UNION ALL ".join(f"""SELECT
    BeamNumber, GroupName, '{model}' AS Model, N1, N2
    FROM '{bp_parq_files[model]}'
    WHERE GroupName IN {target_groups}""" for model in bp_parq_files.keys())

    return property_query


def get_full_beam_force_query(location: str, bf_parq_files: dict, bp_parq_files: dict,
                              excluded_beams: dict, target_groups: str, result_case_filter: str) -> str:
    """Gets the full set of beam forces for beams from the series of bf_parqs, using filtering criteria."""

    prequery = "\n UNION ALL ".join(f"SELECT "
                                    f"BeamNumber, ResultCaseName, ResultCase, Position, '{model_name}' AS Model, "
                                    f"Fx, Fy, Fz, Mx, My, Mz FROM '{bf_parq_files[model_name]}' "
                                    f"WHERE Position IN (0.0, 1.0) AND ResultCaseName NOT LIKE '%BIF%'"
                                    f"AND BeamNumber NOT IN {excluded_beams[model_name][location]}" for model_name in
                                    bf_parq_files)

    full_beam_force_query = f"""SELECT BF.BeamNumber, ResultCaseName, ResultCase, Position, 
    BF.Model, Fx, Fy, Fz, Mx, My, Mz 
    FROM ({prequery}) AS BF 
    JOIN FULL_BEAM_PROPERTIES AS BP ON BF.BeamNumber = BP.BeamNumber 
    AND BP.Model = BF.Model 
    WHERE BF.BeamNumber IN (SELECT DISTINCT BeamNumber FROM BEAM_ENDS)
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
        JOIN FULL_BEAM_PROPERTIES AS BP ON BP.BeamNumber = BF.BeamNumber AND BP.Model = BF.Model
        JOIN BEAM_ENDS AS BE ON BE.BeamNumber = BF.BeamNumber AND BE.Model = BF.Model
        WHERE BF.Position = BE.BeamEnd"""

    return nodal_beam_force_query


locations = ("B1", "B2", "C1", "C2")

model_element_dict = {model_name: [] for model_name in bp_parq_files.keys()}

if __name__ == '__main__':

    configure_logging()
    log = logging.getLogger(__name__)

    with duckdb.connect() as conn:
        log.info("DuckDB database created.")
        # ----------------------------------------------------------------------
        # INPUTS
        # ----------------------------------------------------------------------

        location = "C1"
        beam_forces_parquet_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\02 - Connections\Main Leaf Column Head\C1 Loads\full_beam_forces_ext_als.parquet"
        property_parquet_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\02 - Connections\Main Leaf Column Head\C1 Loads\full_beam_properties_ext_als.parquet"
        beam_ends_parquet_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\02 - Connections\Main Leaf Column Head\C1 Loads\beam_ends_ext_als.parquet"
        nodal_force_parquet_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\02 - Connections\Main Leaf Column Head\C1 Loads\full_nodal_forces_ext_als.parquet"

        # ----------------------------------------------------------------------
        # SUBQUERY COMPONENTS
        # ----------------------------------------------------------------------
        beam_end_query = get_perm_beam_end_query(location, bp_ext_als_parq_files, node_dict, target_groups,
                                                 excluded_beam_dict)

        property_query = get_full_beam_properties_query(bp_ext_als_parq_files, target_groups)

        full_beam_force_query = get_full_beam_force_query(location, bf_ext_als_parq_files, bp_ext_als_parq_files,
                                                          excluded_beam_dict, target_groups, result_case_filter)

        full_nodal_beam_force_query = get_nodal_beam_force_query()

        # ----------------------------------------------------------------------
        # MAIN QUERIES
        # ----------------------------------------------------------------------
        log.info("Generating SQL queries...")
        write_full_beam_forces_query = f"""CREATE TABLE FULL_BEAM_FORCES AS
                    WITH BEAM_ENDS AS ({beam_end_query}),
                    FULL_BEAM_PROPERTIES AS ({property_query})
                    {full_beam_force_query};

                    COPY FULL_BEAM_FORCES
                    TO '{beam_forces_parquet_fp}'
                    (FORMAT PARQUET);
                    """

        write_full_beam_properties_query = f"""CREATE TABLE FULL_BEAM_PROPERTIES AS
                    {property_query};

                    COPY FULL_BEAM_PROPERTIES
                    TO '{property_parquet_fp}'
                    (FORMAT PARQUET);"""

        write_beam_ends_query = f"""CREATE TABLE BEAM_ENDS AS 
                    {beam_end_query};

                    COPY BEAM_ENDS
                    TO '{beam_ends_parquet_fp}'
                    (FORMAT PARQUET);"""

        write_nodal_force_query = f"""CREATE TABLE FULL_NODAL_FORCES AS 
                    WITH BEAM_ENDS AS (SELECT * FROM '{beam_ends_parquet_fp}'),
                    FULL_BEAM_PROPERTIES AS (SELECT * FROM '{property_parquet_fp}'),
                    FULL_BEAM_FORCES AS (SELECT * FROM '{beam_forces_parquet_fp}')
                    {full_nodal_beam_force_query};

                    COPY FULL_NODAL_FORCES
                    TO '{nodal_force_parquet_fp}'
                    (FORMAT PARQUET);"""

        # ----------------------------------------------------------------------
        # WRITE THE BEAM FORCES TABLE TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing global axis beam forces to parquet...")
        conn.execute(write_full_beam_forces_query)
        conn.commit()

        # ----------------------------------------------------------------------
        # WRITE THE BEAM PROPERTIES TABLE TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing beam properties to parquet...")
        conn.execute(write_full_beam_properties_query)
        conn.commit()

        # ----------------------------------------------------------------------
        # WRITE THE BEAM ENDS TABLE TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing beam end information to parquet...")
        conn.execute(write_beam_ends_query)
        conn.commit()

        # ----------------------------------------------------------------------
        # WRITE THE NODAL FORCE RESULTS TO A STANDALONE PARQUET FILE
        # ----------------------------------------------------------------------
        log.info("Writing beam force data at the nodes to parquet...")
        conn.execute(write_nodal_force_query)
        conn.commit()


