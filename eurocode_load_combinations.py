
"""
eurocode_load_combinations.py

Module designed to generate the load combinations as required by EN 1990
"""

from itertools import product
from enum import Enum
from dataclasses import dataclass
from collections import OrderedDict


LOAD_CASE_DICT = {1: "1: SW_Self weight",
                  2: "2: SW_Connection allowance (min)",
                  3: "3: SW_Connection allowance (max)",
                  4: "4: [-]",
                  5: "5: SDL_Cladding (min)",
                  6: "6: SDL_Cladding (additional)",
                  7: "7: SDL_Services (min)",
                  8: "8: SDL_Services (additional)",
                  9: "9: [-]",
                  10: "10: LL_Roof",
                  11: "11: LL_Suspended Floors",
                  12: "12: LL_Ground Slab",
                  13: "13: LL_Rain",
                  14: "14: LL_Plant",
                  15: "15: Ws +X_Walls E",
                  16: "16: Ws +Y_Walls E",
                  17: "17: Ws -X_Walls E",
                  18: "18: Ws -Y_Walls E",
                  19: "19: Ws_Walls IP",
                  20: "20: Ws_Walls IS",
                  21: "21: [-]",
                  22: "22: Ws +X_Roof EP",
                  23: "23: Ws +X_Roof ES",
                  24: "24: Ws +Y_Roof EP",
                  25: "25: Ws +Y_Roof ES",
                  26: "26: Ws -X_Roof EP",
                  27: "27: Ws -X_Roof ES",
                  28: "28: Ws -Y_Roof EP",
                  29: "29: Ws -Y_Roof ES",
                  30: "30: Ws_Roof IP",
                  31: "31: Ws_Roof IS",
                  32: "32: Ws_Roof_Overhang DN",
                  33: "33: Ws_Roof_Overhang UP",
                  34: "34: [-]",
                  35: "35: T (+ve)",
                  36: "36: T (-ve)",
                  37: "37: [-]",
                  38: "38: [-]",
                  39: "39: [-]",
                  40: "40: [-]",
                  41: "41: EHF +X",
                  42: "42: EHF +Y",
                  43: "43: EHF -X",
                  44: "44: EHF -Y",
                  45: "45: EHF +TT",
                  46: "46: EHF -TT",
                  47: "47: [-]",
                  48: "48: [-]",
                  49: "49: [-]",
                  50: "50: W1xpos-R UP",
                  51: "51: W1xpos-R TP",
                  52: "52: W1xpos-R US",
                  53: "53: W1xpos-R TS",
                  54: "54: W1ypos-R UP",
                  55: "55: W1ypos-R TP",
                  56: "56: W1ypos-R US",
                  57: "57: W1ypos-R TS",
                  58: "58: W1xneg-R UP",
                  59: "59: W1xneg-R TP",
                  60: "60: W1xneg-R US",
                  61: "61: W1xneg-R TS",
                  62: "62: W1yneg-R UP",
                  63: "63: W1yneg-R TP",
                  64: "64: W1yneg-R US",
                  65: "65: W1yneg-R TS",
                  66: "66: [-]",
                  67: "67: [-]",
                  68: "68: [-]",
                  69: "69: [-]",
                  70: "70: W1xpos-W",
                  71: "71: W1ypos-W",
                  72: "72: W1xneg-W",
                  73: "73: W1yneg-W",
                  74: "74: EHF DT1",
                  75: "75: EHF DT2",
                  76: "76: EHF DT3",
                  77: "77: EHF DT4",
                  78: "78: BIF +X",
                  79: "79: BIF +Y",
                  80: "80: BIF -X",
                  81: "81: BIF -Y"}


class ActionType(Enum):
    PERMANENT_ACTION = 1
    VARIABLE_ACTION = 2


class VertDirectionTag(Enum):
    UP = 1
    DOWN = 2
    NA = 3

@dataclass
class FactorSet:
    restoring: float
    destabilizing_leading: float
    destabilizing_accompanying: float


