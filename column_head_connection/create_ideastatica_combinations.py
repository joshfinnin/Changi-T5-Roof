
"""Script for generating the load combinations to be used in IDEA StatiCa.
Takes a series of load combinations and outputs the loads for each fictitious element."""

import duckdb
from column_head_connection.nodal_and_cruciform_reactions import get_direction_coefficients
from inputs import BF_EXT_ALS_PARQ_FILE_DICT, BP_EXT_ALS_PARQ_FILE_DICT, node_dict, result_cases_to_ignore, FULL_BEAM_FORCES_PARQUET, BEAM_ENDS_PARQUET, NODAL_FORCE_PARQUET, ordering_dicts
import csv


def get_set_of_combinations(combination_list: list[tuple]) -> list:
    """Function for returning the minimum set of combinations to check."""
    # Have applied the same result case filter to to the load effects before they get into IDEA StatiCa
    combination_list = [c for c in combination_list if c[0] not in result_cases_to_ignore]
    set_of_combinations = list(set(combination_list))
    set_of_combinations.sort(key=lambda x: int(x[0].split(":")[0].strip("'")))
    return set_of_combinations


def get_ordering_key(model: str, location: str):
    if "ALS" in model:
        return location + "_ALS"
    else:
        return location


headers = ["ResultCase", "Node", "ResultCaseName", "Model", "Combination",
           "N", "Vy", "Vz", "T", "Myy", "Mzz",
           "Vxy", "Vxz", "Vyz", "Mxy", "Mxz", "Myz",
           "Vxyz", "Mxyz", "IS Member"]


