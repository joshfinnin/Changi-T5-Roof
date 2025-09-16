
import duckdb
import time
from inputs import (section_data, perm_beam_forces_filtered_parq, node_data,
                    perm_beam_properties_parq, als_summary_parq_folder_dict,
                    result_directory, connection_group_name)

if __name__ == '__main__':

    paths = [perm_beam_forces_filtered_parq] + [parq for parq in als_summary_parq_folder_dict.values()]
    paths = [str(p) for p in paths]
    sections = ",\n".join(str(t) for t in section_data)

    combined_force_outputs = result_directory / f"{connection_group_name}_Combined_Forces.csv"
    extrema_force_outputs = result_directory / f"{connection_group_name}_Extrema_Envelope_Forces.csv"
    critical_combination_sets_outputs = result_directory / f"{connection_group_name}_Critical_Combination_Forces.csv"
    coincident_forces_outputs = result_directory / f"{connection_group_name}_Extrema_Coincident_Forces.csv"

    beam_numbers_to_exclude = (719, 720, 721, 722, 747, 750, 751, 752,
                               823, 825, 827, 828, 834, 835, 838, 839,
                               911, 913, 914, 915, 997, 999, 1000, 1001,
                               1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205,
                               6278, 6288, 6309, 6324, 6328, 6352, 6375, 6386,
                               6419, 6430, 6441, 6517, 6530, 6534, 6538, 6549,
                               6560, 6561, 6580, 6583, 6594, 6602, 6604, 6605,
                               6606, 6613, 6614, 6621, 6623, 6633, 6635, 6636,
                               7053, 7054, 7055, 7056, 7057, 7058, 7059, 7060,
                               7061, 7062, 7063, 7064, 7065, 7066, 7067, 7068)

    force_summary_query = f"""
                CREATE TABLE SECTION_PROPS(
                    SectionProperty,
                    Area, Zex, Zey, Awy, Awz, Zt
                ) AS (
                    VALUES
                    {sections}
                );
                
                CREATE TABLE COMBINED_FORCES AS
                SELECT Node, BF.BeamNumber, Model, ResultCaseName, Position, PropertyName, Area, Zex, Zey,
                Fx, Fy, Fz, Mx, My, Mz, SQRT(Fy**2 + Fz**2) AS Fyz, SQRT(My**2 + Mz**2) AS Myz,
                CASE 
                    WHEN PropertyName LIKE '%CHS%' THEN SQRT((My * 1000000)**2 + (Mz * 1000000)**2) / Zex
                    ELSE ABS(My * 1000000 / Zex) + ABS(Mz * 1000000 / Zey)
                END AS RESOLVED_BENDING,
                CASE
                    WHEN PropertyName LIKE '%CHS%' THEN (Fx * 1000 / Area) + SQRT((My * 1000000)**2 + (Mz * 1000000)**2) / Zex
                    ELSE (Fx * 1000 / Area) + ABS(My * 1000000 / Zex) + ABS(Mz * 1000000 / Zey)
                END AS RESOLVED_NORMAL_POS,
                CASE
                    WHEN PropertyName LIKE '%CHS%' THEN (Fx * 1000 / Area) - SQRT((My * 1000000)**2 + (Mz * 1000000)**2) / Zex
                    ELSE (Fx * 1000 / Area) - ABS(My * 1000000 / Zex) - ABS(Mz * 1000000 / Zey)
                END AS RESOLVED_NORMAL_NEG,
                (Mx * 1000000 / Zt) + (Fy * 1000 / Awy) + (Fz * 1000 / Awz) AS RESOLVED_SHEAR_POS,
                -(Mx * 1000000 / Zt) + (Fy * 1000 / Awy) + (Fz * 1000 / Awz) AS RESOLVED_SHEAR_NEG
                
                FROM read_parquet({paths}) AS BF
                JOIN '{perm_beam_properties_parq}' AS BP ON BP.BeamNumber = BF.BeamNumber
                JOIN SECTION_PROPS AS SP ON PropertyName LIKE '%' || SP.SectionProperty || '%'
                WHERE BF.BeamNumber NOT IN {beam_numbers_to_exclude}
                AND ResultCaseName NOT LIKE '%1a [1a][U]%'
                AND ResultCaseName NOT LIKE '%1b(0) [1b][M]%'
                AND ResultCaseName NOT LIKE '%2&3(0)%'
                AND ResultCaseName NOT LIKE '%1b [1b][M]%'
                AND ResultCaseName NOT LIKE '%2&3 [2+3][M]%'
                ORDER BY Node, ResultCaseName;
                
                COPY COMBINED_FORCES TO '{combined_force_outputs}';
                
                CREATE TABLE EXTREMAS AS
                SELECT Node, BeamNumber,
                MAX(Fx) AS Fx_MAX, MIN(Fx) AS Fx_MIN,
                MAX(Fy) AS Fy_MAX, MIN(Fy) AS Fy_MIN,
                MAX(Fz) AS Fz_MAX, MIN(Fz) AS Fz_MIN,
                MAX(Mx) AS Mx_MAX, MIN(Mx) AS Mx_MIN,
                MAX(My) AS My_MAX, MIN(My) AS My_MIN,
                MAX(Mz) AS Mz_MAX, MIN(Mz) AS Mz_MIN,
                MAX(Fyz) AS Fyz_MAX,
                MAX(Myz) AS Myz_MAX,
                MAX(RESOLVED_BENDING) AS RESOLVED_BENDING_MAX,
                MAX(RESOLVED_NORMAL_POS) AS RESOLVED_NORMAL_MAX_POS,
                MIN(RESOLVED_NORMAL_NEG) AS RESOLVED_NORMAL_MIN_NEG,
                MAX(RESOLVED_SHEAR_POS) AS RESOLVED_SHEAR_MAX_POS,
                MIN(RESOLVED_SHEAR_NEG) AS RESOLVED_SHEAR_MIN_NEG
                FROM COMBINED_FORCES
                JOIN SECTION_PROPS AS SP ON PropertyName LIKE '%' || SP.SectionProperty || '%'
                GROUP BY Node, BeamNumber
                ORDER BY Node, BeamNumber;
                
                COPY EXTREMAS TO '{extrema_force_outputs}';
                
                CREATE TABLE CRITICAL_FORCE_SETS 
                AS SELECT BF.Node, BF.BeamNumber, Model, ResultCaseName, Position,
                 PropertyName, Fx, Fy, Fz, Mx, My, Mz, Fyz, Myz, RESOLVED_BENDING, RESOLVED_NORMAL_POS, 
                 RESOLVED_NORMAL_NEG, RESOLVED_SHEAR_POS, RESOLVED_SHEAR_NEG 
                FROM COMBINED_FORCES AS BF
                JOIN EXTREMAS AS EX ON EX.BeamNumber = BF.BeamNumber AND EX.Node = BF.Node
                WHERE BF.Node IN {node_data}
                AND (Fx IN (Fx_MAX, Fx_MIN)
                OR Fy IN (Fy_MAX, Fy_MIN)
                OR Fz IN (Fz_MAX, Fz_MIN)
                OR Mx IN (Mx_MAX, Mx_MIN)
                OR My IN (My_MAX, My_MIN)
                OR Mz IN (Mz_MAX, Mz_MIN)
                OR Fyz = Fyz_MAX
                OR Myz = Myz_MAX
                OR RESOLVED_BENDING = RESOLVED_BENDING_MAX
                OR RESOLVED_NORMAL_POS = RESOLVED_NORMAL_MAX_POS
                OR RESOLVED_NORMAL_NEG = RESOLVED_NORMAL_MIN_NEG
                OR RESOLVED_SHEAR_POS = RESOLVED_SHEAR_MAX_POS
                OR RESOLVED_SHEAR_NEG = RESOLVED_SHEAR_MIN_NEG)
                
                ORDER BY BF.Node, BF.BeamNumber;
                
                COPY CRITICAL_FORCE_SETS TO '{critical_combination_sets_outputs}';
                
                CREATE TABLE COINCIDENT_FORCES AS 
                SELECT DISTINCT BF.Node, BF.BeamNumber, BF.Model, BF.ResultCaseName, 
                BF.Fx, BF.Fy, BF.Fz, BF.Mx, BF.My, BF.Mz 
                FROM COMBINED_FORCES AS BF
                JOIN CRITICAL_FORCE_SETS AS CS ON BF.Node = CS.Node AND BF.Model = CS.Model AND BF.ResultCaseName = CS.ResultCaseName
                ORDER BY BF.Node, BF.Model, BF.ResultCaseName, BF.BeamNumber;
                
                COPY COINCIDENT_FORCES TO '{coincident_forces_outputs}'
                ;"""

    with duckdb.connect() as conn:

        print(f"Summarizing forces for {connection_group_name}...")
        start = time.time()
        results = conn.execute(force_summary_query).fetchall()
        end = time.time()
        duration = end - start
        print(f"Summarization time: {duration:.2f}s")