class ComponentCase:
    def __init__(self, name: str, combination_factors: FactorSet):
        self.name = name
        self.combination_factors = combination_factors
        self.action_type = None
        self.action = None


class Direction:
    def __init__(self, name: str, component_cases: list[ComponentCase], direction_tag: VertDirectionTag):
        self.name = name
        self.component_cases = component_cases
        self.direction_tag = direction_tag


class Action:
    def __init__(self, name: str, action_type: ActionType, directions: list[Direction]):
        self.name = name
        self.action_type = action_type
        self.directions = directions

        # Make sure that each component, when added to the action, knows what the action is
        for direction in self.directions:
            for component in direction.component_cases:
                component.action_type = self.action_type
                component.action = self

    def __str__(self):
        action_string = f"{self.name}-{self.action_type}"
        return action_string

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.directions)


class CombinationCase:
    """This class represents an individual combination from Eurocode."""
    def __init__(self, permanent_direction: Direction, leading_direction: Direction,
                 accompanying_directions: list[Direction], stage_tag: str):
        self.permanent_direction = permanent_direction
        self.leading_direction = leading_direction
        self.accompanying_directions = accompanying_directions
        self.stage_tag = stage_tag
        self.name = self.__str__()

        # Unpack the directions so that the combination can access the individual component case info
        # Then add components to dictionaries for convenience
        self.permanent_case_dict = {}
        self.leading_case_dict = {}
        self.accompanying_case_dict = {}

        permanent_cases = [c for c in self.permanent_direction.component_cases]
        permanent_case_names = [c.name for c in permanent_cases]
        leading_cases = [c for c in self.leading_direction.component_cases]
        leading_case_names = [c.name for c in leading_cases]
        accompanying_cases = [c for accomp in self.accompanying_directions for c in accomp.component_cases]
        accompanying_case_names = [c.name for c in accompanying_cases]

        for case_name, case in zip(permanent_case_names, permanent_cases):
            self.permanent_case_dict[case_name] = case

        for case_name, case in zip(leading_case_names, leading_cases):
            self.leading_case_dict[case_name] = case

        for case_name, case in zip(accompanying_case_names, accompanying_cases):
            self.accompanying_case_dict[case_name] = case

    def get_combination_string(self):
        """Creates the text file input string for the Strand7 analysis model."""
        spacer = "      "
        factors = []
        for lc_number, lc_name in LOAD_CASE_DICT.items():
            # Handle permanent cases
            if lc_name in self.permanent_case_dict.keys():
                case = self.permanent_case_dict[lc_name]
                if case.action.name == "Gmin":
                    factors.append(case.combination_factors.restoring)
                else:
                    factors.append(case.combination_factors.destabilizing_leading)
            # Handle leading cases
            elif lc_name in self.leading_case_dict.keys():
                case = self.leading_case_dict[lc_name]
                factors.append(case.combination_factors.destabilizing_leading)
            # Handle accompanying cases
            elif lc_name in self.accompanying_case_dict.keys():
                case = self.accompanying_case_dict[lc_name]
                factors.append(case.combination_factors.destabilizing_accompanying)
            # Handle cases that don't appear to be any dict
            else:
                factors.append(0.0)

        factor_string = spacer.join([f"{factor:.14E}" for factor in factors])
        combination_string = f"{self.name}:    {factor_string}\n"
        return combination_string

    def __str__(self):
        """Generates a string to represent a combination.
        At the moment, this is just the short hand name of the combination."""
        combination_name = f"{self.stage_tag}{self.permanent_direction.name} + Ld({self.leading_direction.name}) + " \
                           f"Ac({' + '.join([ac.name for ac in self.accompanying_directions])})"
        return combination_name

    def __repr__(self):
        return f"CombinationObject: {self.__str__()}"


