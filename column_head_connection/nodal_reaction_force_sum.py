"""
Script for extracting the member forces at each corner node on the column head connections.
The reactions from each of the beams that are not internal to the column head are summed for each combination in
the global axes.  The resultant forces for each combination are then reported back in two ways; in the global axes,
and in the axes of the cruciform (45 degrees to global).

Target groups:
Leaf 03-07\03-07\1D\G01 PrimaryTop
Leaf 03-07\03-07\1D\G02 PrimaryBot
Leaf 03-07\03-07\1D\G03 PrimaryDiag
Leaf 03-07\03-07\1D\G04 PrimaryVert
Leaf 03-07\03-07\1D\G27 BracingPlanTop
Leaf 03-07\03-07\1D\G28 BracingPlanBot
"""

import duckdb
import csv
from math import cos, sin, radians

bf_parq_files = {
    "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmax_Parquet\beam_forces.parquet",
    "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmin_Parquet\beam_forces.parquet",
    "UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmax_Parquet\beam_forces.parquet",
    "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmin_Parquet\beam_forces.parquet",
    "0 ALS Removal P-TR01a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\0 ALS Removal P-TR01a-01_GlobalParquet\beam_forces.parquet",
    "1 ALS Removal P-TR01a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\1 ALS Removal P-TR01a-02_GlobalParquet\beam_forces.parquet",
    "10 ALS Removal P-TR02b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\10 ALS Removal P-TR02b-02_GlobalParquet\beam_forces.parquet",
    "100 ALS Removal CHC2-B1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\100 ALS Removal CHC2-B1_GlobalParquet\beam_forces.parquet",
    "101 ALS Removal CHC2-B2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\101 ALS Removal CHC2-B2_GlobalParquet\beam_forces.parquet",
    "102 ALS Removal CHC2-B3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\102 ALS Removal CHC2-B3_GlobalParquet\beam_forces.parquet",
    "103 ALS Removal CHC2-B4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\103 ALS Removal CHC2-B4_GlobalParquet\beam_forces.parquet",
    "104 ALS Removal CHC2-D1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\104 ALS Removal CHC2-D1_GlobalParquet\beam_forces.parquet",
    "105 ALS Removal CHC2-D2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\105 ALS Removal CHC2-D2_GlobalParquet\beam_forces.parquet",
    "106 ALS Removal CHC2-D3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\106 ALS Removal CHC2-D3_GlobalParquet\beam_forces.parquet",
    "107 ALS Removal CHC2-D4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\107 ALS Removal CHC2-D4_GlobalParquet\beam_forces.parquet",
    "11 ALS Removal P-TR02b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\11 ALS Removal P-TR02b-03_GlobalParquet\beam_forces.parquet",
    "12 ALS Removal P-TR03a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\12 ALS Removal P-TR03a-01_GlobalParquet\beam_forces.parquet",
    "13 ALS Removal P-TR03a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\13 ALS Removal P-TR03a-02_GlobalParquet\beam_forces.parquet",
    "14 ALS Removal P-TR03a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\14 ALS Removal P-TR03a-03_GlobalParquet\beam_forces.parquet",
    "15 ALS Removal P-TR03a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\15 ALS Removal P-TR03a-04_GlobalParquet\beam_forces.parquet",
    "16 ALS Removal P-TR03a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\16 ALS Removal P-TR03a-05_GlobalParquet\beam_forces.parquet",
    "17 ALS Removal P-TR03b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\17 ALS Removal P-TR03b-01_GlobalParquet\beam_forces.parquet",
    "18 ALS Removal P-TR03b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\18 ALS Removal P-TR03b-02_GlobalParquet\beam_forces.parquet",
    "19 ALS Removal P-TR03b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\19 ALS Removal P-TR03b-03_GlobalParquet\beam_forces.parquet",
    "2 ALS Removal P-TR01a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\2 ALS Removal P-TR01a-03_GlobalParquet\beam_forces.parquet",
    "20 ALS Removal P-TR03b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\20 ALS Removal P-TR03b-04_GlobalParquet\beam_forces.parquet",
    "21 ALS Removal P-TR03b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\21 ALS Removal P-TR03b-05_GlobalParquet\beam_forces.parquet",
    "22 ALS Removal P-TR04a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\22 ALS Removal P-TR04a-01_GlobalParquet\beam_forces.parquet",
    "23 ALS Removal P-TR04a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\23 ALS Removal P-TR04a-02_GlobalParquet\beam_forces.parquet",
    "24 ALS Removal P-TR04a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\24 ALS Removal P-TR04a-03_GlobalParquet\beam_forces.parquet",
    "25 ALS Removal P-TR04a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\25 ALS Removal P-TR04a-04_GlobalParquet\beam_forces.parquet",
    "26 ALS Removal P-TR04a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\26 ALS Removal P-TR04a-05_GlobalParquet\beam_forces.parquet",
    "27 ALS Removal P-TR04a-06": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\27 ALS Removal P-TR04a-06_GlobalParquet\beam_forces.parquet",
    "28 ALS Removal P-TR04a-07": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\28 ALS Removal P-TR04a-07_GlobalParquet\beam_forces.parquet",
    "29 ALS Removal P-TR04b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\29 ALS Removal P-TR04b-01_GlobalParquet\beam_forces.parquet",
    "3 ALS Removal P-TR01b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\3 ALS Removal P-TR01b-01_GlobalParquet\beam_forces.parquet",
    "30 ALS Removal P-TR04b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\30 ALS Removal P-TR04b-02_GlobalParquet\beam_forces.parquet",
    "31 ALS Removal P-TR04b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\31 ALS Removal P-TR04b-03_GlobalParquet\beam_forces.parquet",
    "32 ALS Removal P-TR04b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\32 ALS Removal P-TR04b-04_GlobalParquet\beam_forces.parquet",
    "33 ALS Removal P-TR04b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\33 ALS Removal P-TR04b-05_GlobalParquet\beam_forces.parquet",
    "34 ALS Removal P-TR04b-06": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\34 ALS Removal P-TR04b-06_GlobalParquet\beam_forces.parquet",
    "35 ALS Removal P-TR04b-07": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\35 ALS Removal P-TR04b-07_GlobalParquet\beam_forces.parquet",
    "36 ALS Removal S-TR02-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\36 ALS Removal S-TR02-01_GlobalParquet\beam_forces.parquet",
    "37 ALS Removal S-TR02-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\37 ALS Removal S-TR02-02_GlobalParquet\beam_forces.parquet",
    "38 ALS Removal S-TR05-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\38 ALS Removal S-TR05-01_GlobalParquet\beam_forces.parquet",
    "39 ALS Removal S-TR05-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\39 ALS Removal S-TR05-02_GlobalParquet\beam_forces.parquet",
    "4 ALS Removal P-TR01b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\4 ALS Removal P-TR01b-02_GlobalParquet\beam_forces.parquet",
    "40 ALS Removal S-TR04-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\40 ALS Removal S-TR04-01_GlobalParquet\beam_forces.parquet",
    "41 ALS Removal S-TR11-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\41 ALS Removal S-TR11-01_GlobalParquet\beam_forces.parquet",
    "42 ALS Removal S-TR13-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\42 ALS Removal S-TR13-01_GlobalParquet\beam_forces.parquet",
    "43 ALS Removal S-TR13-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\43 ALS Removal S-TR13-02_GlobalParquet\beam_forces.parquet",
    "44 ALS Removal S-TR13-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\44 ALS Removal S-TR13-03_GlobalParquet\beam_forces.parquet",
    "45 ALS Removal S-TR13-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\45 ALS Removal S-TR13-04_GlobalParquet\beam_forces.parquet",
    "46 ALS Removal S-TR14-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\46 ALS Removal S-TR14-01_GlobalParquet\beam_forces.parquet",
    "47 ALS Removal S-TR14-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\47 ALS Removal S-TR14-02_GlobalParquet\beam_forces.parquet",
    "48 ALS Removal S-TR14-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\48 ALS Removal S-TR14-03_GlobalParquet\beam_forces.parquet",
    "49 ALS Removal S-TR14-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\49 ALS Removal S-TR14-04_GlobalParquet\beam_forces.parquet",
    "5 ALS Removal P-TR01b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\5 ALS Removal P-TR01b-03_GlobalParquet\beam_forces.parquet",
    "50 ALS Removal S-TR01-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\50 ALS Removal S-TR01-01_GlobalParquet\beam_forces.parquet",
    "51 ALS Removal S-TR01-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\51 ALS Removal S-TR01-02_GlobalParquet\beam_forces.parquet",
    "52 ALS Removal S-TR01a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\52 ALS Removal S-TR01a-05_GlobalParquet\beam_forces.parquet",
    "53 ALS Removal S-TR01b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\53 ALS Removal S-TR01b-05_GlobalParquet\beam_forces.parquet",
    "54 ALS Removal S-TR02-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\54 ALS Removal S-TR02-03_GlobalParquet\beam_forces.parquet",
    "55 ALS Removal S-TR02a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\55 ALS Removal S-TR02a-05_GlobalParquet\beam_forces.parquet",
    "56 ALS Removal S-TR02b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\56 ALS Removal S-TR02b-05_GlobalParquet\beam_forces.parquet",
    "57 ALS Removal S-TR04-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\57 ALS Removal S-TR04-02_GlobalParquet\beam_forces.parquet",
    "58 ALS Removal S-TR05-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\58 ALS Removal S-TR05-03_GlobalParquet\beam_forces.parquet",
    "59 ALS Removal S-TR06-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\59 ALS Removal S-TR06-01_GlobalParquet\beam_forces.parquet",
    "6 ALS Removal P-TR02a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\6 ALS Removal P-TR02a-01_GlobalParquet\beam_forces.parquet",
    "60 ALS Removal S-TR06-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\60 ALS Removal S-TR06-02_GlobalParquet\beam_forces.parquet",
    "61 ALS Removal S-TR06-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\61 ALS Removal S-TR06-03_GlobalParquet\beam_forces.parquet",
    "62 ALS Removal S-TR07-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\62 ALS Removal S-TR07-01_GlobalParquet\beam_forces.parquet",
    "63 ALS Removal S-TR07-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\63 ALS Removal S-TR07-02_GlobalParquet\beam_forces.parquet",
    "64 ALS Removal S-TR07-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\64 ALS Removal S-TR07-03_GlobalParquet\beam_forces.parquet",
    "65 ALS Removal S-TR08-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\65 ALS Removal S-TR08-01_GlobalParquet\beam_forces.parquet",
    "66 ALS Removal S-TR11-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\66 ALS Removal S-TR11-02_GlobalParquet\beam_forces.parquet",
    "67 ALS Removal S-TR12-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\67 ALS Removal S-TR12-01_GlobalParquet\beam_forces.parquet",
    "68 ALS Removal TR01a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\68 ALS Removal TR01a-04_GlobalParquet\beam_forces.parquet",
    "69 ALS Removal TR01b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\69 ALS Removal TR01b-04_GlobalParquet\beam_forces.parquet",
    "7 ALS Removal P-TR02a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\7 ALS Removal P-TR02a-02_GlobalParquet\beam_forces.parquet",
    "70 ALS Removal TR02a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\70 ALS Removal TR02a-04_GlobalParquet\beam_forces.parquet",
    "71 ALS Removal TR02b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\71 ALS Removal TR02b-04_GlobalParquet\beam_forces.parquet",
    "72 ALS Removal CHB1-T1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\72 ALS Removal CHB1-T1_GlobalParquet\beam_forces.parquet",
    "73 ALS Removal CHB1-T2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\73 ALS Removal CHB1-T2_GlobalParquet\beam_forces.parquet",
    "74 ALS Removal CHB1-T3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\74 ALS Removal CHB1-T3_GlobalParquet\beam_forces.parquet",
    "75 ALS Removal CHB1-T4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\75 ALS Removal CHB1-T4_GlobalParquet\beam_forces.parquet",
    "76 ALS Removal CHB1-B1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\76 ALS Removal CHB1-B1_GlobalParquet\beam_forces.parquet",
    "77 ALS Removal CHB1-B2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\77 ALS Removal CHB1-B2_GlobalParquet\beam_forces.parquet",
    "78 ALS Removal CHB1-B3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\78 ALS Removal CHB1-B3_GlobalParquet\beam_forces.parquet",
    "79 ALS Removal CHB1-B4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\79 ALS Removal CHB1-B4_GlobalParquet\beam_forces.parquet",
    "8 ALS Removal P-TR02a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\8 ALS Removal P-TR02a-03_GlobalParquet\beam_forces.parquet",
    "80 ALS Removal CHB1-D1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\80 ALS Removal CHB1-D1_GlobalParquet\beam_forces.parquet",
    "81 ALS Removal CHB1-D2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\81 ALS Removal CHB1-D2_GlobalParquet\beam_forces.parquet",
    "82 ALS Removal CHB1-D3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\82 ALS Removal CHB1-D3_GlobalParquet\beam_forces.parquet",
    "83 ALS Removal CHB1-D4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\83 ALS Removal CHB1-D4_GlobalParquet\beam_forces.parquet",
    "84 ALS Removal CHB2-T1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\84 ALS Removal CHB2-T1_GlobalParquet\beam_forces.parquet",
    "85 ALS Removal CHB2-T2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\85 ALS Removal CHB2-T2_GlobalParquet\beam_forces.parquet",
    "86 ALS Removal CHB2-T3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\86 ALS Removal CHB2-T3_GlobalParquet\beam_forces.parquet",
    "87 ALS Removal CHB2-T4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\87 ALS Removal CHB2-T4_GlobalParquet\beam_forces.parquet",
    "88 ALS Removal CHB2-B1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\88 ALS Removal CHB2-B1_GlobalParquet\beam_forces.parquet",
    "89 ALS Removal CHB2-B2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\89 ALS Removal CHB2-B2_GlobalParquet\beam_forces.parquet",
    "9 ALS Removal P-TR02b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\9 ALS Removal P-TR02b-01_GlobalParquet\beam_forces.parquet",
    "90 ALS Removal CHB2-B3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\90 ALS Removal CHB2-B3_GlobalParquet\beam_forces.parquet",
    "91 ALS Removal CHB2-B4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\91 ALS Removal CHB2-B4_GlobalParquet\beam_forces.parquet",
    "92 ALS Removal CHB2-D1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\92 ALS Removal CHB2-D1_GlobalParquet\beam_forces.parquet",
    "93 ALS Removal CHB2-D2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\93 ALS Removal CHB2-D2_GlobalParquet\beam_forces.parquet",
    "94 ALS Removal CHB2-D3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\94 ALS Removal CHB2-D3_GlobalParquet\beam_forces.parquet",
    "95 ALS Removal CHB2-D4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\95 ALS Removal CHB2-D4_GlobalParquet\beam_forces.parquet",
    "96 ALS Removal CHC2-T1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\96 ALS Removal CHC2-T1_GlobalParquet\beam_forces.parquet",
    "97 ALS Removal CHC2-T2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\97 ALS Removal CHC2-T2_GlobalParquet\beam_forces.parquet",
    "98 ALS Removal CHC2-T3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\98 ALS Removal CHC2-T3_GlobalParquet\beam_forces.parquet",
    "99 ALS Removal CHC2-T4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\99 ALS Removal CHC2-T4_GlobalParquet\beam_forces.parquet",
}

