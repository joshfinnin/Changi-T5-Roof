
"""
database_extraction.py

Module to extract the analysis results from a Strand7 model into a series of Parquet files.
"""

__version__ = "1.4.0"


import ctypes
import pathlib
from getpass import getuser
from dataclasses import dataclass
from enum import Enum
import logging
from typing import Callable, Iterable
import tkinter as tk
from tkinter import filedialog, messagebox
import pyarrow as pa
import pyarrow.parquet as pq
import St7API as St7
from St7API import kMaxStrLen


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

logger = logging.getLogger(__name__)

@dataclass(slots=True)
class ModelExtractionContext:
    """Class to encapsulate information about the model required for the extraction functions."""
    model_name: pathlib.Path
    result_file: pathlib.Path
    uID: ctypes.c_int
    load_cases: ctypes.c_int
    primary_combo_count: ctypes.c_int
    secondary_combo_count: ctypes.c_int
    directory: pathlib.Path


@dataclass(slots=True)
class ParquetSettings:
    label: str
    file_name: str
    schema: pa.Schema
    extractor: Callable[[ModelExtractionContext, "ParquetSettings"], Iterable]
    position_values: tuple = (0.0, 0.25, 0.5, 0.75, 1.0)


_PLATE_LOCAL_STRESS_SCHEMA = pa.schema([("Sxx", pa.float64()),
                                        ("Syy", pa.float64()),
                                        ("Szz", pa.float64()),
                                        ("Sxy", pa.float64()),
                                        ("Syz", pa.float64()),
                                        ("Sxz", pa.float64())])

_PLATE_DERIVED_STRESS_SCHEMA = pa.schema([("S11", pa.float64()),
                                          ("S22", pa.float64()),
                                          ("PrincipalAngle", pa.float64()),
                                          ("VonMises", pa.float64()),
                                          ("Tresca", pa.float64()),
                                          ("MohrCoulomb", pa.float64()),
                                          ("DruckerPrager", pa.float64()),
                                          ("YieldIndex", pa.float64()),
                                          ("MaxAbsPrincipal", pa.float64())])

_PLATE_PROPERTIES_SCHEMA = pa.schema([("PlateNumber", pa.int32()),
                                      ("PropertyName", pa.string()),
                                      ("PropertyType", pa.string()),
                                      ("ElementType", pa.string()),
                                      ("GroupName", pa.string()),
                                      ("PlateIDNumber", pa.int32()),
                                      ("Area", pa.float64()),
                                      ("N1", pa.int32()),
                                      ("N2", pa.int32()),
                                      ("N3", pa.int32()),
                                      ("N4", pa.int32())])

_PLATE_LOADING_SCHEMA = pa.schema([("PlateNumber", pa.int32()),
                                   ("LoadCase", pa.int32()),
                                   ("LoadCaseName", pa.string()),
                                   ("NormalZNegPressure", pa.float64()),
                                   ("NormalZPosPressure", pa.float64()),
                                   ("GlobalXNegPressure", pa.float64()),
                                   ("GlobalYNegPressure", pa.float64()),
                                   ("GlobalZNegPressure", pa.float64()),
                                   ("GlobalNegProjection", pa.string()),
                                   ("GlobalXPosPressure", pa.float64()),
                                   ("GlobalYPosPressure", pa.float64()),
                                   ("GlobalZPosPressure", pa.float64()),
                                   ("GlobalPosProjection", pa.string()),
                                   ("ShearXLocPressure", pa.float64()),
                                   ("ShearYLocPressure", pa.float64())])

_PLATE_NON_STRUCTURAL_MASS_SCHEMA = pa.schema([("LoadEntryID", pa.string()),
                                               ("PlateNumber", pa.int32()),
                                               ("LoadCase", pa.int32()),
                                               ("LoadCaseName", pa.string()),
                                               ("NSMass", pa.float64()),
                                               ("DynamicFactor", pa.float64()),
                                               ("OffsetVecX", pa.float64()),
                                               ("OffsetVecY", pa.float64()),
                                               ("OffsetVecZ", pa.float64())])

_BEAM_FORCE_SCHEMA = pa.schema([
    ("ResultId", pa.string()),
    ("BeamNumber", pa.int32()),
    ("ResultCase", pa.int32()),
    ("ResultCaseName", pa.string()),
    ("Position", pa.float64()),
    ("Fx", pa.float64()),
    ("Fy", pa.float64()),
    ("Fz", pa.float64()),
    ("Mx", pa.float64()),
    ("My", pa.float64()),
    ("Mz", pa.float64())
])

_BEAM_DISPLACEMENT_SCHEMA = pa.schema([("ResultId", pa.string()),
                                       ("BeamNumber", pa.int32()),
                                       ("ResultCase", pa.int32()),
                                       ("ResultCaseName", pa.string()),
                                       ("Position", pa.float64()),
                                       ("Ux", pa.float64()),
                                       ("Uy", pa.float64()),
                                       ("Uz", pa.float64())])

_BEAM_PROPERTIES_SCHEMA = pa.schema([
    ("BeamNumber", pa.int32()),
    ("N1", pa.int32()),
    ("N2", pa.int32()),
    ("Length", pa.float64()),
    ("PropertyName", pa.string()),
    ("GroupName", pa.string()),
    ("BeamIDNumber", pa.int32()),
    ("Dir1_X", pa.float64()),
    ("Dir1_Y", pa.float64()),
    ("Dir1_Z", pa.float64()),
    ("Dir2_X", pa.float64()),
    ("Dir2_Y", pa.float64()),
    ("Dir2_Z", pa.float64()),
    ("Dir3_X", pa.float64()),
    ("Dir3_Y", pa.float64()),
    ("Dir3_Z", pa.float64())
])

_BEAM_DISTRIBUTED_LOADING_SCHEMA = pa.schema([("LoadEntryID", pa.string()),
                                              ("LoadAxesType", pa.string()),
                                              ("BeamNumber", pa.int32()),
                                              ("LoadCase", pa.int32()),
                                              ("LoadCaseName", pa.string()),
                                              ("Axis", pa.int32()),
                                              ("LoadIDNumber", pa.int32()),
                                              ("LoadType", pa.string()),
                                              ("Projected", pa.bool8()),
                                              ("PA", pa.float64()),
                                              ("PB", pa.float64()),
                                              ("P1", pa.float64()),
                                              ("P2", pa.float64()),
                                              ("a", pa.float64()),
                                              ("b", pa.float64())])

