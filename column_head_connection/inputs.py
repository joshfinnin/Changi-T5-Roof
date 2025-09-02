
"""Script containing the inputs for the different modules for the critical combination extraction."""

from math import sin, cos, radians

bf_parq_files = {
    'LB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmax_Parquet\\beam_forces.parquet',
    'LB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmin_Parquet\\beam_forces.parquet',
    'UB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmax_Parquet\\beam_forces.parquet',
    'UB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmin_Parquet\\beam_forces.parquet',
    '0 ALS Removal P-TR01a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\0 ALS Removal P-TR01a-01_GlobalParquet\\beam_forces.parquet',
    '1 ALS Removal P-TR01a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\1 ALS Removal P-TR01a-02_GlobalParquet\\beam_forces.parquet',
    '10 ALS Removal P-TR02b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\10 ALS Removal P-TR02b-02_GlobalParquet\\beam_forces.parquet',
    '100 ALS Removal CHC2-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\100 ALS Removal CHC2-B1_GlobalParquet\\beam_forces.parquet',
    '101 ALS Removal CHC2-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\101 ALS Removal CHC2-B2_GlobalParquet\\beam_forces.parquet',
    '102 ALS Removal CHC2-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\102 ALS Removal CHC2-B3_GlobalParquet\\beam_forces.parquet',
    '103 ALS Removal CHC2-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\103 ALS Removal CHC2-B4_GlobalParquet\\beam_forces.parquet',
    '104 ALS Removal CHC2-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\104 ALS Removal CHC2-D1_GlobalParquet\\beam_forces.parquet',
    '105 ALS Removal CHC2-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\105 ALS Removal CHC2-D2_GlobalParquet\\beam_forces.parquet',
    '106 ALS Removal CHC2-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\106 ALS Removal CHC2-D3_GlobalParquet\\beam_forces.parquet',
    '107 ALS Removal CHC2-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\107 ALS Removal CHC2-D4_GlobalParquet\\beam_forces.parquet',
    '108 ALS Removal CHC1-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\108 ALS Removal CHC1-T1_GlobalParquet\\beam_forces.parquet',
    '109 ALS Removal CHC1-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\109 ALS Removal CHC1-T2_GlobalParquet\\beam_forces.parquet',
    '11 ALS Removal P-TR02b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\11 ALS Removal P-TR02b-03_GlobalParquet\\beam_forces.parquet',
    '110 ALS Removal CHC1-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\110 ALS Removal CHC1-T3_GlobalParquet\\beam_forces.parquet',
    '111 ALS Removal CHC1-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\111 ALS Removal CHC1-T4_GlobalParquet\\beam_forces.parquet',
    '112 ALS Removal CHC1-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\112 ALS Removal CHC1-B1_GlobalParquet\\beam_forces.parquet',
    '113 ALS Removal CHC1-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\113 ALS Removal CHC1-B2_GlobalParquet\\beam_forces.parquet',
    '114 ALS Removal CHC1-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\114 ALS Removal CHC1-B3_GlobalParquet\\beam_forces.parquet',
    '115 ALS Removal CHC1-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\115 ALS Removal CHC1-B4_GlobalParquet\\beam_forces.parquet',
    '116 ALS Removal CHC1-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\116 ALS Removal CHC1-D1_GlobalParquet\\beam_forces.parquet',
    '117 ALS Removal CHC1-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\117 ALS Removal CHC1-D2_GlobalParquet\\beam_forces.parquet',
    '118 ALS Removal CHC1-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\118 ALS Removal CHC1-D3_GlobalParquet\\beam_forces.parquet',
    '119 ALS Removal CHC1-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\119 ALS Removal CHC1-D4_GlobalParquet\\beam_forces.parquet',
    '12 ALS Removal P-TR03a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\12 ALS Removal P-TR03a-01_GlobalParquet\\beam_forces.parquet',
    '13 ALS Removal P-TR03a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\13 ALS Removal P-TR03a-02_GlobalParquet\\beam_forces.parquet',
    '14 ALS Removal P-TR03a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\14 ALS Removal P-TR03a-03_GlobalParquet\\beam_forces.parquet',
    '15 ALS Removal P-TR03a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\15 ALS Removal P-TR03a-04_GlobalParquet\\beam_forces.parquet',
    '16 ALS Removal P-TR03a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\16 ALS Removal P-TR03a-05_GlobalParquet\\beam_forces.parquet',
    '17 ALS Removal P-TR03b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\17 ALS Removal P-TR03b-01_GlobalParquet\\beam_forces.parquet',
    '18 ALS Removal P-TR03b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\18 ALS Removal P-TR03b-02_GlobalParquet\\beam_forces.parquet',
    '19 ALS Removal P-TR03b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\19 ALS Removal P-TR03b-03_GlobalParquet\\beam_forces.parquet',
    '2 ALS Removal P-TR01a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\2 ALS Removal P-TR01a-03_GlobalParquet\\beam_forces.parquet',
    '20 ALS Removal P-TR03b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\20 ALS Removal P-TR03b-04_GlobalParquet\\beam_forces.parquet',
    '21 ALS Removal P-TR03b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\21 ALS Removal P-TR03b-05_GlobalParquet\\beam_forces.parquet',
    '22 ALS Removal P-TR04a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\22 ALS Removal P-TR04a-01_GlobalParquet\\beam_forces.parquet',
    '23 ALS Removal P-TR04a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\23 ALS Removal P-TR04a-02_GlobalParquet\\beam_forces.parquet',
    '24 ALS Removal P-TR04a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\24 ALS Removal P-TR04a-03_GlobalParquet\\beam_forces.parquet',
    '25 ALS Removal P-TR04a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\25 ALS Removal P-TR04a-04_GlobalParquet\\beam_forces.parquet',
    '26 ALS Removal P-TR04a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\26 ALS Removal P-TR04a-05_GlobalParquet\\beam_forces.parquet',
    '27 ALS Removal P-TR04a-06': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\27 ALS Removal P-TR04a-06_GlobalParquet\\beam_forces.parquet',
    '28 ALS Removal P-TR04a-07': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\28 ALS Removal P-TR04a-07_GlobalParquet\\beam_forces.parquet',
    '29 ALS Removal P-TR04b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\29 ALS Removal P-TR04b-01_GlobalParquet\\beam_forces.parquet',
    '3 ALS Removal P-TR01b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\3 ALS Removal P-TR01b-01_GlobalParquet\\beam_forces.parquet',
    '30 ALS Removal P-TR04b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\30 ALS Removal P-TR04b-02_GlobalParquet\\beam_forces.parquet',
    '31 ALS Removal P-TR04b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\31 ALS Removal P-TR04b-03_GlobalParquet\\beam_forces.parquet',
    '32 ALS Removal P-TR04b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\32 ALS Removal P-TR04b-04_GlobalParquet\\beam_forces.parquet',
    '33 ALS Removal P-TR04b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\33 ALS Removal P-TR04b-05_GlobalParquet\\beam_forces.parquet',
    '34 ALS Removal P-TR04b-06': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\34 ALS Removal P-TR04b-06_GlobalParquet\\beam_forces.parquet',
    '35 ALS Removal P-TR04b-07': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\35 ALS Removal P-TR04b-07_GlobalParquet\\beam_forces.parquet',
    '36 ALS Removal S-TR02-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\36 ALS Removal S-TR02-01_GlobalParquet\\beam_forces.parquet',
    '37 ALS Removal S-TR02-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\37 ALS Removal S-TR02-02_GlobalParquet\\beam_forces.parquet',
    '38 ALS Removal S-TR05-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\38 ALS Removal S-TR05-01_GlobalParquet\\beam_forces.parquet',
    '39 ALS Removal S-TR05-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\39 ALS Removal S-TR05-02_GlobalParquet\\beam_forces.parquet',
    '4 ALS Removal P-TR01b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\4 ALS Removal P-TR01b-02_GlobalParquet\\beam_forces.parquet',
    '40 ALS Removal S-TR04-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\40 ALS Removal S-TR04-01_GlobalParquet\\beam_forces.parquet',
    '41 ALS Removal S-TR11-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\41 ALS Removal S-TR11-01_GlobalParquet\\beam_forces.parquet',
    '42 ALS Removal S-TR13-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\42 ALS Removal S-TR13-01_GlobalParquet\\beam_forces.parquet',
    '43 ALS Removal S-TR13-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\43 ALS Removal S-TR13-02_GlobalParquet\\beam_forces.parquet',
    '44 ALS Removal S-TR13-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\44 ALS Removal S-TR13-03_GlobalParquet\\beam_forces.parquet',
    '45 ALS Removal S-TR13-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\45 ALS Removal S-TR13-04_GlobalParquet\\beam_forces.parquet',
    '46 ALS Removal S-TR14-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\46 ALS Removal S-TR14-01_GlobalParquet\\beam_forces.parquet',
    '47 ALS Removal S-TR14-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\47 ALS Removal S-TR14-02_GlobalParquet\\beam_forces.parquet',
    '48 ALS Removal S-TR14-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\48 ALS Removal S-TR14-03_GlobalParquet\\beam_forces.parquet',
    '49 ALS Removal S-TR14-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\49 ALS Removal S-TR14-04_GlobalParquet\\beam_forces.parquet',
    '5 ALS Removal P-TR01b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\5 ALS Removal P-TR01b-03_GlobalParquet\\beam_forces.parquet',
    '50 ALS Removal S-TR01-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\50 ALS Removal S-TR01-01_GlobalParquet\\beam_forces.parquet',
    '51 ALS Removal S-TR01-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\51 ALS Removal S-TR01-02_GlobalParquet\\beam_forces.parquet',
    '52 ALS Removal S-TR01a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\52 ALS Removal S-TR01a-05_GlobalParquet\\beam_forces.parquet',
    '53 ALS Removal S-TR01b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\53 ALS Removal S-TR01b-05_GlobalParquet\\beam_forces.parquet',
    '54 ALS Removal S-TR02-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\54 ALS Removal S-TR02-03_GlobalParquet\\beam_forces.parquet',
    '55 ALS Removal S-TR02a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\55 ALS Removal S-TR02a-05_GlobalParquet\\beam_forces.parquet',
    '56 ALS Removal S-TR02b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\56 ALS Removal S-TR02b-05_GlobalParquet\\beam_forces.parquet',
    '57 ALS Removal S-TR04-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\57 ALS Removal S-TR04-02_GlobalParquet\\beam_forces.parquet',
    '58 ALS Removal S-TR05-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\58 ALS Removal S-TR05-03_GlobalParquet\\beam_forces.parquet',
    '59 ALS Removal S-TR06-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\59 ALS Removal S-TR06-01_GlobalParquet\\beam_forces.parquet',
    '6 ALS Removal P-TR02a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\6 ALS Removal P-TR02a-01_GlobalParquet\\beam_forces.parquet',
    '60 ALS Removal S-TR06-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\60 ALS Removal S-TR06-02_GlobalParquet\\beam_forces.parquet',
    '61 ALS Removal S-TR06-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\61 ALS Removal S-TR06-03_GlobalParquet\\beam_forces.parquet',
    '62 ALS Removal S-TR07-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\62 ALS Removal S-TR07-01_GlobalParquet\\beam_forces.parquet',
    '63 ALS Removal S-TR07-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\63 ALS Removal S-TR07-02_GlobalParquet\\beam_forces.parquet',
    '64 ALS Removal S-TR07-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\64 ALS Removal S-TR07-03_GlobalParquet\\beam_forces.parquet',
    '65 ALS Removal S-TR08-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\65 ALS Removal S-TR08-01_GlobalParquet\\beam_forces.parquet',
    '66 ALS Removal S-TR11-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\66 ALS Removal S-TR11-02_GlobalParquet\\beam_forces.parquet',
    '67 ALS Removal S-TR12-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\67 ALS Removal S-TR12-01_GlobalParquet\\beam_forces.parquet',
    '68 ALS Removal TR01a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\68 ALS Removal TR01a-04_GlobalParquet\\beam_forces.parquet',
    '69 ALS Removal TR01b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\69 ALS Removal TR01b-04_GlobalParquet\\beam_forces.parquet',
    '7 ALS Removal P-TR02a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\7 ALS Removal P-TR02a-02_GlobalParquet\\beam_forces.parquet',
    '70 ALS Removal TR02a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\70 ALS Removal TR02a-04_GlobalParquet\\beam_forces.parquet',
    '71 ALS Removal TR02b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\71 ALS Removal TR02b-04_GlobalParquet\\beam_forces.parquet',
    '72 ALS Removal CHB1-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\72 ALS Removal CHB1-T1_GlobalParquet\\beam_forces.parquet',
    '73 ALS Removal CHB1-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\73 ALS Removal CHB1-T2_GlobalParquet\\beam_forces.parquet',
    '74 ALS Removal CHB1-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\74 ALS Removal CHB1-T3_GlobalParquet\\beam_forces.parquet',
    '75 ALS Removal CHB1-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\75 ALS Removal CHB1-T4_GlobalParquet\\beam_forces.parquet',
    '76 ALS Removal CHB1-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\76 ALS Removal CHB1-B1_GlobalParquet\\beam_forces.parquet',
    '77 ALS Removal CHB1-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\77 ALS Removal CHB1-B2_GlobalParquet\\beam_forces.parquet',
    '78 ALS Removal CHB1-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\78 ALS Removal CHB1-B3_GlobalParquet\\beam_forces.parquet',
    '79 ALS Removal CHB1-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\79 ALS Removal CHB1-B4_GlobalParquet\\beam_forces.parquet',
    '8 ALS Removal P-TR02a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\8 ALS Removal P-TR02a-03_GlobalParquet\\beam_forces.parquet',
    '80 ALS Removal CHB1-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\80 ALS Removal CHB1-D1_GlobalParquet\\beam_forces.parquet',
    '81 ALS Removal CHB1-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\81 ALS Removal CHB1-D2_GlobalParquet\\beam_forces.parquet',
    '82 ALS Removal CHB1-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\82 ALS Removal CHB1-D3_GlobalParquet\\beam_forces.parquet',
    '83 ALS Removal CHB1-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\83 ALS Removal CHB1-D4_GlobalParquet\\beam_forces.parquet',
    '84 ALS Removal CHB2-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\84 ALS Removal CHB2-T1_GlobalParquet\\beam_forces.parquet',
    '85 ALS Removal CHB2-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\85 ALS Removal CHB2-T2_GlobalParquet\\beam_forces.parquet',
    '86 ALS Removal CHB2-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\86 ALS Removal CHB2-T3_GlobalParquet\\beam_forces.parquet',
    '87 ALS Removal CHB2-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\87 ALS Removal CHB2-T4_GlobalParquet\\beam_forces.parquet',
    '88 ALS Removal CHB2-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\88 ALS Removal CHB2-B1_GlobalParquet\\beam_forces.parquet',
    '89 ALS Removal CHB2-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\89 ALS Removal CHB2-B2_GlobalParquet\\beam_forces.parquet',
    '9 ALS Removal P-TR02b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\9 ALS Removal P-TR02b-01_GlobalParquet\\beam_forces.parquet',
    '90 ALS Removal CHB2-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\90 ALS Removal CHB2-B3_GlobalParquet\\beam_forces.parquet',
    '91 ALS Removal CHB2-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\91 ALS Removal CHB2-B4_GlobalParquet\\beam_forces.parquet',
    '92 ALS Removal CHB2-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\92 ALS Removal CHB2-D1_GlobalParquet\\beam_forces.parquet',
    '93 ALS Removal CHB2-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\93 ALS Removal CHB2-D2_GlobalParquet\\beam_forces.parquet',
    '94 ALS Removal CHB2-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\94 ALS Removal CHB2-D3_GlobalParquet\\beam_forces.parquet',
    '95 ALS Removal CHB2-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\95 ALS Removal CHB2-D4_GlobalParquet\\beam_forces.parquet',
    '96 ALS Removal CHC2-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\96 ALS Removal CHC2-T1_GlobalParquet\\beam_forces.parquet',
    '97 ALS Removal CHC2-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\97 ALS Removal CHC2-T2_GlobalParquet\\beam_forces.parquet',
    '98 ALS Removal CHC2-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\98 ALS Removal CHC2-T3_GlobalParquet\\beam_forces.parquet',
    '99 ALS Removal CHC2-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\99 ALS Removal CHC2-T4_GlobalParquet\\beam_forces.parquet'}