bp_parq_files = {
    "LB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmax_Parquet\beam_properties.parquet",
    "LB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_LB_Gmin_Parquet\beam_properties.parquet",
    "UB_Gmax": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmax_Parquet\beam_properties.parquet",
    "UB_Gmin": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Global Axes Results\V1_4_4_UB_Gmin_Parquet\beam_properties.parquet",
    "0 ALS Removal P-TR01a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\0 ALS Removal P-TR01a-01_GlobalParquet\beam_properties.parquet",
    "1 ALS Removal P-TR01a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\1 ALS Removal P-TR01a-02_GlobalParquet\beam_properties.parquet",
    "10 ALS Removal P-TR02b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\10 ALS Removal P-TR02b-02_GlobalParquet\beam_properties.parquet",
    "100 ALS Removal CHC2-B1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\100 ALS Removal CHC2-B1_GlobalParquet\beam_properties.parquet",
    "101 ALS Removal CHC2-B2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\101 ALS Removal CHC2-B2_GlobalParquet\beam_properties.parquet",
    "102 ALS Removal CHC2-B3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\102 ALS Removal CHC2-B3_GlobalParquet\beam_properties.parquet",
    "103 ALS Removal CHC2-B4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\103 ALS Removal CHC2-B4_GlobalParquet\beam_properties.parquet",
    "104 ALS Removal CHC2-D1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\104 ALS Removal CHC2-D1_GlobalParquet\beam_properties.parquet",
    "105 ALS Removal CHC2-D2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\105 ALS Removal CHC2-D2_GlobalParquet\beam_properties.parquet",
    "106 ALS Removal CHC2-D3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\106 ALS Removal CHC2-D3_GlobalParquet\beam_properties.parquet",
    "107 ALS Removal CHC2-D4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\107 ALS Removal CHC2-D4_GlobalParquet\beam_properties.parquet",
    "11 ALS Removal P-TR02b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\11 ALS Removal P-TR02b-03_GlobalParquet\beam_properties.parquet",
    "12 ALS Removal P-TR03a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\12 ALS Removal P-TR03a-01_GlobalParquet\beam_properties.parquet",
    "13 ALS Removal P-TR03a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\13 ALS Removal P-TR03a-02_GlobalParquet\beam_properties.parquet",
    "14 ALS Removal P-TR03a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\14 ALS Removal P-TR03a-03_GlobalParquet\beam_properties.parquet",
    "15 ALS Removal P-TR03a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\15 ALS Removal P-TR03a-04_GlobalParquet\beam_properties.parquet",
    "16 ALS Removal P-TR03a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\16 ALS Removal P-TR03a-05_GlobalParquet\beam_properties.parquet",
    "17 ALS Removal P-TR03b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\17 ALS Removal P-TR03b-01_GlobalParquet\beam_properties.parquet",
    "18 ALS Removal P-TR03b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\18 ALS Removal P-TR03b-02_GlobalParquet\beam_properties.parquet",
    "19 ALS Removal P-TR03b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\19 ALS Removal P-TR03b-03_GlobalParquet\beam_properties.parquet",
    "2 ALS Removal P-TR01a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\2 ALS Removal P-TR01a-03_GlobalParquet\beam_properties.parquet",
    "20 ALS Removal P-TR03b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\20 ALS Removal P-TR03b-04_GlobalParquet\beam_properties.parquet",
    "21 ALS Removal P-TR03b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\21 ALS Removal P-TR03b-05_GlobalParquet\beam_properties.parquet",
    "22 ALS Removal P-TR04a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\22 ALS Removal P-TR04a-01_GlobalParquet\beam_properties.parquet",
    "23 ALS Removal P-TR04a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\23 ALS Removal P-TR04a-02_GlobalParquet\beam_properties.parquet",
    "24 ALS Removal P-TR04a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\24 ALS Removal P-TR04a-03_GlobalParquet\beam_properties.parquet",
    "25 ALS Removal P-TR04a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\25 ALS Removal P-TR04a-04_GlobalParquet\beam_properties.parquet",
    "26 ALS Removal P-TR04a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\26 ALS Removal P-TR04a-05_GlobalParquet\beam_properties.parquet",
    "27 ALS Removal P-TR04a-06": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\27 ALS Removal P-TR04a-06_GlobalParquet\beam_properties.parquet",
    "28 ALS Removal P-TR04a-07": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\28 ALS Removal P-TR04a-07_GlobalParquet\beam_properties.parquet",
    "29 ALS Removal P-TR04b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\29 ALS Removal P-TR04b-01_GlobalParquet\beam_properties.parquet",
    "3 ALS Removal P-TR01b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\3 ALS Removal P-TR01b-01_GlobalParquet\beam_properties.parquet",
    "30 ALS Removal P-TR04b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\30 ALS Removal P-TR04b-02_GlobalParquet\beam_properties.parquet",
    "31 ALS Removal P-TR04b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\31 ALS Removal P-TR04b-03_GlobalParquet\beam_properties.parquet",
    "32 ALS Removal P-TR04b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\32 ALS Removal P-TR04b-04_GlobalParquet\beam_properties.parquet",
    "33 ALS Removal P-TR04b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\33 ALS Removal P-TR04b-05_GlobalParquet\beam_properties.parquet",
    "34 ALS Removal P-TR04b-06": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\34 ALS Removal P-TR04b-06_GlobalParquet\beam_properties.parquet",
    "35 ALS Removal P-TR04b-07": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\35 ALS Removal P-TR04b-07_GlobalParquet\beam_properties.parquet",
    "36 ALS Removal S-TR02-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\36 ALS Removal S-TR02-01_GlobalParquet\beam_properties.parquet",
    "37 ALS Removal S-TR02-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\37 ALS Removal S-TR02-02_GlobalParquet\beam_properties.parquet",
    "38 ALS Removal S-TR05-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\38 ALS Removal S-TR05-01_GlobalParquet\beam_properties.parquet",
    "39 ALS Removal S-TR05-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\39 ALS Removal S-TR05-02_GlobalParquet\beam_properties.parquet",
    "4 ALS Removal P-TR01b-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\4 ALS Removal P-TR01b-02_GlobalParquet\beam_properties.parquet",
    "40 ALS Removal S-TR04-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\40 ALS Removal S-TR04-01_GlobalParquet\beam_properties.parquet",
    "41 ALS Removal S-TR11-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\41 ALS Removal S-TR11-01_GlobalParquet\beam_properties.parquet",
    "42 ALS Removal S-TR13-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\42 ALS Removal S-TR13-01_GlobalParquet\beam_properties.parquet",
    "43 ALS Removal S-TR13-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\43 ALS Removal S-TR13-02_GlobalParquet\beam_properties.parquet",
    "44 ALS Removal S-TR13-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\44 ALS Removal S-TR13-03_GlobalParquet\beam_properties.parquet",
    "45 ALS Removal S-TR13-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\45 ALS Removal S-TR13-04_GlobalParquet\beam_properties.parquet",
    "46 ALS Removal S-TR14-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\46 ALS Removal S-TR14-01_GlobalParquet\beam_properties.parquet",
    "47 ALS Removal S-TR14-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\47 ALS Removal S-TR14-02_GlobalParquet\beam_properties.parquet",
    "48 ALS Removal S-TR14-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\48 ALS Removal S-TR14-03_GlobalParquet\beam_properties.parquet",
    "49 ALS Removal S-TR14-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\49 ALS Removal S-TR14-04_GlobalParquet\beam_properties.parquet",
    "5 ALS Removal P-TR01b-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\5 ALS Removal P-TR01b-03_GlobalParquet\beam_properties.parquet",
    "50 ALS Removal S-TR01-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\50 ALS Removal S-TR01-01_GlobalParquet\beam_properties.parquet",
    "51 ALS Removal S-TR01-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\51 ALS Removal S-TR01-02_GlobalParquet\beam_properties.parquet",
    "52 ALS Removal S-TR01a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\52 ALS Removal S-TR01a-05_GlobalParquet\beam_properties.parquet",
    "53 ALS Removal S-TR01b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\53 ALS Removal S-TR01b-05_GlobalParquet\beam_properties.parquet",
    "54 ALS Removal S-TR02-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\54 ALS Removal S-TR02-03_GlobalParquet\beam_properties.parquet",
    "55 ALS Removal S-TR02a-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\55 ALS Removal S-TR02a-05_GlobalParquet\beam_properties.parquet",
    "56 ALS Removal S-TR02b-05": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\56 ALS Removal S-TR02b-05_GlobalParquet\beam_properties.parquet",
    "57 ALS Removal S-TR04-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\57 ALS Removal S-TR04-02_GlobalParquet\beam_properties.parquet",
    "58 ALS Removal S-TR05-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\58 ALS Removal S-TR05-03_GlobalParquet\beam_properties.parquet",
    "59 ALS Removal S-TR06-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\59 ALS Removal S-TR06-01_GlobalParquet\beam_properties.parquet",
    "6 ALS Removal P-TR02a-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\6 ALS Removal P-TR02a-01_GlobalParquet\beam_properties.parquet",
    "60 ALS Removal S-TR06-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\60 ALS Removal S-TR06-02_GlobalParquet\beam_properties.parquet",
    "61 ALS Removal S-TR06-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\61 ALS Removal S-TR06-03_GlobalParquet\beam_properties.parquet",
    "62 ALS Removal S-TR07-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\62 ALS Removal S-TR07-01_GlobalParquet\beam_properties.parquet",
    "63 ALS Removal S-TR07-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\63 ALS Removal S-TR07-02_GlobalParquet\beam_properties.parquet",
    "64 ALS Removal S-TR07-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\64 ALS Removal S-TR07-03_GlobalParquet\beam_properties.parquet",
    "65 ALS Removal S-TR08-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\65 ALS Removal S-TR08-01_GlobalParquet\beam_properties.parquet",
    "66 ALS Removal S-TR11-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\66 ALS Removal S-TR11-02_GlobalParquet\beam_properties.parquet",
    "67 ALS Removal S-TR12-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\67 ALS Removal S-TR12-01_GlobalParquet\beam_properties.parquet",
    "68 ALS Removal TR01a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\68 ALS Removal TR01a-04_GlobalParquet\beam_properties.parquet",
    "69 ALS Removal TR01b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\69 ALS Removal TR01b-04_GlobalParquet\beam_properties.parquet",
    "7 ALS Removal P-TR02a-02": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\7 ALS Removal P-TR02a-02_GlobalParquet\beam_properties.parquet",
    "70 ALS Removal TR02a-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\70 ALS Removal TR02a-04_GlobalParquet\beam_properties.parquet",
    "71 ALS Removal TR02b-04": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\71 ALS Removal TR02b-04_GlobalParquet\beam_properties.parquet",
    "72 ALS Removal CHB1-T1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\72 ALS Removal CHB1-T1_GlobalParquet\beam_properties.parquet",
    "73 ALS Removal CHB1-T2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\73 ALS Removal CHB1-T2_GlobalParquet\beam_properties.parquet",
    "74 ALS Removal CHB1-T3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\74 ALS Removal CHB1-T3_GlobalParquet\beam_properties.parquet",
    "75 ALS Removal CHB1-T4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\75 ALS Removal CHB1-T4_GlobalParquet\beam_properties.parquet",
    "76 ALS Removal CHB1-B1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\76 ALS Removal CHB1-B1_GlobalParquet\beam_properties.parquet",
    "77 ALS Removal CHB1-B2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\77 ALS Removal CHB1-B2_GlobalParquet\beam_properties.parquet",
    "78 ALS Removal CHB1-B3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\78 ALS Removal CHB1-B3_GlobalParquet\beam_properties.parquet",
    "79 ALS Removal CHB1-B4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\79 ALS Removal CHB1-B4_GlobalParquet\beam_properties.parquet",
    "8 ALS Removal P-TR02a-03": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\8 ALS Removal P-TR02a-03_GlobalParquet\beam_properties.parquet",
    "80 ALS Removal CHB1-D1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\80 ALS Removal CHB1-D1_GlobalParquet\beam_properties.parquet",
    "81 ALS Removal CHB1-D2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\81 ALS Removal CHB1-D2_GlobalParquet\beam_properties.parquet",
    "82 ALS Removal CHB1-D3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\82 ALS Removal CHB1-D3_GlobalParquet\beam_properties.parquet",
    "83 ALS Removal CHB1-D4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\83 ALS Removal CHB1-D4_GlobalParquet\beam_properties.parquet",
    "84 ALS Removal CHB2-T1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\84 ALS Removal CHB2-T1_GlobalParquet\beam_properties.parquet",
    "85 ALS Removal CHB2-T2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\85 ALS Removal CHB2-T2_GlobalParquet\beam_properties.parquet",
    "86 ALS Removal CHB2-T3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\86 ALS Removal CHB2-T3_GlobalParquet\beam_properties.parquet",
    "87 ALS Removal CHB2-T4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\87 ALS Removal CHB2-T4_GlobalParquet\beam_properties.parquet",
    "88 ALS Removal CHB2-B1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\88 ALS Removal CHB2-B1_GlobalParquet\beam_properties.parquet",
    "89 ALS Removal CHB2-B2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\89 ALS Removal CHB2-B2_GlobalParquet\beam_properties.parquet",
    "9 ALS Removal P-TR02b-01": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\9 ALS Removal P-TR02b-01_GlobalParquet\beam_properties.parquet",
    "90 ALS Removal CHB2-B3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\90 ALS Removal CHB2-B3_GlobalParquet\beam_properties.parquet",
    "91 ALS Removal CHB2-B4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\91 ALS Removal CHB2-B4_GlobalParquet\beam_properties.parquet",
    "92 ALS Removal CHB2-D1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\92 ALS Removal CHB2-D1_GlobalParquet\beam_properties.parquet",
    "93 ALS Removal CHB2-D2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\93 ALS Removal CHB2-D2_GlobalParquet\beam_properties.parquet",
    "94 ALS Removal CHB2-D3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\94 ALS Removal CHB2-D3_GlobalParquet\beam_properties.parquet",
    "95 ALS Removal CHB2-D4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\95 ALS Removal CHB2-D4_GlobalParquet\beam_properties.parquet",
    "96 ALS Removal CHC2-T1": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\96 ALS Removal CHC2-T1_GlobalParquet\beam_properties.parquet",
    "97 ALS Removal CHC2-T2": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\97 ALS Removal CHC2-T2_GlobalParquet\beam_properties.parquet",
    "98 ALS Removal CHC2-T3": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\98 ALS Removal CHC2-T3_GlobalParquet\beam_properties.parquet",
    "99 ALS Removal CHC2-T4": r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\ALS\Output\99 ALS Removal CHC2-T4_GlobalParquet\beam_properties.parquet",
}

