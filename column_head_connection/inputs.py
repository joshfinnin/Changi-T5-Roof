
"""Script containing the inputs for the different modules for the critical combination extraction."""

from math import sin, cos, radians

bf_parq_files = {
    'LB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmax_Parquet\\beam_forces.parquet',
    'LB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmin_Parquet\\beam_forces.parquet',
    'UB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmax_Parquet\\beam_forces.parquet',
    'UB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmin_Parquet\\beam_forces.parquet'}

bp_parq_files = {
    'LB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmax_Parquet\\beam_properties.parquet',
    'LB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmin_Parquet\\beam_properties.parquet',
    'UB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmax_Parquet\\beam_properties.parquet',
    'UB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmin_Parquet\\beam_properties.parquet'}

bf_ext_als_parq_files = {
    "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmax_Parquet\beam_forces.parquet",
    "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmin_Parquet\beam_forces.parquet",
    "UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmax_Parquet\beam_forces.parquet",
    "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmin_Parquet\beam_forces.parquet",
    "0 ALS Removal P-TR01a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\0 ALS Removal P-TR01a-01_GlobalParquet\beam_forces.parquet",
    "1 ALS Removal P-TR01a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\1 ALS Removal P-TR01a-02_GlobalParquet\beam_forces.parquet",
    "10 ALS Removal P-TR02b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\10 ALS Removal P-TR02b-02_GlobalParquet\beam_forces.parquet",
    "12 ALS Removal P-TR03a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\12 ALS Removal P-TR03a-01_GlobalParquet\beam_forces.parquet",
    "13 ALS Removal P-TR03a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\13 ALS Removal P-TR03a-02_GlobalParquet\beam_forces.parquet",
    "14 ALS Removal P-TR03a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\14 ALS Removal P-TR03a-03_GlobalParquet\beam_forces.parquet",
    "15 ALS Removal P-TR03a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\15 ALS Removal P-TR03a-04_GlobalParquet\beam_forces.parquet",
    "16 ALS Removal P-TR03a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\16 ALS Removal P-TR03a-05_GlobalParquet\beam_forces.parquet",
    "17 ALS Removal P-TR03b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\17 ALS Removal P-TR03b-01_GlobalParquet\beam_forces.parquet",
    "18 ALS Removal P-TR03b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\18 ALS Removal P-TR03b-02_GlobalParquet\beam_forces.parquet",
    "19 ALS Removal P-TR03b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\19 ALS Removal P-TR03b-03_GlobalParquet\beam_forces.parquet",
    "2 ALS Removal P-TR01a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\2 ALS Removal P-TR01a-03_GlobalParquet\beam_forces.parquet",
    "20 ALS Removal P-TR03b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\20 ALS Removal P-TR03b-04_GlobalParquet\beam_forces.parquet",
    "21 ALS Removal P-TR03b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\21 ALS Removal P-TR03b-05_GlobalParquet\beam_forces.parquet",
    "22 ALS Removal P-TR04a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\22 ALS Removal P-TR04a-01_GlobalParquet\beam_forces.parquet",
    "23 ALS Removal P-TR04a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\23 ALS Removal P-TR04a-02_GlobalParquet\beam_forces.parquet",
    "24 ALS Removal P-TR04a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\24 ALS Removal P-TR04a-03_GlobalParquet\beam_forces.parquet",
    "25 ALS Removal P-TR04a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\25 ALS Removal P-TR04a-04_GlobalParquet\beam_forces.parquet",
    "26 ALS Removal P-TR04a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\26 ALS Removal P-TR04a-05_GlobalParquet\beam_forces.parquet",
    "27 ALS Removal P-TR04a-06": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\27 ALS Removal P-TR04a-06_GlobalParquet\beam_forces.parquet",
    "28 ALS Removal P-TR04a-07": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\28 ALS Removal P-TR04a-07_GlobalParquet\beam_forces.parquet",
    "29 ALS Removal P-TR04b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\29 ALS Removal P-TR04b-01_GlobalParquet\beam_forces.parquet",
    "3 ALS Removal P-TR01b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\3 ALS Removal P-TR01b-01_GlobalParquet\beam_forces.parquet",
    "30 ALS Removal P-TR04b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\30 ALS Removal P-TR04b-02_GlobalParquet\beam_forces.parquet",
    "31 ALS Removal P-TR04b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\31 ALS Removal P-TR04b-03_GlobalParquet\beam_forces.parquet",
    "32 ALS Removal P-TR04b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\32 ALS Removal P-TR04b-04_GlobalParquet\beam_forces.parquet",
    "33 ALS Removal P-TR04b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\33 ALS Removal P-TR04b-05_GlobalParquet\beam_forces.parquet",
    "34 ALS Removal P-TR04b-06": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\34 ALS Removal P-TR04b-06_GlobalParquet\beam_forces.parquet",
    "35 ALS Removal P-TR04b-07": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\35 ALS Removal P-TR04b-07_GlobalParquet\beam_forces.parquet",
    "36 ALS Removal S-TR02-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\36 ALS Removal S-TR02-01_GlobalParquet\beam_forces.parquet",
    "37 ALS Removal S-TR02-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\37 ALS Removal S-TR02-02_GlobalParquet\beam_forces.parquet",
    "38 ALS Removal S-TR05-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\38 ALS Removal S-TR05-01_GlobalParquet\beam_forces.parquet",
    "39 ALS Removal S-TR05-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\39 ALS Removal S-TR05-02_GlobalParquet\beam_forces.parquet",
    "4 ALS Removal P-TR01b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\4 ALS Removal P-TR01b-02_GlobalParquet\beam_forces.parquet",
    "40 ALS Removal S-TR04-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\40 ALS Removal S-TR04-01_GlobalParquet\beam_forces.parquet",
    "41 ALS Removal S-TR11-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\41 ALS Removal S-TR11-01_GlobalParquet\beam_forces.parquet",
    "42 ALS Removal S-TR13-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\42 ALS Removal S-TR13-01_GlobalParquet\beam_forces.parquet",
    "43 ALS Removal S-TR13-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\43 ALS Removal S-TR13-02_GlobalParquet\beam_forces.parquet",
    "44 ALS Removal S-TR13-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\44 ALS Removal S-TR13-03_GlobalParquet\beam_forces.parquet",
    "45 ALS Removal S-TR13-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\45 ALS Removal S-TR13-04_GlobalParquet\beam_forces.parquet",
    "46 ALS Removal S-TR14-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\46 ALS Removal S-TR14-01_GlobalParquet\beam_forces.parquet",
    "47 ALS Removal S-TR14-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\47 ALS Removal S-TR14-02_GlobalParquet\beam_forces.parquet",
    "48 ALS Removal S-TR14-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\48 ALS Removal S-TR14-03_GlobalParquet\beam_forces.parquet",
    "49 ALS Removal S-TR14-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\49 ALS Removal S-TR14-04_GlobalParquet\beam_forces.parquet",
    "5 ALS Removal P-TR01b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\5 ALS Removal P-TR01b-03_GlobalParquet\beam_forces.parquet",
    "50 ALS Removal S-TR01-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\50 ALS Removal S-TR01-01_GlobalParquet\beam_forces.parquet",
    "51 ALS Removal S-TR01-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\51 ALS Removal S-TR01-02_GlobalParquet\beam_forces.parquet",
    "52 ALS Removal S-TR01a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\52 ALS Removal S-TR01a-05_GlobalParquet\beam_forces.parquet",
    "53 ALS Removal S-TR01b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\53 ALS Removal S-TR01b-05_GlobalParquet\beam_forces.parquet",
    "54 ALS Removal S-TR02-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\54 ALS Removal S-TR02-03_GlobalParquet\beam_forces.parquet",
    "55 ALS Removal S-TR02a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\55 ALS Removal S-TR02a-05_GlobalParquet\beam_forces.parquet",
    "56 ALS Removal S-TR02b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\56 ALS Removal S-TR02b-05_GlobalParquet\beam_forces.parquet",
    "57 ALS Removal S-TR04-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\57 ALS Removal S-TR04-02_GlobalParquet\beam_forces.parquet",
    "58 ALS Removal S-TR05-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\58 ALS Removal S-TR05-03_GlobalParquet\beam_forces.parquet",
    "59 ALS Removal S-TR06-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\59 ALS Removal S-TR06-01_GlobalParquet\beam_forces.parquet",
    "6 ALS Removal P-TR02a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\6 ALS Removal P-TR02a-01_GlobalParquet\beam_forces.parquet",
    "60 ALS Removal S-TR06-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\60 ALS Removal S-TR06-02_GlobalParquet\beam_forces.parquet",
    "61 ALS Removal S-TR06-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\61 ALS Removal S-TR06-03_GlobalParquet\beam_forces.parquet",
    "62 ALS Removal S-TR07-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\62 ALS Removal S-TR07-01_GlobalParquet\beam_forces.parquet",
    "63 ALS Removal S-TR07-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\63 ALS Removal S-TR07-02_GlobalParquet\beam_forces.parquet",
    "64 ALS Removal S-TR07-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\64 ALS Removal S-TR07-03_GlobalParquet\beam_forces.parquet",
    "65 ALS Removal S-TR08-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\65 ALS Removal S-TR08-01_GlobalParquet\beam_forces.parquet",
    "66 ALS Removal S-TR11-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\66 ALS Removal S-TR11-02_GlobalParquet\beam_forces.parquet",
    "67 ALS Removal S-TR12-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\67 ALS Removal S-TR12-01_GlobalParquet\beam_forces.parquet",
    "68 ALS Removal TR01a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\68 ALS Removal TR01a-04_GlobalParquet\beam_forces.parquet",
    "69 ALS Removal TR01b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\69 ALS Removal TR01b-04_GlobalParquet\beam_forces.parquet",
    "7 ALS Removal P-TR02a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\7 ALS Removal P-TR02a-02_GlobalParquet\beam_forces.parquet",
    "70 ALS Removal TR02a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\70 ALS Removal TR02a-04_GlobalParquet\beam_forces.parquet",
    "71 ALS Removal TR02b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\71 ALS Removal TR02b-04_GlobalParquet\beam_forces.parquet",
    "8 ALS Removal P-TR02a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\8 ALS Removal P-TR02a-03_GlobalParquet\beam_forces.parquet",
    "9 ALS Removal P-TR02b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\9 ALS Removal P-TR02b-01_GlobalParquet\beam_forces.parquet",
}