_BEAM_NON_STRUCTURAL_MASS_SCHEMA = pa.schema([("LoadEntryID", pa.string()),
                                              ("BeamNumber", pa.int32()),
                                              ("LoadCase", pa.int32()),
                                              ("LoadCaseName", pa.string()),
                                              ("LoadIDNumber", pa.int32()),
                                              ("LoadType", pa.string()),
                                              ("PA", pa.float64()),
                                              ("PB", pa.float64()),
                                              ("P1", pa.float64()),
                                              ("P2", pa.float64()),
                                              ("a", pa.float64()),
                                              ("b", pa.float64()),
                                              ("DynamicFactor", pa.float64()),
                                              ("OffsetVecX", pa.float64()),
                                              ("OffsetVecY", pa.float64()),
                                              ("OffsetVecZ", pa.float64())])

_BEAM_POINT_LOADING_SCHEMA = pa.schema([("LoadEntryID", pa.string()),
                                        ("LoadAxesType", pa.string()),
                                        ("BeamNumber", pa.int32()),
                                        ("LoadCase", pa.int32()),
                                        ("LoadCaseName", pa.string()),
                                        ("LoadIDNumber", pa.int32()),
                                        ("Position", pa.float64()),
                                        ("PointLoadX", pa.float64()),
                                        ("PointLoadY", pa.float64()),
                                        ("PointLoadZ", pa.float64())])

_NODAL_REACTIONS_SCHEMA = pa.schema([
    ("ResultId", pa.string()),
    ("NodeNumber", pa.int32()),
    ("ResultCase", pa.int32()),
    ("ResultCaseName", pa.string()),
    ("Rx", pa.float64()),
    ("Ry", pa.float64()),
    ("Rz", pa.float64()),
    ("Rxx", pa.float64()),
    ("Ryy", pa.float64()),
    ("Rzz", pa.float64())
])

_NODAL_DISPLACEMENTS_SCHEMA = pa.schema([
    ("ResultId", pa.string()),
    ("NodeNumber", pa.int32()),
    ("ResultCase", pa.int32()),
    ("ResultCaseName", pa.string()),
    ("Dx", pa.float64()),
    ("Dy", pa.float64()),
    ("Dz", pa.float64()),
    ("Dxx", pa.float64()),
    ("Dyy", pa.float64()),
    ("Dzz", pa.float64())
])

_NODAL_COORDINATES_SCHEMA = pa.schema([
    ("NodeNumber", pa.int32()),
    ("X", pa.float64()),
    ("Y", pa.float64()),
    ("Z", pa.float64())
])

_NODAL_LOADING_SCHEMA = pa.schema([("LoadEntryID", pa.string()),
                                   ("NodeNumber", pa.int32()),
                                   ("LoadCase", pa.int32()),
                                   ("LoadCaseName", pa.string()),
                                   ("Px", pa.float64()),
                                   ("Py", pa.float64()),
                                   ("Pz", pa.float64())])

def _check_St7_error_message(err_code: int):
    if err_code == 0:
        return

    message = ctypes.create_string_buffer(kMaxStrLen)
    St7.St7GetAPIErrorString(err_code, message, St7.kMaxStrLen)
    if err_code in (10, 118):
        logger.warning(f"{err_code}: {message.value.decode()}")
        return

    else:
        logger.error(f"{err_code}: {message.value.decode()}")
        raise RuntimeError(message.value.decode())

def _clear_lists(lists_to_clear: list):
    """Convenience function for clearing lists."""
    for lst in lists_to_clear:
        lst.clear()

def _create_parq_table(writer: pq.ParquetWriter, lists_to_process: list, schema: pa.Schema):
    array = list(pa.array(data) for data in lists_to_process)
    table = pa.Table.from_arrays(array, schema=schema)
    writer.write_table(table)
    _clear_lists(lists_to_process)


# Initialize Strand7 model
def initialize_model(model_file: pathlib.Path, result_file: pathlib.Path, scratch_path: pathlib.Path):
    uID = ctypes.c_int(1)  # Unique identifier for the model
    _check_St7_error_message(St7.St7Init())
    p_combo_count = ctypes.c_int(0)
    s_combo_count = ctypes.c_int(0)
    try:  # This try block is essential for avoiding getting stuck if the API call fails
        _check_St7_error_message(St7.St7OpenFile(uID, model_file.__str__().encode('utf-8'), scratch_path.__str__().encode('utf-8')))
        logger.info("Model opened.")
        _check_St7_error_message(St7.St7OpenResultFile(uID, result_file.__str__().encode('utf-8'), None, St7.kUseExistingCombinations,
                                                       ctypes.byref(p_combo_count), ctypes.byref(s_combo_count)))
        logger.info("Results accessed.")
        logger.info(f"Primary combinations found: {p_combo_count.value}")
        logger.info(f"Secondary combinations found: {s_combo_count.value}")

        return uID, p_combo_count, s_combo_count

    except ValueError as ve:
        logger.error(ve)
        try:
            St7.St7CloseResultFile(uID)
            St7.St7CloseFile(uID)
            St7.St7Release()
        except Exception as e:
            logger.error(e)
            raise RuntimeError("Failed to close Strand7 model and results.")
        raise ValueError(f"A value error occurred. Likely to be caused by the file names used.") from ve

    except Exception as e:
        logger.error(e)
        try:
            St7.St7CloseResultFile(uID)
            St7.St7CloseFile(uID)
            St7.St7Release()
        except Exception as e:
            logger.error(e)
            raise RuntimeError("Failed to close Strand7 model and results.")
        raise RuntimeError("Failed to initialize Strand7 model and results.") from e