bp_parq_files = {
    'LB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmax_Parquet\\beam_properties.parquet',
    'LB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_LB_Gmin_Parquet\\beam_properties.parquet',
    'UB_Gmax': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmax_Parquet\\beam_properties.parquet',
    'UB_Gmin': 'C:\\Users\\Josh.Finnin\\Mott MacDonald\\MBC SAM Project Portal - 01-Structures\\Work\\Design\\05 - Roof\\01 - FE Models\\V1.4.4\\Global Axes Results\\V1_4_4_UB_Gmin_Parquet\\beam_properties.parquet',
    '0 ALS Removal P-TR01a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\0 ALS Removal P-TR01a-01_GlobalParquet\\beam_properties.parquet',
    '1 ALS Removal P-TR01a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\1 ALS Removal P-TR01a-02_GlobalParquet\\beam_properties.parquet',
    '10 ALS Removal P-TR02b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\10 ALS Removal P-TR02b-02_GlobalParquet\\beam_properties.parquet',
    '100 ALS Removal CHC2-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\100 ALS Removal CHC2-B1_GlobalParquet\\beam_properties.parquet',
    '101 ALS Removal CHC2-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\101 ALS Removal CHC2-B2_GlobalParquet\\beam_properties.parquet',
    '102 ALS Removal CHC2-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\102 ALS Removal CHC2-B3_GlobalParquet\\beam_properties.parquet',
    '103 ALS Removal CHC2-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\103 ALS Removal CHC2-B4_GlobalParquet\\beam_properties.parquet',
    '104 ALS Removal CHC2-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\104 ALS Removal CHC2-D1_GlobalParquet\\beam_properties.parquet',
    '105 ALS Removal CHC2-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\105 ALS Removal CHC2-D2_GlobalParquet\\beam_properties.parquet',
    '106 ALS Removal CHC2-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\106 ALS Removal CHC2-D3_GlobalParquet\\beam_properties.parquet',
    '107 ALS Removal CHC2-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\107 ALS Removal CHC2-D4_GlobalParquet\\beam_properties.parquet',
    '108 ALS Removal CHC1-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\108 ALS Removal CHC1-T1_GlobalParquet\\beam_properties.parquet',
    '109 ALS Removal CHC1-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\109 ALS Removal CHC1-T2_GlobalParquet\\beam_properties.parquet',
    '11 ALS Removal P-TR02b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\11 ALS Removal P-TR02b-03_GlobalParquet\\beam_properties.parquet',
    '110 ALS Removal CHC1-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\110 ALS Removal CHC1-T3_GlobalParquet\\beam_properties.parquet',
    '111 ALS Removal CHC1-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\111 ALS Removal CHC1-T4_GlobalParquet\\beam_properties.parquet',
    '112 ALS Removal CHC1-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\112 ALS Removal CHC1-B1_GlobalParquet\\beam_properties.parquet',
    '113 ALS Removal CHC1-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\113 ALS Removal CHC1-B2_GlobalParquet\\beam_properties.parquet',
    '114 ALS Removal CHC1-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\114 ALS Removal CHC1-B3_GlobalParquet\\beam_properties.parquet',
    '115 ALS Removal CHC1-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\115 ALS Removal CHC1-B4_GlobalParquet\\beam_properties.parquet',
    '116 ALS Removal CHC1-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\116 ALS Removal CHC1-D1_GlobalParquet\\beam_properties.parquet',
    '117 ALS Removal CHC1-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\117 ALS Removal CHC1-D2_GlobalParquet\\beam_properties.parquet',
    '118 ALS Removal CHC1-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\118 ALS Removal CHC1-D3_GlobalParquet\\beam_properties.parquet',
    '119 ALS Removal CHC1-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\119 ALS Removal CHC1-D4_GlobalParquet\\beam_properties.parquet',
    '12 ALS Removal P-TR03a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\12 ALS Removal P-TR03a-01_GlobalParquet\\beam_properties.parquet',
    '13 ALS Removal P-TR03a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\13 ALS Removal P-TR03a-02_GlobalParquet\\beam_properties.parquet',
    '14 ALS Removal P-TR03a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\14 ALS Removal P-TR03a-03_GlobalParquet\\beam_properties.parquet',
    '15 ALS Removal P-TR03a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\15 ALS Removal P-TR03a-04_GlobalParquet\\beam_properties.parquet',
    '16 ALS Removal P-TR03a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\16 ALS Removal P-TR03a-05_GlobalParquet\\beam_properties.parquet',
    '17 ALS Removal P-TR03b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\17 ALS Removal P-TR03b-01_GlobalParquet\\beam_properties.parquet',
    '18 ALS Removal P-TR03b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\18 ALS Removal P-TR03b-02_GlobalParquet\\beam_properties.parquet',
    '19 ALS Removal P-TR03b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\19 ALS Removal P-TR03b-03_GlobalParquet\\beam_properties.parquet',
    '2 ALS Removal P-TR01a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\2 ALS Removal P-TR01a-03_GlobalParquet\\beam_properties.parquet',
    '20 ALS Removal P-TR03b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\20 ALS Removal P-TR03b-04_GlobalParquet\\beam_properties.parquet',
    '21 ALS Removal P-TR03b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\21 ALS Removal P-TR03b-05_GlobalParquet\\beam_properties.parquet',
    '22 ALS Removal P-TR04a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\22 ALS Removal P-TR04a-01_GlobalParquet\\beam_properties.parquet',
    '23 ALS Removal P-TR04a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\23 ALS Removal P-TR04a-02_GlobalParquet\\beam_properties.parquet',
    '24 ALS Removal P-TR04a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\24 ALS Removal P-TR04a-03_GlobalParquet\\beam_properties.parquet',
    '25 ALS Removal P-TR04a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\25 ALS Removal P-TR04a-04_GlobalParquet\\beam_properties.parquet',
    '26 ALS Removal P-TR04a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\26 ALS Removal P-TR04a-05_GlobalParquet\\beam_properties.parquet',
    '27 ALS Removal P-TR04a-06': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\27 ALS Removal P-TR04a-06_GlobalParquet\\beam_properties.parquet',
    '28 ALS Removal P-TR04a-07': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\28 ALS Removal P-TR04a-07_GlobalParquet\\beam_properties.parquet',
    '29 ALS Removal P-TR04b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\29 ALS Removal P-TR04b-01_GlobalParquet\\beam_properties.parquet',
    '3 ALS Removal P-TR01b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\3 ALS Removal P-TR01b-01_GlobalParquet\\beam_properties.parquet',
    '30 ALS Removal P-TR04b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\30 ALS Removal P-TR04b-02_GlobalParquet\\beam_properties.parquet',
    '31 ALS Removal P-TR04b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\31 ALS Removal P-TR04b-03_GlobalParquet\\beam_properties.parquet',
    '32 ALS Removal P-TR04b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\32 ALS Removal P-TR04b-04_GlobalParquet\\beam_properties.parquet',
    '33 ALS Removal P-TR04b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\33 ALS Removal P-TR04b-05_GlobalParquet\\beam_properties.parquet',
    '34 ALS Removal P-TR04b-06': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\34 ALS Removal P-TR04b-06_GlobalParquet\\beam_properties.parquet',
    '35 ALS Removal P-TR04b-07': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\35 ALS Removal P-TR04b-07_GlobalParquet\\beam_properties.parquet',
    '36 ALS Removal S-TR02-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\36 ALS Removal S-TR02-01_GlobalParquet\\beam_properties.parquet',
    '37 ALS Removal S-TR02-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\37 ALS Removal S-TR02-02_GlobalParquet\\beam_properties.parquet',
    '38 ALS Removal S-TR05-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\38 ALS Removal S-TR05-01_GlobalParquet\\beam_properties.parquet',
    '39 ALS Removal S-TR05-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\39 ALS Removal S-TR05-02_GlobalParquet\\beam_properties.parquet',
    '4 ALS Removal P-TR01b-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\4 ALS Removal P-TR01b-02_GlobalParquet\\beam_properties.parquet',
    '40 ALS Removal S-TR04-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\40 ALS Removal S-TR04-01_GlobalParquet\\beam_properties.parquet',
    '41 ALS Removal S-TR11-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\41 ALS Removal S-TR11-01_GlobalParquet\\beam_properties.parquet',
    '42 ALS Removal S-TR13-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\42 ALS Removal S-TR13-01_GlobalParquet\\beam_properties.parquet',
    '43 ALS Removal S-TR13-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\43 ALS Removal S-TR13-02_GlobalParquet\\beam_properties.parquet',
    '44 ALS Removal S-TR13-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\44 ALS Removal S-TR13-03_GlobalParquet\\beam_properties.parquet',
    '45 ALS Removal S-TR13-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\45 ALS Removal S-TR13-04_GlobalParquet\\beam_properties.parquet',
    '46 ALS Removal S-TR14-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\46 ALS Removal S-TR14-01_GlobalParquet\\beam_properties.parquet',
    '47 ALS Removal S-TR14-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\47 ALS Removal S-TR14-02_GlobalParquet\\beam_properties.parquet',
    '48 ALS Removal S-TR14-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\48 ALS Removal S-TR14-03_GlobalParquet\\beam_properties.parquet',
    '49 ALS Removal S-TR14-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\49 ALS Removal S-TR14-04_GlobalParquet\\beam_properties.parquet',
    '5 ALS Removal P-TR01b-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\5 ALS Removal P-TR01b-03_GlobalParquet\\beam_properties.parquet',
    '50 ALS Removal S-TR01-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\50 ALS Removal S-TR01-01_GlobalParquet\\beam_properties.parquet',
    '51 ALS Removal S-TR01-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\51 ALS Removal S-TR01-02_GlobalParquet\\beam_properties.parquet',
    '52 ALS Removal S-TR01a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\52 ALS Removal S-TR01a-05_GlobalParquet\\beam_properties.parquet',
    '53 ALS Removal S-TR01b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\53 ALS Removal S-TR01b-05_GlobalParquet\\beam_properties.parquet',
    '54 ALS Removal S-TR02-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\54 ALS Removal S-TR02-03_GlobalParquet\\beam_properties.parquet',
    '55 ALS Removal S-TR02a-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\55 ALS Removal S-TR02a-05_GlobalParquet\\beam_properties.parquet',
    '56 ALS Removal S-TR02b-05': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\56 ALS Removal S-TR02b-05_GlobalParquet\\beam_properties.parquet',
    '57 ALS Removal S-TR04-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\57 ALS Removal S-TR04-02_GlobalParquet\\beam_properties.parquet',
    '58 ALS Removal S-TR05-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\58 ALS Removal S-TR05-03_GlobalParquet\\beam_properties.parquet',
    '59 ALS Removal S-TR06-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\59 ALS Removal S-TR06-01_GlobalParquet\\beam_properties.parquet',
    '6 ALS Removal P-TR02a-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\6 ALS Removal P-TR02a-01_GlobalParquet\\beam_properties.parquet',
    '60 ALS Removal S-TR06-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\60 ALS Removal S-TR06-02_GlobalParquet\\beam_properties.parquet',
    '61 ALS Removal S-TR06-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\61 ALS Removal S-TR06-03_GlobalParquet\\beam_properties.parquet',
    '62 ALS Removal S-TR07-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\62 ALS Removal S-TR07-01_GlobalParquet\\beam_properties.parquet',
    '63 ALS Removal S-TR07-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\63 ALS Removal S-TR07-02_GlobalParquet\\beam_properties.parquet',
    '64 ALS Removal S-TR07-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\64 ALS Removal S-TR07-03_GlobalParquet\\beam_properties.parquet',
    '65 ALS Removal S-TR08-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\65 ALS Removal S-TR08-01_GlobalParquet\\beam_properties.parquet',
    '66 ALS Removal S-TR11-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\66 ALS Removal S-TR11-02_GlobalParquet\\beam_properties.parquet',
    '67 ALS Removal S-TR12-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\67 ALS Removal S-TR12-01_GlobalParquet\\beam_properties.parquet',
    '68 ALS Removal TR01a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\68 ALS Removal TR01a-04_GlobalParquet\\beam_properties.parquet',
    '69 ALS Removal TR01b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\69 ALS Removal TR01b-04_GlobalParquet\\beam_properties.parquet',
    '7 ALS Removal P-TR02a-02': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\7 ALS Removal P-TR02a-02_GlobalParquet\\beam_properties.parquet',
    '70 ALS Removal TR02a-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\70 ALS Removal TR02a-04_GlobalParquet\\beam_properties.parquet',
    '71 ALS Removal TR02b-04': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\71 ALS Removal TR02b-04_GlobalParquet\\beam_properties.parquet',
    '72 ALS Removal CHB1-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\72 ALS Removal CHB1-T1_GlobalParquet\\beam_properties.parquet',
    '73 ALS Removal CHB1-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\73 ALS Removal CHB1-T2_GlobalParquet\\beam_properties.parquet',
    '74 ALS Removal CHB1-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\74 ALS Removal CHB1-T3_GlobalParquet\\beam_properties.parquet',
    '75 ALS Removal CHB1-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\75 ALS Removal CHB1-T4_GlobalParquet\\beam_properties.parquet',
    '76 ALS Removal CHB1-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\76 ALS Removal CHB1-B1_GlobalParquet\\beam_properties.parquet',
    '77 ALS Removal CHB1-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\77 ALS Removal CHB1-B2_GlobalParquet\\beam_properties.parquet',
    '78 ALS Removal CHB1-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\78 ALS Removal CHB1-B3_GlobalParquet\\beam_properties.parquet',
    '79 ALS Removal CHB1-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\79 ALS Removal CHB1-B4_GlobalParquet\\beam_properties.parquet',
    '8 ALS Removal P-TR02a-03': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\8 ALS Removal P-TR02a-03_GlobalParquet\\beam_properties.parquet',
    '80 ALS Removal CHB1-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\80 ALS Removal CHB1-D1_GlobalParquet\\beam_properties.parquet',
    '81 ALS Removal CHB1-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\81 ALS Removal CHB1-D2_GlobalParquet\\beam_properties.parquet',
    '82 ALS Removal CHB1-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\82 ALS Removal CHB1-D3_GlobalParquet\\beam_properties.parquet',
    '83 ALS Removal CHB1-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\83 ALS Removal CHB1-D4_GlobalParquet\\beam_properties.parquet',
    '84 ALS Removal CHB2-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\84 ALS Removal CHB2-T1_GlobalParquet\\beam_properties.parquet',
    '85 ALS Removal CHB2-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\85 ALS Removal CHB2-T2_GlobalParquet\\beam_properties.parquet',
    '86 ALS Removal CHB2-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\86 ALS Removal CHB2-T3_GlobalParquet\\beam_properties.parquet',
    '87 ALS Removal CHB2-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\87 ALS Removal CHB2-T4_GlobalParquet\\beam_properties.parquet',
    '88 ALS Removal CHB2-B1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\88 ALS Removal CHB2-B1_GlobalParquet\\beam_properties.parquet',
    '89 ALS Removal CHB2-B2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\89 ALS Removal CHB2-B2_GlobalParquet\\beam_properties.parquet',
    '9 ALS Removal P-TR02b-01': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\9 ALS Removal P-TR02b-01_GlobalParquet\\beam_properties.parquet',
    '90 ALS Removal CHB2-B3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\90 ALS Removal CHB2-B3_GlobalParquet\\beam_properties.parquet',
    '91 ALS Removal CHB2-B4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\91 ALS Removal CHB2-B4_GlobalParquet\\beam_properties.parquet',
    '92 ALS Removal CHB2-D1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\92 ALS Removal CHB2-D1_GlobalParquet\\beam_properties.parquet',
    '93 ALS Removal CHB2-D2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\93 ALS Removal CHB2-D2_GlobalParquet\\beam_properties.parquet',
    '94 ALS Removal CHB2-D3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\94 ALS Removal CHB2-D3_GlobalParquet\\beam_properties.parquet',
    '95 ALS Removal CHB2-D4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\95 ALS Removal CHB2-D4_GlobalParquet\\beam_properties.parquet',
    '96 ALS Removal CHC2-T1': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\96 ALS Removal CHC2-T1_GlobalParquet\\beam_properties.parquet',
    '97 ALS Removal CHC2-T2': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\97 ALS Removal CHC2-T2_GlobalParquet\\beam_properties.parquet',
    '98 ALS Removal CHC2-T3': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\98 ALS Removal CHC2-T3_GlobalParquet\\beam_properties.parquet',
    '99 ALS Removal CHC2-T4': 'D:\\Projects\\Changi T5\\MUC\\Strand7 Model Data\\99 ALS Removal CHC2-T4_GlobalParquet\\beam_properties.parquet'}

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