bp_ext_als_parq_files = {
    "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmax_Parquet\beam_properties.parquet",
    "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmin_Parquet\beam_properties.parquet",
    "UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmax_Parquet\beam_properties.parquet",
    "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmin_Parquet\beam_properties.parquet",
    "0 ALS Removal P-TR01a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\0 ALS Removal P-TR01a-01_GlobalParquet\beam_properties.parquet",
    "1 ALS Removal P-TR01a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\1 ALS Removal P-TR01a-02_GlobalParquet\beam_properties.parquet",
    "10 ALS Removal P-TR02b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\10 ALS Removal P-TR02b-02_GlobalParquet\beam_properties.parquet",
    "11 ALS Removal P-TR02b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\11 ALS Removal P-TR02b-03_GlobalParquet\beam_properties.parquet",
    "12 ALS Removal P-TR03a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\12 ALS Removal P-TR03a-01_GlobalParquet\beam_properties.parquet",
    "13 ALS Removal P-TR03a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\13 ALS Removal P-TR03a-02_GlobalParquet\beam_properties.parquet",
    "14 ALS Removal P-TR03a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\14 ALS Removal P-TR03a-03_GlobalParquet\beam_properties.parquet",
    "15 ALS Removal P-TR03a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\15 ALS Removal P-TR03a-04_GlobalParquet\beam_properties.parquet",
    "16 ALS Removal P-TR03a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\16 ALS Removal P-TR03a-05_GlobalParquet\beam_properties.parquet",
    "17 ALS Removal P-TR03b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\17 ALS Removal P-TR03b-01_GlobalParquet\beam_properties.parquet",
    "18 ALS Removal P-TR03b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\18 ALS Removal P-TR03b-02_GlobalParquet\beam_properties.parquet",
    "19 ALS Removal P-TR03b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\19 ALS Removal P-TR03b-03_GlobalParquet\beam_properties.parquet",
    "2 ALS Removal P-TR01a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\2 ALS Removal P-TR01a-03_GlobalParquet\beam_properties.parquet",
    "20 ALS Removal P-TR03b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\20 ALS Removal P-TR03b-04_GlobalParquet\beam_properties.parquet",
    "21 ALS Removal P-TR03b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\21 ALS Removal P-TR03b-05_GlobalParquet\beam_properties.parquet",
    "22 ALS Removal P-TR04a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\22 ALS Removal P-TR04a-01_GlobalParquet\beam_properties.parquet",
    "23 ALS Removal P-TR04a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\23 ALS Removal P-TR04a-02_GlobalParquet\beam_properties.parquet",
    "24 ALS Removal P-TR04a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\24 ALS Removal P-TR04a-03_GlobalParquet\beam_properties.parquet",
    "25 ALS Removal P-TR04a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\25 ALS Removal P-TR04a-04_GlobalParquet\beam_properties.parquet",
    "26 ALS Removal P-TR04a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\26 ALS Removal P-TR04a-05_GlobalParquet\beam_properties.parquet",
    "27 ALS Removal P-TR04a-06": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\27 ALS Removal P-TR04a-06_GlobalParquet\beam_properties.parquet",
    "28 ALS Removal P-TR04a-07": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\28 ALS Removal P-TR04a-07_GlobalParquet\beam_properties.parquet",
    "29 ALS Removal P-TR04b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\29 ALS Removal P-TR04b-01_GlobalParquet\beam_properties.parquet",
    "3 ALS Removal P-TR01b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\3 ALS Removal P-TR01b-01_GlobalParquet\beam_properties.parquet",
    "30 ALS Removal P-TR04b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\30 ALS Removal P-TR04b-02_GlobalParquet\beam_properties.parquet",
    "31 ALS Removal P-TR04b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\31 ALS Removal P-TR04b-03_GlobalParquet\beam_properties.parquet",
    "32 ALS Removal P-TR04b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\32 ALS Removal P-TR04b-04_GlobalParquet\beam_properties.parquet",
    "33 ALS Removal P-TR04b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\33 ALS Removal P-TR04b-05_GlobalParquet\beam_properties.parquet",
    "34 ALS Removal P-TR04b-06": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\34 ALS Removal P-TR04b-06_GlobalParquet\beam_properties.parquet",
    "35 ALS Removal P-TR04b-07": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\35 ALS Removal P-TR04b-07_GlobalParquet\beam_properties.parquet",
    "36 ALS Removal S-TR02-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\36 ALS Removal S-TR02-01_GlobalParquet\beam_properties.parquet",
    "37 ALS Removal S-TR02-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\37 ALS Removal S-TR02-02_GlobalParquet\beam_properties.parquet",
    "38 ALS Removal S-TR05-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\38 ALS Removal S-TR05-01_GlobalParquet\beam_properties.parquet",
    "39 ALS Removal S-TR05-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\39 ALS Removal S-TR05-02_GlobalParquet\beam_properties.parquet",
    "4 ALS Removal P-TR01b-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\4 ALS Removal P-TR01b-02_GlobalParquet\beam_properties.parquet",
    "40 ALS Removal S-TR04-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\40 ALS Removal S-TR04-01_GlobalParquet\beam_properties.parquet",
    "41 ALS Removal S-TR11-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\41 ALS Removal S-TR11-01_GlobalParquet\beam_properties.parquet",
    "42 ALS Removal S-TR13-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\42 ALS Removal S-TR13-01_GlobalParquet\beam_properties.parquet",
    "43 ALS Removal S-TR13-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\43 ALS Removal S-TR13-02_GlobalParquet\beam_properties.parquet",
    "44 ALS Removal S-TR13-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\44 ALS Removal S-TR13-03_GlobalParquet\beam_properties.parquet",
    "45 ALS Removal S-TR13-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\45 ALS Removal S-TR13-04_GlobalParquet\beam_properties.parquet",
    "46 ALS Removal S-TR14-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\46 ALS Removal S-TR14-01_GlobalParquet\beam_properties.parquet",
    "47 ALS Removal S-TR14-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\47 ALS Removal S-TR14-02_GlobalParquet\beam_properties.parquet",
    "48 ALS Removal S-TR14-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\48 ALS Removal S-TR14-03_GlobalParquet\beam_properties.parquet",
    "49 ALS Removal S-TR14-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\49 ALS Removal S-TR14-04_GlobalParquet\beam_properties.parquet",
    "5 ALS Removal P-TR01b-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\5 ALS Removal P-TR01b-03_GlobalParquet\beam_properties.parquet",
    "50 ALS Removal S-TR01-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\50 ALS Removal S-TR01-01_GlobalParquet\beam_properties.parquet",
    "51 ALS Removal S-TR01-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\51 ALS Removal S-TR01-02_GlobalParquet\beam_properties.parquet",
    "52 ALS Removal S-TR01a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\52 ALS Removal S-TR01a-05_GlobalParquet\beam_properties.parquet",
    "53 ALS Removal S-TR01b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\53 ALS Removal S-TR01b-05_GlobalParquet\beam_properties.parquet",
    "54 ALS Removal S-TR02-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\54 ALS Removal S-TR02-03_GlobalParquet\beam_properties.parquet",
    "55 ALS Removal S-TR02a-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\55 ALS Removal S-TR02a-05_GlobalParquet\beam_properties.parquet",
    "56 ALS Removal S-TR02b-05": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\56 ALS Removal S-TR02b-05_GlobalParquet\beam_properties.parquet",
    "57 ALS Removal S-TR04-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\57 ALS Removal S-TR04-02_GlobalParquet\beam_properties.parquet",
    "58 ALS Removal S-TR05-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\58 ALS Removal S-TR05-03_GlobalParquet\beam_properties.parquet",
    "59 ALS Removal S-TR06-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\59 ALS Removal S-TR06-01_GlobalParquet\beam_properties.parquet",
    "6 ALS Removal P-TR02a-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\6 ALS Removal P-TR02a-01_GlobalParquet\beam_properties.parquet",
    "60 ALS Removal S-TR06-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\60 ALS Removal S-TR06-02_GlobalParquet\beam_properties.parquet",
    "61 ALS Removal S-TR06-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\61 ALS Removal S-TR06-03_GlobalParquet\beam_properties.parquet",
    "62 ALS Removal S-TR07-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\62 ALS Removal S-TR07-01_GlobalParquet\beam_properties.parquet",
    "63 ALS Removal S-TR07-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\63 ALS Removal S-TR07-02_GlobalParquet\beam_properties.parquet",
    "64 ALS Removal S-TR07-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\64 ALS Removal S-TR07-03_GlobalParquet\beam_properties.parquet",
    "65 ALS Removal S-TR08-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\65 ALS Removal S-TR08-01_GlobalParquet\beam_properties.parquet",
    "66 ALS Removal S-TR11-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\66 ALS Removal S-TR11-02_GlobalParquet\beam_properties.parquet",
    "67 ALS Removal S-TR12-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\67 ALS Removal S-TR12-01_GlobalParquet\beam_properties.parquet",
    "68 ALS Removal TR01a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\68 ALS Removal TR01a-04_GlobalParquet\beam_properties.parquet",
    "69 ALS Removal TR01b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\69 ALS Removal TR01b-04_GlobalParquet\beam_properties.parquet",
    "7 ALS Removal P-TR02a-02": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\7 ALS Removal P-TR02a-02_GlobalParquet\beam_properties.parquet",
    "70 ALS Removal TR02a-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\70 ALS Removal TR02a-04_GlobalParquet\beam_properties.parquet",
    "71 ALS Removal TR02b-04": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\71 ALS Removal TR02b-04_GlobalParquet\beam_properties.parquet",
    "8 ALS Removal P-TR02a-03": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\8 ALS Removal P-TR02a-03_GlobalParquet\beam_properties.parquet",
    "9 ALS Removal P-TR02b-01": r"D:\Projects\Changi T5\MUC\Strand7 Model Data\9 ALS Removal P-TR02b-01_GlobalParquet\beam_properties.parquet",
}

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


