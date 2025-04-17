
"""
Script for generating the input file for the DC Lightning runs.
"""

import csv
from Geometry.structural_geometry_mappers import query_from_sql
import logging

section_lookup_dict = {"E91 ExhaustSupport {CAT EN-SHS SHS200x200x6.3 20100728}": "SHS200x200x6.3",
                       "E92 ExhaustVert {CAT EN-SHS SHS200x200x8 20110705}": "SHS200x200x8",
                       "E93 ExhaustArc {CAT EN-RHS RHS200x150x6.3 20110705}": "RHS200x150x6.3",
                       "E94 ExhaustBeam {CAT EN-RHS RHS300x200x6.3 20100728}": "RHS300x200x6.3",
                       "E94 ExhaustBeam {CAT EN-RHS RHS300x200x8 20110705}": "RHS300x200x8",
                       "G01 PrimaryTop {CAT EN-CHS CHS356x12.5 20100728}": "CHS355.6x12.5",
                       "G01 PrimaryTop {CAT EN-CHS CHS356x16.0 20100728}": "CHS355.6x16",
                       "G01 PrimaryTop {CAT EN-CHS CHS406x12.5 20100728}": "CHS406.4x12.5",
                       "G01 PrimaryTop {CAT EN-CHS CHS406x16.0 20100728}": "CHS406.4x16",
                       "G01 PrimaryTop {CAT EN-CHS CHS406x25.0 20100728}": "CHS406.4x25",
                       "G02 PrimaryBot {CAT EN-CHS CHS356x12.5 20100728}": "CHS355.6x12.5",
                       "G02 PrimaryBot {CAT EN-CHS CHS356x16.0 20100728}": "CHS355.6x16",
                       "G02 PrimaryBot {CAT EN-CHS CHS406x12.5 20100728}": "CHS406.4x12.5",
                       "G02 PrimaryBot {CAT EN-CHS CHS406x16.0 20100728}": "CHS406.4x16",
                       "G02 PrimaryBot {CAT EN-CHS CHS406x32.0 20110705}": "CHS406.4x32",
                       "G03 PrimaryDiag {CAT EN-CHS CHS168.3x8 20100728}": "CHS168.3x8",
                       "G03 PrimaryDiag {CAT EN-CHS CHS168x6.3 20100728}": "CHS168.3x6.3",
                       "G03 PrimaryDiag {CAT EN-CHS CHS219x6.3 20100728}": "CHS219.1x6.3",
                       "G03 PrimaryDiag {CAT EN-CHS CHS245x6.3 20100728}": "CHS244.5x6.3",
                       "G03 PrimaryDiag {CAT EN-CHS CHS245x8.0 20100728}": "CHS244.5x8",
                       "G03 PrimaryDiag {CAT EN-CHS CHS273x10.0 20100728}": "CHS273x10",
                       "G03 PrimaryDiag {CAT EN-CHS CHS273x12.5 20100728}": "CHS273x12.5",
                       "G03 PrimaryDiag {CAT EN-CHS CHS273x8.0 20100728}": "CHS273x8",
                       "G04 PrimaryVert {CAT EN-CHS CHS140x5.0 20100728}": "CHS139.7x5",
                       "G04 PrimaryVert {CAT EN-CHS CHS168x6.3 20100728}": "CHS168.3x6.3",
                       "G04 PrimaryVert {CAT EN-CHS CHS219x6.3 20100728}": "CHS219.1x6.3",
                       "G05 SecondaryTop {CAT EN-CHS CHS273x10.0 20100728}": "CHS273x10",
                       "G05 SecondaryTop {CAT EN-CHS CHS273x12.5 20100728}": "CHS273x12.5",
                       "G05 SecondaryTop {CAT EN-CHS CHS273x8.0 20100728}": "CHS273x8",
                       "G05 SecondaryTop {CAT EN-CHS CHS324x10.0 20100728}": "CHS323.9x10",
                       "G05 SecondaryTop {CAT EN-CHS CHS324x12.5 20100728}": "CHS323.9x12.5",
                       "G06 SecondaryBot {CAT EN-CHS CHS273x10.0 20100728}": "CHS273x10",
                       "G06 SecondaryBot {CAT EN-CHS CHS273x12.5 20100728}": "CHS273x12.5",
                       "G06 SecondaryBot {CAT EN-CHS CHS273x8.0 20100728}": "CHS273x8",
                       "G06 SecondaryBot {CAT EN-CHS CHS324x10.0 20100728}": "CHS323.9x10",
                       "G06 SecondaryBot {CAT EN-CHS CHS324x12.5 20100728}": "CHS323.9x12.5",
                       "G07 SecondaryDiag {CAT EN-CHS CHS140x10 20100728}": "CHS139.7x10",
                       "G07 SecondaryDiag {CAT EN-CHS CHS140x5.0 20100728}": "CHS139.7x5",
                       "G07 SecondaryDiag {CAT EN-CHS CHS140x6.3 20100728}": "CHS139.7x6.3",
                       "G07 SecondaryDiag {CAT EN-CHS CHS168.3x8 20100708}": "CHS168.3x8",
                       "G07 SecondaryDiag {CAT EN-CHS CHS168x6.3 20100728}": "CHS168.3x6.3",
                       "G07 SecondaryDiag {CAT EN-CHS CHS219x12.5 20100708}": "CHS219.1x12.5",
                       "G07 SecondaryDiag {CAT EN-CHS CHS219x6.3 20100728}": "CHS219.1x6.3",
                       "G07 SecondaryDiag {CAT EN-CHS CHS219x8.0 20100728}": "CHS219.1x8",
                       "G07 SecondaryDiag {CAT EN-CHS CHS245x6.3 20100728}": "CHS244.5x6.3",
                       "G07 SecondaryDiag {CAT EN-CHS CHS245x8.0 20100728}": "CHS244.5x8",
                       "G07 SecondaryVert {CAT EN-CHS CHS140x5.0 20100728}": "CHS139.7x5",
                       "G08 SecondaryVert {CAT EN-CHS CHS114x6.3 20100728}": "CHS114.3x6.3",
                       "G09 EdgeTrussTop {CAT BSI-UC UC203x203x86 20170901}": "UC203x203x86.1",
                       "G09 EdgeTrussTop {CAT BSI-UC UC254x254x107 20170901}": "UC254x254x107.1",
                       "G09 EdgeTrussTop {CAT BSI-UC UC254x254x132 20170901}": "UC254x254x132",
                       "G10 EdgeTrussBot {CAT BSI-UC UC203x203x86 20170901}": "UC203x203x86.1",
                       "G10 EdgeTrussBot {CAT BSI-UC UC254x254x107 20170901}": "UC254x254x107.1",
                       "G10 EdgeTrussBot {CAT BSI-UC UC254x254x132 20170901}": "UC254x254x132",
                       "G100 QLColumn Haunch {UB533x312x270.8}": "UB533x312x270.8",
                       "G100 QLColumn {CAT BS-UB 533x312x272 20170811}": "UB533x312x270.8",
                       "G100 QLColumn {CAT BSI-UC UC356x368x177 20170901}": "UB356x368x177",
                       "G100 QLColumn {CAT BSI-UC UC356x406x287 20170901}": "UB356x406x287.1",
                       "G10x StairBaseSupport": "SHS75x75x6.3",
                       "G10x StairHanger": "SHS100x100x6.3",
                       "G10x StairRoofSupport": "SHS200x200x6.3",
                       "G11 EdgeTrussDiag {CAT BSI-UB UB203x102x23 20170901}": "UB203x102x23.1",
                       "G11 EdgeTrussDiag {CAT EN-CHS CHS114x6.3 20100728}": "CHS114.3x6.3",
                       "G11 EdgeTrussDiag {CAT EN-CHS CHS140x6.3 20100728}": "CHS139.7x6.3",
                       "G11 EdgeTrussDiag {CAT EN-CHS CHS140x8.0 20100728}": "CHS139.7x8",
                       "G11 EdgeTrussDiag {CAT EN-CHS CHS219x8.0 20100728}": "CHS219.1x8",
                       "G12 EdgeTrussVert {CAT BSI-UB UB203x133x25 20170901}": "UB203x133x25.1",
                       "G12 EdgeTrussVert {CAT EN-CHS CHS114x5.0 20100728}": "CHS114.3x5",
                       "G23 PurlinTop {CAT BS-UB 457x191x106 20170811}": "UB457x191x105.7",
                       "G23 PurlinTop {CAT BSI-UB UB457x191x89 20170901}": "UB457x191x89.3",
                       "G23 PurlinTop {CAT EN-RHS RHS300x200x10 20110705}": "RHS300x200x10",
                       "G23 PurlinTop {CAT EN-RHS RHS300x200x12.5 20100728}": "RHS300x200x12.5",
                       "G23 PurlinTop {CAT EN-RHS RHS300x200x8 20110705}": "RHS300x200x8",
                       "G24 PurlinBot {CAT EN-RHS RHS200x150x10 20100728}": "RHS200x150x10",
                       "G24 PurlinBot {CAT EN-RHS RHS200x150x12.5 20100728}": "RHS200x150x12.5",
                       "G24 PurlinBot {CAT EN-RHS RHS200x150x6.3 20100728}": "RHS200x150x6.3",
                       "G24 PurlinBot {CAT EN-RHS RHS200x150x8 20100728}": "RHS200x150x8",
                       "G25 BracingClipOnTop {CAT EN-CHS CHS168.3x8 20100728}": "CHS168.3x8",
                       "G26 BracingClipOnBot {CAT EN-CHS CHS168x6.3 20100728}": "CHS168.3x6.3",
                       "G26 BracingClipOnBot {CAT EN-CHS CHS168x8.0 20100728}": "CHS168.3x8",
                       "G27 BracingPlanTop {CAT EN-CHS CHS168x6.3 20100728}": "CHS168.3x6.3",
                       "G27 BracingPlanTop {CAT EN-CHS CHS219x16 20100728}": "CHS219.1x16",
                       "G27 BracingPlanTop {CAT EN-CHS CHS245x6.3 20100728}": "CHS244.5x6.3",
                       "G28 BracingPlanBot {CAT EN-CHS CHS168x6.3 20100728}": "CHS168.3x6.3",
                       "G28 BracingPlanBot {CAT EN-CHS CHS219x6.3 20100728}": "CHS219.1x6.3",
                       "G29 ClipOnEdge {CAT EN-RHS RHS200x150x6.3 20110705}": "RHS200x150x6.3",
                       "G29 ClipOnEdge {CAT EN-RHS RHS300x250x8 20110705}": "RHS300x200x8",
                       "G30 ClipOnVert {CAT EN-RHS RHS150x100x6.3 20100728}": "RHS150x100x6.3",
                       "G31 ClipOnTop Haunch {RHS250x150x10}": "RHS250x150x10",
                       "G31 ClipOnTop Haunch {RHS450x250x10}": "RHS450x250x10",
                       "G31 ClipOnTop {CAT BSI-UB UB406x178x54 20170901}": "UB406x178x54.1",
                       "G31 ClipOnTop {CAT BSI-UB UB457x191x82 20170901}": "UB457x191x82",
                       "G31 ClipOnTop {CAT EN-RHS RHS250x150x10.0 20100728}": "RHS250x150x10",
                       "G31 ClipOnTop {CAT EN-RHS RHS250x150x6.3 20100728}": "RHS250x150x6.3",
                       "G31 ClipOnTop {CAT EN-RHS RHS250x150x8.0 20100728}": "RHS250x150x8",
                       "G31 ClipOnTop {CAT EN-RHS RHS450x250x10 20110705}": "RHS450x250x10",
                       "G31 ClipOnTop {CAT EN-RHS RHS500x300x10 20110705}": "RHS500x300x10",
                       "G32 ClipOnBot {CAT EN-RHS RHS250x150x6.3 20100728}": "RHS250x150x6.3",
                       "G33 ClipOnDiag {CAT EN-RHS RHS150x100x6.3 20100728}": "RHS150x100x6.3",
                       "G40 FacadeHeader {CAT EN-RHS RHS350x150x12.5 20110705}": "RHS350x150x16",
                       "G41 FacadeBot {RHS400x200x12.5}": "RHS400x200x12.5",
                       "G44 ColHeadDiag {CAT EN-CHS CHS273x10.0 20100728}": "CHS273x10",
                       "G45 ColHeadVert {CAT EN-CHS CHS356x16.0 20100728}": "CHS355.6x16",
                       "G50 ClerestoryMullion {SHS250x250x12.5}": "SHS250x250x12.5",
                       "G60 RooflightPrimary {RHS500x300x12.5}": "RHS500x300x12.5",
                       "G61 RooflightSecondary {RHS200x100x12.5}": "RHS200x100x12.5",
                       "G62 RooflightTertiary {RHS120x60x5}": "RHS120x60x5",
                       "G63 RooflightUpstand {CAT EN-SHS SHS200x200x8 20110705}": "SHS200x200x8",
                       "G80 EdgeArm {CAT EN-RHS RHS150x100x6.3 20100728}": "RHS150x100x6.3",
                       "G81 EdgeOuter {CAT EN-SHS SHS140x140x8 20110705}": "SHS140x140x8",
                       "G82 Outrigger {CAT EN-SHS SHS140x140x6 20100728}": "SHS140x140x6",
                       "G83 EdgePurlinTop {CAT EN-RHS RHS300x200x10 20110705}": "RHS300x200x10",
                       "G84 EdgePurlinBot {CAT EN-RHS RHS250x150x16.0 20100728}": "RHS250x150x16",
                       "G84 EdgePurlinBot {CAT EN-RHS RHS250x150x8.0 20100728}": "RHS250x150x8",
                       "G87 EdgeGutter {CAT EN-RHS RHS100x60x5 20110705}": "RHS100x60x5",
                       "G87 EdgeGutter {CAT EN-RHS RHS300x200x10 20110705}": "RHS300x200x10",
                       "G87 EdgeGutter {CAT EN-RHS RHS300x250x10 20110705}": "RHS300x250x10",
                       "G88 CatWalkStringer {CAT BSI-UB UB356x127x33 20170901}": "UB356x127x33.1",
                       "G88 CatWalkStringer {CAT BSI-UB UB356x171x51 20170901}": "UB356x171x51",
                       "G89 LiftingBeam {CAT BSI-UB UB152x89x16 20170901}": "UB152x89x16",
                       "G90 QLRoofPrimary {CAT BS-UB 533x312x272 20170811}": "UB533x312x270.8",
                       "G90 QLRoofPrimary {UB762x267x308}": "UB762x267x308",
                       "G90 QLRoofPrimary {CAT BSI-UB UB1016x305x249 20170901}": "UB1016x305x249",
                       "G91 QLRoofSecondary {CAT BSI-UB UB406x178x54 20170901}": "UB406x178x54.1",
                       "G91 QLRoofSecondary {CAT EN-RHS RHS500x300x10 20110705}": "RHS500x300x10",
                       "G92 QLRoofBracing {CAT EN-CHS CHS140x8.0 20100728}": "CHS139.7x8",
                       "G93 QLCeilingPrimary {Unknown}": "UB457x191x67.1",
                       "G93 QLCeilingPrimary_{CAT BS-UB 533x210x92 20170811}": "UB533x210x92.1",
                       "G94 QLCeilingSecondary_Comp {UB406x178x60.1}": "UB406x178x60.1",
                       "G95 CeilingSecondaryPortal {CAT BS-UB 533x312x182 20170811}": "UB533x312x181.6",
                       "G95 CeilingSecondaryPortal {CAT BS-UB 533x312x272 20170811}": "UB533x312x270.8",
                       "G96 QLCeilingNoggings {CAT BSI-UB UB127x76x13 20170901}": "UB127x76x13",
                       "G97 QLCeilingBracing {CAT EN-CHS CHS76x6.3 20110705}": "CHS76.1x6.3",
                       "G98 QLVerticalBracing {CAT EN-CHS CHS168x10.0 20100728}": "CHS168.3x10",
                       "G99 QLClipOnExtension {CAT EN-SHS SHS100x100x10 20110705}": "SHS100x100x10",
                       "G40 FacadeHeader {CAT EN-RHS RHS400x200x10 20110705}": "RHS350x150x16",
                       "G100 QLColumn {UB533x312x331}": "UB533x312x331"
                       }

