
"""Script containing the inputs for the different modules for the critical combination extraction."""


from math import sin, cos, radians
import pathlib
from datetime import date

# ----------------------------------------------------------------------
# MASTER FILE INPUTS AND LOCATION DATA
# ----------------------------------------------------------------------
COL_HEAD_LOCATION = "C1"
ALS_ONLY = True  # When True, uses on the PARQ files in the ALS PARQ FILE DICTS.  Ignores PERM forces.bf_ext_als_parq_files
output_folder_path = pathlib.Path(r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - Main Leaf Column Head")

output_date = date.today()
FULL_BEAM_FORCES_PARQUET = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\full_beam_forces.parquet"
BEAM_PROPERTY_PARQUET = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\full_beam_properties.parquet"
BEAM_ENDS_PARQUET = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\beams_ends.parquet"
NODAL_FORCE_PARQUET = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\full_nodal_forces.parquet"
TOP_OF_COLUMN_EXTREMA_OUTPUT_FP = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\{output_date}_{COL_HEAD_LOCATION} Column Head Connections_Column Worst Combinations.csv"
CRUCIFORM_OUTPUT_FP = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\{output_date}_{COL_HEAD_LOCATION} Cruciform Worst Combinations.csv"
NODAL_OUTPUT_FP = output_folder_path / f"{COL_HEAD_LOCATION} Loads\\{output_date}_{COL_HEAD_LOCATION} Nodal Worst Combinations.csv"

# ----------------------------------------------------------------------
# INPUT PARQUET FILES (FORCES AND PROPERTIES)
# ----------------------------------------------------------------------
BF_PERM_PARQ_FILE_DICT = {
    'LB_Gmax': 'C:\\Users\\jason.le\\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_LB_Gmax\\beam_forces.parquet',
    'LB_Gmin': 'C:\\Users\\jason.le\\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_LB_Gmin\\beam_forces.parquet',
    'UB_Gmax': 'C:\\Users\jason.le\\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_UB_Gmax\\beam_forces.parquet',
    'UB_Gmin': 'C:\\Users\\jason.le\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_UB_Gmmin\\beam_forces.parquet'}

BP_PERM_PARQ_FILE_DICT = {
    'LB_Gmax': 'C:\\Users\\jason.le\\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_LB_Gmax\\beam_properties.parquet',
    'LB_Gmin': 'C:\\Users\\jason.le\\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_LB_Gmin\\beam_properties.parquet',
    'UB_Gmax': 'C:\\Users\jason.le\\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_UB_Gmax\\beam_properties.parquet',
    'UB_Gmin': 'C:\\Users\\jason.le\Mott MacDonald\\MBC SAM Project Portal - V1.4.5\\Global Axes Parquet\\V1_4_5_UB_Gmmin\\beam_properties.parquet'}

BF_EXT_ALS_PARQ_FILE_DICT = {
    r"108 ALS Removal CHC1-T1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\108 ALS Removal CHC1-T1\beam_forces.parquet"
}

BP_EXT_ALS_PARQ_FILE_DICT = {
    r"0 ALS Removal P-TR01a-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\0 ALS Removal P-TR01a-01\beam_properties.parquet",
    r"1 ALS Removal P-TR01a-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\1 ALS Removal P-TR01a-02\beam_properties.parquet",
    r"2 ALS Removal P-TR01a-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\2 ALS Removal P-TR01a-03\beam_properties.parquet",
    r"3 ALS Removal P-TR01b-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\3 ALS Removal P-TR01b-01\beam_properties.parquet",
    r"4 ALS Removal P-TR01b-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\4 ALS Removal P-TR01b-02\beam_properties.parquet",
    r"5 ALS Removal P-TR01b-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\5 ALS Removal P-TR01b-03\beam_properties.parquet",
    r"6 ALS Removal P-TR02a-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\6 ALS Removal P-TR02a-01\beam_properties.parquet",
    r"7 ALS Removal P-TR02a-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\7 ALS Removal P-TR02a-02\beam_properties.parquet",
    r"8 ALS Removal P-TR02a-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\8 ALS Removal P-TR02a-03\beam_properties.parquet",
    r"9 ALS Removal P-TR02b-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\9 ALS Removal P-TR02b-01\beam_properties.parquet",
    r"10 ALS Removal P-TR02b-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\10 ALS Removal P-TR02b-02\beam_properties.parquet",
    r"11 ALS Removal P-TR02b-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\11 ALS Removal P-TR02b-03\beam_properties.parquet",
    r"12 ALS Removal P-TR03a-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\12 ALS Removal P-TR03a-01\beam_properties.parquet",
    r"13 ALS Removal P-TR03a-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\13 ALS Removal P-TR03a-02\beam_properties.parquet",
    r"14 ALS Removal P-TR03a-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\14 ALS Removal P-TR03a-03\beam_properties.parquet",
    r"15 ALS Removal P-TR03a-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\15 ALS Removal P-TR03a-04\beam_properties.parquet",
    r"16 ALS Removal P-TR03a-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\16 ALS Removal P-TR03a-05\beam_properties.parquet",
    r"17 ALS Removal P-TR03b-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\17 ALS Removal P-TR03b-01\beam_properties.parquet",
    r"18 ALS Removal P-TR03b-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\18 ALS Removal P-TR03b-02\beam_properties.parquet",
    r"19 ALS Removal P-TR03b-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\19 ALS Removal P-TR03b-03\beam_properties.parquet",
    r"20 ALS Removal P-TR03b-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\20 ALS Removal P-TR03b-04\beam_properties.parquet",
    r"21 ALS Removal P-TR03b-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\21 ALS Removal P-TR03b-05\beam_properties.parquet",
    r"22 ALS Removal P-TR04a-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\22 ALS Removal P-TR04a-01\beam_properties.parquet",
    r"23 ALS Removal P-TR04a-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\23 ALS Removal P-TR04a-02\beam_properties.parquet",
    r"24 ALS Removal P-TR04a-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\24 ALS Removal P-TR04a-03\beam_properties.parquet",
    r"25 ALS Removal P-TR04a-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\25 ALS Removal P-TR04a-04\beam_properties.parquet",
    r"26 ALS Removal P-TR04a-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\26 ALS Removal P-TR04a-05\beam_properties.parquet",
    r"27 ALS Removal P-TR04a-06": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\27 ALS Removal P-TR04a-06\beam_properties.parquet",
    r"28 ALS Removal P-TR04a-07": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\28 ALS Removal P-TR04a-07\beam_properties.parquet",
    r"29 ALS Removal P-TR04b-01": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\29 ALS Removal P-TR04b-01\beam_properties.parquet",
    r"30 ALS Removal P-TR04b-02": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\30 ALS Removal P-TR04b-02\beam_properties.parquet",
    r"31 ALS Removal P-TR04b-03": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\31 ALS Removal P-TR04b-03\beam_properties.parquet",
    r"32 ALS Removal P-TR04b-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\32 ALS Removal P-TR04b-04\beam_properties.parquet",
    r"33 ALS Removal P-TR04b-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\33 ALS Removal P-TR04b-05\beam_properties.parquet",
    r"34 ALS Removal P-TR04b-06": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\34 ALS Removal P-TR04b-06\beam_properties.parquet",
    r"35 ALS Removal P-TR04b-07": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\35 ALS Removal P-TR04b-07\beam_properties.parquet",
    r"52 ALS Removal P-TR01a-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\52 ALS Removal P-TR01a-05\beam_properties.parquet",
    r"53 ALS Removal P-TR01b-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\53 ALS Removal P-TR01b-05\beam_properties.parquet",
    r"55 ALS Removal P-TR02a-05": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\55 ALS Removal P-TR02a-05\beam_properties.parquet",
    r"57 ALS Removal P-TR04-02": r"CC:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\OutputsGlobal Axes Parquet\57 ALS Removal P-TR04-02\beam_properties.parquet",
    r"68 ALS Removal P-TR01a-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\68 ALS Removal P-TR01a-04\beam_properties.parquet",
    r"69 ALS Removal P-TR01b-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\69 ALS Removal P-TR01b-04\beam_properties.parquet",
    r"70 ALS Removal P-TR02a-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\70 ALS Removal P-TR02a-04\beam_properties.parquet",
    r"71 ALS Removal P-TR02b-04": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\71 ALS Removal P-TR02b-04\beam_properties.parquet",
    r"72 ALS Removal CHB1-T1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\72 ALS Removal CHB1-T1\beam_properties.parquet",
    r"73 ALS Removal CHB1-T2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\73 ALS Removal CHB1-T2\beam_properties.parquet",
    r"74 ALS Removal CHB1-T3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\74 ALS Removal CHB1-T3\beam_properties.parquet",
    r"75 ALS Removal CHB1-T4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\75 ALS Removal CHB1-T4\beam_properties.parquet",
    r"76 ALS Removal CHB1-B1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\76 ALS Removal CHB1-B1\beam_properties.parquet",
    r"77 ALS Removal CHB1-B2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\77 ALS Removal CHB1-B2\beam_properties.parquet",
    r"78 ALS Removal CHB1-B3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\78 ALS Removal CHB1-B3\beam_properties.parquet",
    r"79 ALS Removal CHB1-B4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\79 ALS Removal CHB1-B4\beam_properties.parquet",
    r"80 ALS Removal CHB1-D1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\80 ALS Removal CHB1-D1\beam_properties.parquet",
    r"81 ALS Removal CHB1-D2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\81 ALS Removal CHB1-D2\beam_properties.parquet",
    r"82 ALS Removal CHB1-D3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\82 ALS Removal CHB1-D3\beam_properties.parquet",
    r"83 ALS Removal CHB1-D4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\83 ALS Removal CHB1-D4\beam_properties.parquet",
    r"84 ALS Removal CHB2-T1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\84 ALS Removal CHB2-T1\beam_properties.parquet",
    r"85 ALS Removal CHB2-T2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\85 ALS Removal CHB2-T2\beam_properties.parquet",
    r"86 ALS Removal CHB2-T3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\86 ALS Removal CHB2-T3\beam_properties.parquet",
    r"87 ALS Removal CHB2-T4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\87 ALS Removal CHB2-T4\beam_properties.parquet",
    r"88 ALS Removal CHB2-B1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\88 ALS Removal CHB2-B1\beam_properties.parquet",
    r"89 ALS Removal CHB2-B2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\89 ALS Removal CHB2-B2\beam_properties.parquet",
    r"90 ALS Removal CHB2-B3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\90 ALS Removal CHB2-B3\beam_properties.parquet",
    r"91 ALS Removal CHB2-B4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\91 ALS Removal CHB2-B4\beam_properties.parquet",
    r"92 ALS Removal CHB2-D1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\92 ALS Removal CHB2-D1\beam_properties.parquet",
    r"93 ALS Removal CHB2-D2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\93 ALS Removal CHB2-D2\beam_properties.parquet",
    r"94 ALS Removal CHB2-D3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\94 ALS Removal CHB2-D3\beam_properties.parquet",
    r"95 ALS Removal CHB2-D4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\95 ALS Removal CHB2-D4\beam_properties.parquet",
    r"96 ALS Removal CHC2-T1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\96 ALS Removal CHC2-T1\beam_properties.parquet",
    r"97 ALS Removal CHC2-T2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\97 ALS Removal CHC2-T2\beam_properties.parquet",
    r"98 ALS Removal CHC2-T3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\98 ALS Removal CHC2-T3\beam_properties.parquet",
    r"99 ALS Removal CHC2-T4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\99 ALS Removal CHC2-T4\beam_properties.parquet",
    r"100 ALS Removal CHC2-B1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\100 ALS Removal CHC2-B1\beam_properties.parquet",
    r"101 ALS Removal CHC2-B2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\101 ALS Removal CHC2-B2\beam_properties.parquet",
    r"102 ALS Removal CHC2-B3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\102 ALS Removal CHC2-B3\beam_properties.parquet",
    r"103 ALS Removal CHC2-B4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\103 ALS Removal CHC2-B4\beam_properties.parquet",
    r"104 ALS Removal CHC2-D1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\104 ALS Removal CHC2-D1\beam_properties.parquet",
    r"105 ALS Removal CHC2-D2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\105 ALS Removal CHC2-D2\beam_properties.parquet",
    r"106 ALS Removal CHC2-D3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\106 ALS Removal CHC2-D3\beam_properties.parquet",
    r"107 ALS Removal CHC2-D4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\107 ALS Removal CHC2-D4\beam_properties.parquet",
    r"108 ALS Removal CHC1-T1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\108 ALS Removal CHC1-T1\beam_properties.parquet",
    r"109 ALS Removal CHC1-T2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\109 ALS Removal CHC1-T2\beam_properties.parquet",
    r"110 ALS Removal CHC1-T3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\110 ALS Removal CHC1-T3\beam_properties.parquet",
    r"111 ALS Removal CHC1-T4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\111 ALS Removal CHC1-T4\beam_properties.parquet",
    r"112 ALS Removal CHC1-B1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\112 ALS Removal CHC1-B1\beam_properties.parquet",
    r"113 ALS Removal CHC1-B2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\113 ALS Removal CHC1-B2\beam_properties.parquet",
    r"114 ALS Removal CHC1-B3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\114 ALS Removal CHC1-B3\beam_properties.parquet",
    r"115 ALS Removal CHC1-B4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\115 ALS Removal CHC1-B4\beam_properties.parquet",
    r"116 ALS Removal CHC1-D1": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\116 ALS Removal CHC1-D1\beam_properties.parquet",
    r"117 ALS Removal CHC1-D2": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\117 ALS Removal CHC1-D2\beam_properties.parquet",
    r"118 ALS Removal CHC1-D3": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\118 ALS Removal CHC1-D3\beam_properties.parquet",
    r"119 ALS Removal CHC1-D4": r"C:\Users\jason.le\Mott MacDonald\MBC SAM Project Portal - V1.4.5\ALS\Outputs\Global Axes Parquet\119 ALS Removal CHC1-D4\beam_properties.parquet"
}

# ----------------------------------------------------------------------
# COLUMN NUMBERS AND NODE NUMBERS
# ----------------------------------------------------------------------
column_beam_number_dict = {'B1': 2652, 'B2': 2665, 'C1': 2662, 'C2': 2663}

B1_node_force_cos_ang_dict = {1811: cos(radians(315)), 1748: cos(radians(315)),
                              1742: cos(radians(225)), 1678: cos(radians(225)),
                              1670: cos(radians(135)), 1609: cos(radians(135)),
                              3059: cos(radians(45)), 1672: cos(radians(45))}

B1_node_force_sin_ang_dict = {1811: sin(radians(315)), 1748: sin(radians(315)),
                              1742: sin(radians(225)), 1678: sin(radians(225)),
                              1670: sin(radians(135)), 1609: sin(radians(135)),
                              3059: sin(radians(45)), 1672: sin(radians(45))}

B2_node_force_cos_ang_dict = {899: cos(radians(315)), 823: cos(radians(315)),
                              835: cos(radians(225)), 770: cos(radians(225)),
                              779: cos(radians(135)), 714: cos(radians(135)),
                              843: cos(radians(45)), 768: cos(radians(45))}

B2_node_force_sin_ang_dict = {899: sin(radians(315)), 823: sin(radians(315)),
                              835: sin(radians(225)), 770: sin(radians(225)),
                              779: sin(radians(135)), 714: sin(radians(135)),
                              843: sin(radians(45)), 768: sin(radians(45))}

C1_node_force_cos_ang_dict = {2753: cos(radians(315)), 2719: cos(radians(315)),
                              2721: cos(radians(225)), 2680: cos(radians(225)),
                              2690: cos(radians(135)), 2644: cos(radians(135)),
                              2726: cos(radians(45)), 2691: cos(radians(45))}

C1_node_force_sin_ang_dict = {2753: sin(radians(315)), 2719: sin(radians(315)),
                              2721: sin(radians(225)), 2680: sin(radians(225)),
                              2690: sin(radians(135)), 2644: sin(radians(135)),
                              2726: sin(radians(45)), 2691: sin(radians(45))}

C2_node_force_cos_ang_dict = {2140: cos(radians(315)), 2073: cos(radians(315)),
                              3058: cos(radians(225)), 2015: cos(radians(225)),
                              2028: cos(radians(135)), 1950: cos(radians(135)),
                              2094: cos(radians(45)), 2024: cos(radians(45))}

C2_node_force_sin_ang_dict = {2140: sin(radians(315)), 2073: sin(radians(315)),
                              3058: sin(radians(225)), 2015: sin(radians(225)),
                              2028: sin(radians(135)), 1950: sin(radians(135)),
                              2094: sin(radians(45)), 2024: sin(radians(45))}

node_cos_ang_dicts = {}
node_sin_ang_dicts = {}

for model in BP_PERM_PARQ_FILE_DICT.keys():
    node_cos_ang_dicts["B1"] = B1_node_force_cos_ang_dict
    node_sin_ang_dicts["B1"] = B1_node_force_sin_ang_dict

    node_cos_ang_dicts["B2"] = B2_node_force_cos_ang_dict
    node_sin_ang_dicts["B2"] = B2_node_force_sin_ang_dict

    node_cos_ang_dicts["C1"] = C1_node_force_cos_ang_dict
    node_sin_ang_dicts["C1"] = C1_node_force_sin_ang_dict

    node_cos_ang_dicts["C2"] = C2_node_force_cos_ang_dict
    node_sin_ang_dicts["C2"] = C2_node_force_sin_ang_dict


NODE_DICT = {"B1": tuple(k for k in B1_node_force_cos_ang_dict.keys()),
             "B2": tuple(k for k in B2_node_force_cos_ang_dict.keys()),
             "C1": tuple(k for k in C1_node_force_cos_ang_dict.keys()),
             "C2": tuple(k for k in C2_node_force_cos_ang_dict.keys())}

# How are we going to do the differential loadings?
# Each differential condition is composed of sets of nodes moving in opposite directions.
# So a differential case is composed of:
# a) An axis
# b) A collection of nodes moving in the positive direction of that axis
# c) A collection of nodes moving in the negative direction of that axis

node_pairs_for_differential = {
    "Fx": {"B1": {"Set 1": [], "Set 2": []},
           "B2": {"Set 1": [], "Set 2": []},
           "C1": {"Set 1": [], "Set 2": []},
           "C2": {"Set 1": [], "Set 2": []}},
    "Fy": {"B1": {"Set 1": [], "Set 2": []},
           "B2": {"Set 1": [], "Set 2": []},
           "C1": {"Set 1": [], "Set 2": []},
           "C2": {"Set 1": [], "Set 2": []}},
    "Fxy": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}},
    "Fz1": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}},
    "Fz2": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}},
    "DT1": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}},
    "DT2": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}},
    "DT3": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}},
    "DT4": {"B1": {"Set 1": [], "Set 2": []},
            "B2": {"Set 1": [], "Set 2": []},
            "C1": {"Set 1": [], "Set 2": []},
            "C2": {"Set 1": [], "Set 2": []}}}