column_beam_number_dict = {'LB_Gmax': {'B1': 2665, 'B2': 2690, 'C1': 2685, 'C2': 2687},
                           'LB_Gmin': {'B1': 2665, 'B2': 2690, 'C1': 2685, 'C2': 2687},
                           'UB_Gmax': {'B1': 2665, 'B2': 2690, 'C1': 2685, 'C2': 2687},
                           'UB_Gmin': {'B1': 2665, 'B2': 2690, 'C1': 2685, 'C2': 2687},
                           '0 ALS Removal P-TR01a-01': {'B1': 2658, 'B2': 2683, 'C1': 2678, 'C2': 2680},
                           '1 ALS Removal P-TR01a-02': {'B1': 2660, 'B2': 2685, 'C1': 2680, 'C2': 2682},
                           '10 ALS Removal P-TR02b-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '100 ALS Removal CHC2-B1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '101 ALS Removal CHC2-B2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '102 ALS Removal CHC2-B3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '103 ALS Removal CHC2-B4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '104 ALS Removal CHC2-D1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '105 ALS Removal CHC2-D2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '106 ALS Removal CHC2-D3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '107 ALS Removal CHC2-D4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '11 ALS Removal P-TR02b-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '12 ALS Removal P-TR03a-01': {'B1': 2663, 'B2': 2688, 'C1': 2683, 'C2': 2685},
                           '13 ALS Removal P-TR03a-02': {'B1': 2663, 'B2': 2688, 'C1': 2683, 'C2': 2685},
                           '14 ALS Removal P-TR03a-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '15 ALS Removal P-TR03a-04': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '16 ALS Removal P-TR03a-05': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '17 ALS Removal P-TR03b-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '18 ALS Removal P-TR03b-02': {'B1': 2663, 'B2': 2688, 'C1': 2683, 'C2': 2685},
                           '19 ALS Removal P-TR03b-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '2 ALS Removal P-TR01a-03': {'B1': 2661, 'B2': 2686, 'C1': 2681, 'C2': 2683},
                           '20 ALS Removal P-TR03b-04': {'B1': 2660, 'B2': 2685, 'C1': 2680, 'C2': 2682},
                           '21 ALS Removal P-TR03b-05': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '22 ALS Removal P-TR04a-01': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '23 ALS Removal P-TR04a-02': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '24 ALS Removal P-TR04a-03': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '25 ALS Removal P-TR04a-04': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '26 ALS Removal P-TR04a-05': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '27 ALS Removal P-TR04a-06': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '28 ALS Removal P-TR04a-07': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '29 ALS Removal P-TR04b-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '3 ALS Removal P-TR01b-01': {'B1': 2661, 'B2': 2686, 'C1': 2681, 'C2': 2683},
                           '30 ALS Removal P-TR04b-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '31 ALS Removal P-TR04b-03': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '32 ALS Removal P-TR04b-04': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '33 ALS Removal P-TR04b-05': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '34 ALS Removal P-TR04b-06': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '35 ALS Removal P-TR04b-07': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '36 ALS Removal S-TR02-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '37 ALS Removal S-TR02-02': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '38 ALS Removal S-TR05-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '39 ALS Removal S-TR05-02': {'B1': 2663, 'B2': 2688, 'C1': 2683, 'C2': 2685},
                           '4 ALS Removal P-TR01b-02': {'B1': 2659, 'B2': 2684, 'C1': 2679, 'C2': 2681},
                           '40 ALS Removal S-TR04-01': {'B1': 2660, 'B2': 2685, 'C1': 2680, 'C2': 2682},
                           '41 ALS Removal S-TR11-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '42 ALS Removal S-TR13-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '43 ALS Removal S-TR13-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '44 ALS Removal S-TR13-03': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '45 ALS Removal S-TR13-04': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '46 ALS Removal S-TR14-01': {'B1': 2658, 'B2': 2683, 'C1': 2678, 'C2': 2680},
                           '47 ALS Removal S-TR14-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '48 ALS Removal S-TR14-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '49 ALS Removal S-TR14-04': {'B1': 2660, 'B2': 2685, 'C1': 2680, 'C2': 2682},
                           '5 ALS Removal P-TR01b-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '50 ALS Removal S-TR01-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '51 ALS Removal S-TR01-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '52 ALS Removal S-TR01a-05': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '53 ALS Removal S-TR01b-05': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '54 ALS Removal S-TR02-03': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '55 ALS Removal S-TR02a-05': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '56 ALS Removal S-TR02b-05': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '57 ALS Removal S-TR04-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '58 ALS Removal S-TR05-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '59 ALS Removal S-TR06-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '6 ALS Removal P-TR02a-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '60 ALS Removal S-TR06-02': {'B1': 2663, 'B2': 2688, 'C1': 2683, 'C2': 2685},
                           '61 ALS Removal S-TR06-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '62 ALS Removal S-TR07-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '63 ALS Removal S-TR07-02': {'B1': 2663, 'B2': 2688, 'C1': 2683, 'C2': 2685},
                           '64 ALS Removal S-TR07-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '65 ALS Removal S-TR08-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '66 ALS Removal S-TR11-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '67 ALS Removal S-TR12-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '68 ALS Removal TR01a-04': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '69 ALS Removal TR01b-04': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '7 ALS Removal P-TR02a-02': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '70 ALS Removal TR02a-04': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '71 ALS Removal TR02b-04': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '72 ALS Removal CHB1-T1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '73 ALS Removal CHB1-T2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '74 ALS Removal CHB1-T3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '75 ALS Removal CHB1-T4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '76 ALS Removal CHB1-B1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '77 ALS Removal CHB1-B2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '78 ALS Removal CHB1-B3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '79 ALS Removal CHB1-B4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '8 ALS Removal P-TR02a-03': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '80 ALS Removal CHB1-D1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '81 ALS Removal CHB1-D2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '82 ALS Removal CHB1-D3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '83 ALS Removal CHB1-D4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '84 ALS Removal CHB2-T1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '85 ALS Removal CHB2-T2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '86 ALS Removal CHB2-T3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '87 ALS Removal CHB2-T4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '88 ALS Removal CHB2-B1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '89 ALS Removal CHB2-B2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '9 ALS Removal P-TR02b-01': {'B1': 2662, 'B2': 2687, 'C1': 2682, 'C2': 2684},
                           '90 ALS Removal CHB2-B3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '91 ALS Removal CHB2-B4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '92 ALS Removal CHB2-D1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '93 ALS Removal CHB2-D2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '94 ALS Removal CHB2-D3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '95 ALS Removal CHB2-D4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '96 ALS Removal CHC2-T1': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '97 ALS Removal CHC2-T2': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '98 ALS Removal CHC2-T3': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686},
                           '99 ALS Removal CHC2-T4': {'B1': 2664, 'B2': 2689, 'C1': 2684, 'C2': 2686}}