position_dict = {0.0: 1,
                 0.25: 2,
                 0.5: 3,
                 0.75: 4,
                 1.0: 5}


def rnd(f: float, precision=2):
    return round(f, precision)


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # FILE PATH INPUTS FOR THE STRAND DATABASES AND OUTPUT FILE
    # ----------------------------------------------------------------------

    strand_db_dict = {"UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\UB_Gmax\V1_3_6_UB_Gmax.db",
                      "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\UB_Gmin\V1_3_6_UB_Gmin.db",
                      "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\LB_Gmax\V1_3_6_LB_Gmax.db",
                      "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\LB_Gmin\V1_3_6_LB_Gmin.db"}

    effective_length_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\Updated Staging\Purlin Checks\Initial_Effective_Lengths.csv"
    output_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\Updated Staging\Purlin Checks\V1_3_6_Combined_Unstaged_Model_Checks.csv"
    logging_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.6\Updated Staging\Purlin Checks\DC Lighting Unstaged Input File Error Log.txt"

    # ----------------------------------------------------------------------
    # SETUP LOGGING
    # ----------------------------------------------------------------------

    logging.basicConfig(filename=logging_fp, level=logging.INFO)
    logging_warnings = []

    # ----------------------------------------------------------------------
    # GET EFFECTIVE LENGTH INPUTS
    # ----------------------------------------------------------------------

    with open(effective_length_fp, 'r') as length_file:
        effective_length_dict = {int(d["BeamNumber"]): d for d in csv.DictReader(length_file)}

    # ----------------------------------------------------------------------
    # ITERATE THROUGH THE FORCE RESULTS AND WRITE THE INPUT FILE FOR THE
    # DC LIGHTNING RUNS
    # ----------------------------------------------------------------------

    FORCE_QUERY = """SELECT
    BF.BeamNumber,
    ResultCase,
    ResultCaseName,
    PropertyName,
    GroupName,
    Position,
    Fx,
    Fy,
    Fz,
    Mx,
    My,
    Mz
    FROM BeamForces AS BF
    JOIN BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber
    WHERE GroupName LIKE "%PurlinTop%" 
    OR GroupName LIKE "%PurlinBot%";"""

    with open(output_fp, 'w+') as output_file:
        output_file.write("Id,BeamNumber,ResultCase,StationPoint,CrossSectionId,Steel Grade,L_cry [m],L_crz [m],L_crt [m],L_c [m],N_Ed [kN],V_yEd [kN],V_zEd [kN],M_yEd [kNm],M_zEd [kNm],M_TEd [kNm],National Annex\n")

        # Iterate through each of the model database files to get the results
        for model_name, model_db in strand_db_dict.items():
            force_results = query_from_sql(model_db, FORCE_QUERY, results_as_dict=True)

            for result in force_results:
                # There are some keys that won't map correctly (not meant to be designed in this module)
                try:
                    beam_number = result["BeamNumber"]
                    Lby = effective_length_dict[beam_number]["Lby"]
                    Lbz = effective_length_dict[beam_number]["Lbz"]
                    Lbt = effective_length_dict[beam_number]["Lbt"]
                    case_name = result["ResultCaseName"]
                    case_name = case_name.replace(":", "#")
                    position = result["Position"]
                    profile = section_lookup_dict[result["PropertyName"]]
                    Fx = rnd(result["Fx"])
                    Fy = rnd(result["Fy"])
                    Fz = rnd(result["Fz"])
                    Mx = rnd(result["Mx"])
                    My = rnd(result["My"])
                    Mz = rnd(result["Mz"])
                    result_string = f"{model_name}-{beam_number}-{case_name}-{position},{beam_number},1,{position},{profile},S355,{Lby},{Lbz},{Lbt},{Lbz},{Fx},{Fy},{Fz},{My},{Mz},{Mx},ss_SG\n"
                    output_file.write(result_string)

                except KeyError as ke:
                    logging_warnings.append(f"Unable to locate section for property: {ke}")

    logging_warnings = list(set(logging_warnings))
    logging_warnings.sort()
    for warning in logging_warnings:
        logging.warning(warning)