# ----------------------------------------------------------------------
# BEAMS AND GROUPS TO EXCLUDE FROM THE FORCE SUMMATION
# ----------------------------------------------------------------------
EXCLUDED_BEAM_DICT = {
                "B1": (823, 825, 827, 828, 834, 835, 838, 839, 6278, 6324, 6328, 6549, 6580, 6602, 6613, 6614),
                "B2": (1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205, 6419, 6430, 6534, 6538, 6604, 6605, 6606, 6636),
                "C1": (719, 720, 721, 722, 747, 750, 751, 752, 6288, 6309, 6441, 6594, 6621, 6623, 6633, 6635),
                "C2": (911, 913, 914, 915, 997, 999, 1000, 1001, 6352, 6375, 6386, 6517, 6530, 6560, 6561, 6583)}

TARGET_GROUPS = ("'Leaf 03-07\\03-07\\1D\\G01 PrimaryTop'",
                 "'Leaf 03-07\\03-07\\1D\\G02 PrimaryBot'",
                 "'Leaf 03-07\\03-07\\1D\\G03 PrimaryDiag'",
                 "'Leaf 03-07\\03-07\\1D\\G04 PrimaryVert'",
                 "'Leaf 03-07\\03-07\\1D\\G27 BracingPlanTop'",
                 "'Leaf 03-07\\03-07\\1D\\G28 BracingPlanBot'")