if __name__ == '__main__':
    
    # The below load combinations are to be entered manually from the studies on the worst combinations
    B1_target_combinations = [
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
        ("'1305: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF DT1) [2+3][M]'", "'UB_Gmax'"),
        ("'43: S2_Gmax + LL + Wind Y Pos Down + EHF DT1 [2+3][M]'", "'6 ALS Removal P-TR02a-01'"),
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
        ("'537: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (+ve) + EHF -X) [1b][M]'", "'UB_Gmax'"),
        ("'775: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF -X) [1b][M]'", "'UB_Gmax'"),
        ("'776: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF +Y) [1b][M]'", "'UB_Gmax'"),
        ("'1257: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF +X) [2+3][M]'", "'UB_Gmax'"),
        ("'17: S2_Gmax + LL + Wind X Pos Down + EHF +X [2+3][M]'", "'21 ALS Removal P-TR03b-05'"),
        ("'50: S2_Gmax + LL + Wind Y Neg Down + EHF -Y [2+3][M]'", "'55 ALS Removal S-TR02a-05'"),
        ("'709: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (+ve) + EHF -X) [2+3][M]'", "'UB_Gmin'"),
        ("'554: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (-ve) + EHF +TT) [1b][M]'", "'UB_Gmax'"),
        ("'556: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (-ve) + EHF DT1) [1b][M]'", "'LB_Gmax'"),
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
        ("'537: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (+ve) + EHF -X) [1b][M]'", "'UB_Gmax'"),
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
        ("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
        ("'43: S2_Gmax + LL + Wind Y Pos Down + EHF DT1 [2+3][M]'", "'6 ALS Removal P-TR02a-01'"),
        ("'9: S2_Gmax + LL + EHF +Y [2+3][M]'", "'6 ALS Removal P-TR02a-01'"),
        ("'1304: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF -TT) [2+3][M]'", "'LB_Gmax'"),
        ("'776: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF +Y) [1b][M]'", "'UB_Gmax'"),
        ("'8: S2_Gmax + LL + EHF -X [2+3][M]'", "'6 ALS Removal P-TR02a-01'"),
        ("'10: S2_Gmax + LL + EHF -Y [2+3][M]'", "'55 ALS Removal S-TR02a-05'"),
        ("'1257: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF +X) [2+3][M]'", "'UB_Gmax'"),
        ("'709: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (+ve) + EHF -X) [2+3][M]'", "'UB_Gmin'"),
        ("'1349: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF DT3) [2+3][M]'", "'LB_Gmax'"),
        ("'10: S2_Gmax + LL + EHF -Y [2+3][M]'", "'52 ALS Removal S-TR01a-05'"),
        ("'554: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (-ve) + EHF +TT) [1b][M]'", "'UB_Gmax'"),
        ("'556: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (-ve) + EHF DT1) [1b][M]'", "'LB_Gmax'"),
        ("'559: S1_Gmax + Ld(Wind Y Neg Down2) + Ac(LL + T (-ve) + EHF DT4) [1b][M]'", "'UB_Gmax'"),
        ("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
        ("'1261: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF +TT) [2+3][M]'", "'LB_Gmax'"),
        ("'738: S2_Gmin + Ld(Wind Y Pos Up) + Ac(T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmin'"),
        ("'1007: S2_Gmin + Ld(T (+ve)) + Ac(Wind 45 X Neg Y Neg + EHF -TT) [2+3][M]'", "'LB_Gmin'"),
        ("'1016: S2_Q [2+3][M]'", "'UB_Gmax'"),
        ("'1257: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF +X) [2+3][M]'", "'UB_Gmax'"),
        ("'1344: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF -Y) [2+3][M]'", "'UB_Gmax'"),
        ("'203: S1_Gmin + Ld(Wind Y Neg Up2) + Ac(T (+ve) + EHF -Y) [1b][M]'", "'UB_Gmin'"),
        ("'709: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (+ve) + EHF -X) [2+3][M]'", "'UB_Gmin'"),
        ("'738: S2_Gmin + Ld(Wind Y Pos Up) + Ac(T (+ve) + EHF +Y) [2+3][M]'", "'UB_Gmin'"),
        ("'10: S2_Gmax + LL + EHF -Y [2+3][M]'", "'70 ALS Removal TR02a-04'")]

    B2_target_combinations = [
        ("'1319: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF DT1) [2+3][M]'", "'LB_Gmax'"),
        ("'444: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF DT1) [1b][M]'", "'UB_Gmax'"),
        ("'719: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Pos Down2 + EHF -X) [1b][M]'", "'UB_Gmax'"),
        ("'720: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Pos Down2 + EHF +Y) [1b][M]'", "'LB_Gmax'"),
        ("'1266: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF DT4) [2+3][M]'", "'LB_Gmax'"),
        ("'858: S1_Gmax + Ld(T (-ve)) + Ac(LL + Wind X Pos Down2 + EHF +X) [1b][M]'", "'UB_Gmax'"),
        ("'1348: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF DT2) [2+3][M]'", "'LB_Gmax'"),
        ("'1348: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF DT2) [2+3][M]'", "'UB_Gmax'"),
        ("'446: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF DT3) [1b][M]'", "'UB_Gmax'"),
        ("'441: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF -Y) [1b][M]'", "'UB_Gmax'"),
        ("'54: S2_Gmax + LL + Wind Y Neg Down + EHF DT2 [2+3][M]'", "'71 ALS Removal TR02b-04'"),
        ("'1344: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1512: S2_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1599: S2_Gmax + Ld(T (-ve)) + Ac(LL + Wind X Neg Down + EHF DT1) [2+3][M]'", "'LB_Gmax'"),
        ("'724: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Pos Down2 + EHF DT1) [1b][M]'", "'LB_Gmax'"),
        ("'1322: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF DT4) [2+3][M]'", "'LB_Gmax'"),
        ("'444: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF DT1) [1b][M]'", "'UB_Gmax'"),
        ("'1345: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF +TT) [2+3][M]'", "'LB_Gmax'"),
        ("'1512: S2_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'10: S2_Gmax + LL + EHF -Y [2+3][M]'", "'8 ALS Removal P-TR02a-03'"),
        ("'1345: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF +TT) [2+3][M]'", "'LB_Gmax'"),
        ("'1348: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF DT2) [2+3][M]'", "'LB_Gmax'"),
        ("'50: S2_Gmax + LL + Wind Y Neg Down + EHF -Y [2+3][M]'", "'8 ALS Removal P-TR02a-03'"),
        ("'446: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF DT3) [1b][M]'", "'UB_Gmax'"),
        ("'441: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF -Y) [1b][M]'", "'LB_Gmax'"),
        ("'441: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF -Y) [1b][M]'", "'UB_Gmax'"),
        ("'54: S2_Gmax + LL + Wind Y Neg Down + EHF DT2 [2+3][M]'", "'71 ALS Removal TR02b-04'"),
        ("'1345: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF +TT) [2+3][M]'", "'LB_Gmax'"),
        ("'1512: S2_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1599: S2_Gmax + Ld(T (-ve)) + Ac(LL + Wind X Neg Down + EHF DT1) [2+3][M]'", "'LB_Gmax'"),
        ("'693: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind X Pos Down2 + EHF -Y) [1b][M]'", "'LB_Gmax'"),
        ("'1016: S2_Q [2+3][M]'", "'LB_Gmax'"),
        ("'1257: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF +X) [2+3][M]'", "'LB_Gmax'"),
        ("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1330: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1359: S2_Gmax + Ld(Wind 45 X Pos Y Pos) + Ac(LL + T (+ve) + EHF +TT) [2+3][M]'", "'LB_Gmax'"),
        ("'709: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (+ve) + EHF -X) [2+3][M]'", "'LB_Gmin'"),
        ("'839: S2_Gmin + Ld(Wind 45 X Neg Y Pos) + Ac(T (-ve) + EHF -TT) [2+3][M]'", "'LB_Gmin'"),
        ("'881: S2_Gmin + Ld(Wind 45 X Neg Y Neg) + Ac(T (+ve) + EHF -TT) [2+3][M]'", "'LB_Gmin'"),
        ("'442: S1_Gmax + Ld(Wind Y Pos Down2) + Ac(LL + T (-ve) + EHF +TT) [1b][M]'", "'UB_Gmax'"),
        ("'709: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (+ve) + EHF -X) [2+3][M]'", "'UB_Gmin'"),
        ("'752: S2_Gmin + Ld(Wind Y Pos Up) + Ac(T (-ve) + EHF +Y) [2+3][M]'", "'UB_Gmin'"),
        ("'22: S2_Gmax + LL + Wind X Pos Down + EHF -TT [2+3][M]'", "'45 ALS Removal S-TR13-04'")
    ]

    C1_target_combinations = [("'4: S1_Gmax + Ld(LL) + Ac(Wind X Pos Down1 + T (+ve) + EHF +X) [1b][M]'", "'UB_Gmax'"),
("'774: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF +X) [1b][M]'", "'UB_Gmax'"),
("'780: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF DT1) [1b][M]'", "'LB_Gmax'"),
("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
("'1306: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF DT2) [2+3][M]'", "'LB_Gmax'"),
("'1265: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (-ve) + EHF DT3) [2+3][M]'", "'UB_Gmax'"),
("'1320: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF DT2) [2+3][M]'", "'UB_Gmax'"),
("'200: S1_Gmax + Ld(LL) + Ac(Wind Y Neg Down2 + T (+ve) + EHF +X) [1b][M]'", "'UB_Gmax'"),
("'219: S1_Gmax + Ld(LL) + Ac(Wind Y Neg Down2 + T (-ve) + EHF -TT) [1b][M]'", "'LB_Gmax'"),
("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
("'1614: S2_Gmax + Ld(T (-ve)) + Ac(LL + Wind Y Pos Down + EHF DT2) [2+3][M]'", "'UB_Gmax'"),
("'203: S1_Gmin + Ld(Wind Y Neg Up2) + Ac(T (+ve) + EHF -Y) [1b][M]'", "'UB_Gmin'"),
("'1294: S2_Gmax + Ld(Wind X Neg Down) + Ac(LL + T (-ve) + EHF DT4) [2+3][M]'", "'UB_Gmax'"),
("'776: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF +Y) [1b][M]'", "'UB_Gmax'"),
("'1294: S2_Gmax + Ld(Wind X Neg Down) + Ac(LL + T (-ve) + EHF DT4) [2+3][M]'", "'UB_Gmax'"),
("'4: S1_Gmax + Ld(LL) + Ac(Wind X Pos Down1 + T (+ve) + EHF +X) [1b][M]'", "'UB_Gmax'"),
("'780: S1_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down2 + EHF DT1) [1b][M]'", "'LB_Gmax'"),
("'7: S2_Gmax + LL + EHF +X [2+3][M]'", "'17 ALS Removal P-TR03b-01'"),
("'1301: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
("'1306: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF DT2) [2+3][M]'", "'LB_Gmax'"),
("'17: S2_Gmax + LL + Wind X Pos Down + EHF +X [2+3][M]'", "'53 ALS Removal S-TR01b-05'"),
("'1320: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF DT2) [2+3][M]'", "'UB_Gmax'"),
("'219: S1_Gmax + Ld(LL) + Ac(Wind Y Neg Down2 + T (-ve) + EHF -TT) [1b][M]'", "'LB_Gmax'"),
("'222: S1_Gmax + Ld(LL) + Ac(Wind Y Neg Down2 + T (-ve) + EHF DT3) [1b][M]'", "'UB_Gmax'"),
("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
("'203: S1_Gmin + Ld(Wind Y Neg Up2) + Ac(T (+ve) + EHF -Y) [1b][M]'", "'UB_Gmin'"),
("'609: S1_Gmin + Ld(T (-ve)) + Ac(Wind Y Neg Up2 + EHF -Y) [1b][M]'", "'UB_Gmin'"),
("'9: S2_Gmax + LL + EHF +Y [2+3][M]'", "'3 ALS Removal P-TR01b-01'"),
("'1359: S2_Gmax + Ld(Wind 45 X Pos Y Pos) + Ac(LL + T (+ve) + EHF +TT) [2+3][M]'", "'LB_Gmax'"),
("'1444: S2_Gmax + Ld(Wind 45 X Neg Y Neg) + Ac(LL + T (+ve) + EHF -TT) [2+3][M]'", "'LB_Gmax'"),
("'217: S1_Gmin + Ld(Wind Y Neg Up2) + Ac(T (-ve) + EHF -Y) [1b][M]'", "'LB_Gmin'"),
("'738: S2_Gmin + Ld(Wind Y Pos Up) + Ac(T (+ve) + EHF +Y) [2+3][M]'", "'LB_Gmin'"),
("'4: S1_Gmax + Ld(LL) + Ac(Wind X Pos Down1 + T (+ve) + EHF +X) [1b][M]'", "'UB_Gmax'"),
("'9: S1_Gmax + Ld(LL) + Ac(Wind X Pos Down1 + T (+ve) + EHF -TT) [1b][M]'", "'UB_Gmax'"),
("'1016: S2_Q [2+3][M]'", "'UB_Gmax'"),
("'1344: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (-ve) + EHF -Y) [2+3][M]'", "'UB_Gmax'"),
("'723: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (-ve) + EHF -X) [2+3][M]'", "'UB_Gmin'"),
("'738: S2_Gmin + Ld(Wind Y Pos Up) + Ac(T (+ve) + EHF +Y) [2+3][M]'", "'UB_Gmin'"),
("'848: S2_Gmin + Ld(Wind 45 X Pos Y Neg) + Ac(T (+ve) + EHF +X) [2+3][M]'", "'UB_Gmin'"),
("'853: S2_Gmin + Ld(Wind 45 X Pos Y Neg) + Ac(T (+ve) + EHF -TT) [2+3][M]'", "'UB_Gmin'"),
("'10: S2_Gmax + LL + EHF -Y [2+3][M]'", "'32 ALS Removal P-TR04b-04'")
    ]

    C2_target_combinations = [
        ("'1243: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (+ve) + EHF +X) [2+3][M]'", "'LB_Gmax'"),
        ("'1330: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1335: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF DT3) [2+3][M]'", "'LB_Gmax'"),
        ("'17: S2_Gmax + LL + Wind X Pos Down + EHF +X [2+3][M]'", "'39 ALS Removal S-TR05-02'"),
        ("'1249: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (+ve) + EHF DT1) [2+3][M]'", "'UB_Gmax'"),
        ("'1308: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (+ve) + EHF DT4) [2+3][M]'", "'LB_Gmax'"),
        ("'1515: S2_Gmax + Ld(T (+ve)) + Ac(LL + Wind Y Neg Down + EHF DT1) [2+3][M]'", "'LB_Gmax'"),
        ("'1314: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF -X) [2+3][M]'", "'LB_Gmax'"),
        ("'53: S2_Gmax + LL + Wind Y Neg Down + EHF DT1 [2+3][M]'", "'5 ALS Removal P-TR01b-03'"),
        ("'1327: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF +X) [2+3][M]'", "'LB_Gmax'"),
        ("'1330: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1243: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (+ve) + EHF +X) [2+3][M]'", "'UB_Gmax'"),
        ("'1279: S2_Gmax + Ld(Wind X Neg Down) + Ac(LL + T (+ve) + EHF DT3) [2+3][M]'", "'LB_Gmax'"),
        ("'1330: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'17: S2_Gmax + LL + Wind X Pos Down + EHF +X [2+3][M]'", "'39 ALS Removal S-TR05-02'"),
        ("'50: S2_Gmax + LL + Wind Y Neg Down + EHF -Y [2+3][M]'", "'2 ALS Removal P-TR01a-03'"),
        ("'1249: S2_Gmax + Ld(Wind X Pos Down) + Ac(LL + T (+ve) + EHF DT1) [2+3][M]'", "'UB_Gmax'"),
        ("'50: S2_Gmax + LL + Wind Y Neg Down + EHF -Y [2+3][M]'", "'5 ALS Removal P-TR01b-03'"),
        ("'53: S2_Gmax + LL + Wind Y Neg Down + EHF DT1 [2+3][M]'", "'68 ALS Removal TR01a-04'"),
        ("'53: S2_Gmax + LL + Wind Y Neg Down + EHF DT1 [2+3][M]'", "'5 ALS Removal P-TR01b-03'"),
        ("'1330: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1016: S2_Q [2+3][M]'", "'LB_Gmax'"),
        ("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'LB_Gmax'"),
        ("'1330: S2_Gmax + Ld(Wind Y Neg Down) + Ac(LL + T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmax'"),
        ("'767: S2_Gmin + Ld(Wind Y Neg Up) + Ac(T (+ve) + EHF -Y) [2+3][M]'", "'LB_Gmin'"),
        ("'792: S2_Gmin + Ld(Wind 45 X Pos Y Pos) + Ac(T (+ve) + EHF +X) [2+3][M]'", "'LB_Gmin'"),
        ("'796: S2_Gmin + Ld(Wind 45 X Pos Y Pos) + Ac(T (+ve) + EHF +TT) [2+3][M]'", "'LB_Gmin'"),
        ("'50: S1_Gmax + Ld(LL) + Ac(Wind X Pos Down2 + T (-ve) + EHF +TT) [1b][M]'", "'UB_Gmax'"),
        ("'1016: S2_Q [2+3][M]'", "'UB_Gmax'"),
        ("'1315: S2_Gmax + Ld(Wind Y Pos Down) + Ac(LL + T (-ve) + EHF +Y) [2+3][M]'", "'UB_Gmax'"),
        ("'1355: S2_Gmax + Ld(Wind 45 X Pos Y Pos) + Ac(LL + T (+ve) + EHF +X) [2+3][M]'", "'UB_Gmax'"),
        ("'713: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (+ve) + EHF -TT) [2+3][M]'", "'UB_Gmin'"),
        ("'723: S2_Gmin + Ld(Wind X Neg Up) + Ac(T (-ve) + EHF -X) [2+3][M]'", "'UB_Gmin'"),
        ("'796: S2_Gmin + Ld(Wind 45 X Pos Y Pos) + Ac(T (+ve) + EHF +TT) [2+3][M]'", "'UB_Gmin'")
        ]

    target_combination_dict = {"B1": get_set_of_combinations(B1_target_combinations),
                               "B2": get_set_of_combinations(B2_target_combinations),
                               "C1": get_set_of_combinations(C1_target_combinations),
                               "C2": get_set_of_combinations(C2_target_combinations)}

    location = "B2"

    target_combinations = target_combination_dict[location]
    load_effect_indices = {loc.strip("'") + "_" + mdl.strip("'"): i for (loc, mdl), i in
                           zip(target_combinations, range(1, len(target_combinations) + 1))}

    with duckdb.connect() as conn:
        direction_coefficients = get_direction_coefficients(location, BP_EXT_ALS_PARQ_FILE_DICT)
        combination_string = ", ".join(f"({c}, {m})" for c, m in target_combinations)
        combination_filter_query = f"""SELECT * FROM (VALUES {combination_string}) AS COMBOS(ResultCaseName, Model)"""
        nodal_force_query = " UNION ALL ".join(f"""SELECT * FROM '{NODAL_FORCE_PARQUET}' 
        WHERE Node IN {node_dict[get_ordering_key(model, location)]} AND Model = '{model}'""" for model in BF_EXT_ALS_PARQ_FILE_DICT)

        query = f"""WITH FULL_BEAM_FORCES AS (SELECT * FROM '{FULL_BEAM_FORCES_PARQUET}'),
        BEAM_ENDS AS (SELECT * FROM '{BEAM_ENDS_PARQUET}'),
        NODAL_BEAM_FORCES AS ({nodal_force_query}),
        COMBINATIONS AS ({combination_filter_query}),
        COMBO_RESULTS AS
        (
        SELECT 
        Node,
        NF.ResultCaseName,
        NF.ResultCase,
        NF.Model,
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
        FROM NODAL_BEAM_FORCES AS NF
        JOIN COMBINATIONS AS COMB ON COMB.ResultCaseName = NF.ResultCaseName
        WHERE NF.ResultCaseName = COMB.ResultCaseName AND NF.Model = COMB.Model
        GROUP BY NF.Node, NF.Model, NF.ResultCaseName, NF.ResultCase),

        DIRECTION_COEFFICIENTS AS (SELECT * FROM (VALUES {direction_coefficients}) AS dc(Node, Model, cos_coeff, sin_coeff))

        SELECT
        ResultCase,
        COMBO_RESULTS.Node,
        ResultCaseName,
        COMBO_RESULTS.Model,
        concat_ws('_', ResultCaseName, COMBO_RESULTS.Model) AS Combination,
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
        JOIN DIRECTION_COEFFICIENTS AS DC ON DC.Node = COMBO_RESULTS.Node AND DC.Model = COMBO_RESULTS.Model
        ORDER BY ResultCase, COMBO_RESULTS.Model
        """

        results = conn.execute(query).fetchall()

        results.sort(key=lambda x: (load_effect_indices[x[4]], ordering_dicts[get_ordering_key(x[3], location)][x[1]][1]))

        print("\t".join(headers))
        for result in results:
            result = list(result)
            result[4] = load_effect_indices[result[4]]
            model = result[3]
            result.append(ordering_dicts[get_ordering_key(model, location)][result[1]][0])
            print("\t".join(str(r) for r in result))

        # with open(bf_parq, 'w+', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #     writer.writerow(headers)
        #     writer.writerows(results)

