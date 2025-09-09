import pathlib
import duckdb
import time
from inputs import (section_data, perm_beam_forces_filtered_parq, perm_beam_properties_parq,
                    als_summary_parq_folder_dict)
from QL_inputs import CAL_10, CAL_13

if __name__ == '__main__':

    with duckdb.connect() as conn:
        paths = [perm_beam_forces_filtered_parq] + [parq for parq in als_summary_parq_folder_dict.values()]
        paths = [str(p) for p in paths]

        # TODO UPDATE SPREADSHEET NAMES BELOW
        group_name = "Secondary Truss Splices"
        result_directory = pathlib.Path(r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Secondary Truss Splice Reactions")
        combined_force_outputs = result_directory / f"{group_name}_Combined_Forces.csv"
        extrema_envelope_outputs = result_directory / f"{group_name}_Extrema_Envelope_Forces.csv"
        critical_combination_sets_outputs = result_directory / f"{group_name}_Critical_Combination_Forces.csv"
        coincident_forces_outputs = result_directory / f"{group_name}_Extrema_Coincident_Forces.csv"
        complete_envelope_outputs = result_directory / f"{group_name}_Complete_Envelope_Forces.csv"

        # CONVERT THE SECTION PROPERTIES TO A LOOKUP TABLE (CHANGE THIS TO A DIRECT CSV READ LATER)
        sections = ",\n".join(str(t) for t in section_data)

        force_input_table = f"""CREATE TABLE INPUT_FORCES AS (SELECT * FROM read_parquet({paths}) AS BF);
                                COPY INPUT_FORCES TO 'E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\QA\input_forces.parquet';"""
        conn.execute(force_input_table)

        force_summary_query = f"""
                    CREATE TABLE SECTION_PROPS(
                        SectionProperty,
                        Area, Zex, Zey, Awy, Awz, Zt
                    ) AS (
                        VALUES
                        {sections}
                        );
    
                    CREATE TABLE COMBINED_FORCES AS
                    SELECT BF.BeamNumber, Model, ResultCaseName, Position, PropertyName, Area, Zex, Zey,
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
    
                    FROM INPUT_FORCES AS BF
                    JOIN '{perm_beam_properties_parq}' AS BP ON BP.BeamNumber = BF.BeamNumber
                    JOIN SECTION_PROPS AS SP ON PropertyName LIKE '%' || SP.SectionProperty || '%'
                    AND ResultCaseName NOT LIKE '%1a [1a][U]%'
                    AND ResultCaseName NOT LIKE '%1b(0) [1b][M]%'
                    AND ResultCaseName NOT LIKE '%2&3(0)%'
                    AND ResultCaseName NOT LIKE '%1b [1b][M]%'
                    AND ResultCaseName NOT LIKE '%2&3 [2+3][M]%'
                    ORDER BY BF.BeamNumber, Model, ResultCase, Position;
    
                    COPY COMBINED_FORCES TO '{combined_force_outputs}';
                    COPY COMBINED_FORCES TO 'E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\QA\combined_forces.parquet';
    
                    CREATE TABLE EXTREMAS AS
                    SELECT BeamNumber, Position,
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
                    GROUP BY BeamNumber, Position
                    ORDER BY BeamNumber, Position;
    
                    COPY EXTREMAS TO '{extrema_envelope_outputs}';
                    
                    CREATE TABLE COMPLETE_ENVELOPE AS
                    SELECT 'ALL' AS BeamNumber,
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
                    JOIN SECTION_PROPS AS SP ON PropertyName LIKE '%' || SP.SectionProperty || '%';
    
                    COPY COMPLETE_ENVELOPE TO '{complete_envelope_outputs}';
    
                    CREATE TABLE CRITICAL_FORCE_SETS 
                    AS SELECT BF.BeamNumber, Model, ResultCaseName, BF.Position,
                     PropertyName, Fx, Fy, Fz, Mx, My, Mz, Fyz, Myz, RESOLVED_BENDING, RESOLVED_NORMAL_POS, 
                     RESOLVED_NORMAL_NEG, RESOLVED_SHEAR_POS, RESOLVED_SHEAR_NEG 
                    FROM COMBINED_FORCES AS BF
                    JOIN EXTREMAS AS EX ON EX.BeamNumber = BF.BeamNumber
                    AND EX.Position = BF.Position
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
                    ORDER BY BF.BeamNumber, BF.Position;
    
                    COPY CRITICAL_FORCE_SETS TO '{critical_combination_sets_outputs}';
    
                    CREATE TABLE COINCIDENT_FORCES AS 
                    SELECT DISTINCT BF.BeamNumber, BF.Model, BF.Position, BF.ResultCaseName,
                    BF.Fx, BF.Fy, BF.Fz, BF.Mx, BF.My, BF.Mz 
                    FROM COMBINED_FORCES AS BF
                    JOIN CRITICAL_FORCE_SETS AS CS ON BF.BeamNumber = CS.BeamNumber 
                    AND BF.Model = CS.Model 
                    AND BF.ResultCaseName = CS.ResultCaseName
                    ORDER BY BF.BeamNumber, BF.Position, BF.Model, BF.ResultCaseName;
    
                    COPY COINCIDENT_FORCES TO '{coincident_forces_outputs}'
                    ;"""

        print(f"Summarizing forces...")
        start = time.time()
        results = conn.execute(force_summary_query).fetchall()
        end = time.time()
        duration = end - start
        print(f"Summarization time: {duration:.1f}s")