B1_node_force_cos_ang_dict = {1782: cos(radians(225)), 1715: cos(radians(225)),
                              1852: cos(radians(315)), 1788: cos(radians(315)),
                              1707: cos(radians(135)), 1644: cos(radians(135)),
                              17761: cos(radians(45)), 1709: cos(radians(45))}

B1_als_node_force_cos_ang_dict = {1782: cos(radians(225)), 1715: cos(radians(225)),
                              1852: cos(radians(315)), 1788: cos(radians(315)),
                              1707: cos(radians(135)), 1644: cos(radians(135)),
                              17761: cos(radians(45)), 1709: cos(radians(45))}

B1_node_force_sin_ang_dict = {1782: sin(radians(225)), 1715: sin(radians(225)),
                              1852: sin(radians(315)), 1788: sin(radians(315)),
                              1707: sin(radians(135)), 1644: sin(radians(135)),
                              17761: sin(radians(45)), 1709: sin(radians(45))}

B1_als_node_force_sin_ang_dict = {1782: sin(radians(225)), 1715: sin(radians(225)),
                                  1852: sin(radians(315)), 1788: sin(radians(315)),
                                  1707: sin(radians(135)), 1644: sin(radians(135)),
                                  17761: sin(radians(45)), 1709: sin(radians(45))}