TARGET_GROUPS = f"({', '.join(g for g in TARGET_GROUPS)})"

# ----------------------------------------------------------------------
# RESULT CASES TO IGNORE
# ----------------------------------------------------------------------
result_cases_to_ignore = ["'1: 1a [1a][U]'", "'2: 1b(0) [1b][M]'",
                          "'3: 1b [1b][M]'", "'1012: 1b [1b][M]'",
                          "'1013: 2&3(0) [2+3][M]'", "'1014: 2&3 [2+3][M]'",
                          "'1015: S2_G [2+3][M]'", "'1016: S2_Q [2+3][M]'", "'1017: S2_Gmax [2+3][M]'",
                          "'1018: S2_Gmax+LL [2+3][M]'", "'676: 1b(e) [1b][M]'",
                          "'677: 2&3 [2+3][M]'", "'678: 2&3(0) [2+3][M]'",
                          "'679: S2_Gmin [2+3][M]'"]

RESULT_CASE_FILTER = f"({', '.join(result_cases_to_ignore)})"

#------------------------------------------------------
#Ordering dicts for column head nodes for IdeaStatica
#------------------------------------------------------

B1_ordering_dict = {1811: ("Top 1", 1),
                    1748: ("Btm 1", 2),
                    1742: ("Top 2", 3),
                    1678: ("Btm 2", 4),
                    1670: ("Top 3", 5),
                    1609: ("Btm 3", 6),
                    3059: ("Top 4", 7),
                    1672: ("Btm 4", 8)}

