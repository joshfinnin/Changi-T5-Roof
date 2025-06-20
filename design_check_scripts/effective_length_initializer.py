
"""
effective_length_initializer.py

Module for determining the effective lengths of the beams in the Strand7 model.
Uses the BeamJoiner class, and writes the effective length table to a CSV file.
"""

from Geometry.structural_geometry_mappers import BeamJoiner, Beam
from sqlite3 import *
from typing import Union
import csv

# 1, 2, 3, 4, 15, 16, and 66 within the _group_num_dict is redundant. Stair 03 and Stair 04 groups excluded.
_group_num_dict = {1: r'Leaf 03-07\03-07\1D\E9x Exhaust\E91 ExhaustSupport',
                   2: r'Leaf 03-07\03-07\1D\E9x Exhaust\E92 ExhaustVert',
                   3: r'Leaf 03-07\03-07\1D\E9x Exhaust\E93 ExhaustArc',
                   4: r'Leaf 03-07\03-07\1D\E9x Exhaust\E94 ExhaustBeam',
                   5: r'Leaf 03-07\03-07\1D\G01 PrimaryTop',
                   6: r'Leaf 03-07\03-07\1D\G02 PrimaryBot',
                   7: r'Leaf 03-07\03-07\1D\G03 PrimaryDiag',
                   8: r'Leaf 03-07\03-07\1D\G04 PrimaryVert',
                   9: r'Leaf 03-07\03-07\1D\G05 SecondaryTop',
                   10: r'Leaf 03-07\03-07\1D\G06 SecondaryBot',
                   11: r'Leaf 03-07\03-07\1D\G07 SecondaryDiag',
                   12: r'Leaf 03-07\03-07\1D\G08 SecondaryVert',
                   13: r'Leaf 03-07\03-07\1D\G09 EdgeTrussTop',
                   14: r'Leaf 03-07\03-07\1D\G10 EdgeTrussBot',
                   15: r'Leaf 03-07\03-07\1D\G10x StairsPhase1a',
                   16: r'Leaf 03-07\03-07\1D\G10x StairsPhase1b',
                   17: r'Leaf 03-07\03-07\1D\G11 EdgeTrussDiag',
                   18: r'Leaf 03-07\03-07\1D\G12 EdgeTrussVert',
                   19: r'Leaf 03-07\03-07\1D\G23 PurlinTop',
                   20: r'Leaf 03-07\03-07\1D\G24 PurlinBot',
                   21: r'Leaf 03-07\03-07\1D\G25 BracingClipOnTop',
                   22: r'Leaf 03-07\03-07\1D\G26 BracingClipOnBot',
                   23: r'Leaf 03-07\03-07\1D\G27 BracingPlanTop',
                   24: r'Leaf 03-07\03-07\1D\G28 BracingPlanBot',
                   25: r'Leaf 03-07\03-07\1D\G29 ClipOnEdge',
                   26: r'Leaf 03-07\03-07\1D\G30 ClipOnVert',
                   27: r'Leaf 03-07\03-07\1D\G31 ClipOnTop',
                   28: r'Leaf 03-07\03-07\1D\G32 ClipOnBot',
                   29: r'Leaf 03-07\03-07\1D\G33 ClipOnDiag',
                   30: r'Leaf 03-07\03-07\1D\G41 FacadeBot',
                   31: r'Leaf 03-07\03-07\1D\G43 ColumnHeadExt',
                   32: r'Leaf 03-07\03-07\1D\G44 ColHeadDiag',
                   33: r'Leaf 03-07\03-07\1D\G45 ColHeadVert',
                   34: r'Leaf 03-07\03-07\1D\G60 RooflightPrimary',
                   35: r'Leaf 03-07\03-07\1D\G61 RooflightSecondary',
                   36: r'Leaf 03-07\03-07\1D\G62 RooflightTertiary',
                   37: r'Leaf 03-07\03-07\1D\G63 RooflightUpstand',
                   38: r'Leaf 03-07\03-07\1D\G69 PileCap',
                   39: r'Leaf 03-07\03-07\1D\G7x Column\G70 ColumnBaseExt',
                   40: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-1',
                   41: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-2',
                   42: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-3',
                   43: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-4',
                   44: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-5',
                   45: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-6',
                   46: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-7',
                   47: r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-8',
                   48: r'Leaf 03-07\03-07\1D\G80 EdgeArm',
                   49: r'Leaf 03-07\03-07\1D\G81 EdgeOuter',
                   50: r'Leaf 03-07\03-07\1D\G82 Outrigger',
                   51: r'Leaf 03-07\03-07\1D\G83 EdgePurlinTop',
                   52: r'Leaf 03-07\03-07\1D\G84 EdgePurlinBot',
                   53: r'Leaf 03-07\03-07\1D\G87 EdgeGutter',
                   54: r'Leaf 03-07\03-07\1D\G88 CatWalkStringer',
                   55: r'Leaf 03-07\03-07\1D\G89 LiftingBeam',
                   56: r'Leaf 03-07\03-07\Facade\FacadeMullionA',
                   57: r'Leaf 03-07\03-07\Facade\FacadeMullionB',
                   58: r'Leaf 03-07\03-07\Facade\FacadeMullionC',
                   59: r'Leaf 03-07\03-07\Facade\FacadeMullionD',
                   60: r'Leaf 03-07\03-07\Facade\FacadeTransomA',
                   61: r'Leaf 03-07\03-07\Facade\FacadeTransomB',
                   62: r'Leaf 03-07\03-07\Facade\FacadeTransomC',
                   63: r'Leaf 03-07\03-07\Facade\G40 FacadeHeader',
                   64: r'Leaf 03-07\03-07\Facade\G50 ClerestoryMullion',
                   65: r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\2D_ExhaustPanels',
                   66: r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\G90_ExhaustDummy',
                   67: r'Leaf 03-07\03-08\1D\3809 G69 Ground beams',
                   68: r'Leaf 03-07\03-08\1D\3809 QL_G09 EdgeTrussTop',
                   69: r'Leaf 03-07\03-08\1D\3810 QL_G10 EdgeTrussBot',
                   70: r'Leaf 03-07\03-08\1D\3811 QL_G11 EdgeTrussDiag',
                   71: r'Leaf 03-07\03-08\1D\3812 QL_G12 EdgeTrussVert',
                   72: r'Leaf 03-07\03-08\1D\3822 QL_G22 QLRoofSecondaryClerestory',
                   73: r'Leaf 03-07\03-08\1D\3823 QL_G23 QLRoofPurlin',
                   74: r'Leaf 03-07\03-08\1D\3829 QL_G29 ClipOnEdge',
                   75: r'Leaf 03-07\03-08\1D\3831 QL_G31 ClipOnTop',
                   76: r'Leaf 03-07\03-08\1D\3874 QL_G70 QLColumn',
                   77: r'Leaf 03-07\03-08\1D\3887 QL_G87 EdgeGutter',
                   78: r'Leaf 03-07\03-08\1D\3890 QL_G90 QLRoofPrimary',
                   79: r'Leaf 03-07\03-08\1D\3891 QL_G91 QLRoofSecondary',
                   80: r'Leaf 03-07\03-08\1D\3892 QL_G92 QLRoofBracing',
                   81: r'Leaf 03-07\03-08\1D\3893 QL_G93 QLCeilingPrimary',
                   82: r'Leaf 03-07\03-08\1D\3894 QL_G94 QLCeilingSecondary',
                   83: r'Leaf 03-07\03-08\1D\3895 QL_G95 QLCeilingPortal',
                   84: r'Leaf 03-07\03-08\1D\3896 QL_G96 QLCeilingNoggings',
                   85: r'Leaf 03-07\03-08\1D\3897 QL_G97 QLCeilingBracing',
                   86: r'Leaf 03-07\03-08\1D\3898 QL_G98 QLVerticalBracing',
                   87: r'Leaf 03-07\03-08\1D\3899 QL_G99 QLClipOnExtension',
                   88: r'Leaf 03-07\03-08\Facade\3850 QL_G50 Clerestory',
                   89: r'Leaf 03-07\03-08\Facade\3851 QL_G51 Mullion Typical',
                   90: r'Leaf 03-07\03-08\Facade\3854 QL_G54 Mullion Glazed',
                   91: r'Leaf 03-07\03-07\1D\E9x Exhaust',}