B1_node_force_cos_ang_dict = {1811: cos(radians(315)), 1748: cos(radians(315)),
                              1742: cos(radians(225)), 1678: cos(radians(225)),
                              1670: cos(radians(135)), 1609: cos(radians(135)),
                              8059: cos(radians(45)), 1672: cos(radians(45))}

# The below needs to be updated
B1_als_node_force_cos_ang_dict = {1852: cos(radians(315)), 1788: cos(radians(315)),
                                  1782: cos(radians(225)), 1715: cos(radians(225)),
                                  1707: cos(radians(135)), 1644: cos(radians(135)),
                                  17761: cos(radians(45)), 1709: cos(radians(45))}

B1_node_force_sin_ang_dict = {1811: sin(radians(315)), 1748: sin(radians(315)),
                              1742: sin(radians(225)), 1678: sin(radians(225)),
                              1670: sin(radians(135)), 1609: sin(radians(135)),
                              8059: sin(radians(45)), 1672: sin(radians(45))}

# The below needs to be updated
B1_als_node_force_sin_ang_dict = {1782: sin(radians(225)), 1715: sin(radians(225)),
                                  1852: sin(radians(315)), 1788: sin(radians(315)),
                                  1707: sin(radians(135)), 1644: sin(radians(135)),
                                  17761: sin(radians(45)), 1709: sin(radians(45))}