class CombinationFactory:
    """
    Class to produced the ULS load combinations from the base
    """
    def __init__(self, actions: list[Action], stage_tag: str):
        self.actions = actions
        self.stage_tag = stage_tag

    def get_uls_combinations(self) -> list[CombinationCase]:
        """Method for producing the load combinations for the MUC."""

        combinations = []

        # Separate out permanent and variable actions
        permanent_actions = [action for action in self.actions if action.action_type is ActionType.PERMANENT_ACTION]
        variable_actions = [action for action in self.actions if action.action_type is ActionType.VARIABLE_ACTION]

        # Iterate through the variable actions, treating each individual action as a leading action
        for lead_action in variable_actions:

            # All other actions are then accompanying actions
            accompanying_actions = [action for action in variable_actions if action != lead_action]

            # Then, iterate through each permanent direction
            for perm_action in permanent_actions:
                for perm_dir in perm_action.directions:

                    # Then each direction in leading
                    for lead_dir in lead_action.directions:

                        # Thne each direction in accompanying
                        for accomp_dir_set in product(*accompanying_actions):

                            # accompanying_actions = [Action(Wind), Action(Live), Action(Thermal)]
                            # We have a corresponding combination
                            combination = CombinationCase(perm_dir, lead_dir, list(accomp_dir_set), self.stage_tag)
                            combinations.append(combination)

        return combinations