node_cos_ang_dicts = {m: {} for m in bf_parq_files.keys()}
node_sin_ang_dicts = {m: {} for m in bf_parq_files.keys()}

for model in bp_parq_files.keys():
    node_cos_ang_dicts[model]["B1"] = B1_node_force_cos_ang_dict
    node_sin_ang_dicts[model]["B1"] = B1_node_force_sin_ang_dict

    node_cos_ang_dicts[model]["B2"] = B2_node_force_cos_ang_dict
    node_sin_ang_dicts[model]["B2"] = B2_node_force_sin_ang_dict

    node_cos_ang_dicts[model]["C1"] = C1_node_force_cos_ang_dict
    node_sin_ang_dicts[model]["C1"] = C1_node_force_sin_ang_dict

    node_cos_ang_dicts[model]["C2"] = C2_node_force_cos_ang_dict
    node_sin_ang_dicts[model]["C2"] = C2_node_force_sin_ang_dict


node_dict = {"B1": (1715, 1782, 1788, 1852, 1709, 17761, 1644, 1707),
             "B2": (794, 726, 791, 21153, 867, 809, 875, 931),
             "C1": (2749, 2791, 2789, 2823, 21152, 2796, 2705, 2760),
             "C2": (2066, 17744, 2131, 2198, 2079, 2152, 1993, 2083)}

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