B2_node_force_cos_ang_dict = {899: cos(radians(315)), 823: cos(radians(315)),
                              835: cos(radians(225)), 770: cos(radians(225)),
                              779: cos(radians(135)), 714: cos(radians(135)),
                              843: cos(radians(45)), 768: cos(radians(45))}

# The below needs to be updated
B2_als_node_force_cos_ang_dict = {931: cos(radians(315)), 21165: cos(radians(315)),
                                  867: cos(radians(225)), 794: cos(radians(225)),
                                  809: cos(radians(135)), 726: cos(radians(135)),
                                  875: cos(radians(45)), 791: cos(radians(45))}

B2_node_force_sin_ang_dict = {899: sin(radians(315)), 823: sin(radians(315)),
                              835: sin(radians(225)), 770: sin(radians(225)),
                              779: sin(radians(135)), 714: sin(radians(135)),
                              843: sin(radians(45)), 768: sin(radians(45))}

# The below needs to be updated
B2_als_node_force_sin_ang_dict = {931: sin(radians(315)), 21165: sin(radians(315)),
                                  867: sin(radians(225)), 794: sin(radians(225)),
                                  809: sin(radians(135)), 726: sin(radians(135)),
                                  875: sin(radians(45)), 791: sin(radians(45))}

C1_node_force_cos_ang_dict = {2723: cos(radians(315)), 2719: cos(radians(315)),
                              2721: cos(radians(225)), 2680: cos(radians(225)),
                              2690: cos(radians(135)), 2644: cos(radians(135)),
                              2726: cos(radians(45)), 2691: cos(radians(45))}