_group_name_dict = {v: k for k, v in _group_num_dict.items()}


def bimap_group(g_key: Union[int, str]) -> Union[int, str]:
    """Implements a pseudo bimap for the group dictionaries"""
    global _group_num_dict, _group_name_dict

    if isinstance(g_key, int):
        group = _group_num_dict[g_key]
    else:
        group = _group_name_dict[g_key]

    return group


def get_groups_as_strings(groups: tuple[int, ...], own_group: str) -> tuple[str, ...]:
    """Takes the collection of integer group references and returns the equivalent group strings as a tuple."""
    # Need to take special care where the input contains a single other restraint group (don't ignore own group)
    groups_as_strings = list(bimap_group(num) if num != 0 else own_group for num in groups)

    # If the previous step has not inserted own_group, insert it here
    if groups[0] != 0:
        groups_as_strings.insert(0, own_group)

    groups_as_strings = tuple(groups_as_strings)
    return groups_as_strings


def get_beam_joining_geometry(cursor: Cursor, groups: tuple[str, ...]) -> list[dict]:
    """
    Creates the SQL query string for getting the relevant geometry for the
    BeamJoiner from the SQLite database.
    """

    query = f'''SELECT
    BeamNumber,
    node1.X AS X1,
    node1.Y AS Y1,
    node1.Z AS Z1,
    node2.X AS X2,
    node2.Y AS Y2,
    node2.Z AS Z2,
    PropertyName,
    GroupName
    FROM BeamProperties AS BP
    JOIN NodalCoordinates AS node1 ON node1.NodeNumber = BP.N1
    JOIN NodalCoordinates AS node2 ON node2.NodeNumber = BP.N2
    WHERE GroupName IN ("{'", "'.join(g for g in groups)}");'''

    geometry_results = [dict(r) for r in cursor.execute(query).fetchall()]

    return geometry_results