# Function to extract nodal reactions
def extract_nodal_reactions(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nNodes = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyNODE, ctypes.byref(nNodes)))

    number_of_cases = mctx.primary_combo_count.value + mctx.secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetResultCaseName(mctx.uID, case_number, case_name, St7.kMaxStrLen))

        case_name_string = str(case_name.value.decode())
        logger.info(f"Extracting node reactions for result case {case_name_string}...")

        reaction_array = ctypes.c_double * 6
        reactions = reaction_array()

        for node in range(1, nNodes.value + 1):

            _check_St7_error_message(St7.St7GetNodeResult(mctx.uID, St7.rtNodeReact, node, case_number, reactions))
            result_id = f"{node}-{case_number}"
            fx = float(reactions[0])
            fy = float(reactions[1])
            fz = float(reactions[2])
            mx = float(reactions[3])
            my = float(reactions[4])
            mz = float(reactions[5])

            result = (result_id, node, case_number, case_name_string, fx, fy, fz, mx, my, mz)

            yield result

    logger.info("Nodal reactions written to DB.")


# Function to extract nodal displacements
def extract_nodal_displacements(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nNodes = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyNODE, ctypes.byref(nNodes)))

    number_of_cases = mctx.primary_combo_count.value + mctx.secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetResultCaseName(mctx.uID, case_number, case_name, St7.kMaxStrLen))
        logger.info(f"Extracting node displacements for result case {case_name.value.decode()}...")

        for node in range(1, nNodes.value + 1):

            displacement_array = ctypes.c_double * 6
            displacements = displacement_array()

            _check_St7_error_message(St7.St7GetNodeResult(mctx.uID, St7.rtNodeDisp, node, case_number, displacements))
            result_id = f"{node}-{case_number}"
            dx = displacements[0]
            dy = displacements[1]
            dz = displacements[2]
            dxx = displacements[3]
            dyy = displacements[4]
            dzz = displacements[5]

            result = (result_id, node, case_number, case_name.value.decode(), dx, dy, dz, dxx, dyy, dzz)
            yield result


# Function to extract nodal coordinates
def extract_nodal_coordinates(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nNodes = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyNODE, ctypes.byref(nNodes)))

    logger.info("Extracting nodal coordinates...")

    node_coordinate_array = ctypes.c_double * 3
    node_coordinates = node_coordinate_array()

    for node in range(1, nNodes.value + 1):
        _check_St7_error_message(St7.St7GetNodeXYZ(mctx.uID, node, node_coordinates))

        x_coord = node_coordinates[0]
        y_coord = node_coordinates[1]
        z_coord = node_coordinates[2]

        result = (node, x_coord, y_coord, z_coord)

        yield result


# Function to extract the nodal loading
def extract_nodal_loading(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nNodes = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyNODE, ctypes.byref(nNodes)))

    logger.info("Extracting nodal loading...")

    for node in range(1, nNodes.value + 1):

        node_force_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyNODE, node, St7.aoForce, ctypes.byref(node_force_count)))

        node_force_entity_array = ctypes.c_int * (node_force_count.value * 4)
        node_force_entities = node_force_entity_array()

        _check_St7_error_message(St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyNODE, node, St7.aoForce, node_force_count, node_force_entities))

        for i in range(node_force_count.value):
            node_force_array = ctypes.c_double * 3
            node_forces = node_force_array()

            load_case = node_force_entities[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)

            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))
            _check_St7_error_message(St7.St7GetNodeForce3(mctx.uID, node, load_case, node_forces))

            px = node_forces[0]
            py = node_forces[1]
            pz = node_forces[2]
            sid = f"{node}-{load_case}"

            result = (sid, node, load_case, load_case_name.value.decode(), px, py, pz)

            yield result


# Function to extract beam attributes and properties
def extract_beam_properties(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nBeams = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyBEAM, ctypes.byref(nBeams)))

    logger.info("Extracting beam attributes and properties...")

    for beam in range(1, nBeams.value + 1):
        # Create an array to store the connection information
        connection_array = ctypes.c_int * St7.kMaxElementNode
        connections = connection_array()

        # Access the beam connection information
        _check_St7_error_message(St7.St7GetElementConnection(mctx.uID, St7.tyBEAM, beam, connections))

        # Access the beam id information
        id_number = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetBeamID(mctx.uID, beam, id_number))

        # Access the property associated with the beam
        property_number = ctypes.c_int(0)
        property_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetElementProperty(mctx.uID, St7.ptBEAMPROP, beam, ctypes.byref(property_number)))
        _check_St7_error_message(St7.St7GetPropertyName(mctx.uID, St7.ptBEAMPROP, property_number, property_name, St7.kMaxStrLen))

        # Access the group associated with the beam
        group_id = ctypes.c_int(0)
        group_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetEntityGroup(mctx.uID, St7.tyBEAM, beam, ctypes.byref(group_id)))
        _check_St7_error_message(St7.St7GetGroupIDName(mctx.uID, group_id, group_name, St7.kMaxStrLen))

        # Access the beam axes data
        axis_data = ctypes.c_double * 9
        axis_array = axis_data()

        _check_St7_error_message(St7.St7GetBeamAxisSystemInitial(mctx.uID, beam, axis_array))

        # Access the beam geometric data
        element_data = ctypes.c_double * 3
        element_data_array = element_data()

        _check_St7_error_message(St7.St7GetElementData(mctx.uID, St7.tyBEAM, beam, 0, element_data_array))

        node1 = connections[1]
        node2 = connections[2]
        length = element_data_array[0]
        dir1_x = axis_array[0]
        dir1_y = axis_array[1]
        dir1_z = axis_array[2]
        dir2_x = axis_array[3]
        dir2_y = axis_array[4]
        dir2_z = axis_array[5]
        dir3_x = axis_array[6]
        dir3_y = axis_array[7]
        dir3_z = axis_array[8]

        result = (beam, node1, node2, length, property_name.value.decode(),
                  group_name.value.decode(), id_number.value, dir1_x, dir1_y, dir1_z,
                  dir2_x, dir2_y, dir2_z, dir3_x, dir3_y, dir3_z)
        yield result