B1_ALS_ordering_dict = {1811: ("Top 1", 1),
                    1748: ("Btm 1", 2),
                    1742: ("Top 2", 3),
                    1678: ("Btm 2", 4),
                    1670: ("Top 3", 5),
                    1609: ("Btm 3", 6),
                    3059: ("Top 4", 7),
                    1672: ("Btm 4", 8)}

B2_ordering_dict = {899: ("Top 1", 2),
                    823: ("Btm 1", 1),
                    835: ("Top 2", 3),
                    770: ("Btm 2", 4),
                    779: ("Top 3", 5),
                    714: ("Btm 3", 6),
                    843: ("Top 4", 7),
                    768: ("Btm 4", 8)}

B2_ALS_ordering_dict = {899: ("Top 1", 2),
                    823: ("Btm 1", 1),
                    835: ("Top 2", 3),
                    770: ("Btm 2", 4),
                    779: ("Top 3", 5),
                    714: ("Btm 3", 6),
                    843: ("Top 4", 7),
                    768: ("Btm 4", 8)}

C1_ordering_dict = {2753: ("Top 1", 2),
                    2719: ("Btm 1", 1),
                    2721: ("Top 2", 3),
                    2680: ("Btm 2", 4),
                    2690: ("Top 3", 5),
                    2644: ("Btm 3", 6),
                    2726: ("Top 4", 7),
                    2691: ("Btm 4", 8)}