# The below needs to be updated
C1_als_node_force_cos_ang_dict = {2824: cos(radians(315)), 2790: cos(radians(315)),
                                  2792: cos(radians(225)), 2750: cos(radians(225)),
                                  2761: cos(radians(135)), 2706: cos(radians(135)),
                                  2797: cos(radians(45)), 21163: cos(radians(45))}

C1_node_force_sin_ang_dict = {2723: sin(radians(315)), 2719: sin(radians(315)),
                              2721: sin(radians(225)), 2680: sin(radians(225)),
                              2690: sin(radians(135)), 2644: sin(radians(135)),
                              2726: sin(radians(45)), 2691: sin(radians(45))}

# The below needs to be updated
C1_als_node_force_sin_ang_dict = {2824: sin(radians(315)), 2790: sin(radians(315)),
                                  2792: sin(radians(225)), 2750: sin(radians(225)),
                                  2761: sin(radians(135)), 2706: sin(radians(135)),
                                  2797: sin(radians(45)), 21163: sin(radians(45))}

C2_node_force_cos_ang_dict = {2140: cos(radians(315)), 2073: cos(radians(315)),
                              3058: cos(radians(225)), 2015: cos(radians(225)),
                              2028: cos(radians(135)), 1950: cos(radians(135)),
                              2094: cos(radians(45)), 2024: cos(radians(45))}

