
"""
Script for generating the input cruciform_output_file for the DC Lightning runs.
"""

import csv
import logging
import datetime
import duckdb

from end_reaction_schedule import inputs as end_reaction_inputs

# Dictionary used to map from the Strand7 property names to the DC Lightning section catalogue
SECTION_LOOKUP_FILE = r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Member Checks\Section Lookup Table.csv"
with open(SECTION_LOOKUP_FILE, 'r') as section_file:
    reader = csv.reader(section_file)
    reader.__next__()  # Skip the first row
    section_lookup_dict = {row[0]: row[1] for row in reader}

# Dictionary used to map the station point float to a corresponding integer value
# Seems to work fine, but need to be careful with this approach as it risks near-miss issues
POSITION_DICT = {0.0: 1,
                 0.25: 2,
                 0.5: 3,
                 0.75: 4,
                 1.0: 5}

# Function for extracting the beam information for
def get_beam_force_query(model: str, bf_parq: str, bp_parq: str, target_beams: tuple=None, envelope=False):

    if target_beams is None:
        if "ALS" in model:
            query = f"""SELECT ResultCase, ResultCaseName, BeamIDNumber AS BeamNumber, Position, GroupName, PropertyName, 
                        Fx, Fy, Fz, Mx, My, Mz 
                        FROM '{bf_parq}' AS BF
                        JOIN '{bp_parq}' AS BP ON BF.BeamNumber = BP.BeamNumber"""
        else:
            query = f"""SELECT ResultCase, ResultCaseName, BF.BeamNumber, Position, GroupName, PropertyName, 
                        Fx, Fy, Fz, Mx, My, Mz
                        FROM '{bf_parq}' AS BF
                        JOIN '{bp_parq}' AS BP ON BF.BeamNumber = BF.BeamNumber"""
    else:
        if envelope:
            if "ALS" in model:
                query = f"""SELECT 0 AS ResultCase, 'ENV' AS ResultCaseName, BP.BeamIDNumber AS BeamNumber, Position, GroupName, PropertyName, 
                            MAX(Fx), MAX(ABS(Fy)), MAX(ABS(Fz)), MAX(ABS(Mx)), MAX(ABS(My)), MAX(ABS(Mz)) FROM (SELECT BeamNumber, BeamIDNumber, GroupName, PropertyName, 
                            FROM '{bp_parq}' WHERE BeamIDNumber IN {target_beams}) AS BP
                            JOIN '{bf_parq}' AS BF ON BF.BeamNumber = BP.BeamNumber
                            GROUP BY BP.BeamIDNumber, Position, GroupName, PropertyName
                            
                            UNION ALL
                            
                            SELECT 0 AS ResultCase, 'ENV' AS ResultCaseName, BP.BeamIDNumber AS BeamNumber, Position, GroupName, PropertyName, 
                            MIN(Fx), MAX(ABS(Fy)), MAX(ABS(Fz)), MAX(ABS(Mx)), MAX(ABS(My)), MAX(ABS(Mz)) FROM (SELECT BeamNumber, BeamIDNumber, GroupName, PropertyName, 
                            FROM '{bp_parq}' WHERE BeamIDNumber IN {target_beams}) AS BP
                            JOIN '{bf_parq}' AS BF ON BF.BeamNumber = BP.BeamNumber
                            GROUP BY BP.BeamIDNumber, Position, GroupName, PropertyName
                            """
            else:
                query = f"""SELECT 0 AS ResultCase, 'ENV' AS ResultCaseName, BF.BeamNumber, Position, GroupName, PropertyName, 
                            MAX(Fx), MAX(ABS(Fy)), MAX(ABS(Fz)), MAX(ABS(Mx)), MAX(ABS(My)), MAX(ABS(Mz)) FROM (SELECT BeamNumber, GroupName, PropertyName FROM '{bp_parq}'
                            WHERE BeamNumber IN {target_beams}) AS BP
                            JOIN '{bf_parq}' AS BF ON BF.BeamNumber = BP.BeamNumber
                            GROUP BY BF.BeamNumber, Position, GroupName, PropertyName

                            UNION ALL

                            SELECT 0 AS ResultCase, 'ENV' AS ResultCaseName, BF.BeamNumber, Position, GroupName, PropertyName, 
                            MIN(Fx), MAX(ABS(Fy)), MAX(ABS(Fz)), MAX(ABS(Mx)), MAX(ABS(My)), MAX(ABS(Mz)) FROM (SELECT BeamNumber, GroupName, PropertyName FROM '{bp_parq}'
                            WHERE BeamNumber IN {target_beams}) AS BP
                            JOIN '{bf_parq}' AS BF ON BF.BeamNumber = BP.BeamNumber
                            GROUP BY BF.BeamNumber, Position, GroupName, PropertyName"""

        else:
            if "ALS" in model:
                query = f"""SELECT ResultCase, ResultCaseName, BP.BeamIDNumber AS BeamNumber, Position, GroupName, PropertyName, 
                            Fx, Fy, Fz, Mx, My, Mz FROM (SELECT BeamNumber, BeamIDNumber, GroupName, PropertyName, 
                            FROM '{bp_parq}' WHERE BeamIDNumber IN {target_beams}) AS BP
                            JOIN '{bf_parq}' AS BF ON BF.BeamNumber = BP.BeamNumber"""
            else:
                query = f"""SELECT ResultCase, ResultCaseName, BF.BeamNumber, Position, GroupName, PropertyName, 
                            Fx, Fy, Fz, Mx, My, Mz FROM (SELECT BeamNumber, GroupName, PropertyName FROM '{bp_parq}'
                            WHERE BeamNumber IN {target_beams}) AS BP
                            JOIN '{bf_parq}' AS BF ON BF.BeamNumber = BP.BeamNumber"""

    return query