# Function to extract beam distributed loading, both global and principal
def extract_beam_distributed_loading(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nBeams = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyBEAM, ctypes.byref(nBeams)))

    logger.info(f"Extracting beam distributed loads...")

    for beam in range(1, nBeams.value + 1):

        # We need to access the number of different loads of a given type applied to a beam
        dist_principal_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyBEAM, beam, St7.aoBeamDLL,
                                               ctypes.byref(dist_principal_load_count)))

        load_entity_array = ctypes.c_int * (dist_principal_load_count.value * 4)
        load_entity_values = load_entity_array()

        # Once we have the number of loads, we can access information about each of the loads
        _check_St7_error_message(St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyBEAM, beam, St7.aoBeamDLL,
                                          dist_principal_load_count, load_entity_values))

        # Now that we have the information about the
        for i in range(dist_principal_load_count.value):
            axis = load_entity_values[(4 * i) + St7.ipAttrAxis]
            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)

            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))

            id_number = load_entity_values[(4 * i) + St7.ipAttrID]
            sid = f"{beam}-DLL-{load_case}-{id_number}"
            dl_type = ctypes.c_int(0)
            dl_value_array = ctypes.c_double * 6
            dl_values = dl_value_array()

            _check_St7_error_message(St7.St7GetBeamDistributedForcePrincipal6ID(mctx.uID, beam, axis, load_case,
                                                                                id_number, ctypes.byref(dl_type),
                                                                                dl_values))
            if dl_type.value == St7.dlConstant:
                dl_type = "Constant"
            elif dl_type.value == St7.dlLinear:
                dl_type = "Linear"
            elif dl_type.value == St7.dlTriangular:
                dl_type = "Triangular"
            elif dl_type.value == St7.dlThreePoint0:
                dl_type = "ThreePoint0"
            elif dl_type.value == St7.dlThreePoint1:
                dl_type = "ThreePoint1"
            elif dl_type.value == St7.dlTrapezoidal:
                dl_type = "Trapezoidal"
            else:
                raise ValueError(f"Load type not recognized for beam {beam}, load case {load_case}, load id {id_number}")

            projected = False

            pa = dl_values[0]
            pb = dl_values[1]
            p1 = dl_values[2]
            p2 = dl_values[3]
            a = dl_values[4]
            b = dl_values[5]

            result = (sid, "DistPrincipal", beam, load_case, load_case_name.value.decode(), axis, id_number, dl_type,
                      projected, pa, pb, p1, p2, a, b)
            yield result

        # Rinse and repeat the exercise for the global loads
        dist_global_load_count = ctypes.c_int(0)
        St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyBEAM, beam, St7.aoBeamDLG,
                                               ctypes.byref(dist_global_load_count))
        load_entity_array = ctypes.c_int * (dist_global_load_count.value * 4)
        load_entity_values = load_entity_array()

        St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyBEAM, beam, St7.aoBeamDLG,
                                          dist_global_load_count, load_entity_values)

        for i in range(dist_global_load_count.value):
            axis = load_entity_values[(4 * i) + St7.ipAttrAxis]
            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen)
            id_number = load_entity_values[(4 * i) + St7.ipAttrID]
            sid = f"{beam}-DLG-{load_case}-{id_number}"
            dl_type = ctypes.c_int(0)
            dl_value_array = ctypes.c_double * 6
            dl_values = dl_value_array()
            projected = ctypes.c_int(0)
            St7.St7GetBeamDistributedForceGlobal6ID(mctx.uID, beam, axis, load_case, id_number, ctypes.byref(projected),
                                                    ctypes.byref(dl_type), dl_values)
            if dl_type.value == St7.dlConstant:
                dl_type = "Constant"
            elif dl_type.value == St7.dlLinear:
                dl_type = "Linear"
            elif dl_type.value == St7.dlTriangular:
                dl_type = "Triangular"
            elif dl_type.value == St7.dlThreePoint0:
                dl_type = "ThreePoint0"
            elif dl_type.value == St7.dlThreePoint1:
                dl_type = "ThreePoint1"
            elif dl_type.value == St7.dlTrapezoidal:
                dl_type = "Trapezoidal"
            else:
                raise ValueError(f"Load type not recognized for beam {beam}, load case {load_case}, load id {id_number}")

            if projected.value == St7.bpProjected:
                projected = True
            else:
                projected = False

            pa = dl_values[0]
            pb = dl_values[1]
            p1 = dl_values[2]
            p2 = dl_values[3]
            a = dl_values[4]
            b = dl_values[5]

            result = (sid, "DistGlobal", beam, load_case, load_case_name.value.decode(), axis, id_number, dl_type,
                      projected, pa, pb, p1, p2, a, b)
            yield result


# Function to extract beam non-structural masses
def extract_beam_ns_mass_loading(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nBeams = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyBEAM, ctypes.byref(nBeams)))

    logger.info(f"Extracting beam non-structural masses...")

    for beam in range(1, nBeams.value + 1):

        # We need to access the number of different loads of a given type applied to a beam
        ns_mass_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyBEAM, beam, St7.aoBeamNSMass,
                                               ctypes.byref(ns_mass_load_count)))

        load_entity_array = ctypes.c_int * (ns_mass_load_count.value * 4)
        load_entity_values = load_entity_array()

        # Once we have the number of loads, we can access information about each of the loads
        _check_St7_error_message(St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyBEAM, beam, St7.aoBeamNSMass,
                                          ns_mass_load_count, load_entity_values))

        for i in range(ns_mass_load_count.value):
            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))
            id_number = load_entity_values[(4 * i) + St7.ipAttrID]
            ns_mass_type = ctypes.c_int(0)
            ns_mass_array = ctypes.c_double * 10
            ns_masses = ns_mass_array()
            _check_St7_error_message(St7.St7GetBeamNSMass10ID(mctx.uID, beam, load_case, id_number, ctypes.byref(ns_mass_type), ns_masses))

            if ns_mass_type.value == St7.dlConstant:
                ns_mass_type = "Constant"
            elif ns_mass_type.value == St7.dlLinear:
                ns_mass_type = "Linear"
            elif ns_mass_type.value == St7.dlTriangular:
                ns_mass_type = "Triangular"
            elif ns_mass_type.value == St7.dlThreePoint0:
                ns_mass_type = "ThreePoint0"
            elif ns_mass_type.value == St7.dlThreePoint1:
                ns_mass_type = "ThreePoint1"
            elif ns_mass_type.value == St7.dlTrapezoidal:
                ns_mass_type = "Trapezoidal"
            else:
                raise ValueError(f"Non-structural mass load type not recognized for beam {beam}, load case {load_case}, id {id_number}")

            pa = ns_masses[0]
            pb = ns_masses[1]
            p1 = ns_masses[2]
            p2 = ns_masses[3]
            a = ns_masses[4]
            b = ns_masses[5]

            dynamic_factor = ns_masses[6]
            offset_vec_x = ns_masses[7]
            offset_vec_y = ns_masses[8]
            offset_vec_z = ns_masses[9]

            sid = f"{beam}-NSM-{load_case}-{id_number}"

            result = (sid, beam, load_case, load_case_name.value.decode(), id_number, ns_mass_type,
                      pa, pb, p1, p2, a, b, dynamic_factor, offset_vec_x, offset_vec_y, offset_vec_z)

            yield result