# The below needs to be updated
C2_als_node_force_cos_ang_dict = {2199: cos(radians(315)), 2131: cos(radians(315)),
                                  17744: cos(radians(225)), 2066: cos(radians(225)),
                                  2083: cos(radians(135)), 1993: cos(radians(135)),
                                  2153: cos(radians(45)), 2079: cos(radians(45))}

C2_node_force_sin_ang_dict = {2140: sin(radians(315)), 2073: sin(radians(315)),
                              3058: sin(radians(225)), 2015: sin(radians(225)),
                              2028: sin(radians(135)), 1950: sin(radians(135)),
                              2094: sin(radians(45)), 2024: sin(radians(45))}

# The below needs to be updated
C2_als_node_force_sin_ang_dict = {2199: sin(radians(315)), 2131: sin(radians(315)),
                                  17744: sin(radians(225)), 2066: sin(radians(225)),
                                  2083: sin(radians(135)), 1993: sin(radians(135)),
                                  2153: sin(radians(45)), 2079: sin(radians(45))}

node_cos_ang_dicts = {m: {} for m in bf_parq_files.keys()}
node_sin_ang_dicts = {m: {} for m in bf_parq_files.keys()}

for model in bp_parq_files.keys():
    if "ALS" in model:
        node_cos_ang_dicts[model]["B1"] = B1_als_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["B1"] = B1_als_node_force_sin_ang_dict

        node_cos_ang_dicts[model]["B2"] = B2_als_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["B2"] = B2_als_node_force_sin_ang_dict

        node_cos_ang_dicts[model]["C1"] = C1_als_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["C1"] = C1_als_node_force_sin_ang_dict

        node_cos_ang_dicts[model]["C2"] = C2_als_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["C2"] = C2_als_node_force_sin_ang_dict

    else:
        node_cos_ang_dicts[model]["B1"] = B1_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["B1"] = B1_node_force_sin_ang_dict

        node_cos_ang_dicts[model]["B2"] = B2_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["B2"] = B2_node_force_sin_ang_dict

        node_cos_ang_dicts[model]["C1"] = C1_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["C1"] = C1_node_force_sin_ang_dict

        node_cos_ang_dicts[model]["C2"] = C2_node_force_cos_ang_dict
        node_sin_ang_dicts[model]["C2"] = C2_node_force_sin_ang_dict