B2_node_force_cos_ang_dict = {931: cos(radians(315)), 21153: cos(radians(315)),
                              867: cos(radians(225)), 794: cos(radians(225)),
                              809: cos(radians(135)), 726: cos(radians(135)),
                              875: cos(radians(45)), 791: cos(radians(45))}

B2_als_node_force_cos_ang_dict = {931: cos(radians(315)), 21165: cos(radians(315)),
                                  867: cos(radians(225)), 794: cos(radians(225)),
                                  809: cos(radians(135)), 726: cos(radians(135)),
                                  875: cos(radians(45)), 791: cos(radians(45))}

B2_node_force_sin_ang_dict = {931: sin(radians(315)), 21153: sin(radians(315)),
                              867: sin(radians(225)), 794: sin(radians(225)),
                              809: sin(radians(135)), 726: sin(radians(135)),
                              875: sin(radians(45)), 791: sin(radians(45))}

B2_als_node_force_sin_ang_dict = {931: sin(radians(315)), 21165: sin(radians(315)),
                              867: sin(radians(225)), 794: sin(radians(225)),
                              809: sin(radians(135)), 726: sin(radians(135)),
                              875: sin(radians(45)), 791: sin(radians(45))}

C1_node_force_cos_ang_dict = {2823: cos(radians(315)), 2789: cos(radians(315)),
                              2791: cos(radians(225)), 2749: cos(radians(225)),
                              2760: cos(radians(135)), 2705: cos(radians(135)),
                              2796: cos(radians(45)), 21152: cos(radians(45))}

C1_als_node_force_cos_ang_dict = {2824: cos(radians(315)), 2790: cos(radians(315)),
                                  2792: cos(radians(225)), 2750: cos(radians(225)),
                                  2761: cos(radians(135)), 2706: cos(radians(135)),
                                  2797: cos(radians(45)), 21163: cos(radians(45))}

C1_node_force_sin_ang_dict = {2823: sin(radians(315)), 2789: sin(radians(315)),
                              2791: sin(radians(225)), 2749: sin(radians(225)),
                              2760: sin(radians(135)), 2705: sin(radians(135)),
                              2796: sin(radians(45)), 21152: sin(radians(45))}

C1_als_node_force_sin_ang_dict = {2824: sin(radians(315)), 2790: sin(radians(315)),
                                  2792: sin(radians(225)), 2750: sin(radians(225)),
                                  2761: sin(radians(135)), 2706: sin(radians(135)),
                                  2797: sin(radians(45)), 21163: sin(radians(45))}

C2_node_force_cos_ang_dict = {2198: cos(radians(315)), 2131: cos(radians(315)),
                              17744: cos(radians(225)), 2066: cos(radians(225)),
                              2083: cos(radians(135)), 1993: cos(radians(135)),
                              2152: cos(radians(45)), 2079: cos(radians(45))}

C2_als_node_force_cos_ang_dict = {2199: cos(radians(315)), 2131: cos(radians(315)),
                                  17744: cos(radians(225)), 2066: cos(radians(225)),
                                  2083: cos(radians(135)), 1993: cos(radians(135)),
                                  2153: cos(radians(45)), 2079: cos(radians(45))}

C2_node_force_sin_ang_dict = {2198: sin(radians(315)), 2131: sin(radians(315)),
                              17744: sin(radians(225)), 2066: sin(radians(225)),
                              2083: sin(radians(135)), 1993: sin(radians(135)),
                              2152: sin(radians(45)), 2079: sin(radians(45))}

C2_als_node_force_sin_ang_dict = {2199: sin(radians(315)), 2131: sin(radians(315)),
                                  17744: sin(radians(225)), 2066: sin(radians(225)),
                                  2083: sin(radians(135)), 1993: sin(radians(135)),
                                  2153: sin(radians(45)), 2079: sin(radians(45))}

node_cos_ang_dicts = {"B1": B1_node_force_cos_ang_dict,
                      "B1_ALS": B1_als_node_force_cos_ang_dict,
                      "B2": B2_node_force_cos_ang_dict,
                      "B2_ALS": B2_als_node_force_cos_ang_dict,
                      "C1": C1_node_force_cos_ang_dict,
                      "C1_ALS": C1_als_node_force_cos_ang_dict,
                      "C2": C2_node_force_cos_ang_dict,
                      "C2_ALS": C2_als_node_force_cos_ang_dict}

node_sin_ang_dicts = {"B1": B1_node_force_sin_ang_dict,
                      "B1_ALS": B1_als_node_force_sin_ang_dict,
                      "B2": B2_node_force_sin_ang_dict,
                      "B2_ALS": B2_als_node_force_sin_ang_dict,
                      "C1": C1_node_force_sin_ang_dict,
                      "C1_ALS": C1_als_node_force_sin_ang_dict,
                      "C2": C2_node_force_sin_ang_dict,
                      "C2_ALS": C2_als_node_force_sin_ang_dict}

node_dict = {"B1": (1715, 1782, 1788, 1852, 1709, 17761, 1644, 1707),
             "B1_ALS": (1852, 1788, 1782, 1715, 1707, 1644, 17761, 1709),
             "B2": (794, 726, 791, 21153, 867, 809, 875, 931),
             "B2_ALS": (931, 21165, 867, 794, 809, 726, 875, 791),
             "C1": (2749, 2791, 2789, 2823, 21152, 2796, 2705, 2760),
             "C1_ALS": (2824, 2790, 2792, 2750, 2761, 2706, 2797, 21163),
             "C2": (2066, 17744, 2131, 2198, 2079, 2152, 1993, 2083),
             "C2_ALS": (2199, 2131, 17744, 2066, 2083, 1993, 2153, 2079)}

