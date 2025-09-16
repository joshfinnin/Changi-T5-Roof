
import pathlib
import csv

# ----------------------------------------------------------------------
# FILE PATH INPUTS
# ----------------------------------------------------------------------
parq_output_directory = pathlib.Path(r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Main Column Baseplates\Filtered_Parquet")
connection_group_name = "Main Column Baseplates"
result_directory = pathlib.Path(
    r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Main Column Baseplates")

# ----------------------------------------------------------------------
# INPUT FOR SPLICE CONNECTION BEAM NUMBERS AND POSITIONS TO QUERY
# ----------------------------------------------------------------------
# NOTE: This is not used if extracting nodal forces
splice_input_csv = r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Main Column Baseplates\Column Base Points.csv"
with open(splice_input_csv, 'r') as splice_file:
    splice_positions = [r for r in csv.reader(splice_file)][1:]  # Ignore headers
    splice_data = tuple((int(s[0]), float(s[1])) for s in splice_positions)

# ----------------------------------------------------------------------
# INPUT FOR NODAL LOCATIONS TO QUERY
# ----------------------------------------------------------------------
# NOTE: This is not used if extracting splice forces
node_number_csv = r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\QL\CAL 12 Group 14 Nodes.csv"
with open(node_number_csv, 'r') as node_file:
    nodes = [r for r in csv.reader(node_file)][1:]  # Ignore headers
    node_data = tuple(int(n[0]) for n in nodes)

# ----------------------------------------------------------------------
# SECTION PROPERTY INPUTS
# ----------------------------------------------------------------------
section_properties_input_csv = r"E:\Projects\Changi\MUC\Section_Property_Definitions.csv"
# Read the section properties from an external file
with open(section_properties_input_csv, 'r') as section_file:
    section_data = [r for r in csv.reader(section_file)][1:]  # Ignore headers
    # Convert everything that isn't the section name to a float
    section_data = tuple(tuple([r[0]] + [float(n) for n in r[1:]]) for r in section_data)

# ----------------------------------------------------------------------
# PERMANENT MODEL INPUTS
# ----------------------------------------------------------------------
perm_forces_parq_dict = {
    "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_LB_Gmax_Parquet\beam_forces.parquet",
    "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_LB_Gmin_Parquet\beam_forces.parquet",
    "UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_UB_Gmax_Parquet\beam_forces.parquet",
    "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_UB_Gmin_Parquet\beam_forces.parquet",
    "SIF": r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\sif_full_beam_forces.parquet"}

perm_props_parq_dict = {
    "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_LB_Gmax_Parquet\beam_properties.parquet",
    "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_LB_Gmin_Parquet\beam_properties.parquet",
    "UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_UB_Gmax_Parquet\beam_properties.parquet",
    "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_UB_Gmin_Parquet\beam_properties.parquet",
    "SIF": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5\V1_4_5_LB_Gmax_SIF_Parquet\beam_properties.parquet"}

perm_beam_properties_parq = r"E:\Projects\Changi\MUC\Strand7 Model\adjusted_beam_properties.parquet"  # This has been altered for the column head truss chords (end nodes were redefined to force mapping)

perm_beam_forces_filtered_parq = parq_output_directory / "PERM_BEAM_FORCES.parquet"

# ----------------------------------------------------------------------
# ALS MODEL INPUTS
# ----------------------------------------------------------------------
als_directory = pathlib.Path(r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet")

als_models = [r"0 ALS Removal P-TR01a-01",
              r"1 ALS Removal P-TR01a-02",
              r"2 ALS Removal P-TR01a-03",
              r"3 ALS Removal P-TR01b-01",
              r"4 ALS Removal P-TR01b-02",
              r"5 ALS Removal P-TR01b-03",
              r"6 ALS Removal P-TR02a-01",
              r"7 ALS Removal P-TR02a-02",
              r"8 ALS Removal P-TR02a-03",
              r"9 ALS Removal P-TR02b-01",
              r"10 ALS Removal P-TR02b-02",
              r"11 ALS Removal P-TR02b-03",
              r"12 ALS Removal P-TR03a-01_BIF",
              r"13 ALS Removal P-TR03a-02",
              r"14 ALS Removal P-TR03a-03_BIF",
              r"15 ALS Removal P-TR03a-04",
              r"16 ALS Removal P-TR03a-05",
              r"17 ALS Removal P-TR03b-01",
              r"18 ALS Removal P-TR03b-02",
              r"19 ALS Removal P-TR03b-03",
              r"20 ALS Removal P-TR03b-04",
              r"21 ALS Removal P-TR03b-05",
              r"22 ALS Removal P-TR04a-01",
              r"23 ALS Removal P-TR04a-02",
              r"24 ALS Removal P-TR04a-03",
              r"25 ALS Removal P-TR04a-04",
              r"26 ALS Removal P-TR04a-05",
              r"27 ALS Removal P-TR04a-06",
              r"28 ALS Removal P-TR04a-07",
              r"29 ALS Removal P-TR04b-01_BIF",
              r"30 ALS Removal P-TR04b-02",
              r"31 ALS Removal P-TR04b-03_BIF",
              r"32 ALS Removal P-TR04b-04",
              r"33 ALS Removal P-TR04b-05",
              r"34 ALS Removal P-TR04b-06",
              r"35 ALS Removal P-TR04b-07",
              r"36 ALS Removal S-TR02-01",
              r"37 ALS Removal S-TR02-02",
              r"38 ALS Removal S-TR05-01",
              r"39 ALS Removal S-TR05-02",
              r"40 ALS Removal S-TR04-01",
              r"41 ALS Removal S-TR11-01",
              r"42 ALS Removal S-TR13-01",
              r"43 ALS Removal S-TR13-02",
              r"44 ALS Removal S-TR13-03",
              r"45 ALS Removal S-TR13-04",
              r"46 ALS Removal S-TR14-01",
              r"47 ALS Removal S-TR14-02",
              r"48 ALS Removal S-TR14-03",
              r"49 ALS Removal S-TR14-04",
              r"50 ALS Removal S-TR01-01",
              r"51 ALS Removal S-TR01-02",
              r"52 ALS Removal P-TR01a-05",
              r"53 ALS Removal P-TR01b-05",
              r"54 ALS Removal S-TR02-03",
              r"55 ALS Removal P-TR02a-05",
              r"56 ALS Removal S-TR02b-05",
              r"57 ALS Removal P-TR04-02",
              r"58 ALS Removal S-TR05-03",
              r"59 ALS Removal S-TR06-01",
              r"60 ALS Removal S-TR06-02",
              r"61 ALS Removal S-TR06-03",
              r"62 ALS Removal S-TR07-01",
              r"63 ALS Removal S-TR07-02",
              r"64 ALS Removal S-TR07-03",
              r"65 ALS Removal S-TR08-01",
              r"66 ALS Removal S-TR11-02",
              r"67 ALS Removal S-TR12-01",
              r"68 ALS Removal P-TR01a-04",
              r"69 ALS Removal P-TR01b-04",
              r"70 ALS Removal P-TR02a-04",
              r"71 ALS Removal P-TR02b-04",
              r"72 ALS Removal CHB1-T1",
              r"73 ALS Removal CHB1-T2",
              r"74 ALS Removal CHB1-T3",
              r"75 ALS Removal CHB1-T4",
              r"76 ALS Removal CHB1-B1",
              r"77 ALS Removal CHB1-B2",
              r"78 ALS Removal CHB1-B3",
              r"79 ALS Removal CHB1-B4",
              r"80 ALS Removal CHB1-D1",
              r"81 ALS Removal CHB1-D2",
              r"82 ALS Removal CHB1-D3",
              r"83 ALS Removal CHB1-D4",
              r"84 ALS Removal CHB2-T1",
              r"85 ALS Removal CHB2-T2",
              r"86 ALS Removal CHB2-T3",
              r"87 ALS Removal CHB2-T4",
              r"88 ALS Removal CHB2-B1",
              r"89 ALS Removal CHB2-B2",
              r"90 ALS Removal CHB2-B3",
              r"91 ALS Removal CHB2-B4",
              r"92 ALS Removal CHB2-D1",
              r"93 ALS Removal CHB2-D2",
              r"94 ALS Removal CHB2-D3",
              r"95 ALS Removal CHB2-D4",
              r"96 ALS Removal CHC2-T1",
              r"97 ALS Removal CHC2-T2",
              r"98 ALS Removal CHC2-T3",
              r"99 ALS Removal CHC2-T4",
              r"100 ALS Removal CHC2-B1",
              r"101 ALS Removal CHC2-B2",
              r"102 ALS Removal CHC2-B3",
              r"103 ALS Removal CHC2-B4",
              r"104 ALS Removal CHC2-D1",
              r"105 ALS Removal CHC2-D2",
              r"106 ALS Removal CHC2-D3",
              r"107 ALS Removal CHC2-D4",
              r"108 ALS Removal CHC1-T1",
              r"109 ALS Removal CHC1-T2",
              r"110 ALS Removal CHC1-T3",
              r"111 ALS Removal CHC1-T4",
              r"112 ALS Removal CHC1-B1",
              r"113 ALS Removal CHC1-B2",
              r"114 ALS Removal CHC1-B3",
              r"115 ALS Removal CHC1-B4",
              r"116 ALS Removal CHC1-D1",
              r"117 ALS Removal CHC1-D2",
              r"118 ALS Removal CHC1-D3",
              r"119 ALS Removal CHC1-D4",
              r"120 ALS Removal S-TR01-03",
              r"121 ALS Removal S-TR01-04",
              r"122 ALS Removal S-TR02-04",
              r"123 ALS Removal S-TR02-05",
              r"124 ALS Removal S-TR03-01",
              r"125 ALS Removal S-TR05-04",
              r"126 ALS Removal S-TR05-05",
              r"127 ALS Removal S-TR06-04",
              r"128 ALS Removal S-TR06-05",
              r"129 ALS Removal S-TR07-03",
              r"130 ALS Removal S-TR07-04",
              r"131 ALS Removal S-TR09-01",
              r"132 ALS Removal S-TR09-02",
              r"133 ALS Removal S-TR09-03",
              r"134 ALS Removal S-TR09-04",
              r"135 ALS Removal S-TR09-05",
              r"136 ALS Removal S-TR10-01",
              r"137 ALS Removal S-TR10-02",
              r"138 ALS Removal S-TR10-03",
              r"139 ALS Removal S-TR10-04",
              r"140 ALS Removal S-TR10-05",
              r"141 ALS Removal S-TR13-05",
              r"142 ALS Removal S-TR14-05"]


als_force_parq_dict = {m: als_directory / f"{m}\\beam_forces.parquet" for m in als_models}
als_prop_parq_dict = {m: als_directory / f"{m}\\beam_properties.parquet" for m in als_models}
als_summary_parq_folder_dict = {model: parq_output_directory / (model + "_filtered.parquet") for model in als_models}