excluded_beam_dict = {
                "B1": (823, 825, 827, 828, 834, 835, 838, 839, 6278, 6324, 6328, 6549, 6580, 6602, 6613, 6614),
                "B2": (1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205, 6419, 6430, 6534, 6538, 6604, 6605, 6606, 6636),
                "C1": (719, 720, 721, 722, 747, 750, 751, 752, 6288, 6309, 6441, 6594, 6621, 6623, 6633, 6635),
                "C2": (911, 913, 914, 915, 997, 999, 1000, 1001, 6352, 6375, 6386, 6517, 6530, 6560, 6561, 6583)}

target_groups = ("'Leaf 03-07\\03-07\\1D\\G01 PrimaryTop'",
                 "'Leaf 03-07\\03-07\\1D\\G02 PrimaryBot'",
                 "'Leaf 03-07\\03-07\\1D\\G03 PrimaryDiag'",
                 "'Leaf 03-07\\03-07\\1D\\G04 PrimaryVert'",
                 "'Leaf 03-07\\03-07\\1D\\G27 BracingPlanTop'",
                 "'Leaf 03-07\\03-07\\1D\\G28 BracingPlanBot'")

target_groups = f"({', '.join(g for g in target_groups)})"

result_cases_to_ignore = ["'1: 1a [1a][U]'", "'2: 1b(0) [1b][M]'",
                          "'3: 1b [1b][M]'", "'1012: 1b [1b][M]'",
                          "'1013: 2&3(0) [2+3][M]'", "'1014: 2&3 [2+3][M]'",
                          "'1015: S2_G [2+3][M]'", "'1016: S2_Q [2+3][M]'", "'1017: S2_Gmax [2+3][M]'",
                          "'1018: S2_Gmax+LL [2+3][M]'", "'676: 1b(e) [1b][M]'",
                          "'677: 2&3 [2+3][M]'", "'678: 2&3(0) [2+3][M]'",
                          "'679: S2_Gmin [2+3][M]'"]

result_case_filter = f"({', '.join(result_cases_to_ignore)})"