# Convenience function for rounding to a predetermined precision
def rnd(f: float, precision=2):
    return round(f, precision)


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # FILE PATH INPUTS FOR THE STRAND DATABASES AND OUTPUT FILE
    # ----------------------------------------------------------------------

    # NOTE: The below envelope command controls whether the script envelopes load combinations for
    # individual station points within a single model.
    # i.e. If True, it will envelope all load combinations for an individual station point on each
    # beam within a single model so that each beam within a model having 1000 combinations x 5 station
    # points, will reduce to 2 combinations (max and min axial force, plus the maximum absolute value
    # of each other force) x 5 station points. This should not be overly conservative as it does not
    # envelope between models (i.e. maxima from the ALS models are not considered coincident with
    # permanent models)
    ENVELOPE = True

    # The below group filter determines which group of elements to filter by from the Strand7 model
    GROUP_FILTER = "EdgeTrussTop"

    # Effective length input file, generated using the
    # effective_length_initializer.py module
    EFFECTIVE_LENGTH_FP = r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Member Checks\Effective_Lengths.csv"

    # Output file of this script, which is the DC Lightning input file
    OUTPUT_FP = f"E:\\Projects\\Changi\\MUC\\Strand7 Model\\V1_4_5\\Member Checks\\{GROUP_FILTER}_DC_input.csv"

    # Logging file, to capture some errors in mapping or other error types handled
    LOGGING_FP = f"E:\\Projects\\Changi\\MUC\\Strand7 Model\\V1_4_5\\Member Checks\\{datetime.date.today()}_error_log.txt"

    # ----------------------------------------------------------------------
    # SETUP LOGGING
    # ----------------------------------------------------------------------
    logging.basicConfig(filename=LOGGING_FP, level=logging.INFO)
    logging_warnings = []
    logging_errors = []

    # ----------------------------------------------------------------------
    # GET EFFECTIVE LENGTH INPUTS
    # ----------------------------------------------------------------------
    with open(EFFECTIVE_LENGTH_FP, 'r') as length_file:
        effective_length_dict = {int(d["BeamNumber"]): d for d in csv.DictReader(length_file)}

    # ----------------------------------------------------------------------
    # ITERATE THROUGH THE FORCE RESULTS AND WRITE THE INPUT FILE FOR THE
    # DC LIGHTNING RUNS
    # ----------------------------------------------------------------------

    with open(OUTPUT_FP, 'w+') as output_file:
        output_file.write("Id,Source.ResultFileId,Source.ResultCaseNum,Source.ResultCaseName,Source.ResultBound,Source.BeamNum,Source.BeamPosition,Source.BeamGroupName,Source.BeamOptimisationGroup,CrossSectionId,Steel Grade,L_crT [m],L_cry [m],C_my,L_crz [m],C_mz,L_c [m],C_mLT,z_g [mm],C_1,C_2,alpha_cr_min,lambda_cr_max,N_Ed [kN],V_yEd [kN],V_zEd [kN],M_yEd [kNm],M_zEd [kNm],T_Ed [kNm],National Annex\n")

        with duckdb.connect() as conn:

            bf_parq_files = end_reaction_inputs.perm_forces_parq_dict | end_reaction_inputs.als_force_parq_dict
            bp_parq_files = end_reaction_inputs.perm_props_parq_dict | end_reaction_inputs.als_prop_parq_dict

            target_beams = conn.execute(f"""SELECT BeamNumber FROM '{end_reaction_inputs.perm_props_parq_dict["LB_Gmax"]}' AS BP
                                            WHERE GroupName LIKE '%{GROUP_FILTER}%'""").fetchall()
            target_beams = tuple(r[0] for r in target_beams)

            id = 1

            # Iterate through each of the model database files to get the results
            for model, bf_parq in bf_parq_files.items():
                print(f"Extracting from model {model}...")

                bp_parq = bp_parq_files[model]
                force_result_query = get_beam_force_query(model, bf_parq, bp_parq,
                                                          target_beams=target_beams, envelope=True)
                force_results = conn.execute(force_result_query).fetchall()
                for result in force_results:
                    # There are some keys that won't map correctly (not meant to be designed in this module)
                    try:
                        beam_number = result[2]
                        Lcry = effective_length_dict[beam_number]["L_cry"]
                        Lcrz = effective_length_dict[beam_number]["L_crz"]
                        Lcrt = effective_length_dict[beam_number]["L_crT"]
                        Lc = effective_length_dict[beam_number]["L_c"]
                        C1 = effective_length_dict[beam_number]["C_1"]
                        C2 = effective_length_dict[beam_number]["C_2"]
                        zg = effective_length_dict[beam_number]["z_g"]
                        Cmy = effective_length_dict[beam_number]["C_my"]
                        Cmz = effective_length_dict[beam_number]["C_mz"]
                        Cmlt = effective_length_dict[beam_number]["C_mLT"]
                        case_number = result[0]
                        case_name = result[1]
                        case_name = case_name.replace(":", "#")
                        position = result[3]
                        group_name = result[4]
                        property_name = result[5]
                        profile = section_lookup_dict[property_name]
                        Fx = rnd(result[6])
                        Fy = rnd(result[7])
                        Fz = rnd(result[8])
                        Mx = rnd(result[9])
                        My = rnd(result[10])
                        Mz = rnd(result[11])
                        result_string = f"{id},{model},{case_number},{case_name},{model},{beam_number},{position},{group_name},{property_name},{profile},S355,{Lcrt},{Lcry},{Cmy},{Lcrz},{Cmz},{Lc},{Cmlt},{zg},{C1},{C2},,,{Fx},{Fy},{Fz},{My},{Mz},{Mx},ss_SG\n"
                        output_file.write(result_string)

                        if id % 100_000 == 0:
                            print(f"\t{id:,.0f} input rows written...")
                        id += 1


                    except KeyError as ke:
                        logging_warnings.append(f"Issue with dict key.\n"
                                                f"Unable to locate section for property: {ke}")

                    except OSError as ose:
                        logging_errors.append(f"Failed to write to output_file {OUTPUT_FP}. File may be in use or locked.")

    # Write relevant messages to log output_file.
    logging_warnings = list(set(logging_warnings))
    logging_warnings.sort()

    logging_errors = list(set(logging_errors))
    logging_errors.sort()

    for warning in logging_warnings:
        logging.warning(warning)

    for error in logging_errors:
        logging.error(error)