def get_system_length(beam_groups: list[list[Beam]]) -> dict:

    length_dict = {}
    for beam_group in beam_groups:
        system_length = sum(b.length for b in beam_group)
        for beam in beam_group:
            length_dict[beam.number] = system_length

    return length_dict


def rnd(f: float, precision=2):
    return round(f, precision)


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # FILE PATH INPUTS FOR THE STRAND DATABASES AND OUTPUT FILE
    # ----------------------------------------------------------------------

    strand_db_fp = r"C:\Users\lisa.lin\Mott MacDonald\MBC SAM Project Portal - Task 17 - Prototype\WIP\01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\V1_4_4_LB_Gmax.db"

    csv_fp = r"C:\Users\lisa.lin\Mott MacDonald\MBC SAM Project Portal - Task 17 - Prototype\WIP\01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.4\Effective_Lengths.csv"

    # ----------------------------------------------------------------------
    # DEFINES THE GROUPS THAT CAN BE USED FOR RESTRAINT OF ANOTHER GROUP FOR
    # EACH INDIVIDUAL GROUP IN EACH INDIVIDUAL AXIS
    # ----------------------------------------------------------------------

    MAJOR_AXIS_RESTRAINT_GROUPS_DICT = {r'Leaf 03-07\03-07\1D\E9x Exhaust\E91 ExhaustSupport': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust\E92 ExhaustVert': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust\E93 ExhaustArc': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust\E94 ExhaustBeam': (0,),
                                        r'Leaf 03-07\03-07\1D\G01 PrimaryTop': (7, 8, 33),
                                        r'Leaf 03-07\03-07\1D\G02 PrimaryBot': (7, 8, 33),
                                        r'Leaf 03-07\03-07\1D\G03 PrimaryDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G04 PrimaryVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G05 SecondaryTop': (5, 11, 12),
                                        r'Leaf 03-07\03-07\1D\G06 SecondaryBot': (6, 11, 12),
                                        r'Leaf 03-07\03-07\1D\G07 SecondaryDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G08 SecondaryVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G09 EdgeTrussTop': (5, 9),
                                        r'Leaf 03-07\03-07\1D\G10 EdgeTrussBot': (6, 10),
                                        r'Leaf 03-07\03-07\1D\G11 EdgeTrussDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G12 EdgeTrussVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G23 PurlinTop': (5, 9),
                                        r'Leaf 03-07\03-07\1D\G24 PurlinBot': (6, 10),
                                        r'Leaf 03-07\03-07\1D\G25 BracingClipOnTop': (0,),
                                        r'Leaf 03-07\03-07\1D\G26 BracingClipOnBot': (0,),
                                        r'Leaf 03-07\03-07\1D\G27 BracingPlanTop': (0,),
                                        r'Leaf 03-07\03-07\1D\G28 BracingPlanBot': (0,),
                                        r'Leaf 03-07\03-07\1D\G29 ClipOnEdge': (27,),
                                        r'Leaf 03-07\03-07\1D\G30 ClipOnVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G31 ClipOnTop': (26,29),
                                        r'Leaf 03-07\03-07\1D\G32 ClipOnBot': (26,29),
                                        r'Leaf 03-07\03-07\1D\G33 ClipOnDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G41 FacadeBot': (10,),
                                        r'Leaf 03-07\03-07\1D\G43 ColumnHeadExt': (0,),
                                        r'Leaf 03-07\03-07\1D\G44 ColHeadDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G45 ColHeadVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G60 RooflightPrimary': (0,),
                                        r'Leaf 03-07\03-07\1D\G61 RooflightSecondary': (34,),
                                        r'Leaf 03-07\03-07\1D\G62 RooflightTertiary': (34, 35),
                                        r'Leaf 03-07\03-07\1D\G63 RooflightUpstand': (0,),
                                        r'Leaf 03-07\03-07\1D\G69 PileCap': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G70 ColumnBaseExt': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-1': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-2': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-3': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-4': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-5': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-6': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-7': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-8': (0,),
                                        r'Leaf 03-07\03-07\1D\G80 EdgeArm': (0,),
                                        r'Leaf 03-07\03-07\1D\G81 EdgeOuter': (48,),
                                        r'Leaf 03-07\03-07\1D\G82 Outrigger': (0,),
                                        r'Leaf 03-07\03-07\1D\G83 EdgePurlinTop': (27,),
                                        r'Leaf 03-07\03-07\1D\G84 EdgePurlinBot': (28,),
                                        r'Leaf 03-07\03-07\1D\G87 EdgeGutter': (27,),
                                        r'Leaf 03-07\03-07\1D\G88 CatWalkStringer': (6, 10),
                                        r'Leaf 03-07\03-07\1D\G89 LiftingBeam': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionA': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionB': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionC': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionD': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeTransomA': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeTransomB': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeTransomC': (0,),
                                        r'Leaf 03-07\03-07\Facade\G40 FacadeHeaderA': (0,),
                                        r'Leaf 03-07\03-07\Facade\G50 ClerestoryMullion': (0,),
                                        r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\2D_ExhaustPanels': (0,),
                                        r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\G90_ExhaustDummy': (0,),
                                        r'Leaf 03-07\03-08\1D\3809 G69 Ground beams': (0,),
                                        r'Leaf 03-07\03-08\1D\3809 QL_G09 EdgeTrussTop': (78,),
                                        r'Leaf 03-07\03-08\1D\3810 QL_G10 EdgeTrussBot': (71, 76),
                                        r'Leaf 03-07\03-08\1D\3811 QL_G11 EdgeTrussDiag': (0,),
                                        r'Leaf 03-07\03-08\1D\3812 QL_G12 EdgeTrussVert': (0,),
                                        r'Leaf 03-07\03-08\1D\3822 QL_G22 QLRoofSecondaryClerestory': (78,),
                                        r'Leaf 03-07\03-08\1D\3823 QL_G23 QLRoofPurlin': (78,),
                                        r'Leaf 03-07\03-08\1D\3829 QL_G29 ClipOnEdge': (75,),
                                        r'Leaf 03-07\03-08\1D\3831 QL_G31 ClipOnTop': (78,),
                                        r'Leaf 03-07\03-08\1D\3874 QL_G70 QLColumn': (0,),
                                        r'Leaf 03-07\03-08\1D\3887 QL_G87 EdgeGutter': (75,),
                                        r'Leaf 03-07\03-08\1D\3890 QL_G90 QLRoofPrimary': (76,),
                                        r'Leaf 03-07\03-08\1D\3891 QL_G91 QLRoofSecondary': (78,),
                                        r'Leaf 03-07\03-08\1D\3892 QL_G92 QLRoofBracing': (0,),
                                        r'Leaf 03-07\03-08\1D\3893 QL_G93 QLCeilingPrimary': (76,),
                                        r'Leaf 03-07\03-08\1D\3894 QL_G94 QLCeilingSecondary': (81,),
                                        r'Leaf 03-07\03-08\1D\3895 QL_G95 QLCeilingPortal': (76,),
                                        r'Leaf 03-07\03-08\1D\3896 QL_G96 QLCeilingNoggings': (82, 83),
                                        r'Leaf 03-07\03-08\1D\3897 QL_G97 QLCeilingBracing': (0,),
                                        r'Leaf 03-07\03-08\1D\3898 QL_G98 QLVerticalBracing': (0,),
                                        r'Leaf 03-07\03-08\1D\3899 QL_G99 QLClipOnExtension': (0,),
                                        r'Leaf 03-07\03-08\Facade\3850 QL_G50 Clerestory': (0,),
                                        r'Leaf 03-07\03-08\Facade\3851 QL_G51 Mullion Typical': (0,),
                                        r'Leaf 03-07\03-08\Facade\3854 QL_G54 Mullion Glazed': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust': (9, 19),
                                        }

    MINOR_AXIS_RESTRAINT_GROUPS_DICT = {r'Leaf 03-07\03-07\1D\E9x Exhaust\E91 ExhaustSupport': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust\E92 ExhaustVert': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust\E93 ExhaustArc': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust\E94 ExhaustBeam': (0,),
                                        r'Leaf 03-07\03-07\1D\G01 PrimaryTop': (9, 23),
                                        r'Leaf 03-07\03-07\1D\G02 PrimaryBot': (10, 24),
                                        r'Leaf 03-07\03-07\1D\G03 PrimaryDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G04 PrimaryVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G05 SecondaryTop': (5,),
                                        r'Leaf 03-07\03-07\1D\G06 SecondaryBot': (6,),
                                        r'Leaf 03-07\03-07\1D\G07 SecondaryDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G08 SecondaryVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G09 EdgeTrussTop': (5, 9, 17, 18),
                                        r'Leaf 03-07\03-07\1D\G10 EdgeTrussBot': (6, 10, 17, 18),
                                        r'Leaf 03-07\03-07\1D\G11 EdgeTrussDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G12 EdgeTrussVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G23 PurlinTop': (5, 9, 23),
                                        r'Leaf 03-07\03-07\1D\G24 PurlinBot': (6, 10, 24),
                                        r'Leaf 03-07\03-07\1D\G25 BracingClipOnTop': (0,),
                                        r'Leaf 03-07\03-07\1D\G26 BracingClipOnBot': (0,),
                                        r'Leaf 03-07\03-07\1D\G27 BracingPlanTop': (0,),
                                        r'Leaf 03-07\03-07\1D\G28 BracingPlanBot': (0,),
                                        r'Leaf 03-07\03-07\1D\G29 ClipOnEdge': (27,),
                                        r'Leaf 03-07\03-07\1D\G30 ClipOnVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G31 ClipOnTop': (21,),
                                        r'Leaf 03-07\03-07\1D\G32 ClipOnBot': (22,),
                                        r'Leaf 03-07\03-07\1D\G33 ClipOnDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G41 FacadeBot': (10,),
                                        r'Leaf 03-07\03-07\1D\G43 ColumnHeadExt': (0,),
                                        r'Leaf 03-07\03-07\1D\G44 ColHeadDiag': (0,),
                                        r'Leaf 03-07\03-07\1D\G45 ColHeadVert': (0,),
                                        r'Leaf 03-07\03-07\1D\G60 RooflightPrimary': (0,),
                                        r'Leaf 03-07\03-07\1D\G61 RooflightSecondary': (34,),
                                        r'Leaf 03-07\03-07\1D\G62 RooflightTertiary': (34, 35),
                                        r'Leaf 03-07\03-07\1D\G63 RooflightUpstand': (0,),
                                        r'Leaf 03-07\03-07\1D\G69 PileCap': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G70 ColumnBaseExt': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-1': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-2': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-3': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-4': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-5': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-6': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-7': (0,),
                                        r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-8': (0,),
                                        r'Leaf 03-07\03-07\1D\G80 EdgeArm': (0,),
                                        r'Leaf 03-07\03-07\1D\G81 EdgeOuter': (48, 50),
                                        r'Leaf 03-07\03-07\1D\G82 Outrigger': (0,),
                                        r'Leaf 03-07\03-07\1D\G83 EdgePurlinTop': (27,),
                                        r'Leaf 03-07\03-07\1D\G84 EdgePurlinBot': (28,),
                                        r'Leaf 03-07\03-07\1D\G87 EdgeGutter': (27,),
                                        r'Leaf 03-07\03-07\1D\G88 CatWalkStringer': (6, 10),
                                        r'Leaf 03-07\03-07\1D\G89 LiftingBeam': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionA': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionB': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionC': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeMullionD': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeTransomA': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeTransomB': (0,),
                                        r'Leaf 03-07\03-07\Facade\FacadeTransomC': (0,),
                                        r'Leaf 03-07\03-07\Facade\G40 FacadeHeaderA': (0,),
                                        r'Leaf 03-07\03-07\Facade\G50 ClerestoryMullion': (0,),
                                        r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\2D_ExhaustPanels': (0,),
                                        r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\G90_ExhaustDummy': (0,),
                                        r'Leaf 03-07\03-08\1D\3809 G69 Ground beams': (0,),
                                        r'Leaf 03-07\03-08\1D\3809 QL_G09 EdgeTrussTop': (78, 70),
                                        r'Leaf 03-07\03-08\1D\3810 QL_G10 EdgeTrussBot': (70,),
                                        r'Leaf 03-07\03-08\1D\3811 QL_G11 EdgeTrussDiag': (0,),
                                        r'Leaf 03-07\03-08\1D\3812 QL_G12 EdgeTrussVert': (0,),
                                        r'Leaf 03-07\03-08\1D\3822 QL_G22 QLRoofSecondaryClerestory': (78,),
                                        r'Leaf 03-07\03-08\1D\3823 QL_G23 QLRoofPurlin': (78,),
                                        r'Leaf 03-07\03-08\1D\3829 QL_G29 ClipOnEdge': (75,),
                                        r'Leaf 03-07\03-08\1D\3831 QL_G31 ClipOnTop': (0,),
                                        r'Leaf 03-07\03-08\1D\3874 QL_G70 QLColumn': (0,),
                                        r'Leaf 03-07\03-08\1D\3887 QL_G87 EdgeGutter': (75,),
                                        r'Leaf 03-07\03-08\1D\3890 QL_G90 QLRoofPrimary': (76, 79, 80),
                                        r'Leaf 03-07\03-08\1D\3891 QL_G91 QLRoofSecondary': (78, 80),
                                        r'Leaf 03-07\03-08\1D\3892 QL_G92 QLRoofBracing': (0,),
                                        r'Leaf 03-07\03-08\1D\3893 QL_G93 QLCeilingPrimary': (76,),
                                        r'Leaf 03-07\03-08\1D\3894 QL_G94 QLCeilingSecondary': (81, 84, 85),
                                        r'Leaf 03-07\03-08\1D\3895 QL_G95 QLCeilingPortal': (81, 84, 85),
                                        r'Leaf 03-07\03-08\1D\3896 QL_G96 QLCeilingNoggings': (82, 83),
                                        r'Leaf 03-07\03-08\1D\3897 QL_G97 QLCeilingBracing': (0,),
                                        r'Leaf 03-07\03-08\1D\3898 QL_G98 QLVerticalBracing': (0,),
                                        r'Leaf 03-07\03-08\1D\3899 QL_G99 QLClipOnExtension': (0,),
                                        r'Leaf 03-07\03-08\Facade\3850 QL_G50 Clerestory': (0,),
                                        r'Leaf 03-07\03-08\Facade\3851 QL_G51 Mullion Typical': (0,),
                                        r'Leaf 03-07\03-08\Facade\3854 QL_G54 Mullion Glazed': (0,),
                                        r'Leaf 03-07\03-07\1D\E9x Exhaust': (9, 19),
                                        }

    TORSIONAL_AXIS_RESTRAINT_GROUPS_DICT = {r'Leaf 03-07\03-07\1D\E9x Exhaust\E91 ExhaustSupport': (0,),
                                            r'Leaf 03-07\03-07\1D\E9x Exhaust\E92 ExhaustVert': (0,),
                                            r'Leaf 03-07\03-07\1D\E9x Exhaust\E93 ExhaustArc': (0,),
                                            r'Leaf 03-07\03-07\1D\E9x Exhaust\E94 ExhaustBeam': (0,),
                                            r'Leaf 03-07\03-07\1D\G01 PrimaryTop': (9, 23),
                                            r'Leaf 03-07\03-07\1D\G02 PrimaryBot': (10, 24),
                                            r'Leaf 03-07\03-07\1D\G03 PrimaryDiag': (0,),
                                            r'Leaf 03-07\03-07\1D\G04 PrimaryVert': (0,),
                                            r'Leaf 03-07\03-07\1D\G05 SecondaryTop': (5,),
                                            r'Leaf 03-07\03-07\1D\G06 SecondaryBot': (6,),
                                            r'Leaf 03-07\03-07\1D\G07 SecondaryDiag': (0,),
                                            r'Leaf 03-07\03-07\1D\G08 SecondaryVert': (0,),
                                            r'Leaf 03-07\03-07\1D\G09 EdgeTrussTop': (5, 9, 17, 18),
                                            r'Leaf 03-07\03-07\1D\G10 EdgeTrussBot': (6, 10, 17, 18),
                                            r'Leaf 03-07\03-07\1D\G11 EdgeTrussDiag': (0,),
                                            r'Leaf 03-07\03-07\1D\G12 EdgeTrussVert': (0,),
                                            r'Leaf 03-07\03-07\1D\G23 PurlinTop': (5, 9, 23),
                                            r'Leaf 03-07\03-07\1D\G24 PurlinBot': (6, 10, 24),
                                            r'Leaf 03-07\03-07\1D\G25 BracingClipOnTop': (0,),
                                            r'Leaf 03-07\03-07\1D\G26 BracingClipOnBot': (0,),
                                            r'Leaf 03-07\03-07\1D\G27 BracingPlanTop': (0,),
                                            r'Leaf 03-07\03-07\1D\G28 BracingPlanBot': (0,),
                                            r'Leaf 03-07\03-07\1D\G29 ClipOnEdge': (27,),
                                            r'Leaf 03-07\03-07\1D\G30 ClipOnVert': (0,),
                                            r'Leaf 03-07\03-07\1D\G31 ClipOnTop': (21,),
                                            r'Leaf 03-07\03-07\1D\G32 ClipOnBot': (22,),
                                            r'Leaf 03-07\03-07\1D\G33 ClipOnDiag': (0,),
                                            r'Leaf 03-07\03-07\1D\G41 FacadeBot': (10,),
                                            r'Leaf 03-07\03-07\1D\G43 ColumnHeadExt': (0,),
                                            r'Leaf 03-07\03-07\1D\G44 ColHeadDiag': (0,),
                                            r'Leaf 03-07\03-07\1D\G45 ColHeadVert': (0,),
                                            r'Leaf 03-07\03-07\1D\G60 RooflightPrimary': (0,),
                                            r'Leaf 03-07\03-07\1D\G61 RooflightSecondary': (34,),
                                            r'Leaf 03-07\03-07\1D\G62 RooflightTertiary': (34, 35),
                                            r'Leaf 03-07\03-07\1D\G63 RooflightUpstand': (0,),
                                            r'Leaf 03-07\03-07\1D\G69 PileCap': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G70 ColumnBaseExt': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-1': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-2': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-3': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-4': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-5': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-6': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-7': (0,),
                                            r'Leaf 03-07\03-07\1D\G7x Column\G71 PrimaryColumn-8': (0,),
                                            r'Leaf 03-07\03-07\1D\G80 EdgeArm': (0,),
                                            r'Leaf 03-07\03-07\1D\G81 EdgeOuter': (48, 50),
                                            r'Leaf 03-07\03-07\1D\G82 Outrigger': (0,),
                                            r'Leaf 03-07\03-07\1D\G83 EdgePurlinTop': (27,),
                                            r'Leaf 03-07\03-07\1D\G84 EdgePurlinBot': (28,),
                                            r'Leaf 03-07\03-07\1D\G87 EdgeGutter': (27,),
                                            r'Leaf 03-07\03-07\1D\G88 CatWalkStringer': (6, 10),
                                            r'Leaf 03-07\03-07\1D\G89 LiftingBeam': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeMullionA': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeMullionB': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeMullionC': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeMullionD': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeTransomA': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeTransomB': (0,),
                                            r'Leaf 03-07\03-07\Facade\FacadeTransomC': (0,),
                                            r'Leaf 03-07\03-07\Facade\G40 FacadeHeaderA': (0,),
                                            r'Leaf 03-07\03-07\Facade\G50 ClerestoryMullion': (0,),
                                            r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\2D_ExhaustPanels': (0,),
                                            r'Leaf 03-07\03-07\Non-Structural\ExhaustHood\G90_ExhaustDummy': (0,),
                                            r'Leaf 03-07\03-08\1D\3809 G69 Ground beams': (0,),
                                            r'Leaf 03-07\03-08\1D\3809 QL_G09 EdgeTrussTop': (78, 70),
                                            r'Leaf 03-07\03-08\1D\3810 QL_G10 EdgeTrussBot': (70,),
                                            r'Leaf 03-07\03-08\1D\3811 QL_G11 EdgeTrussDiag': (0,),
                                            r'Leaf 03-07\03-08\1D\3812 QL_G12 EdgeTrussVert': (0,),
                                            r'Leaf 03-07\03-08\1D\3822 QL_G22 QLRoofSecondaryClerestory': (78,),
                                            r'Leaf 03-07\03-08\1D\3823 QL_G23 QLRoofPurlin': (78,),
                                            r'Leaf 03-07\03-08\1D\3829 QL_G29 ClipOnEdge': (75,),
                                            r'Leaf 03-07\03-08\1D\3831 QL_G31 ClipOnTop': (0,),
                                            r'Leaf 03-07\03-08\1D\3874 QL_G70 QLColumn': (0,),
                                            r'Leaf 03-07\03-08\1D\3887 QL_G87 EdgeGutter': (75,),
                                            r'Leaf 03-07\03-08\1D\3890 QL_G90 QLRoofPrimary': (76, 79, 80),
                                            r'Leaf 03-07\03-08\1D\3891 QL_G91 QLRoofSecondary': (78, 80),
                                            r'Leaf 03-07\03-08\1D\3892 QL_G92 QLRoofBracing': (0,),
                                            r'Leaf 03-07\03-08\1D\3893 QL_G93 QLCeilingPrimary': (76,),
                                            r'Leaf 03-07\03-08\1D\3894 QL_G94 QLCeilingSecondary': (81, 84, 85),
                                            r'Leaf 03-07\03-08\1D\3895 QL_G95 QLCeilingPortal': (81, 84, 85),
                                            r'Leaf 03-07\03-08\1D\3896 QL_G96 QLCeilingNoggings': (82, 83),
                                            r'Leaf 03-07\03-08\1D\3897 QL_G97 QLCeilingBracing': (0,),
                                            r'Leaf 03-07\03-08\1D\3898 QL_G98 QLVerticalBracing': (0,),
                                            r'Leaf 03-07\03-08\1D\3899 QL_G99 QLClipOnExtension': (0,),
                                            r'Leaf 03-07\03-08\Facade\3850 QL_G50 Clerestory': (0,),
                                            r'Leaf 03-07\03-08\Facade\3851 QL_G51 Mullion Typical': (0,),
                                            r'Leaf 03-07\03-08\Facade\3854 QL_G54 Mullion Glazed': (0,),
                                            r'Leaf 03-07\03-07\1D\E9x Exhaust': (9, 19),
                                            }

    # ----------------------------------------------------------------------
    # ACCESS THE SQLITE DATABASE TO GET THE GEOMETRY
    # ----------------------------------------------------------------------

    connection = connect(strand_db_fp)
    connection.row_factory = Row

    cursor = connection.cursor()

    # ----------------------------------------------------------------------
    # ITERATE THROUGH THE INPUTS AND WRITE THE EFFECTIVE LENGTHS FOR THE
    # DC LIGHTNING DESIGN RUNS TO A CSV
    # ----------------------------------------------------------------------

    with open(csv_fp, 'w+', newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write headers
        headers = ["BeamNumber", "GroupName", "L_crT", "L_cry", "L_crz", "L_c", "C_1", "C2", "z_g", "C_my", "C_mz", "C_mLT"]
        writer.writerow(headers)

        for group_name in MAJOR_AXIS_RESTRAINT_GROUPS_DICT.keys():
            # Get the group integers
            major_axis_restraint_groups = MAJOR_AXIS_RESTRAINT_GROUPS_DICT[group_name]
            minor_axis_restraint_groups = MINOR_AXIS_RESTRAINT_GROUPS_DICT[group_name]
            torsional_axis_restraint_groups = TORSIONAL_AXIS_RESTRAINT_GROUPS_DICT[group_name]

            # Get the equivalent string names
            major_axis_restraint_group_names = get_groups_as_strings(major_axis_restraint_groups, own_group=group_name)
            minor_axis_restraint_group_names = get_groups_as_strings(minor_axis_restraint_groups, own_group=group_name)
            torsional_axis_restraint_group_names = get_groups_as_strings(torsional_axis_restraint_groups, own_group=group_name)

            # Use these to query the database
            major_axis_geometry_data = get_beam_joining_geometry(cursor, major_axis_restraint_group_names)
            minor_axis_geometry_data = get_beam_joining_geometry(cursor, minor_axis_restraint_group_names)
            torsional_axis_geometry_data = get_beam_joining_geometry(cursor, torsional_axis_restraint_group_names)

            # With the geometry, use the BeamJoiner class to determine the effective lengths
            major_axis_beams = [
                Beam(d["BeamNumber"], (d["X1"], d["Y1"], d["Z1"]), (d["X2"], d["Y2"], d["Z2"]), d["PropertyName"],
                     group=d["GroupName"]) for d in major_axis_geometry_data]

            minor_axis_beams = [
                Beam(d["BeamNumber"], (d["X1"], d["Y1"], d["Z1"]), (d["X2"], d["Y2"], d["Z2"]), d["PropertyName"],
                     group=d["GroupName"]) for d in minor_axis_geometry_data]

            torsional_axis_beams = [
                Beam(d["BeamNumber"], (d["X1"], d["Y1"], d["Z1"]), (d["X2"], d["Y2"], d["Z2"]), d["PropertyName"],
                     group=d["GroupName"]) for d in torsional_axis_geometry_data]

            print("Forming beam joiner for major axis...")
            major_axis_beam_joiner = BeamJoiner(major_axis_beams, target_groups=(group_name,))
            print("Forming beam joiner for minor axis...")
            minor_axis_beam_joiner = BeamJoiner(minor_axis_beams, target_groups=(group_name,))
            print("Forming beam joiner for torsional axis...")
            torsional_axis_beam_joiner = BeamJoiner(torsional_axis_beams, target_groups=(group_name,))

            major_groups = major_axis_beam_joiner.beam_groups
            minor_groups = minor_axis_beam_joiner.beam_groups
            torsional_groups = torsional_axis_beam_joiner.beam_groups

            major_axis_length_dict = get_system_length(major_groups)
            minor_axis_length_dict = get_system_length(minor_groups)
            torsional_axis_length_dict = get_system_length(torsional_groups)

            for beam_number in major_axis_length_dict.keys():
                major_length = major_axis_length_dict[beam_number]
                minor_length = minor_axis_length_dict[beam_number]
                torsional_length = torsional_axis_length_dict[beam_number]
                writer.writerow([beam_number, group_name, torsional_length, major_length, minor_length, minor_length, 1, 0, 0, 1, 1, 1])