model_element_dict = {
    'LB_Gmax': (
        659, 3603, 665, 921, 3609, 671, 929, 930, 2551, 1828, 3748, 2552, 1065, 1066, 1834, 1835, 1836, 3752, 5940,
        5189, 711,
        3784, 3788, 3791, 5594, 5606, 1007, 1011, 1013, 1014, 2549, 2550),
    'LB_Gmin': (
        659, 3603, 665, 921, 3609, 671, 929, 930, 2551, 1828, 3748, 2552, 1065, 1066, 1834, 1835, 1836, 3752, 5940,
        5189, 711,
        3784, 3788, 3791, 5594, 5606, 1007, 1011, 1013, 1014, 2549, 2550), 'UB_Gmax': (
        659, 3603, 665, 921, 3609, 671, 929, 930, 2551, 1828, 3748, 2552, 1065, 1066, 1834, 1835, 1836, 3752, 5940,
        5189, 711,
        3784, 3788, 3791, 5594, 5606, 1007, 1011, 1013, 1014, 2549, 2550), 'UB_Gmin': (
        659, 3603, 665, 921, 3609, 671, 929, 930, 2551, 1828, 3748, 2552, 1065, 1066, 1834, 1835, 1836, 3752, 5940,
        5189, 711,
        3784, 3788, 3791, 5594, 5606, 1007, 1011, 1013, 1014, 2549, 2550), '0 ALS Removal P-TR01a-01': (
        3596, 3602, 659, 919, 665, 3740, 927, 928, 1824, 671, 3744, 1830, 1063, 1064, 1831, 1832, 5930, 5180, 3775,
        3779, 3782,
        711, 5584, 3803, 5596, 1005, 2543, 2544, 1009, 2545, 1011, 1012, 2546), '1 ALS Removal P-TR01a-02': (
        3597, 659, 3603, 665, 921, 3741, 671, 1824, 929, 930, 3745, 1830, 1831, 1832, 1065, 1066, 5926, 5178, 3776,
        3780, 711,
        3783, 5580, 5592, 3804, 1007, 2544, 2545, 2546, 1011, 2547, 1013, 1014), '10 ALS Removal P-TR02b-02': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '100 ALS Removal CHC2-B1': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '101 ALS Removal CHC2-B2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '102 ALS Removal CHC2-B3': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '103 ALS Removal CHC2-B4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '104 ALS Removal CHC2-D1': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '105 ALS Removal CHC2-D2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '106 ALS Removal CHC2-D3': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '107 ALS Removal CHC2-D4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '11 ALS Removal P-TR02b-03': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '12 ALS Removal P-TR03a-01': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 3744, 1827, 3748, 1064, 1065, 1833, 1834, 1835, 5936, 5186, 3780, 711,
        3784,
        3787, 5590, 3808, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549, 2550), '13 ALS Removal P-TR03a-02': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 3744, 1827, 3748, 1064, 1065, 1833, 1834, 1835, 5936, 5186, 3780, 711,
        3784,
        3787, 5590, 3808, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549, 2550), '14 ALS Removal P-TR03a-03': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '15 ALS Removal P-TR03a-04': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '16 ALS Removal P-TR03a-05': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '17 ALS Removal P-TR03b-01': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '18 ALS Removal P-TR03b-02': (
        3601, 659, 3607, 920, 665, 5917, 671, 928, 929, 3745, 1827, 3749, 1064, 1065, 1833, 1834, 1835, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1006, 1010, 2547, 1012, 1013, 2548, 2549, 2550), '19 ALS Removal P-TR03b-03': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '2 ALS Removal P-TR01a-03': (
        3598, 659, 3604, 665, 921, 671, 3743, 929, 1826, 3747, 1063, 1064, 1832, 1833, 5934, 5184, 3778, 3782, 711,
        3785, 5588,
        3806, 5600, 1006, 2545, 1010, 2546, 1012, 2547, 2548), '20 ALS Removal P-TR03b-04': (
        3598, 659, 3604, 917, 665, 925, 926, 671, 1824, 3742, 3746, 1061, 1062, 1830, 1831, 1832, 5934, 5184, 3778,
        3782, 711,
        3785, 5588, 3806, 5600, 1003, 1007, 2544, 1009, 1010, 2545, 2546, 2547), '21 ALS Removal P-TR03b-05': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '22 ALS Removal P-TR04a-01': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '23 ALS Removal P-TR04a-02': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '24 ALS Removal P-TR04a-03': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '25 ALS Removal P-TR04a-04': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '26 ALS Removal P-TR04a-05': (
        3600, 658, 3606, 920, 664, 670, 928, 929, 1826, 3745, 3749, 1064, 1832, 1833, 1834, 5936, 3781, 710, 3785, 3788,
        5590,
        3809, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549), '27 ALS Removal P-TR04a-06': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '28 ALS Removal P-TR04a-07': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '29 ALS Removal P-TR04b-01': (
        3600, 658, 3606, 920, 664, 670, 928, 929, 1826, 3745, 3749, 1064, 1832, 1833, 1834, 5936, 3781, 710, 3785, 3788,
        5590,
        3809, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549), '3 ALS Removal P-TR01b-01': (
        3598, 659, 3604, 665, 921, 671, 3743, 929, 1826, 3747, 1063, 1064, 1832, 1833, 5934, 5184, 3778, 3782, 711,
        3785, 5588,
        3806, 5600, 1006, 2545, 1010, 2546, 1012, 2547, 2548), '30 ALS Removal P-TR04b-02': (
        3600, 658, 3606, 920, 664, 670, 928, 929, 1826, 3745, 3749, 1064, 1832, 1833, 1834, 5936, 3781, 710, 3785, 3788,
        5590,
        3809, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549), '31 ALS Removal P-TR04b-03': (
        3600, 659, 3606, 665, 921, 671, 929, 930, 2551, 1828, 3745, 1065, 1066, 1834, 1835, 1836, 5935, 5185, 3780, 711,
        3786,
        5589, 3807, 5601, 1007, 1011, 1013, 1014, 2549, 2550), '32 ALS Removal P-TR04b-04': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3745, 3749, 1065, 1066, 1833, 1834, 1835, 5937, 5187,
        3781, 711,
        3785, 3788, 5591, 3809, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '33 ALS Removal P-TR04b-05': (
        3600, 658, 3606, 920, 664, 670, 928, 929, 1826, 3745, 3749, 1064, 1832, 1833, 1834, 5936, 3781, 710, 3785, 3788,
        5590,
        3809, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549), '34 ALS Removal P-TR04b-06': (
        3600, 658, 3606, 920, 664, 670, 928, 929, 1826, 3745, 3749, 1064, 1832, 1833, 1834, 5936, 3781, 710, 3785, 3788,
        5590,
        3809, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549), '35 ALS Removal P-TR04b-07': (
        3600, 658, 3606, 920, 664, 670, 928, 929, 1826, 3745, 3749, 1064, 1832, 1833, 1834, 5936, 3781, 710, 3785, 3788,
        5590,
        3809, 5602, 1006, 1010, 2547, 1012, 1013, 2548, 2549), '36 ALS Removal S-TR02-01': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '37 ALS Removal S-TR02-02': (
        3601, 659, 3607, 665, 921, 671, 929, 930, 2551, 1828, 3746, 3750, 2552, 1065, 1066, 1834, 1835, 1836, 5936,
        5187, 3782,
        711, 3786, 3789, 5591, 3810, 5603, 1007, 1011, 1013, 1014, 2549, 2550), '38 ALS Removal S-TR05-01': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '39 ALS Removal S-TR05-02': (
        5898, 3601, 659, 3607, 665, 921, 671, 929, 930, 1827, 2551, 3746, 3750, 1065, 1066, 1833, 1834, 1835, 5186,
        3782, 711,
        3786, 3789, 5590, 3809, 5602, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '4 ALS Removal P-TR01b-02': (
        3596, 658, 3602, 920, 664, 3740, 670, 1823, 928, 929, 3744, 1829, 1830, 1831, 1064, 1065, 5928, 5178, 3776,
        3780, 710,
        3783, 5582, 5594, 3804, 1006, 2543, 2544, 2545, 1010, 2546, 1012, 1013), '40 ALS Removal S-TR04-01': (
        3598, 659, 3604, 920, 665, 671, 928, 929, 1824, 3743, 3747, 1830, 1063, 1064, 1831, 1832, 5934, 5184, 3778,
        3782, 711,
        3785, 5588, 3806, 5600, 1005, 2544, 1009, 2545, 1011, 1012, 2546, 2547), '41 ALS Removal S-TR11-01': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '42 ALS Removal S-TR13-01': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '43 ALS Removal S-TR13-02': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '44 ALS Removal S-TR13-03': (
        3601, 659, 3607, 665, 921, 671, 929, 930, 2551, 1828, 3746, 3750, 2552, 1065, 1066, 1834, 1835, 1836, 5936,
        5187, 3782,
        711, 3786, 3789, 5591, 3810, 5603, 1007, 1011, 1013, 1014, 2549, 2550), '45 ALS Removal S-TR13-04': (
        3601, 659, 3607, 665, 921, 671, 929, 930, 2551, 1828, 3746, 3750, 2552, 1065, 1066, 1834, 1835, 1836, 5936,
        5187, 3782,
        711, 3786, 3789, 5591, 3810, 5603, 1007, 1011, 1013, 1014, 2549, 2550), '46 ALS Removal S-TR14-01': (
        3594, 656, 3600, 918, 662, 3738, 668, 1822, 926, 927, 3742, 1828, 1061, 1062, 1829, 1830, 5929, 5179, 3774,
        3778, 708,
        3781, 5583, 3802, 5595, 1004, 2543, 1008, 2544, 1010, 1011, 2545, 2546), '47 ALS Removal S-TR14-02': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '48 ALS Removal S-TR14-03': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '49 ALS Removal S-TR14-04': (
        3598, 659, 3604, 920, 665, 671, 928, 929, 1824, 3743, 3747, 1830, 1063, 1064, 1831, 1832, 5934, 5184, 3778,
        3782, 711,
        3785, 5588, 3806, 5600, 1005, 2544, 1009, 2545, 1011, 1012, 2546, 2547), '5 ALS Removal P-TR01b-03': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '50 ALS Removal S-TR01-01': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '51 ALS Removal S-TR01-02': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '52 ALS Removal S-TR01a-05': (
        3600, 659, 3606, 920, 665, 671, 928, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '53 ALS Removal S-TR01b-05': (
        3601, 659, 3607, 665, 921, 671, 929, 930, 2551, 1828, 3746, 3750, 2552, 1065, 1066, 1834, 1835, 1836, 5936,
        5187, 3782,
        711, 3786, 3789, 5591, 3810, 5603, 1007, 1011, 1013, 1014, 2549, 2550), '54 ALS Removal S-TR02-03': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 2551, 1828, 3747, 3751, 1065, 1066, 1834, 1835, 1836, 5937, 5187, 711,
        3783,
        3787, 3790, 5591, 3811, 5603, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '55 ALS Removal S-TR02a-05': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '56 ALS Removal S-TR02b-05': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '57 ALS Removal S-TR04-02': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '58 ALS Removal S-TR05-03': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '59 ALS Removal S-TR06-01': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '6 ALS Removal P-TR02a-01': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '60 ALS Removal S-TR06-02': (
        3601, 659, 3607, 665, 921, 671, 929, 930, 1827, 3746, 3750, 1064, 1065, 1833, 1834, 1835, 5931, 5188, 3782, 711,
        3786,
        3789, 5585, 5597, 3810, 1007, 1011, 2547, 1013, 1014, 2548, 2549, 2550), '61 ALS Removal S-TR06-03': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '62 ALS Removal S-TR07-01': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '63 ALS Removal S-TR07-02': (
        3601, 659, 3607, 665, 921, 671, 929, 930, 1827, 3746, 3750, 1064, 1065, 1833, 1834, 1835, 5935, 5188, 3782, 711,
        3786,
        3789, 5589, 5601, 3810, 1007, 1011, 2547, 1013, 1014, 2548, 2549, 2550), '64 ALS Removal S-TR07-03': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '65 ALS Removal S-TR08-01': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '66 ALS Removal S-TR11-02': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '67 ALS Removal S-TR12-01': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '68 ALS Removal TR01a-04': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '69 ALS Removal TR01b-04': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '7 ALS Removal P-TR02a-02': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '70 ALS Removal TR02a-04': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '71 ALS Removal TR02b-04': (
        3600, 659, 3606, 919, 665, 927, 928, 671, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 1834, 5937, 5187, 3781, 711,
        3785,
        3788, 5591, 3809, 5603, 1005, 1009, 2546, 1011, 1012, 2547, 2548, 2549), '72 ALS Removal CHB1-T1': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '73 ALS Removal CHB1-T2': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '74 ALS Removal CHB1-T3': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '75 ALS Removal CHB1-T4': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '76 ALS Removal CHB1-B1': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '77 ALS Removal CHB1-B2': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '78 ALS Removal CHB1-B3': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '79 ALS Removal CHB1-B4': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '8 ALS Removal P-TR02a-03': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '80 ALS Removal CHB1-D1': (
        3602, 659, 920, 665, 3608, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '81 ALS Removal CHB1-D2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '82 ALS Removal CHB1-D3': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '83 ALS Removal CHB1-D4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '84 ALS Removal CHB2-T1': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '85 ALS Removal CHB2-T2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '86 ALS Removal CHB2-T3': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '87 ALS Removal CHB2-T4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '88 ALS Removal CHB2-B1': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '89 ALS Removal CHB2-B2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '9 ALS Removal P-TR02b-01': (
        3600, 659, 3606, 665, 921, 671, 929, 1826, 3745, 3749, 1063, 1064, 1832, 1833, 5937, 5187, 3781, 711, 3785,
        3788, 5591,
        3809, 5603, 1006, 2546, 1011, 1012, 2547, 2548, 2549), '90 ALS Removal CHB2-B3': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '91 ALS Removal CHB2-B4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '92 ALS Removal CHB2-D1': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '93 ALS Removal CHB2-D2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '94 ALS Removal CHB2-D3': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '95 ALS Removal CHB2-D4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '96 ALS Removal CHC2-T1': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '97 ALS Removal CHC2-T2': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550), '98 ALS Removal CHC2-T3': (
        3602, 659, 3608, 665, 921, 671, 928, 929, 1827, 2551, 3747, 3751, 1064, 1065, 1833, 1834, 1835, 5938, 5188, 711,
        3783,
        3787, 3790, 5592, 3811, 5604, 1006, 1010, 1012, 1013, 2548, 2549, 2550), '99 ALS Removal CHC2-T4': (
        3602, 659, 3608, 665, 921, 671, 929, 930, 1827, 2551, 3747, 3751, 1065, 1066, 1833, 1834, 1835, 5939, 5189, 711,
        3783,
        3787, 3790, 5593, 3811, 5605, 1007, 1011, 2548, 1013, 1014, 2549, 2550)}