if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # USER NOTES/INSTRUCTIONS
    # The following code has been developed to generate load combinations to
    # Eurocode for Strand7 in bulk.
    # 1. The component names should match exactly the individual load cases
    # from the Strand model (for consistency).
    # 2. These are used to generate ComponentCases using a FactorSet.  The
    # FactorSet is in essence the load factors stipulated by Eurocode A1.1,
    # A1.2, and A1.3 to be applied for the different roles in the
    # combinations.
    # 3. The ComponentCases can be linked to a single Direction, or
    # multiple Directions, each of which has a name and VertDirectionTag
    # 4. An Action can then be defined through a collection of Directions,
    # an ActionType, and a name.
    # 5. A series of Actions are provided to a CombinationFactory.
    # 6. The CombinationFactory then uses the Eurocode algorithm to
    # generate load combinations in bulk.
    # 7. These are then written to file, and a string represention printed
    # to the console.
    # The USER SHOULD ENSURE that the file path for the output .lcf file is
    # correct,component cases are correct, the directions are correct, the
    # actions are appropriately included, the factors are correct, and any
    # filtering at the end is appropriate to their needs.
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # DEFINE OUTPUT FILE PATH
    # ----------------------------------------------------------------------
    combination_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.9\Stage 2&3.lcf"

    # ----------------------------------------------------------------------
    # PERMANENT ACTIONS
    # ----------------------------------------------------------------------
    gmin_factor_set = FactorSet(1.0, 0.0, 0.0)
    gmin_component_names = ["1: SW_Self weight",
                            "2: SW_Connection allowance (min)",
                            "5: SDL_Cladding (min)"]
    gmin_components = [ComponentCase(c, gmin_factor_set) for c in gmin_component_names]
    gmin_direction = [Direction("Gmin", gmin_components, VertDirectionTag.NA)]
    GMIN_ACTION = Action("Gmin", ActionType.PERMANENT_ACTION, gmin_direction)

    gmax_factor_set = FactorSet(0.0, 1.35, 1.35)
    gmax_component_names = ["1: SW_Self weight",
                            "3: SW_Connection allowance (max)",
                            "5: SDL_Cladding (min)",
                            "6: SDL_Cladding (additional)",
                            "7: SDL_Services (min)",
                            "8: SDL_Services (additional)"]
    gmax_components = [ComponentCase(c, gmax_factor_set) for c in gmax_component_names]
    gmax_direction = [Direction("Gmax", gmax_components, VertDirectionTag.NA)]
    GMAX_ACTION = Action("Gmax", ActionType.PERMANENT_ACTION, gmax_direction)

    # ----------------------------------------------------------------------
    # WIND ACTIONS
    # ----------------------------------------------------------------------
    wind_orthogonal_factor_set = FactorSet(0.0, 1.5, 1.5 * 0.5)  # psi_0 factor of 0.5 from Table SS NA.A1.2(B)
    wind_45_factor_set = FactorSet(0.0, 1.5 * 0.7, 1.5 * 0.5 * 0.7)  # Same as above, but using 70% of each orthogonal

    # Stage 1 orthogonal wind up case names
    wind_s1_XPU1_component_names = ["50: W1xpos-R UP", "70: W1xpos-W"]
    wind_s1_XPU2_component_names = ["51: W1xpos-R TP", "70: W1xpos-W"]
    wind_s1_YPU1_component_names = ["54: W1ypos-R UP", "71: W1ypos-W"]
    wind_s1_YPU2_component_names = ["55: W1ypos-R TP", "71: W1ypos-W"]
    wind_s1_XNU1_component_names = ["58: W1xneg-R UP", "72: W1xneg-W"]
    wind_s1_XNU2_component_names = ["59: W1xneg-R TP", "72: W1xneg-W"]
    wind_s1_YNU1_component_names = ["62: W1yneg-R UP", "73: W1yneg-W"]
    wind_s1_YNU2_component_names = ["63: W1yneg-R TP", "73: W1yneg-W"]

    # Stage 1 orthogonal wind down case names
    wind_s1_XPD1_component_names = ["52: W1xpos-R US", "70: W1xpos-W"]
    wind_s1_XPD2_component_names = ["53: W1xpos-R TS", "70: W1xpos-W"]
    wind_s1_YPD1_component_names = ["56: W1ypos-R US", "71: W1ypos-W"]
    wind_s1_YPD2_component_names = ["57: W1ypos-R TS", "71: W1ypos-W"]
    wind_s1_XND1_component_names = ["60: W1xneg-R US", "72: W1xneg-W"]
    wind_s1_XND2_component_names = ["61: W1xneg-R TS", "72: W1xneg-W"]
    wind_s1_YND1_component_names = ["64: W1yneg-R US", "73: W1yneg-W"]
    wind_s1_YND2_component_names = ["65: W1yneg-R TS", "73: W1yneg-W"]

    # Stage 1 45 degree wind case names
    wind_s1_45_XPYP_component_names = ["70: W1xpos-W", "71: W1ypos-W"]
    wind_s1_45_XPYN_component_names = ["70: W1xpos-W", "73: W1yneg-W"]
    wind_s1_45_XNYP_component_names = ["72: W1xneg-W", "71: W1ypos-W"]
    wind_s1_45_XNYN_component_names = ["72: W1xneg-W", "73: W1yneg-W"]

    # Stage 2 orthogonal wind up case names
    wind_s2_XPU_component_names = ["15: Ws +X_Walls E", "19: Ws_Walls IP", "30: Ws_Roof IP", "22: Ws +X_Roof EP", "33: Ws_Roof_Overhang UP"]
    wind_s2_XNU_component_names = ["17: Ws -X_Walls E", "19: Ws_Walls IP", "30: Ws_Roof IP", "26: Ws -X_Roof EP", "33: Ws_Roof_Overhang UP"]
    wind_s2_YPU_component_names = ["16: Ws +Y_Walls E", "19: Ws_Walls IP", "30: Ws_Roof IP", "24: Ws +Y_Roof EP", "33: Ws_Roof_Overhang UP"]
    wind_s2_YNU_component_names = ["18: Ws -Y_Walls E", "19: Ws_Walls IP", "30: Ws_Roof IP", "28: Ws -Y_Roof EP", "33: Ws_Roof_Overhang UP"]

    # Stage 2 orthogonal wind down case names
    wind_s2_XPD_component_names = ["15: Ws +X_Walls E", "20: Ws_Walls IS", "31: Ws_Roof IS", "23: Ws +X_Roof ES", "32: Ws_Roof_Overhang DN"]
    wind_s2_XND_component_names = ["17: Ws -X_Walls E", "20: Ws_Walls IS", "31: Ws_Roof IS", "27: Ws -X_Roof ES", "32: Ws_Roof_Overhang DN"]
    wind_s2_YPD_component_names = ["16: Ws +Y_Walls E", "20: Ws_Walls IS", "31: Ws_Roof IS", "25: Ws +Y_Roof ES", "32: Ws_Roof_Overhang DN"]
    wind_s2_YND_component_names = ["18: Ws -Y_Walls E", "20: Ws_Walls IS", "31: Ws_Roof IS", "29: Ws -Y_Roof ES", "32: Ws_Roof_Overhang DN"]

    # Stage 2 45 degree wind case names
    wind_s2_45_XPYP_component_names = ["15: Ws +X_Walls E", "16: Ws +Y_Walls E", "19: Ws_Walls IP"]
    wind_s2_45_XNYP_component_names = ["17: Ws -X_Walls E", "16: Ws +Y_Walls E", "19: Ws_Walls IP"]
    wind_45_XPYN_component_names = ["15: Ws +X_Walls E", "18: Ws -Y_Walls E", "19: Ws_Walls IP"]
    wind_45_XNYN_component_names = ["17: Ws -X_Walls E", "18: Ws -Y_Walls E", "19: Ws_Walls IP"]

    # Stage 1 component cases
    wind_s1_XPU1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XPU1_component_names]
    wind_s1_XPU2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XPU2_component_names]
    wind_s1_YPU1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YPU1_component_names]
    wind_s1_YPU2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YPU2_component_names]
    wind_s1_XNU1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XNU1_component_names]
    wind_s1_XNU2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XNU2_component_names]
    wind_s1_YNU1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YNU1_component_names]
    wind_s1_YNU2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YNU2_component_names]

    wind_s1_XPD1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XPD1_component_names]
    wind_s1_XPD2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XPD2_component_names]
    wind_s1_YPD1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YPD1_component_names]
    wind_s1_YPD2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YPD2_component_names]
    wind_s1_XND1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XND1_component_names]
    wind_s1_XND2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_XND2_component_names]
    wind_s1_YND1_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YND1_component_names]
    wind_s1_YND2_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_YND2_component_names]

    wind_s1_45_XPYP_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_45_XPYP_component_names]
    wind_s1_45_XPYN_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_45_XPYN_component_names]
    wind_s1_45_XNYP_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_45_XNYP_component_names]
    wind_s1_45_XNYN_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s1_45_XNYN_component_names]

    # Stage 2 component cases
    wind_s2_XPU_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_XPU_component_names]
    wind_s2_XNU_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_XNU_component_names]
    wind_s2_YPU_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_YPU_component_names]
    wind_s2_YNU_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_YNU_component_names]

    wind_s2_XPD_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_XPD_component_names]
    wind_s2_XND_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_XND_component_names]
    wind_s2_YPD_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_YPD_component_names]
    wind_s2_YND_components = [ComponentCase(c, wind_orthogonal_factor_set) for c in wind_s2_YND_component_names]

    wind_s2_45_XPYP_components = [ComponentCase(c, wind_45_factor_set) for c in wind_s2_45_XPYP_component_names]
    wind_s2_45_XNYP_components = [ComponentCase(c, wind_45_factor_set) for c in wind_s2_45_XNYP_component_names]
    wind_s2_45_XPYN_components = [ComponentCase(c, wind_45_factor_set) for c in wind_45_XPYN_component_names]
    wind_s2_45_XNYN_components = [ComponentCase(c, wind_45_factor_set) for c in wind_45_XNYN_component_names]

    wind_stage1_directions = [Direction("Wind X Pos Up1", wind_s1_XPU1_components, VertDirectionTag.UP),
                              Direction("Wind X Pos Up2", wind_s1_XPU2_components, VertDirectionTag.UP),
                              Direction("Wind Y Pos Up1", wind_s1_YPU1_components, VertDirectionTag.UP),
                              Direction("Wind Y Pos Up2", wind_s1_YPU2_components, VertDirectionTag.UP),
                              Direction("Wind X Neg Up1", wind_s1_XNU1_components, VertDirectionTag.UP),
                              Direction("Wind X Neg Up2", wind_s1_XNU2_components, VertDirectionTag.UP),
                              Direction("Wind Y Neg Up1", wind_s1_YNU1_components, VertDirectionTag.UP),
                              Direction("Wind Y Neg Up2", wind_s1_YNU2_components, VertDirectionTag.UP),

                              Direction("Wind X Pos Down1", wind_s1_XPD1_components, VertDirectionTag.DOWN),
                              Direction("Wind X Pos Down2", wind_s1_XPD2_components, VertDirectionTag.DOWN),
                              Direction("Wind Y Pos Down1", wind_s1_YPD1_components, VertDirectionTag.DOWN),
                              Direction("Wind Y Pos Down2", wind_s1_YPD2_components, VertDirectionTag.DOWN),
                              Direction("Wind X Neg Down1", wind_s1_XND1_components, VertDirectionTag.DOWN),
                              Direction("Wind X Neg Down2", wind_s1_XND2_components, VertDirectionTag.DOWN),
                              Direction("Wind Y Neg Down1", wind_s1_YND1_components, VertDirectionTag.DOWN),
                              Direction("Wind Y Neg Down2", wind_s1_YND2_components, VertDirectionTag.DOWN),

                              Direction("Wind 45 X Pos Y Pos", wind_s1_45_XPYP_components, VertDirectionTag.NA),
                              Direction("Wind 45 X Pos Y Pos", wind_s1_45_XPYN_components, VertDirectionTag.NA),
                              Direction("Wind 45 X Neg Y Pos", wind_s1_45_XNYP_components, VertDirectionTag.NA),
                              Direction("Wind 45 X Neg Y Neg", wind_s1_45_XNYN_components, VertDirectionTag.NA)
                              ]

    wind_stage2_directions = [Direction("Wind X Pos Up", wind_s2_XPU_components, VertDirectionTag.UP),
                              Direction("Wind X Neg Up", wind_s2_XNU_components, VertDirectionTag.UP),
                              Direction("Wind Y Pos Up", wind_s2_YPU_components, VertDirectionTag.UP),
                              Direction("Wind Y Neg Up", wind_s2_YNU_components, VertDirectionTag.UP),
                              Direction("Wind X Pos Down", wind_s2_XPD_components, VertDirectionTag.DOWN),
                              Direction("Wind X Neg Down", wind_s2_XND_components, VertDirectionTag.DOWN),
                              Direction("Wind Y Pos Down", wind_s2_YPD_components, VertDirectionTag.DOWN),
                              Direction("Wind Y Neg Down", wind_s2_YND_components, VertDirectionTag.DOWN),
                              Direction("Wind 45 X Pos Y Pos", wind_s2_45_XPYP_components, VertDirectionTag.NA),
                              Direction("Wind 45 X Neg Y Pos", wind_s2_45_XNYP_components, VertDirectionTag.NA),
                              Direction("Wind 45 X Pos Y Neg", wind_s2_45_XPYN_components, VertDirectionTag.NA),
                              Direction("Wind 45 X Neg Y Neg", wind_s2_45_XNYN_components, VertDirectionTag.NA)]

    WIND_STAGE1_ACTION = Action("Wind Stage 1", ActionType.VARIABLE_ACTION, wind_stage1_directions)
    WIND_STAGE2_ACTION = Action("Wind Stage 2", ActionType.VARIABLE_ACTION, wind_stage2_directions)

    # ----------------------------------------------------------------------
    # LIVE ACTIONS
    # ----------------------------------------------------------------------
    live_factor_set = FactorSet(0.0, 1.5, 1.0)
    live_component_names = ["10: LL_Roof",
                            "11: LL_Suspended Floors",
                            "12: LL_Ground Slab",
                            "13: LL_Rain",
                            "14: LL_Plant"]
    live_components = [ComponentCase(c, live_factor_set) for c in live_component_names]
    live_directions = [Direction("LL", live_components, VertDirectionTag.DOWN)]
    LIVE_ACTION = Action("LL", ActionType.VARIABLE_ACTION, live_directions)

    # ----------------------------------------------------------------------
    # THERMAL ACTIONS
    # ----------------------------------------------------------------------
    thermal_factor_set = FactorSet(0.0, 1.5, 0.6)
    thermal_component_names = ["35: T (+ve)", "36: T (-ve)"]
    thermal_components = [ComponentCase(c, thermal_factor_set) for c in thermal_component_names]
    thermal_directions = [Direction(c.name.split(": ")[-1], [c], VertDirectionTag.NA) for c in thermal_components]
    THERMAL_ACTION = Action("Thermal", ActionType.VARIABLE_ACTION, thermal_directions)

    # ----------------------------------------------------------------------
    # EHF ACTIONS
    # ----------------------------------------------------------------------
    ehf_factor_set = FactorSet(1.0, 1.0, 1.0)
    ehf_component_names = ["41: EHF +X", "43: EHF -X",
                           "42: EHF +Y", "44: EHF -Y",
                           "45: EHF +TT", "46: EHF -TT",
                           "74: EHF DT1", "75: EHF DT2", "76: EHF DT3", "77: EHF DT4",
                           "78: BIF +X", "79: BIF +Y", "80: BIF -X", "81: BIF -Y"]

    ehf_components = [ComponentCase(c, ehf_factor_set) for c in ehf_component_names]
    ehf_directions = [Direction(c.name.split(": ")[-1], [c], VertDirectionTag.NA) for c in ehf_components]
    EHF_ACTION = Action("EHF", ActionType.VARIABLE_ACTION, ehf_directions)

    # ----------------------------------------------------------------------
    # GENERATE THE FULL LIST OF COMBINATIONS USING A COMBINATION FACTORY
    # ----------------------------------------------------------------------

    actions_stage1_up = [GMIN_ACTION, WIND_STAGE1_ACTION, THERMAL_ACTION, EHF_ACTION]
    actions_stage1_down = [GMAX_ACTION, LIVE_ACTION, WIND_STAGE1_ACTION, THERMAL_ACTION, EHF_ACTION]
    actions_stage2_up = [GMIN_ACTION, WIND_STAGE2_ACTION, THERMAL_ACTION, EHF_ACTION]
    actions_stage2_down = [GMAX_ACTION, LIVE_ACTION, WIND_STAGE2_ACTION, THERMAL_ACTION, EHF_ACTION]

    # ----------------------------------------------------------------------
    # USER INPUT REQUIRED HERE
    # ----------------------------------------------------------------------
    combo_factory = CombinationFactory(actions_stage1_down, stage_tag="S1_") # <--------  EDIT THIS LINE TO USE THE ACTION LIST
    vertical_filter = VertDirectionTag.UP  # <----------- FILTER SHOULD BE THE OPPOSITE OF THE ACTION SET (i.e. actions_stage1_down => VertDirectionTag.UP)

    with open(combination_fp, 'w+') as file:

        for combination in combo_factory.get_uls_combinations():
            # Ignore all cases where the leading action is an EHF
            if combination.leading_direction.component_cases[0].action.name == "EHF":
                continue

            # # For the time being, ignore all cases where the leading action is thermal
            # elif combination.leading_direction.component_cases[0].action.name:
            #     continue

            elif combination.leading_direction.direction_tag == vertical_filter:
                continue

            elif any(acc_dir.direction_tag == vertical_filter for acc_dir in combination.accompanying_directions):
                continue

            else:
                file.write(combination.get_combination_string())
                print(combination.name)