# Function to extract beam point loading, both global and principal
def extract_beam_point_loading(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nBeams = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyBEAM, ctypes.byref(nBeams)))
    logger.info(f"Extracting beam point loads...")

    for beam in range(1, nBeams.value + 1):

        # Principal axis point load extraction
        point_principal_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyBEAM, beam, St7.aoBeamCFL,
                                               ctypes.byref(point_principal_load_count)))

        load_entity_array = ctypes.c_int * (point_principal_load_count.value * 4)
        load_entity_values = load_entity_array()

        _check_St7_error_message(St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyBEAM, beam, St7.aoBeamCFL,
                                          point_principal_load_count, load_entity_values))

        point_load_force_array = ctypes.c_double * 4
        point_load_forces = point_load_force_array()

        for i in range(point_principal_load_count.value):
            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))
            id_number = load_entity_values[(4 * i) + St7.ipAttrID]
            _check_St7_error_message(St7.St7GetBeamPointForcePrincipal4ID(mctx.uID, beam, load_case, id_number, point_load_forces))
            position = point_load_forces[3]
            point_load_x = point_load_forces[0]
            point_load_y = point_load_forces[1]
            point_load_z = point_load_forces[2]
            sid = f"{beam}-CFL-{load_case}-{id_number}"

            result = (sid, "Principal", beam, load_case, load_case_name.value.decode(), id_number,
                      position, point_load_x, point_load_y, point_load_z)

            yield result

        # Global axis point loads
        point_global_load_count = ctypes.c_int(0)
        St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyBEAM, beam, St7.aoBeamCFG,
                                               ctypes.byref(point_global_load_count))

        load_entity_array = ctypes.c_int * (point_global_load_count.value * 4)
        load_entity_values = load_entity_array()

        St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyBEAM, beam, St7.aoBeamCFG,
                                          point_global_load_count, load_entity_values)

        point_load_force_array = ctypes.c_double * 4
        point_load_forces = point_load_force_array()

        for i in range(point_global_load_count.value):
            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen)
            id_number = load_entity_values[(4 * i) + St7.ipAttrID]
            St7.St7GetBeamPointForceGlobal4ID(mctx.uID, beam, load_case, id_number, point_load_forces)
            position = point_load_forces[3]
            point_load_x = point_load_forces[0]
            point_load_y = point_load_forces[1]
            point_load_z = point_load_forces[2]
            sid = f"{beam}-CFG-{load_case}-{id_number}"

            result = (sid, "Global", beam, load_case, load_case_name.value.decode(), id_number,
                      position, point_load_x, point_load_y, point_load_z)

            yield result


# Function to extract the beam force results
def extract_beam_forces(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nBeams = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyBEAM, ctypes.byref(nBeams)))

    # The following ensures that the result positions are output as a ratio of the overall member length (0.0...1.0)
    _check_St7_error_message(St7.St7SetBeamResultPosMode(mctx.uID, St7.bpParam))

    number_of_cases = mctx.primary_combo_count.value + mctx.secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetResultCaseName(mctx.uID, case_number, case_name, St7.kMaxStrLen))
        logger.info(f"Extracting beam forces for result case {case_name.value.decode()}...")

        for beam in range(1, nBeams.value + 1):

            # Number of result columns (i.e. fields)
            number_columns = ctypes.c_int(0)

            force_array = ctypes.c_double * (len(pfs.position_values) * St7.kMaxBeamResult)
            forces = force_array()

            # Station positions along the element for querying loads
            position_values_c = [ctypes.c_double(p) for p in pfs.position_values]
            pos_array = ctypes.c_double * len(position_values_c)
            positions = pos_array(*position_values_c)

            # Get the beam results using the Strand API
            _check_St7_error_message(St7.St7GetBeamResultArrayPos(mctx.uID, St7.rtBeamForce, St7.stBeamPrincipal, beam, case_number,
                                         len(pfs.position_values), positions, ctypes.byref(number_columns), forces))

            # Access the forces from each beam at each station position, and add these to the result list
            for i in range(len(pfs.position_values)):
                position = f"{pfs.position_values[i]:.2f}"
                fx = forces[(i * 6) + St7.ipBeamAxialF]
                fy = forces[(i * 6) + St7.ipBeamSF1]
                fz = forces[(i * 6) + St7.ipBeamSF2]
                mx = forces[(i * 6) + St7.ipBeamTorque]
                my = forces[(i * 6) + St7.ipBeamBM2]
                mz = forces[(i * 6) + St7.ipBeamBM1]
                sid = f"{beam}-{case_number}-{position}"
                result = (sid, beam, case_number, case_name.value.decode(), float(position), fx, fy, fz, mx, my, mz)
                yield result