node_dict = {"B1": (1715, 1782, 1788, 1852, 1709, 17761, 1644, 1707),
             "B1_ALS": (1852, 1788, 1782, 1715, 1707, 1644, 17761, 1709),
             "B2": (794, 726, 791, 21153, 867, 809, 875, 931),
             "B2_ALS": (931, 21165, 867, 794, 809, 726, 875, 791),
             "C1": (2749, 2791, 2789, 2823, 21152, 2796, 2705, 2760),
             "C1_ALS": (2824, 2790, 2792, 2750, 2761, 2706, 2797, 21163),
             "C2": (2066, 17744, 2131, 2198, 2079, 2152, 1993, 2083),
             "C2_ALS": (2199, 2131, 17744, 2066, 2083, 1993, 2153, 2079)}

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
    "LB_Gmax": {"B1": (823, 825, 827, 828, 834, 835, 838, 839, 6278, 6324, 6328, 6549, 6580, 6602, 6613, 6614),
                "B2": (1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205, 6419, 6430, 6534, 6538, 6604, 6605, 6606, 6636),
                "C1": (719, 720, 721, 722, 747, 750, 751, 752, 6288, 6309, 6441, 6594, 6621, 6623, 6633, 6635),
                "C2": (911, 913, 914, 915, 997, 999, 1000, 1001, 6352, 6375, 6386, 6517, 6530, 6560, 6561, 6583)},
    "LB_Gmin": {"B1": (823, 825, 827, 828, 834, 835, 838, 839, 6278, 6324, 6328, 6549, 6580, 6602, 6613, 6614),
                "B2": (1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205, 6419, 6430, 6534, 6538, 6604, 6605, 6606, 6636),
                "C1": (719, 720, 721, 722, 747, 750, 751, 752, 6288, 6309, 6441, 6594, 6621, 6623, 6633, 6635),
                "C2": (911, 913, 914, 915, 997, 999, 1000, 1001, 6352, 6375, 6386, 6517, 6530, 6560, 6561, 6583)},
    "UB_Gmax": {"B1": (823, 825, 827, 828, 834, 835, 838, 839, 6278, 6324, 6328, 6549, 6580, 6602, 6613, 6614),
                "B2": (1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205, 6419, 6430, 6534, 6538, 6604, 6605, 6606, 6636),
                "C1": (719, 720, 721, 722, 747, 750, 751, 752, 6288, 6309, 6441, 6594, 6621, 6623, 6633, 6635),
                "C2": (911, 913, 914, 915, 997, 999, 1000, 1001, 6352, 6375, 6386, 6517, 6530, 6560, 6561, 6583)},
    "UB_Gmin": {"B1": (823, 825, 827, 828, 834, 835, 838, 839, 6278, 6324, 6328, 6549, 6580, 6602, 6613, 6614),
                "B2": (1097, 1101, 1104, 1105, 1197, 1203, 1204, 1205, 6419, 6430, 6534, 6538, 6604, 6605, 6606, 6636),
                "C1": (719, 720, 721, 722, 747, 750, 751, 752, 6288, 6309, 6441, 6594, 6621, 6623, 6633, 6635),
                "C2": (911, 913, 914, 915, 997, 999, 1000, 1001, 6352, 6375, 6386, 6517, 6530, 6560, 6561, 6583)}}

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