excluded_beam_dict = {
    "LB_Gmax": {"B1": (844, 848, 834, 832, 843, 847, 836, 837),
                "B2": (1206, 1212, 1213, 1214, 1106, 1113, 1110, 1114),
                "C1": (756, 729, 761, 731, 759, 728, 760, 730),
                "C2": (1006, 920, 1010, 924, 1009, 923, 1008, 922)},
    "LB_Gmin": {"B1": (844, 848, 834, 832, 843, 847, 836, 837),
                "B2": (1206, 1212, 1213, 1214, 1106, 1113, 1110, 1114),
                "C1": (756, 729, 761, 731, 759, 728, 760, 730),
                "C2": (1006, 920, 1010, 924, 1009, 923, 1008, 922)},
    "UB_Gmax": {"B1": (844, 848, 834, 832, 843, 847, 836, 837),
                "B2": (1206, 1212, 1213, 1214, 1106, 1113, 1110, 1114),
                "C1": (756, 729, 761, 731, 759, 728, 760, 730),
                "C2": (1006, 920, 1010, 924, 1009, 923, 1008, 922)},
    "UB_Gmin": {"B1": (844, 848, 834, 832, 843, 847, 836, 837),
                "B2": (1206, 1212, 1213, 1214, 1106, 1113, 1110, 1114),
                "C1": (756, 729, 761, 731, 759, 728, 760, 730),
                "C2": (1006, 920, 1010, 924, 1009, 923, 1008, 922)},
    '0 ALS Removal P-TR01a-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1806, 1807, 1808, 1809),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1818, 1819, 1820, 1821),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1810, 1811, 1812, 1813),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1814, 1815, 1816, 1817)},
    '1 ALS Removal P-TR01a-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1806, 1807, 1808, 1809),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1818, 1819, 1820, 1821),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1810, 1811, 1812, 1813),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1814, 1815, 1816, 1817)},
    '10 ALS Removal P-TR02b-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '100 ALS Removal CHC2-B1': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '101 ALS Removal CHC2-B2': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '102 ALS Removal CHC2-B3': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '103 ALS Removal CHC2-B4': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '104 ALS Removal CHC2-D1': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '105 ALS Removal CHC2-D2': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '106 ALS Removal CHC2-D3': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '107 ALS Removal CHC2-D4': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '11 ALS Removal P-TR02b-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '12 ALS Removal P-TR03a-01': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '13 ALS Removal P-TR03a-02': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '14 ALS Removal P-TR03a-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '15 ALS Removal P-TR03a-04': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '16 ALS Removal P-TR03a-05': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '17 ALS Removal P-TR03b-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '18 ALS Removal P-TR03b-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1809, 1810, 1811, 1812),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '19 ALS Removal P-TR03b-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '2 ALS Removal P-TR01a-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '20 ALS Removal P-TR03b-04': {
        'B1': (828, 830, 832, 833, 839, 840, 843, 844, 1806, 1807, 1808, 1809),
        'B2': (1102, 1106, 1109, 1110, 1202, 1208, 1209, 1210, 1818, 1819, 1820, 1821),
        'C1': (727, 728, 729, 730, 753, 756, 757, 758, 1810, 1811, 1812, 1813),
        'C2': (916, 918, 919, 920, 1002, 1004, 1005, 1006, 1814, 1815, 1816, 1817)},
    '21 ALS Removal P-TR03b-05': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '22 ALS Removal P-TR04a-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '23 ALS Removal P-TR04a-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '24 ALS Removal P-TR04a-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '25 ALS Removal P-TR04a-04': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '26 ALS Removal P-TR04a-05': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '27 ALS Removal P-TR04a-06': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '28 ALS Removal P-TR04a-07': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '29 ALS Removal P-TR04b-01': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '3 ALS Removal P-TR01b-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '30 ALS Removal P-TR04b-02': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '31 ALS Removal P-TR04b-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '32 ALS Removal P-TR04b-04': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '33 ALS Removal P-TR04b-05': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '34 ALS Removal P-TR04b-06': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '35 ALS Removal P-TR04b-07': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '36 ALS Removal S-TR02-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '37 ALS Removal S-TR02-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '38 ALS Removal S-TR05-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '39 ALS Removal S-TR05-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1809, 1810, 1811, 1812),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '4 ALS Removal P-TR01b-02': {
        'B1': (831, 833, 835, 836, 842, 843, 846, 847, 1805, 1806, 1807, 1808),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1817, 1818, 1819, 1820),
        'C1': (727, 728, 729, 730, 755, 758, 759, 760, 1809, 1810, 1811, 1812),
        'C2': (919, 921, 922, 923, 1005, 1007, 1008, 1009, 1813, 1814, 1815, 1816)},
    '40 ALS Removal S-TR04-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1806, 1807, 1808, 1809),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1818, 1819, 1820, 1821),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1810, 1811, 1812, 1813),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1814, 1815, 1816, 1817)},
    '41 ALS Removal S-TR11-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '42 ALS Removal S-TR13-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '43 ALS Removal S-TR13-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '44 ALS Removal S-TR13-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '45 ALS Removal S-TR13-04': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '46 ALS Removal S-TR14-01': {
        'B1': (829, 831, 833, 834, 840, 841, 844, 845, 1804, 1805, 1806, 1807),
        'B2': (1102, 1106, 1109, 1110, 1202, 1208, 1209, 1210, 1816, 1817, 1818, 1819),
        'C1': (725, 726, 727, 728, 753, 756, 757, 758, 1808, 1809, 1810, 1811),
        'C2': (917, 919, 920, 921, 1003, 1005, 1006, 1007, 1812, 1813, 1814, 1815)},
    '47 ALS Removal S-TR14-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '48 ALS Removal S-TR14-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '49 ALS Removal S-TR14-04': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1806, 1807, 1808, 1809),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1818, 1819, 1820, 1821),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1810, 1811, 1812, 1813),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1814, 1815, 1816, 1817)},
    '5 ALS Removal P-TR01b-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '50 ALS Removal S-TR01-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '51 ALS Removal S-TR01-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '52 ALS Removal S-TR01a-05': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (919, 921, 922, 923, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '53 ALS Removal S-TR01b-05': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '54 ALS Removal S-TR02-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
        'B2': (1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824, 1825),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '55 ALS Removal S-TR02a-05': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '56 ALS Removal S-TR02b-05': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '57 ALS Removal S-TR04-02': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '58 ALS Removal S-TR05-03': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '59 ALS Removal S-TR06-01': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '6 ALS Removal P-TR02a-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '60 ALS Removal S-TR06-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1809, 1810, 1811, 1812),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '61 ALS Removal S-TR06-03': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '62 ALS Removal S-TR07-01': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '63 ALS Removal S-TR07-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1809, 1810, 1811, 1812),
        'B2': (1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823, 1824),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
        'C2': (920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '64 ALS Removal S-TR07-03': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '65 ALS Removal S-TR08-01': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '66 ALS Removal S-TR11-02': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '67 ALS Removal S-TR12-01': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '68 ALS Removal TR01a-04': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '69 ALS Removal TR01b-04': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '7 ALS Removal P-TR02a-02': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '70 ALS Removal TR02a-04': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '71 ALS Removal TR02b-04': {
        'B1': (832, 834, 836, 837, 841, 842, 845, 846, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (918, 920, 921, 922, 1004, 1006, 1007, 1008, 1816, 1817, 1818, 1819)},
    '72 ALS Removal CHB1-T1': {'B1': (832, 834, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '73 ALS Removal CHB1-T2': {'B1': (832, 834, 836, 837, 843, 844, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '74 ALS Removal CHB1-T3': {'B1': (832, 834, 836, 837, 843, 844, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '75 ALS Removal CHB1-T4': {'B1': (832, 834, 836, 837, 843, 844, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '76 ALS Removal CHB1-B1': {'B1': (832, 834, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '77 ALS Removal CHB1-B2': {'B1': (832, 834, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '78 ALS Removal CHB1-B3': {'B1': (832, 834, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '79 ALS Removal CHB1-B4': {'B1': (832, 834, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '8 ALS Removal P-TR02a-03': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '80 ALS Removal CHB1-D1': {'B1': (832, 834, 836, 842, 843, 846, 847, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   919, 921, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '81 ALS Removal CHB1-D2': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '82 ALS Removal CHB1-D3': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '83 ALS Removal CHB1-D4': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '84 ALS Removal CHB2-T1': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '85 ALS Removal CHB2-T2': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '86 ALS Removal CHB2-T3': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '87 ALS Removal CHB2-T4': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '88 ALS Removal CHB2-B1': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '89 ALS Removal CHB2-B2': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '9 ALS Removal P-TR02b-01': {
        'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1808, 1809, 1810, 1811),
        'B2': (1104, 1108, 1111, 1112, 1204, 1210, 1211, 1212, 1820, 1821, 1822, 1823),
        'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1812, 1813, 1814, 1815),
        'C2': (920, 922, 923, 924, 1005, 1007, 1008, 1009, 1816, 1817, 1818, 1819)},
    '90 ALS Removal CHB2-B3': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '91 ALS Removal CHB2-B4': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '92 ALS Removal CHB2-D1': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '93 ALS Removal CHB2-D2': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1817, 1818, 1819, 1820)},
    '94 ALS Removal CHB2-D3': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '95 ALS Removal CHB2-D4': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '96 ALS Removal CHC2-T1': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '97 ALS Removal CHC2-T2': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)},
    '98 ALS Removal CHC2-T3': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1809, 1810, 1811, 1812),
                               'B2': (
                                   1105, 1109, 1112, 1113, 1205, 1211, 1212, 1213, 1821, 1822, 1823,
                                   1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1813, 1814, 1815, 1816),
                               'C2': (920, 922, 923, 1005, 1007, 1008, 1009, 1817, 1818, 1819, 1820)},
    '99 ALS Removal CHC2-T4': {'B1': (832, 834, 836, 837, 843, 844, 847, 848, 1810, 1811, 1812, 1813),
                               'B2': (
                                   1106, 1110, 1113, 1114, 1206, 1212, 1213, 1214, 1822, 1823, 1824),
                               'C1': (728, 729, 730, 731, 756, 759, 760, 761, 1814, 1815, 1816, 1817),
                               'C2': (
                                   920, 922, 923, 924, 1006, 1008, 1009, 1010, 1818, 1819, 1820, 1821)}}

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


def get_direction_coefficients(location: str) -> str:
    direction_coefficients = ", ".join(
        f"({node}, {node_cos_ang_dicts[location][node]}, {node_sin_ang_dicts[location][node]})" for node in
        node_cos_ang_dicts[location].keys())

    return direction_coefficients


def _get_beam_end_query(location: str, bp_parq_files: dict, node_dict: dict, target_groups: str,
                        excluded_beams: dict) -> str:
    """Gets the SQL write_full_beam_forces_query for finding the relevant ends of the beam."""

    models = bp_parq_files.keys()

    nodes = {m_name: node_dict[location] if "ALS" not in m_name else node_dict[location + "_ALS"] for m_name in models}

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


    # beam_end_query = f"""
    # SELECT BeamNumber, 0.0 AS BeamEnd, -1 AS Sign
    # FROM '{bp_parq}'
    # WHERE N1 IN {nodes}
    # AND GroupName IN {target_groups}
    # AND BeamNumber NOT IN {excluded_beams}
    #
    # UNION ALL
    #
    # SELECT BeamNumber, 1.0 AS BeamEnd, 1 AS Sign
    # FROM '{bp_parq}'
    # WHERE N2 IN {nodes}
    # AND GroupName IN {target_groups}
    # AND BeamNumber NOT IN {excluded_beams}"""

    return beam_end_query


def _get_nodal_beam_force_query(location: str, bp_parq_files: dict,
                                target_groups: str, excluded_beams: dict) -> str:

    """Gets the nodal beam forces occurring at a particular location"""

    nodal_beam_force_query = "\n UNION ALL ".join(f"""
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
        WHERE
        BF.BeamNumber NOT IN {excluded_beams[model][location]}
        AND ResultCaseName NOT LIKE '%BIF%'
        AND BF.Position = BE.BeamEnd
        AND BP.GroupName IN {target_groups}""" for model in bp_parq_files.keys())

    return nodal_beam_force_query


def get_full_beam_force_query(location: str, bf_parq_files: dict, bp_parq_files: dict,
                              excluded_beams: dict, target_groups: str, result_case_filter: str) -> str:

    """Gets the full set of beam forces for beams from the series of bf_models, using filtering criteria."""

    prequery = "\n UNION ALL ".join(f"SELECT "
                                    f"BeamNumber, ResultCaseName, ResultCase, Position, '{model_name}' AS Model, "
                                    f"Fx, Fy, Fz, Mx, My, Mz FROM '{bf_parq_files[model_name]}' "
                                    f"WHERE Position IN (0.0, 1.0) AND ResultCaseName NOT LIKE '%BIF%' "
                                    f"AND BeamNumber IN {model_element_dict[model_name]} "
                                    f"AND BeamNumber NOT IN {excluded_beams[model_name][location]}" for model_name in bf_parq_files)

    full_beam_force_query = f"""SELECT BF.BeamNumber, ResultCaseName, ResultCase, Position, 
    BF.Model, Fx, Fy, Fz, Mx, My, Mz 
    FROM ({prequery}) AS BF 
    JOIN FULL_BEAM_PROPERTIES AS BP ON BF.BeamNumber = BP.BeamNumber 
    AND BP.Model = BF.Model 
    WHERE BF.BeamNumber IN (SELECT DISTINCT BeamNumber FROM BEAM_ENDS)
    AND ResultCaseName NOT IN {result_case_filter}
    AND BP.GroupName IN {target_groups}"""

    return full_beam_force_query


def get_full_beam_properties_query(bp_parq_files: dict, target_groups: str) -> str:
    """Function to get the properties corresponding to each and every beam from the different bf_models."""

    query = " UNION ALL ".join(f"""SELECT
    BeamNumber, GroupName, '{model}' AS Model, N1, N2
    FROM '{bp_parq_files[model]}'
    WHERE GroupName IN {target_groups}""" for model in bp_parq_files.keys())

    return query


def get_full_combined_nodal_force_query(location: str, bp_parq_files: dict, node_dict: dict,
                                        target_groups: str, excluded_beams: dict) -> str:

    query = f"""WITH FULL_BEAM_FORCES AS ({full_beam_force_query}),
        FULL_BEAM_PROPERTIES AS ({full_beam_property_query}),
        BEAM_ENDS AS ({_get_beam_end_query(location, bp_parq_files, node_dict, target_groups, excluded_beams)}),
        NODAL_BEAM_FORCES AS
        ({_get_nodal_beam_force_query(location, bp_parq_files, target_groups, excluded_beams)})
        SELECT Node, ResultCaseName, Model, SUM(Fx), SUM(Fy), SUM(Fz), SUM(Mx), SUM(My), SUM(Mz)
        FROM NODAL_BEAM_FORCES
        GROUP BY Node, ResultCaseName, Model"""

    return query


def get_combined_cruciform_force_envelope(location: str, full_beam_force_query: str, node_dict: dict,
                                          target_groups: str, excluded_beams: dict,
                                          direction_coefficients: str, transform=False):

    if not transform:
        combined_force_envelope_query = f"""
        WITH BEAM_ENDS AS ({_get_beam_end_query(location, bp_parq_files, node_dict, target_groups, excluded_beams)}),
        FULL_BEAM_PROPERTIES AS ({full_beam_property_query}),
        FULL_BEAM_FORCES AS ({full_beam_force_query}),
        NODAL_BEAM_FORCES AS
        ({_get_nodal_beam_force_query(location, bp_parq_files, target_groups, excluded_beams)}),
    
        COMBO_RESULTS AS
        (
        SELECT 
        Node,
        ResultCaseName,
        Model,
        SUM(Fx) AS Fx, SUM(Fy) AS Fy, SUM(Fz) AS Fz,
        SUM(Mx) AS Mx, SUM(My) AS My, SUM(Mz) AS Mz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2) AS Fxy,
        SQRT(SUM(Fx)**2 + SUM(Fz)**2) AS Fxz,
        SQRT(SUM(Fy)**2 + SUM(Fz)**2) AS Fyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2) AS Mxy,
        SQRT(SUM(Mx)**2 + SUM(Mz)**2) AS Mxz,
        SQRT(SUM(My)**2 + SUM(Mz)**2) AS Myz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2 + SUM(Fz)**2) AS Fxyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2 + SUM(Mz)**2) AS Mxyz
        FROM NODAL_BEAM_FORCES AS BF
        GROUP BY Node, Model, ResultCaseName),
        
        WITH_EXTREMAS AS (SELECT
        Node,
        ResultCaseName,
        Model,
        Fx, Fy, Fz, Mx, My, Mz, Fxy, Fxz, Fyz, Mxy, Mxz, Myz, Fxyz, Mxyz,
        MAX(Fx) OVER() AS Fx_MAX, MIN(Fx) OVER() AS Fx_MIN,
        MAX(Fy) OVER() AS Fy_MAX, MIN(Fy) OVER() AS Fy_MIN,
        MAX(Fz) OVER() AS Fz_MAX, MIN(Fz) OVER() AS Fz_MIN,
        MAX(Mx) OVER() AS Mx_MAX, MIN(Mx) OVER() AS Mx_MIN,
        MAX(My) OVER() AS My_MAX, MIN(My) OVER() AS My_MIN,
        MAX(Mz) OVER() AS Mz_MAX, MIN(Mz) OVER() AS Mz_MIN,
        MAX(Fxy) OVER() AS Fxy_MAX, MAX(Fxz) OVER() AS Fxz_MAX, MAX(Fyz) OVER() AS Fyz_MAX,
        MAX(Mxy) OVER() AS Mxy_MAX, MAX(Mxz) OVER() AS Mxz_MAX, MAX(Myz) OVER() AS Myz_MAX,
        MAX(Fxyz) OVER() AS Fxyz_MAX, MAX(Mxyz) OVER() AS Mxyz_MAX
        FROM COMBO_RESULTS)
    
        SELECT
        Node,
        ResultCaseName,
        Model,
        Fx, Fy, Fz, Mx, My, Mz, Fxy, Fxz, Fyz, Mxy, Mxz, Myz, Fxyz, Mxyz
        FROM WITH_EXTREMAS
        WHERE
        Fx IN (Fx_MAX, Fx_MIN) OR
        Fy IN (Fy_MAX, Fy_MIN) OR
        Fz IN (Fz_MAX, Fz_MIN) OR
        Mx IN (Mx_MAX, Mx_MIN) OR
        My IN (My_MAX, My_MIN) OR
        Mz IN (Mz_MAX, Mz_MIN) OR
        Fxy = Fxy_MAX OR
        Fxz = Fxz_MAX OR
        Fyz = Fyz_MAX OR
        Mxy = Mxy_MAX OR
        Mxz = Mxz_MAX OR
        Myz = Myz_MAX OR
        Fxyz = Fxyz_MAX OR
        Mxyz = Mxyz_MAX
        ORDER BY Node, ResultCaseName"""

    else:

        # The below are multipliers for the transformation of forces to the column head axes.
        # The directional multipliers are based on whether they are to the North or South of the
        # column head, and whether they occur to the East or West of the column head.
        combined_force_envelope_query = f"""
        WITH FULL_BEAM_FORCES AS ({full_beam_force_query}),
        BEAM_ENDS AS ({_get_beam_end_query(location, bp_parq_files, node_dict, target_groups, excluded_beams)}),
        NODAL_BEAM_FORCES AS ({_get_nodal_beam_force_query(location, bp_parq_files, target_groups, excluded_beams)}),

        COMBO_RESULTS AS
        (
        SELECT 
        Node,
        ResultCaseName,
        Model,
        SUM(Fx) AS Fx, SUM(Fy) AS Fy, SUM(Fz) AS Fz,
        SUM(Mx) AS Mx, SUM(My) AS My, SUM(Mz) AS Mz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2) AS Fxy,
        SQRT(SUM(Fx)**2 + SUM(Fz)**2) AS Fxz,
        SQRT(SUM(Fy)**2 + SUM(Fz)**2) AS Fyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2) AS Mxy,
        SQRT(SUM(Mx)**2 + SUM(Mz)**2) AS Mxz,
        SQRT(SUM(My)**2 + SUM(Mz)**2) AS Myz,
        SQRT(SUM(Fx)**2 + SUM(Fy)**2 + SUM(Fz)**2) AS Fxyz,
        SQRT(SUM(Mx)**2 + SUM(My)**2 + SUM(Mz)**2) AS Mxyz
        FROM NODAL_BEAM_FORCES AS BF
        GROUP BY Node, Model, ResultCaseName),
        
        DIRECTION_COEFFICIENTS AS (SELECT * FROM (VALUES {direction_coefficients}) AS dc(Node, cos_coeff, sin_coeff)),
        
        ROTATED_SUMS AS (SELECT
        COMBO_RESULTS.Node,
        ResultCaseName,
        Model,
        cos_coeff * Fx - sin_coeff * Fy AS N,
        sin_coeff * Fx + cos_coeff * Fy AS Vy,
        Fz AS Vz,
        cos_coeff * Mx - sin_coeff * My AS T,
        sin_coeff * Mx + cos_coeff * My AS Myy,
        Mz AS Mzz,
        Fxy AS Vxy,
        SQRT((cos_coeff * Fx - sin_coeff * Fy)**2 + Fz**2) AS Vxz,
        SQRT((sin_coeff * Fx + cos_coeff * Fy)**2 + Fz**2) AS Vyz,
        SQRT((cos_coeff * Mx - sin_coeff * My)**2 + (sin_coeff * Mx + cos_coeff * My)**2) AS Mxy,
        SQRT((cos_coeff * Mx - sin_coeff * My)**2 + Mz**2) AS Mxz,
        SQRT((sin_coeff * Mx + cos_coeff * My)**2 + Mz**2) AS Myz,
        SQRT((cos_coeff * Fx - sin_coeff * Fy)**2 + (sin_coeff * Fx + cos_coeff * Fy)**2 + Fz**2) AS Vxyz,
        SQRT((cos_coeff * Mx - sin_coeff * My)**2 + (sin_coeff * Mx + cos_coeff * My)**2 + Mz**2) AS Mxyz
        FROM COMBO_RESULTS
        JOIN DIRECTION_COEFFICIENTS AS DC ON DC.Node = COMBO_RESULTS.Node
        ),
        
        EXTREMAS AS (SELECT
        MAX(N) AS N_MAX, MIN(N) AS N_MIN,
        MAX(Vy) AS Vy_MAX, MIN(Vy) AS Vy_MIN,
        MAX(Vz) AS Vz_MAX, MIN(Vz) AS Vz_MIN,
        MAX(T) AS T_MAX, MIN(T) AS T_MIN,
        MAX(Myy) AS Myy_MAX, MIN(Myy) AS Myy_MIN,
        MAX(Mzz) AS Mzz_MAX, MIN(Mzz) AS Mzz_MIN,
        MAX(Vxy) AS Vxy_MAX,
        MAX(Vxz) AS Vxz_MAX,
        MAX(Vyz) AS Vyz_MAX,
        MAX(Mxy) AS Mxy_MAX,
        MAX(Mxz) AS Mxz_MAX,
        MAX(Myz) AS Myz_MAX,
        MAX(Vxyz) AS Vxyz_MAX,
        MAX(Mxyz) AS Mxyz_MAX
        FROM ROTATED_SUMS)

        SELECT
        ROTATED_SUMS.Node,
        ResultCaseName,
        Model,
        N, Vy, Vz, T, Myy, Mzz, Vxy, Vxz, Vyz, Mxy, Mxz, Myz, Vxyz, Mxyz
        FROM ROTATED_SUMS
        CROSS JOIN EXTREMAS AS EX
        WHERE
        N IN (N_MAX, N_MIN) OR
        Vy IN (Vy_MAX, Vy_MIN) OR
        Vz IN (Vz_MAX, Vz_MIN) OR
        T IN (T_MAX, T_MIN) OR
        Myy IN (Myy_MAX, Myy_MIN) OR
        Mzz IN (Mzz_MAX, Mzz_MIN) OR
        Vxy = Vxy_MAX OR
        Vxz = Vxz_MAX OR
        Vyz = Vyz_MAX OR
        Mxy = Mxy_MAX OR
        Mxz = Mxz_MAX OR
        Myz = Myz_MAX OR
        Vxyz = Vxyz_MAX OR
        Mxyz = Mxyz_MAX
        ORDER BY ROTATED_SUMS.Node, ResultCaseName"""

    return combined_force_envelope_query


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # INPUTS
    # ----------------------------------------------------------------------

    output_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\02 - Connections\Main Leaf Column Head\C2 Loads\2025-07-28 C2 Column Head Connections_Cruciform Full Combinations_ALS.csv"

    location = "C2"
    direction_coefficients = get_direction_coefficients(location)
    transform_axes = False

    with duckdb.connect() as conn:

        with open(output_fp, 'w+', newline='') as output_file:

            # Get a writer for the cruciform_output_file and write the headers

            if not transform_axes:
                headers = ("Node", "ResultCaseName", "Model",
                           "Fx", "Fy", "Fz", "Mx", "My", "Mz",
                           "Fxy", "Fxz", "Fyz", "Mxy", "Mxz", "Myz", "Fxyz", "Mxyz")
            else:
                headers = ("Node", "ResultCaseName", "Model",
                           "N", "Vy", "Vz", "T", "Myy", "Mzz",
                           "Vxy", "Vxz", "Vyz", "Mxy", "Mxz", "Myz", "Vxyz", "Mxyz")

            writer = csv.writer(output_file)
            writer.writerow(headers)

            # This write_full_beam_forces_query merges all of the results from the different analysis model variants into a single set
            full_beam_force_query = get_full_beam_force_query(location, bf_parq_files, bp_parq_files,
                                                              excluded_beam_dict, target_groups, result_case_filter)

            full_beam_property_query = get_full_beam_properties_query(bp_parq_files, target_groups)

            # The below write_full_beam_forces_query
            # a) gets the full result set as a single table (FULL_BEAM_FORCES),
            # b) matches the end positions with the target nodes and filters out unnecessary records (BEAM_ENDS)
            # loc) finds the results that occur at the positions in the filtered table (NODAL_BEAM_FORCES),
            # d) sums the forces in NODAL_BEAM_FORCES that occur for the same node and same combination (COMBO_RESULTS),
            # e) selects the individual results if they correspond to any of the prescribed extrema values
            combined_cruciform_force_envelope_query = get_combined_cruciform_force_envelope(location,
                                                                                            full_beam_force_query,
                                                                                            node_dict,
                                                                                            target_groups,
                                                                                            excluded_beam_dict,
                                                                                            direction_coefficients,
                                                                                            transform=transform_axes)

            full_nodal_force_query = get_full_combined_nodal_force_query(location,
                                                                         bp_parq_files,
                                                                         node_dict,
                                                                         target_groups,
                                                                         excluded_beam_dict)

            # Write the results to cruciform_output_file
            results = conn.execute(combined_cruciform_force_envelope_query).fetchall()
            # for result in results:
            #     print(result)
            writer.writerows(results)