# Function to extract the beam displacement results
def extract_beam_displacements(mctx: ModelExtractionContext, pfs: ParquetSettings):
    nBeams = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyBEAM, ctypes.byref(nBeams)))

    # The following ensures that the result positions are output as a ratio of the overall member length (0.0...1.0)
    _check_St7_error_message(St7.St7SetBeamResultPosMode(mctx.uID, St7.bpParam))

    number_of_cases = mctx.primary_combo_count.value + mctx.secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetResultCaseName(mctx.uID, case_number, case_name, St7.kMaxStrLen))
        logger.info(f"Extracting beam displacements for result case {case_name.value.decode()}...")

        for beam in range(1, nBeams.value + 1):

            # Number of result columns (i.e. fields)
            number_columns = ctypes.c_int(0)

            disp_array = ctypes.c_double * (len(pfs.position_values) * St7.kMaxBeamResult)
            displacements = disp_array()

            # Station positions along the element for querying loads
            position_values_c = [ctypes.c_double(p) for p in pfs.position_values]
            pos_array = ctypes.c_double * len(position_values_c)
            positions = pos_array(*position_values_c)

            # Get the beam results using the Strand API
            _check_St7_error_message(St7.St7GetBeamResultArrayPos(mctx.uID, St7.rtBeamDisp, St7.stBeamGlobal, beam, case_number,
                                         len(pfs.position_values), positions, ctypes.byref(number_columns), displacements))

            # Access the forces from each beam at each station position, and add these to the result list
            for i in range(len(pfs.position_values)):
                position = pfs.position_values[i]
                ux = displacements[(i * 6) + 0]
                uy = displacements[(i * 6) + 1]
                uz = displacements[(i * 6) + 2]
                sid = f"{beam}-{case_number}-{position:.2f}"
                result = (sid, beam, case_number, case_name.value.decode(), position, ux, uy, uz)
                yield result


# Function to extract the plate attributes and properties
def extract_plate_properties(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nPlates = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyPLATE, ctypes.byref(nPlates)))

    logger.info("Extracting plate attributes and properties...")

    for plate in range(1, nPlates.value + 1):

        # Create an array to store the connection information
        connection_array = ctypes.c_int * St7.kMaxElementNode
        connections = connection_array()

        # Access the beam connection information
        _check_St7_error_message(St7.St7GetElementConnection(mctx.uID, St7.tyPLATE, plate, connections))

        # Access the plate id information
        id_number = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetPlateID(mctx.uID, plate, id_number))

        # Access the property associated with the plate
        property_number = ctypes.c_int(0)
        property_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        property_type = ctypes.c_int(0)
        material_type = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetElementProperty(mctx.uID, St7.ptPLATEPROP, plate, ctypes.byref(property_number)))
        _check_St7_error_message(St7.St7GetPropertyName(mctx.uID, St7.ptPLATEPROP, property_number, property_name, St7.kMaxStrLen))
        _check_St7_error_message(St7.St7GetPlatePropertyType(mctx.uID, property_number, ctypes.byref(property_type), ctypes.byref(material_type)))

        # Need to convert the plate property type to a string that is human interpretable
        if property_type.value == St7.ptNull:
            property_type = "None"
        elif property_type.value == St7.ptPlaneStress:
            property_type = "PlaneStress"
        elif property_type.value == St7.ptPlaneStrain:
            property_type = "PlaneStrain"
        elif property_type.value == St7.ptAxisymmetric:
            property_type = "Axisymmetric"
        elif property_type.value == St7.ptPlateShell:
            property_type = "PlateShell"
        elif property_type.value == St7.ptShearPanel:
            property_type = "ShearPanel"
        elif property_type.value == St7.ptMembrane:
            property_type = "Membrane"
        elif property_type.value == St7.ptLoadPatch:
            property_type = "LoadPatch"
        else:
            raise ValueError(f"Type of plate object is not recognized: plate number {plate}")

        # Access the group associated with the plate
        group_id = ctypes.c_int(0)
        group_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        _check_St7_error_message(St7.St7GetEntityGroup(mctx.uID, St7.tyPLATE, plate, ctypes.byref(group_id)))
        _check_St7_error_message(St7.St7GetGroupIDName(mctx.uID, group_id, group_name, St7.kMaxStrLen))

        # Access the plate geometric data
        element_data = ctypes.c_double * 1
        element_data_array = element_data()

        _check_St7_error_message(St7.St7GetElementData(mctx.uID, St7.tyPLATE, plate, 0, element_data_array))

        node_count = connections[0]
        n1 = connections[1]
        n2 = connections[2]
        n3 = connections[3]

        if node_count == 3:
            n4 = 0
            element_type = "TRI"
        else:
            n4 = connections[4]
            element_type = "QUAD"

        area = element_data_array[0]

        result = (plate, property_name.value.decode(), property_type, element_type, group_name.value.decode(),
                  id_number.value, area, n1, n2, n3, n4)

        yield result