C1_ALS_ordering_dict = {2753: ("Top 1", 2),
                    2719: ("Btm 1", 1),
                    2721: ("Top 2", 3),
                    2680: ("Btm 2", 4),
                    2690: ("Top 3", 5),
                    2644: ("Btm 3", 6),
                    2726: ("Top 4", 7),
                    2691: ("Btm 4", 8)}

C2_ordering_dict = {2140: ("Top 1", 1),
                    2073: ("Btm 1", 2),
                    3058: ("Top 2", 3),
                    2015: ("Btm 2", 4),
                    2028: ("Top 3", 5),
                    1950: ("Btm 3", 6),
                    2094: ("Top 4", 7),
                    2024: ("Btm 4", 8)}

C2_ALS_ordering_dict = {2140: ("Top 1", 1),
                    2073: ("Btm 1", 2),
                    3058: ("Top 2", 3),
                    2015: ("Btm 2", 4),
                    2028: ("Top 3", 5),
                    1950: ("Btm 3", 6),
                    2094: ("Top 4", 7),
                    2024: ("Btm 4", 8)}

ordering_dicts = {"B1": B1_ordering_dict,
                  "B1_ALS": B1_ALS_ordering_dict,
                  "B2": B2_ordering_dict,
                  "B2_ALS": B2_ALS_ordering_dict,
                  "C1": C1_ordering_dict,
                  "C1_ALS": C1_ALS_ordering_dict,
                  "C2": C2_ordering_dict,
                  "C2_ALS": C2_ALS_ordering_dict}