# Function to extract the plate loading from the model
def extract_plate_loading(mctx: ModelExtractionContext, pfs: ParquetSettings):

    nPlates = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyPLATE, ctypes.byref(nPlates)))

    logger.info(f"Extracting plate loads...")

    for plate in range(1, nPlates.value + 1):

        plate_normal_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyPLATE, plate,
                                                                        St7.aoPlateFacePressure, ctypes.byref(plate_normal_load_count)))

        load_entity_array = ctypes.c_int * (plate_normal_load_count.value * 4)
        load_entity_values = load_entity_array()

        _check_St7_error_message(St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyPLATE, plate, St7.aoPlateFacePressure,
                                          plate_normal_load_count, load_entity_values))

        for i in range(plate_normal_load_count.value):

            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))

            # Get the plate normal loading
            norm_pressure_array = ctypes.c_double * 2
            norm_pressures = norm_pressure_array()
            _check_St7_error_message(St7.St7GetPlateNormalPressure2(mctx.uID, plate, load_case, norm_pressures))
            norm_neg_pressure = norm_pressures[0]
            norm_pos_pressure = norm_pressures[1]

            result = (plate, load_case, load_case_name.value.decode(),
                      norm_neg_pressure, norm_pos_pressure,
                      0.0, 0.0, 0.0, "None",
                      0.0, 0.0, 0.0, "None",
                      0.0, 0.0)

            yield result

        plate_global_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyPLATE, plate,
                                                                        St7.aoPlateGlobalPressure,
                                                                        ctypes.byref(plate_global_load_count)))

        load_entity_array = ctypes.c_int * (plate_global_load_count.value * 4)
        load_entity_values = load_entity_array()

        _check_St7_error_message(
            St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyPLATE, plate, St7.aoPlateGlobalPressure,
                                              plate_global_load_count, load_entity_values))

        for i in range(plate_global_load_count.value):

            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))

            # Get the plate global loading
            glob_pressure_array = ctypes.c_double * 3
            glob_pos_pressures = glob_pressure_array()
            glob_neg_pressures = glob_pressure_array()
            glob_neg_proj = ctypes.c_int(0)
            glob_pos_proj = ctypes.c_int(0)
            _check_St7_error_message(St7.St7GetPlateGlobalPressure3S(mctx.uID, plate, St7.psPlateMinusZ, load_case, ctypes.byref(glob_neg_proj), glob_neg_pressures))
            _check_St7_error_message(St7.St7GetPlateGlobalPressure3S(mctx.uID, plate, St7.psPlatePlusZ, load_case, ctypes.byref(glob_pos_proj), glob_pos_pressures))
            glob_neg_x_pressure = glob_neg_pressures[0]
            glob_neg_y_pressure = glob_neg_pressures[1]
            glob_neg_z_pressure = glob_neg_pressures[2]
            glob_pos_x_pressure = glob_pos_pressures[0]
            glob_pos_y_pressure = glob_pos_pressures[1]
            glob_pos_z_pressure = glob_pos_pressures[2]

            if glob_neg_proj.value == St7.ppProjResultant:
                glob_neg_proj = "Resultant"
            elif glob_neg_proj.value == St7.ppProjComponents:
                glob_neg_proj = "Components"
            else:
                glob_neg_proj = "None"

            if glob_pos_proj.value == St7.ppProjResultant:
                glob_pos_proj = "Resultant"
            elif glob_pos_proj.value == St7.ppProjComponents:
                glob_pos_proj = "Components"
            else:
                glob_pos_proj = "None"

            result = (plate, load_case, load_case_name.value.decode(),
                      0.0, 0.0,
                      glob_neg_x_pressure, glob_neg_y_pressure, glob_neg_z_pressure, glob_neg_proj,
                      glob_pos_x_pressure, glob_pos_y_pressure, glob_pos_z_pressure, glob_pos_proj,
                      0.0, 0.0)

            yield result

        plate_shear_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyPLATE, plate,
                                                                        St7.aoPlateFaceShear,
                                                                        ctypes.byref(plate_shear_load_count)))

        load_entity_array = ctypes.c_int * (plate_shear_load_count.value * 4)
        load_entity_values = load_entity_array()

        _check_St7_error_message(
            St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyPLATE, plate, St7.aoPlateFaceShear,
                                              plate_shear_load_count, load_entity_values))

        for i in range(plate_shear_load_count.value):
            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))

            # Get the plate shear loading
            shear_stress_array = ctypes.c_double * 2
            shear_stresses = shear_stress_array()
            _check_St7_error_message(St7.St7GetPlateShear2(mctx.uID, plate, load_case, shear_stresses))
            shear_stress_x = shear_stresses[0]
            shear_stress_y = shear_stresses[1]

            result = (plate, load_case, load_case_name.value.decode(),
                      0.0, 0.0,
                      0.0, 0.0, 0.0, "None",
                      0.0, 0.0, 0.0, "None",
                      shear_stress_x, shear_stress_y)

            yield result


# Function to extract the plate non-structural masses
def extract_plate_non_structural_mass(mctx: ModelExtractionContext, pfs: ParquetSettings):
    nPlates = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetTotal(mctx.uID, St7.tyPLATE, ctypes.byref(nPlates)))

    logger.info("Extracting plate non-structural masses...")

    for plate in range(1, nPlates.value + 1):

        plate_mass_load_count = ctypes.c_int(0)
        _check_St7_error_message(St7.St7GetEntityAttributeSequenceCount(mctx.uID, St7.tyPLATE, plate,
                                                                        St7.aoPlateNSMass, ctypes.byref(plate_mass_load_count)))

        load_entity_array = ctypes.c_int * (plate_mass_load_count.value * 4)
        load_entity_values = load_entity_array()

        _check_St7_error_message(St7.St7GetEntityAttributeSequence(mctx.uID, St7.tyPLATE, plate, St7.aoPlateNSMass,
                                          plate_mass_load_count, load_entity_values))



        for i in range(plate_mass_load_count.value):

            plate_ns_mass_array = ctypes.c_double * 6
            plate_ns_masses = plate_ns_mass_array()

            load_case = load_entity_values[(4 * i) + St7.ipAttrCase]
            load_case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            id_number = load_entity_values[(4 * i) + St7.ipAttrID]
            _check_St7_error_message(St7.St7GetLoadCaseName(mctx.uID, load_case, load_case_name, kMaxStrLen))

            _check_St7_error_message(St7.St7GetPlateNSMass5ID(mctx.uID, plate, load_case, id_number, plate_ns_masses))

            ns_mass = plate_ns_masses[0]
            dynamic_factor = plate_ns_masses[1]
            offset_vec_x = plate_ns_masses[2]
            offset_vec_y = plate_ns_masses[3]
            offset_vec_z = plate_ns_masses[4]

            sid = f"{plate}-NSM-{load_case}"

            result = (plate, load_case, load_case_name.value.decode(), ns_mass, dynamic_factor, offset_vec_x, offset_vec_y, offset_vec_z)

            yield result


# Function to extract the plate local stress results
def extract_plate_local_stresses(mctx: ModelExtractionContext, pfs: ParquetSettings):
    pass


# Function to extract the plate combined stress results
def extract_plate_combined_stresses(mctx: ModelExtractionContext, pfs: ParquetSettings):
    pass


# Main function for extracting results
def extract_model_data(model_file: pathlib.Path, result_file: pathlib.Path, scratch_path: pathlib.Path,
                       directory: pathlib.Path, output_options=None):

    # Initialize the Strand7 model
    init = initialize_model(model_file, result_file, scratch_path)
    uID, primary_combo_count, secondary_combo_count = init

    # Get the number of load cases
    load_case_count = ctypes.c_int(0)
    _check_St7_error_message(St7.St7GetNumLoadCase(uID, ctypes.byref(load_case_count)))

    model_context = ModelExtractionContext(model_file, result_file, uID, load_case_count, primary_combo_count,
                                           secondary_combo_count, directory)

    # Logic for creating the parquet files
    directory.mkdir(parents=True, exist_ok=True)

    if output_options is None:
        for rt in ResultType:
            parquet_insert(model_context, rt)

    else:
        for rt in ResultType:
            if output_options[rt.label]:
                parquet_insert(model_context, rt)

    # Close the Strand7 model
    _check_St7_error_message(St7.St7CloseResultFile(uID))
    _check_St7_error_message(St7.St7CloseFile(uID))
    _check_St7_error_message(St7.St7Release())


class ResultType(Enum):

    NODAL_COORDINATES = ParquetSettings("Nodal Coordinates",
                                        "nodal_coordinates.parquet",
                                        schema=_NODAL_COORDINATES_SCHEMA,
                                        extractor=extract_nodal_coordinates)

    NODAL_LOADING = ParquetSettings("Nodal Loading",
                                    "nodal_loading.parquet",
                                    schema=_NODAL_LOADING_SCHEMA,
                                    extractor=extract_nodal_loading)

    NODAL_REACTIONS = ParquetSettings("Nodal Reactions",
                                      "nodal_reactions.parquet",
                                      schema=_NODAL_REACTIONS_SCHEMA,
                                      extractor=extract_nodal_reactions)

    NODAL_DISPLACEMENTS = ParquetSettings("Nodal Displacements",
                                          "nodal_displacements.parquet",
                                          schema=_NODAL_DISPLACEMENTS_SCHEMA,
                                          extractor=extract_nodal_displacements)

    BEAM_PROPERTIES = ParquetSettings("Beam Properties",
                                      "beam_properties.parquet",
                                      schema=_BEAM_PROPERTIES_SCHEMA,
                                      extractor=extract_beam_properties)

    BEAM_DISTRIBUTED_LOADING = ParquetSettings("Beam Distributed Loading",
                                               "beam_distributed_loading.parquet",
                                               schema=_BEAM_DISTRIBUTED_LOADING_SCHEMA,
                                               extractor=extract_beam_distributed_loading)

    BEAM_NS_MASS_LOADING = ParquetSettings("Beam NS Mass Loading",
                                           "beam_ns_mass_loading.parquet",
                                           schema=_BEAM_NON_STRUCTURAL_MASS_SCHEMA,
                                           extractor=extract_beam_ns_mass_loading)

    BEAM_POINT_LOADING = ParquetSettings("Beam Point Loading",
                                         "beam_point_loading.parquet",
                                         schema=_BEAM_POINT_LOADING_SCHEMA,
                                         extractor=extract_beam_point_loading)

    BEAM_FORCES = ParquetSettings("Beam Forces",
                                  "beam_forces.parquet",
                                  schema=_BEAM_FORCE_SCHEMA,
                                  extractor=extract_beam_forces)

    BEAM_DISPLACEMENTS = ParquetSettings("Beam Displacements",
                                         "beam_displacements.parquet",
                                         schema=_BEAM_DISPLACEMENT_SCHEMA,
                                         extractor=extract_beam_displacements)

    PLATE_PROPERTIES = ParquetSettings("Plate Properties",
                                       "plate_properties.parquet",
                                       schema=_PLATE_PROPERTIES_SCHEMA,
                                       extractor=extract_plate_properties)

    PLATE_LOADING = ParquetSettings("Plate Loading",
                                    "plate_loading.parquet",
                                    schema=_PLATE_LOADING_SCHEMA,
                                    extractor=extract_plate_loading)

    PLATE_NS_MASS_LOADING = ParquetSettings("Plate NS Mass Loading",
                                            "plate_ns_mass_loading.parquet",
                                            schema=_PLATE_NON_STRUCTURAL_MASS_SCHEMA,
                                            extractor=extract_plate_non_structural_mass)


    @property
    def label(self):
        return self.value.label

    @label.setter
    def label(self, v):
        self.value.label = v

    @property
    def file_name(self):
        return self.value.file_name

    @file_name.setter
    def file_name(self, v):
        self.value.file_name = v

    @property
    def schema(self):
        return self.value.schema

    @schema.setter
    def schema(self, v):
        self.value.schema = v

    @property
    def extractor(self):
        return self.value.extractor

    @extractor.setter
    def extractor(self, v):
        self.value.extractor = v

    @property
    def position_values(self):
        return self.value.position_values

    @position_values.setter
    def position_values(self, v):
        self.value.position_values = v


# Generic function for inserting the results of the extraction into parquet files
def parquet_insert(mctx: ModelExtractionContext, rt: ResultType):
    """Generic function to write the results from the extraction processes to the parquet files"""

    counter = 0

    with pq.ParquetWriter(mctx.directory / rt.file_name, schema=rt.schema) as writer:
        result_lists = None
        for r in rt.extractor(mctx, rt.value):
            if result_lists is None:
                result_lists = [[] for _ in range(len(r))]
            for i, v in enumerate(r):
                result_lists[i].append(v)
            counter += 1

            if counter % 50_000 == 0:
                if result_lists:
                    _create_parq_table(writer, result_lists, rt.schema)

        if result_lists:
            _create_parq_table(writer, result_lists, rt.schema)


if __name__ == '__main__':

    # Create scratch path if not exists
    scratch_folder = pathlib.Path(f"C:\\Users\\{getuser()}\\Documents\\Changi T5_Database_Scratch")
    scratch_folder.mkdir(parents=True, exist_ok=True)

    root = tk.Tk()
    root.withdraw()

    # Collect the input file paths
    model_file = pathlib.Path(filedialog.askopenfilename(title="Select your Strand7 model file"))
    result_file = pathlib.Path(filedialog.askopenfilename(title="Select your Strand7 results file"))

    # Determine the output database format and collect corresponding inputs
    directory = pathlib.Path(filedialog.askdirectory(title="Select the directory for your parquet files"))

    extract_model_data(model_file, result_file, scratch_path=scratch_folder, directory=directory)


