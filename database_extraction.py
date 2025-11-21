
"""
database_extractor.py

Module to extract the analysis results from a Strand7 model into a SQLite database or Parquet files.
"""

__version__ = "1.2.0"

import ctypes
from sqlite3 import Connection, Cursor, connect

import pyarrow as pa
import pyarrow.parquet as pq
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pathlib
from getpass import getuser
import logging
import St7API as St7
from St7API import kMaxStrLen

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
                                   ("NormalZPosPressure", pa.float64()),
                                   ("NormalZNegPressure", pa.float64()),
                                   ("GlobalXPressure", pa.float64()),
                                   ("GlobalYPressure", pa.float64()),
                                   ("GlobalZPressure", pa.float64()),
                                   ("ShearXLocPressure", pa.float64()),
                                   ("ShearYLocPressure", pa.float64())])

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

# WIP SCHEMA FOR BEAM LOADING - LOAD IDS MAKE THIS DIFFICULT
_BEAM_LOADING_SCHEMA = pa.schema([("BeamNumber", pa.int32()),
                                  ("LoadCase", pa.int32()),
                                  ("LoadCaseName", pa.string()),
                                  ("PrincXDist", pa.float64()),
                                  ("PrincYDist", pa.float64()),
                                  ("PrincZDist", pa.float64()),
                                  ("GlobXDist", pa.float64()),
                                  ("GlobYDist", pa.float64()),
                                  ("GlobZDist", pa.float64()),
                                  ("PrincXPoint", pa.float64())])

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

# WIP SCHEMA FOR NODAL LOADING - LOAD IDS MAKE THIS DIFFICULT
_NODAL_LOADING_SCHEMA = pa.schema([])

SCHEMAS = {"BeamForces": _BEAM_FORCE_SCHEMA,
           "BeamProperties": _BEAM_PROPERTIES_SCHEMA,
           "NodalReactions": _NODAL_REACTIONS_SCHEMA,
           "NodalDisplacements": _NODAL_DISPLACEMENTS_SCHEMA,
           "NodalCoordinates": _NODAL_COORDINATES_SCHEMA,
           "PlateLocalStresses": _PLATE_LOCAL_STRESS_SCHEMA,
           "PlateCombinedStresses": _PLATE_DERIVED_STRESS_SCHEMA,
           "PlateProperties": _PLATE_PROPERTIES_SCHEMA,
           "PlateLoading": _PLATE_LOADING_SCHEMA}


def _log_error_message(err_code: int):
    message = St7.St7GetAPIErrorString(err_code, St7.kMaxStrLen).value.decode()
    print(message)

def _clear_lists(lists_to_clear: tuple):
    """Convenience function for clearing lists."""
    for lst in lists_to_clear:
        lst.clear()

def _create_parq_table(writer: pq.ParquetWriter, lists_to_process: tuple, schema: pa.Schema):
    array = list(pa.array(data) for data in lists_to_process)
    table = pa.Table.from_arrays(array, schema=schema)
    writer.write_table(table)
    _clear_lists(lists_to_process)

# Function to create a database and table
def create_sqlite_database(conn: Connection, cursor: Cursor):

    # Create table for node reactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NodalReactions (
            ResultId TEXT PRIMARY KEY,
            NodeNumber INTEGER,
            ResultCase INTEGER,
            ResultCaseName TEXT,
            ReactionX REAL,
            ReactionY REAL,
            ReactionZ REAL,
            ReactionXX REAL,
            ReactionYY REAL,
            ReactionZZ REAL
        )
    ''')

    cursor.execute("""CREATE INDEX idx_node_reactions_nodenumber_resultcase_resultcasename ON NodalReactions(NodeNumber, ResultCase, ResultCaseName);""")

    # Create table for node displacements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NodalDisplacements (
            ResultId TEXT PRIMARY KEY,
            NodeNumber INTEGER,
            ResultCase INTEGER,
            ResultCaseName TEXT,
            DisplacementX REAL,
            DisplacementY REAL,
            DisplacementZ REAL,
            RotationXX REAL,
            RotationYY REAL,
            RotationZZ REAL
        )
    ''')

    cursor.execute("""CREATE INDEX idx_node_displacements_nodenumber_resultcase_resultcasename ON NodalDisplacements(NodeNumber, ResultCase, ResultCaseName);""")

    # Create table for nodal coordinates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NodalCoordinates (
            NodeNumber INTEGER PRIMARY KEY,
            X REAL,
            Y REAL,
            Z REAL
        )
    ''')

    # Create table for element attributes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BeamProperties (
            BeamNumber INTEGER PRIMARY KEY,
            N1 INTEGER,
            N2 INTEGER,
            Length REAL,
            PropertyName TEXT,
            GroupName TEXT,
            BeamIDNumber INTEGER
        )
    ''')

    cursor.execute("""CREATE INDEX idx_beam_attributes_propertyname ON BeamProperties(PropertyName, GroupName, BeamIDNumber);""")

    # Create table for element forces
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BeamForces (
            ResultId TEXT PRIMARY KEY,
            BeamNumber INTEGER,
            ResultCase INTEGER,
            ResultCaseName TEXT,
            Position REAL,
            Fx REAL,
            Fy REAL,
            Fz REAL,
            Mx REAL,
            My REAL,
            Mz REAL
        )
    ''')

    cursor.execute("""CREATE INDEX idx_beam_forces_beamnumber_resultcase_resultcasename_propertyname ON BeamForces(BeamNumber, ResultCase, ResultCaseName);""")

    # Create table for element displacements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BeamDisplacements (
            ResultId TEXT PRIMARY KEY,
            BeamNumber INTEGER,
            ResultCase INTEGER,
            ResultCaseName TEXT,
            Position REAL,
            Dx REAL,
            Dy REAL,
            Dz REAL,
            Rx REAL,
            Ry REAL,
            Rz REAL
        )
    ''')

    cursor.execute("""CREATE INDEX idx_beam_displacements_beamnumber_resultcase_resultcasename_propertyname ON BeamDisplacements(BeamNumber, ResultCase, ResultCaseName);""")

    conn.commit()


# Function to insert nodal reactions into the database
def sql_insert_nodal_reactions(conn: Connection, cursor: Cursor, uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                               secondary_combo_count: ctypes.c_int):

    nodal_reactions = []

    insertion_query = """
            INSERT INTO NodalReactions (ResultId, NodeNumber, ResultCase, ResultCaseName, ReactionX, ReactionY, ReactionZ, ReactionXX, ReactionYY, ReactionZZ)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    for result in extract_nodal_reactions(uID, primary_combo_count=primary_combo_count,
                                          secondary_combo_count=secondary_combo_count):
        nodal_reactions.append(result)

        if len(nodal_reactions) % 50_000 == 0:
            cursor.executemany(insertion_query, nodal_reactions)
            nodal_reactions.clear()

    cursor.executemany(insertion_query, nodal_reactions)
    nodal_reactions.clear()

    conn.commit()

    print("Nodal reactions written to DB.")


# Function to insert nodal displacements into the database
def sql_insert_nodal_displacements(conn: Connection, cursor: Cursor, uID: ctypes.c_int,
                                   primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):

    insertion_query = """
        INSERT INTO NodalDisplacements (ResultId, NodeNumber, ResultCase, ResultCaseName, DisplacementX, DisplacementY, DisplacementZ, RotationXX, RotationYY, RotationZZ)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    nodal_displacements = []

    for result in extract_nodal_displacements(uID, primary_combo_count, secondary_combo_count):

        nodal_displacements.append(result)

        if len(nodal_displacements) % 50_000 == 0:
            cursor.executemany(insertion_query, nodal_displacements)
            nodal_displacements.clear()

    cursor.executemany(insertion_query, nodal_displacements)
    nodal_displacements.clear()

    conn.commit()
    print("Nodal displacements written to the DB.")


# Function to insert nodal coordinates into the database
def sql_insert_nodal_coordinates(conn: Connection, cursor: Cursor, uID: ctypes.c_int):

    nodal_coordinates = []

    insertion_query = """INSERT INTO NodalCoordinates (NodeNumber, X, Y, Z)
    VALUES (?, ?, ?, ?)"""

    for result in extract_nodal_coordinates(uID):
        nodal_coordinates.append(result)

        # Write out the results every 50_000 results or so
        if len(nodal_coordinates) % 50_000 == 0:
            cursor.executemany(insertion_query, nodal_coordinates)
            nodal_coordinates.clear()

    cursor.executemany(insertion_query, nodal_coordinates)
    nodal_coordinates.clear()

    conn.commit()

    print("Nodal coordinates written to DB.")


# Function to insert element properties into the database
def sql_insert_beam_properties(conn: Connection, cursor: Cursor, uID: ctypes.c_int):

    beam_properties = []

    insertion_query = """INSERT INTO BeamProperties (BeamNumber, N1, N2, Length, PropertyName, GroupName, BeamIDNumber)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""

    for result in extract_beam_properties(uID):

        beam_properties.append(result)

        # Write out the results every 50_000 results or so
        if len(beam_properties) % 50_000 == 0:
            cursor.executemany(insertion_query, beam_properties)
            beam_properties.clear()

    cursor.executemany(insertion_query, beam_properties)
    beam_properties.clear()

    conn.commit()

    print("Beam attributes and properties written to DB.")


# Function to insert element forces into the database
def sql_insert_beam_forces(conn: Connection, cursor: Cursor, uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                           secondary_combo_count: ctypes.c_int):
    beam_results = []

    insertion_query = """INSERT INTO BeamForces (ResultId, BeamNumber, ResultCase, ResultCaseName, Position, Fx, Fy, Fz, Mx, My, Mz)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    for result in extract_beam_forces(uID, primary_combo_count, secondary_combo_count):

        beam_results.append(result)

        # Write out the results every 50_000 results or so
        if len(beam_results) % 50_000 == 0:
            cursor.executemany(insertion_query, beam_results)
            beam_results.clear()

    # Final executemany call outside the loop to insert any residual results
    cursor.executemany(insertion_query, beam_results)
    beam_results.clear()

    conn.commit()

    print("Beam force results written to DB.")


# Function to insert element displacements into the database
def sql_insert_beam_displacements(conn: Connection, cursor: Cursor, beam_results: list):

    insertion_query = """INSERT INTO BeamDisplacements (ResultId, BeamNumber, ResultCase, ResultCaseName, Position, Dx, Dy, Dz, Rx, Ry, Rz)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    cursor.executemany(insertion_query, beam_results)

    conn.commit()


def parquet_insert_nodal_coordinates(uID: ctypes.c_int, directory: pathlib.Path):

    node_numbers = []
    x_coords = []
    y_coords = []
    z_coords = []

    lists_to_process = (node_numbers, x_coords, y_coords, z_coords)

    counter = 0

    with pq.ParquetWriter(directory / "nodal_coordinates.parquet", schema=SCHEMAS["NodalCoordinates"]) as writer:
        for r in extract_nodal_coordinates(uID):
            node_numbers.append(r[0])
            x_coords.append(r[1])
            y_coords.append(r[2])
            z_coords.append(r[3])

            counter += 1

            if counter % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["NodalCoordinates"])

        _create_parq_table(writer, lists_to_process, SCHEMAS["NodalCoordinates"])

    print("Nodal coordinates written to DB.")


def parquet_insert_nodal_reactions(uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                                   secondary_combo_count: ctypes.c_int, directory: pathlib.Path):

    result_ids = []
    node_numbers = []
    case_numbers = []
    case_names = []
    rxs = []
    rys = []
    rzs = []
    rxxs = []
    ryys = []
    rzzs = []

    lists_to_process = (result_ids, node_numbers, case_numbers, case_names, rxs, rys, rzs, rxxs, ryys, rzzs)

    with pq.ParquetWriter(directory / "nodal_reactions.parquet", schema=SCHEMAS["NodalReactions"]) as writer:

        counter = 0

        for r in extract_nodal_reactions(uID, primary_combo_count=primary_combo_count,
                                         secondary_combo_count=secondary_combo_count):
            result_ids.append(r[0])
            node_numbers.append(r[1])
            case_numbers.append(r[2])
            case_names.append(r[3])
            rxs.append(r[4])
            rys.append(r[5])
            rzs.append(r[6])
            rxxs.append(r[7])
            ryys.append(r[8])
            rzzs.append(r[9])

            counter += 1

            if counter % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["NodalReactions"])

        _create_parq_table(writer, lists_to_process, SCHEMAS["NodalReactions"])

        print("Nodal reactions written to DB.")


def parquet_insert_nodal_displacements(uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                                       secondary_combo_count: ctypes.c_int, directory: pathlib.Path):

    result_ids = []
    node_numbers = []
    case_numbers = []
    case_names = []
    dxs = []
    dys = []
    dzs = []
    dxxs = []
    dyys = []
    dzzs = []

    lists_to_process = (result_ids, node_numbers, case_numbers, case_names, dxs, dys, dzs, dxxs, dyys, dzzs)

    count = 0

    with pq.ParquetWriter(directory / "nodal_displacements.parquet", schema=SCHEMAS["NodalDisplacements"]) as writer:

        for r in extract_nodal_displacements(uID, primary_combo_count, secondary_combo_count):

            result_ids.append(r[0])
            node_numbers.append(r[1])
            case_numbers.append(r[2])
            case_names.append(r[3])
            dxs.append(r[4])
            dys.append(r[5])
            dzs.append(r[6])
            dxxs.append(r[7])
            dyys.append(r[8])
            dzzs.append(r[9])

            count += 1

            if count % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["NodalDisplacements"])

        _create_parq_table(writer, lists_to_process, SCHEMAS["NodalDisplacements"])

    print("Nodal displacements written to DB.")


def parquet_insert_beam_properties(uID: ctypes.c_int, directory: pathlib.Path):
    """
    Function for creating the parquet cruciform_output_file for beam properties.
    :param uID:
    :param directory:
    :return:
    """

    beam_numbers = []
    n1s = []
    n2s = []
    lengths = []
    property_names = []
    group_names = []
    beam_id_numbers = []
    dir1_xs = []
    dir1_ys = []
    dir1_zs = []
    dir2_xs = []
    dir2_ys = []
    dir2_zs = []
    dir3_xs = []
    dir3_ys = []
    dir3_zs = []

    lists_to_process = (beam_numbers, n1s, n2s, lengths, property_names, group_names, beam_id_numbers,
                        dir1_xs, dir1_ys, dir1_zs, dir2_xs, dir2_ys, dir2_zs, dir3_xs, dir3_ys, dir3_zs)

    with pq.ParquetWriter(directory / "beam_properties.parquet", SCHEMAS["BeamProperties"]) as writer:

        counter = 0

        for r in extract_beam_properties(uID):
            beam_numbers.append(r[0])
            n1s.append(r[1])
            n2s.append(r[2])
            lengths.append(r[3])
            property_names.append(r[4])  # Can I just get rid of the string casting that I did above?
            group_names.append(r[5])
            beam_id_numbers.append(r[6])
            dir1_xs.append(r[7])
            dir1_ys.append(r[8])
            dir1_zs.append(r[9])
            dir2_xs.append(r[10])
            dir2_ys.append(r[11])
            dir2_zs.append(r[12])
            dir3_xs.append(r[13])
            dir3_ys.append(r[14])
            dir3_zs.append(r[15])
            counter += 1
            if counter % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["BeamProperties"])

        # We write one last time for any remaining data in the lists
        _create_parq_table(writer, lists_to_process, SCHEMAS["BeamProperties"])

    print("Beam attributes and properties written to DB.")


def parquet_insert_beam_forces(uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                               secondary_combo_count: ctypes.c_int, directory: pathlib.Path):
    """
    """

    result_ids = []
    beam_numbers = []
    case_numbers = []
    case_names = []
    position_results = []
    fxs = []
    fys = []
    fzs = []
    mxs = []
    mys = []
    mzs = []

    lists_to_process = (result_ids, beam_numbers, case_numbers, case_names, position_results, fxs, fys, fzs, mxs, mys, mzs)

    with pq.ParquetWriter(directory / "beam_forces.parquet", SCHEMAS["BeamForces"]) as writer:

        counter = 0

        for r in extract_beam_forces(uID, primary_combo_count, secondary_combo_count):
            result_ids.append(r[0])
            beam_numbers.append(r[1])
            case_numbers.append(r[2])
            case_names.append(r[3])
            position_results.append(r[4])  # Can I just get rid of the string casting that I did above?
            fxs.append(r[5])
            fys.append(r[6])
            fzs.append(r[7])
            mxs.append(r[8])
            mys.append(r[9])
            mzs.append(r[10])
            counter += 1
            if counter % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["BeamForces"])

        # We write one last time for any remaining data in the lists
        _create_parq_table(writer, lists_to_process, SCHEMAS["BeamForces"])

    print("Beam force results written to DB.")


def parquet_insert_plate_properties(uID: ctypes.c_int, directory: pathlib.Path):

    plate_numbers = []
    n1s = []
    n2s = []
    n3s = []
    n4s = []
    areas = []
    property_names = []
    property_types = []
    element_types = []
    group_names = []
    plate_id_numbers = []

    lists_to_process = (plate_numbers, property_names, property_types, element_types, group_names, plate_id_numbers,
                        areas, n1s, n2s, n3s, n4s)

    with pq.ParquetWriter(directory / "plate_properties.parquet", SCHEMAS["PlateProperties"]) as writer:

        counter = 0

        for r in extract_plate_properties(uID):
            plate_numbers.append(r[0])
            n1s.append(r[1])
            n2s.append(r[2])
            n3s.append(r[3])
            n4s.append(r[4])
            if r[4] != 0:
                element_types.append("QUAD")
            else:
                element_types.append("TRI")
            areas.append(r[5])
            property_names.append(r[6])
            property_types.append(r[7])
            group_names.append(r[8])
            plate_id_numbers.append(r[9])

            counter += 1
            if counter % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["PlateProperties"])

        _create_parq_table(writer, lists_to_process, SCHEMAS["PlateProperties"])

    print("Plate attributes and properties written to DB.")


def parquet_insert_plate_loading(uID: ctypes.c_int, load_case_count: ctypes.c_int, directory: pathlib.Path):

    plate_numbers = []
    case_numbers = []
    case_names = []
    norm_neg_pressures = []
    norm_pos_pressures = []
    glob_neg_x_pressures = []
    glob_neg_y_pressures = []
    glob_neg_z_pressures = []
    glob_pos_x_pressures = []
    glob_pos_y_pressures = []
    glob_pos_z_pressures = []
    shear_stress_xs = []
    shear_stress_ys = []

    lists_to_process = (plate_numbers, case_numbers, case_names,
                        norm_neg_pressures, norm_pos_pressures,
                        glob_neg_x_pressures, glob_neg_y_pressures, glob_neg_z_pressures,
                        glob_pos_x_pressures, glob_pos_y_pressures, glob_pos_z_pressures,
                        shear_stress_xs, shear_stress_ys)

    with pq.ParquetWriter(directory / "plate_loading.parquet", SCHEMAS["PlateLoading"]) as writer:

        counter = 0

        for r in extract_plate_loading(uID, load_case_count):
            plate_numbers.append(r[0])
            case_numbers.append(r[1])
            case_names.append(r[2])
            norm_neg_pressures.append(r[3])
            norm_pos_pressures.append(r[4])
            glob_neg_x_pressures.append(r[5])
            glob_neg_y_pressures.append(r[6])
            glob_neg_z_pressures.append(r[7])
            glob_pos_x_pressures.append(r[8])
            glob_pos_y_pressures.append(r[9])
            glob_pos_z_pressures.append(r[10])
            shear_stress_xs.append(r[11])
            shear_stress_ys.append(r[12])

            counter += 1
            if counter % 50_000 == 0:
                _create_parq_table(writer, lists_to_process, SCHEMAS["PlateLoading"])

        _create_parq_table(writer, lists_to_process, SCHEMAS["PlateLoading"])

    print("Plate loading written to DB.")


def parquet_insert_plate_local_stresses(uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                                        secondary_combo_count: ctypes.c_int, directory: pathlib.Path):
    pass


def parquet_insert_plate_combined_stresses(uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                                           secondary_combo_count: ctypes.c_int, directory: pathlib.Path):
    pass


# Initialize Strand7 model
def initialize_model(model_file: str, result_file: str, scratch_path: str):
    uID = ctypes.c_int(1)  # Unique identifier for the model
    St7.St7Init()
    p_combo_count = ctypes.c_int(0)
    s_combo_count = ctypes.c_int(0)
    try:  # This try block is essential for avoiding getting stuck if the API call fails
        St7.St7OpenFile(uID, model_file.encode('utf-8'), scratch_path.encode())
        print("Model opened.")
        St7.St7OpenResultFile(uID, result_file.encode(), None, St7.kUseExistingCombinations,
                              ctypes.byref(p_combo_count), ctypes.byref(s_combo_count))
        print("Results accessed.")
        print(f"Primary combinations found: {p_combo_count.value}")
        print(f"Secondary combinations found: {s_combo_count.value}")

        return uID, p_combo_count, s_combo_count

    except:
        St7.St7Release()
        return None


# Function to extract nodal reactions
def extract_nodal_reactions(uID: ctypes.c_int, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, case_number, case_name, St7.kMaxStrLen)

        case_name_string = str(case_name.value.decode())
        print(f"Extracting node reactions for load case {case_name_string}...")

        for node in range(1, nNodes.value + 1):

            reaction_array = ctypes.c_double * 6
            reactions = reaction_array()

            St7.St7GetNodeResult(uID, St7.rtNodeReact, node, case_number, reactions)
            result_id = f"{node}-{case_number}"
            fx = float(reactions[0])
            fy = float(reactions[1])
            fz = float(reactions[2])
            mx = float(reactions[3])
            my = float(reactions[4])
            mz = float(reactions[5])

            result = (result_id, node, case_number, case_name_string, fx, fy, fz, mx, my, mz)

            yield result

    print("Nodal reactions written to DB.")


# Function to extract nodal displacements
def extract_nodal_displacements(uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                                secondary_combo_count: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, case_number, case_name, St7.kMaxStrLen)
        print(f"Extracting node displacements for load case {case_name.value.decode()}...")

        for node in range(1, nNodes.value + 1):

            displacement_array = ctypes.c_double * 6
            displacements = displacement_array()

            St7.St7GetNodeResult(uID, St7.rtNodeDisp, node, case_number, displacements)
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
def extract_nodal_coordinates(uID: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    print("Extracting nodal coordinates...")

    node_coordinate_array = ctypes.c_double * 3
    node_coordinates = node_coordinate_array()

    for node in range(1, nNodes.value + 1):
        St7.St7GetNodeXYZ(uID, node, node_coordinates)

        x_coord = node_coordinates[0]
        y_coord = node_coordinates[1]
        z_coord = node_coordinates[2]

        result = (node, x_coord, y_coord, z_coord)

        yield result


# Function to extract beam attributes and properties
def extract_beam_properties(uID: ctypes.c_int):

    nBeams = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyBEAM, ctypes.byref(nBeams))

    print("Extracting beam attributes and properties...")

    for beam in range(1, nBeams.value + 1):
        # Create an array to store the connection information
        connection_array = ctypes.c_int * St7.kMaxElementNode
        connections = connection_array()

        # Access the beam connection information
        St7.St7GetElementConnection(uID, St7.tyBEAM, beam, connections)

        # Access the beam id information
        id_number = ctypes.c_int(0)
        St7.St7GetBeamID(uID, beam, id_number)

        # Access the property associated with the beam
        property_number = ctypes.c_int(0)
        property_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetElementProperty(uID, St7.ptBEAMPROP, beam, ctypes.byref(property_number))
        St7.St7GetPropertyName(uID, St7.ptBEAMPROP, property_number, property_name, St7.kMaxStrLen)

        # Access the group associated with the beam
        group_id = ctypes.c_int(0)
        group_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetEntityGroup(uID, St7.tyBEAM, beam, ctypes.byref(group_id))
        St7.St7GetGroupIDName(uID, group_id, group_name, St7.kMaxStrLen)

        # Access the beam axes data
        axis_data = ctypes.c_double * 9
        axis_array = axis_data()

        St7.St7GetBeamAxisSystemInitial(uID, beam, axis_array)

        # Access the beam geometric data
        element_data = ctypes.c_double * 3
        element_data_array = element_data()

        St7.St7GetElementData(uID, St7.tyBEAM, beam, 0, element_data_array)

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

        del axis_array, element_data_array

        result = (beam, node1, node2, length, property_name.value.decode(),
                  group_name.value.decode(), id_number.value, dir1_x, dir1_y, dir1_z,
                  dir2_x, dir2_y, dir2_z, dir3_x, dir3_y, dir3_z)
        yield result


# Function to extract the beam force results
def extract_beam_forces(uID: ctypes.c_int, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):

    nBeams = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyBEAM, ctypes.byref(nBeams))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    # The following ensures that the result positions are output as a ratio of the overall member length (0.0...1.0)
    St7.St7SetBeamResultPosMode(uID, St7.bpParam)

    # The following setting (number of stations and positions) is hard-baked
    # Can decouple from this function in the future, but haven't needed to so far.
    num_stations_requested = 5
    position_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    # Shifted beam results outside the result case loop - SQL transaction will occur only once at the end
    # rather than after every result case, which should enhance performance a bit.  May need to
    # adjust this in the future though, as the batch sizes might get too big to hold in memory all at once.

    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, case_number, case_name, St7.kMaxStrLen)
        print(f"Extracting beam forces for result case {case_name.value.decode()}...")

        for beam in range(1, nBeams.value + 1):

            # Number of result columns (i.e. fields)
            number_columns = ctypes.c_int(0)

            force_array = ctypes.c_double * (num_stations_requested * St7.kMaxBeamResult)
            forces = force_array()

            # Station positions along the element for querying loads
            position_values_c = [ctypes.c_double(p) for p in position_values]
            pos_array = ctypes.c_double * len(position_values_c)
            positions = pos_array(*position_values_c)

            # Get the beam results using the Strand API
            St7.St7GetBeamResultArrayPos(uID, St7.rtBeamForce, St7.stBeamPrincipal, beam, case_number,
                                         num_stations_requested, positions, ctypes.byref(number_columns), forces)

            # Access the forces from each beam at each station position, and add these to the result list
            for i in range(num_stations_requested):
                position = f"{position_values[i]:.2f}"
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
def extract_beam_displacements(conn: Connection, cursor: Cursor, uID: ctypes.c_int, primary_combo_count: ctypes.c_int,
                               secondary_combo_count: ctypes.c_int):
    nBeams = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyBEAM, ctypes.byref(nBeams))

    # The following ensures that the result positions are output as a ratio of the overall member length (0.0...1.0)
    St7.St7SetBeamResultPosMode(uID, St7.bpParam)

    num_stations_requested = 5

    # Shifted beam results outside the result case loop - transactions will occur once at the end rather than after
    # every result case, which should enhance performance
    beam_results = []
    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for case_number in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, case_number, case_name, St7.kMaxStrLen)
        print(f"Extracting beam displacements for result case {case_name.value.decode()}...")

        for beam in range(1, nBeams.value + 1):

            # Number of result columns (i.e. fields)
            number_columns = ctypes.c_int(0)

            displacement_array = ctypes.c_double * (num_stations_requested * St7.kMaxBeamResult)
            displacements = displacement_array()

            # Station positions along the element for querying loads
            position_values = [0.0, 0.25, 0.5, 0.75, 1.0]
            position_values_c = [ctypes.c_double(p) for p in position_values]
            pos_array = ctypes.c_double * len(position_values_c)
            positions = pos_array(*position_values_c)

            # Get the beam results using the Strand API
            St7.St7GetBeamResultArrayPos(uID, St7.rtBeamDisp, St7.stBeamPrincipal, beam, case_number,
                                         num_stations_requested, positions, ctypes.byref(number_columns), displacements)

            # Access the forces from each beam at each station position, and add these to the result list
            for i in range(num_stations_requested):
                position = position_values[i]
                dx = displacements[(i * 6) + 0]
                dy = displacements[(i * 6) + 1]
                dz = displacements[(i * 6) + 2]
                rx = displacements[(i * 6) + 3]
                ry = displacements[(i * 6) + 4]
                rz = displacements[(i * 6) + 5]
                sid = f"{beam}-{case_number}-{position:.2f}"
                result = (sid, beam, case_number, case_name.value.decode(), position, dx, dy, dz, rx, ry, rz)
                beam_results.append(result)

        # Insert the beam displacement results into the database
        if len(beam_results) == 0:
            print("Warning: Beam displacement result set is empty.")
        else:
            # Implementing smarter batching
            if case_number % 100 == 0 or case_number == number_of_cases:
                sql_insert_beam_displacements(conn, cursor, beam_results)
                beam_results.clear()

# Function to extract the plate attributes and properties
def extract_plate_properties(uID: ctypes.c_int):

    nPlates = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyPLATE, ctypes.byref(nPlates))

    print("Extracting plate attributes and properties...")

    for plate in range(1, nPlates.value + 1):

        # Create an array to store the connection information
        connection_array = ctypes.c_int * St7.kMaxElementNode
        connections = connection_array()

        # Access the beam connection information
        St7.St7GetElementConnection(uID, St7.tyPLATE, plate, connections)

        # Access the plate id information
        id_number = ctypes.c_int(0)
        St7.St7GetPlateID(uID, plate, id_number)

        # Access the property associated with the plate
        property_number = ctypes.c_int(0)
        property_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        property_type = ctypes.c_int(0)
        material_type = ctypes.c_int(0)
        St7.St7GetElementProperty(uID, St7.ptPLATEPROP, plate, ctypes.byref(property_number))
        St7.St7GetPropertyName(uID, St7.ptPLATEPROP, property_number, property_name, St7.kMaxStrLen)
        St7.St7GetPlatePropertyType(uID, property_number, ctypes.byref(property_type), ctypes.byref(material_type))

        # Access the group associated with the plate
        group_id = ctypes.c_int(0)
        group_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetEntityGroup(uID, St7.tyPLATE, plate, ctypes.byref(group_id))
        St7.St7GetGroupIDName(uID, group_id, group_name, St7.kMaxStrLen)

        # Access the plate geometric data
        element_data = ctypes.c_double * 1
        element_data_array = element_data()

        St7.St7GetElementData(uID, St7.tyPLATE, plate, 0, element_data_array)

        node_count = connections[0]
        n1 = connections[1]
        n2 = connections[2]
        n3 = connections[3]

        if node_count == 3:
            n4 = 0
        else:
            n4 = connections[4]

        area = element_data_array[0]

        del element_data_array, connections

        result = (plate, n1, n2, n3, n4, area, property_name.value.decode(), property_type.value,
                  group_name.value.decode(), id_number.value)

        yield result


# Function to extract the plate loading from the model
def extract_plate_loading(uID: ctypes.c_int, load_case_count: ctypes.c_int):

    nPlates = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyPLATE, ctypes.byref(nPlates))
    print("Extracting plate loads...")

    for plate in range(1, nPlates.value + 1):
        for case_number in range(1, load_case_count.value + 1):

            case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
            St7.St7GetLoadCaseName(uID, case_number, ctypes.byref(case_name), kMaxStrLen)  # Not sure if this is OK

            # Get the plate normal loading
            norm_pressure_array = ctypes.c_double * 2
            norm_pressures = norm_pressure_array()
            St7.St7GetPlateNormalPressure2(uID, plate, case_number, ctypes.byref(norm_pressures))
            norm_neg_pressure = norm_pressures[0]
            norm_pos_pressure = norm_pressure_array[1]

            # Get the plate global loading
            glob_pressure_array = ctypes.c_double * 3
            glob_pos_pressures = glob_pressure_array()
            glob_neg_pressures = glob_pressure_array()
            St7.St7GetPlateGlobalPressure3S(uID, plate, St7.psPlateMinusZ, case_number, St7.ppNone, ctypes.byref(glob_neg_pressures))
            St7.St7GetPlateGlobalPressure3S(uID, plate, St7.psPlatePlusZ, case_number, St7.ppNone, ctypes.byref(glob_pos_pressures))
            glob_neg_x_pressure = glob_neg_pressures[0]
            glob_neg_y_pressure = glob_neg_pressures[1]
            glob_neg_z_pressure = glob_neg_pressures[2]
            glob_pos_x_pressure = glob_pos_pressures[0]
            glob_pos_y_pressure = glob_pos_pressures[1]
            glob_pos_z_pressure = glob_pos_pressures[2]

            # Get the plate shear loading
            shear_stress_array = ctypes.c_double * 2
            shear_stresses = shear_stress_array()
            St7.St7GetPlateShear2(uID, plate, case_number, ctypes.byref(shear_stresses))
            shear_stress_x = shear_stresses[0]
            shear_stress_y = shear_stresses[1]

            result = (plate, case_number, case_name.value.decode(),
                      norm_neg_pressure, norm_pos_pressure,
                      glob_neg_x_pressure, glob_neg_y_pressure, glob_neg_z_pressure,
                      glob_pos_x_pressure, glob_pos_y_pressure, glob_pos_z_pressure,
                      shear_stress_x, shear_stress_y)

            yield result

# Function to extract the plate local stress results
def extract_plate_local_stresses(uID: ctypes.c_int, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):
    pass

# Function to extract the plate combined stress results
def extract_plate_combined_stresses(uID: ctypes.c_int, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):
    pass


# Main function for extracting results
def extract_model_data(model_file: str, result_file: str, scratch_path: str, parquet=False, directory=None,
                       db_fp: str = None):

    # Initialize the Strand7 model
    init = initialize_model(model_file, result_file, scratch_path)
    if not init:
        raise RuntimeError("Failed to initialize Strand7 model and results.")
    uID, primary_combo_count, secondary_combo_count = init

    # Get the number of load cases
    load_case_count = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(load_case_count))

    # Logic for creating the parquet files
    if parquet:
        parquet_insert_nodal_coordinates(uID, directory)
        parquet_insert_nodal_reactions(uID, primary_combo_count, secondary_combo_count, directory)
        parquet_insert_nodal_displacements(uID, primary_combo_count, secondary_combo_count, directory)
        parquet_insert_beam_forces(uID, primary_combo_count, secondary_combo_count, directory)
        parquet_insert_beam_properties(uID, directory)
        # parquet_insert_plate_properties(uID, directory)
        # parquet_insert_plate_loading(uID, load_case_count, directory)

    # If not running the parquet extraction, the program will extract to a SQLite db
    else:
        with connect(db_fp) as conn:

            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            conn.execute("PRAGMA temp_store = MEMORY;")

            cursor = conn.cursor()

            # Ensure the database is ready
            create_sqlite_database(conn, cursor)

            if uID is None:
                pass

            else:

                # Extract nodal coordinates and store them in the database
                sql_insert_nodal_coordinates(conn, cursor, uID)

                # Extract nodal reactions and store them in the database
                sql_insert_nodal_reactions(conn, cursor, uID, primary_combo_count, secondary_combo_count)

                # Extract nodal displacements and store them in the database
                sql_insert_nodal_displacements(conn, cursor, uID, primary_combo_count, secondary_combo_count)

                # Extract the beam properties and store them in the database
                sql_insert_beam_properties(conn, cursor, uID)

                # Extract beam forces and store them in the database
                sql_insert_beam_forces(conn, cursor, uID, primary_combo_count, secondary_combo_count)

                # Extract beam displacements and store them in the database
                extract_beam_displacements(conn, cursor, uID, primary_combo_count, secondary_combo_count)

    # Close the Strand7 model
    St7.St7CloseResultFile(uID)
    St7.St7CloseFile(uID)
    St7.St7Release()


if __name__ == '__main__':
    # ----------------------------------------------------------------------
    # USER NOTES
    # 1. The Strand model must be analyzed and have results before running
    # this script.
    # 2. The model must be closed when running the script (can't be open in
    # the background as the script will access it using the API).
    # 3. If you have accidentally run the script while the model is open,
    # make sure to delete the empty database output_file that it created
    # before rerunning the script.
    # ----------------------------------------------------------------------

    # Do you want it to extract in parquet format?

    # Create scratch path if not exists
    scratch_folder = f"C:\\Users\\{getuser()}\\Documents\\Changi T5_Database_Scratch"
    if not os.path.exists(scratch_folder):
        os.mkdir(scratch_folder)

    root = tk.Tk()
    root.withdraw()

    # Collect the input file paths
    model_file = filedialog.askopenfilename(title="Select your Strand7 model file")
    result_file = filedialog.askopenfilename(title="Select your Strand7 results file")

    # Determine the output database format and collect corresponding inputs
    parquet_output = messagebox.askyesno("Output Format", "Do you want parquet file outputs (will default to SQLite otherwise)?")
    if parquet_output:
        directory = pathlib.Path(filedialog.askdirectory(title="Select the directory for your parquet files"))
        db_fp = None
    else:
        db_fp = filedialog.asksaveasfilename(title="Save database file as", defaultextension=".db")
        directory = None

    extract_model_data(model_file, result_file, scratch_path=scratch_folder, parquet=parquet_output, directory=directory, db_fp=db_fp)

    # nla_dict = {
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\36 ALS Removal S-TR02-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\36 ALS Removal S-TR02-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\36 ALS Removal S-TR02-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\37 ALS Removal S-TR02-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\37 ALS Removal S-TR02-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\37 ALS Removal S-TR02-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\38 ALS Removal S-TR05-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\38 ALS Removal S-TR05-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\38 ALS Removal S-TR05-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\39 ALS Removal S-TR05-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\39 ALS Removal S-TR05-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\39 ALS Removal S-TR05-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\40 ALS Removal S-TR04-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\40 ALS Removal S-TR04-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\40 ALS Removal S-TR04-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\41 ALS Removal S-TR11-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\41 ALS Removal S-TR11-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\41 ALS Removal S-TR11-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\42 ALS Removal S-TR13-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\42 ALS Removal S-TR13-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\42 ALS Removal S-TR13-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\43 ALS Removal S-TR13-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\43 ALS Removal S-TR13-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\43 ALS Removal S-TR13-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\44 ALS Removal S-TR13-03.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\44 ALS Removal S-TR13-03.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\44 ALS Removal S-TR13-03"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\45 ALS Removal S-TR13-04.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\45 ALS Removal S-TR13-04.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\45 ALS Removal S-TR13-04"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\46 ALS Removal S-TR14-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\46 ALS Removal S-TR14-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\46 ALS Removal S-TR14-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\47 ALS Removal S-TR14-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\47 ALS Removal S-TR14-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\47 ALS Removal S-TR14-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\48 ALS Removal S-TR14-03.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\48 ALS Removal S-TR14-03.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\48 ALS Removal S-TR14-03"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\49 ALS Removal S-TR14-04.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\49 ALS Removal S-TR14-04.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\49 ALS Removal S-TR14-04"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\50 ALS Removal S-TR01-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\50 ALS Removal S-TR01-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\50 ALS Removal S-TR01-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\51 ALS Removal S-TR01-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\51 ALS Removal S-TR01-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\51 ALS Removal S-TR01-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\54 ALS Removal S-TR02-03.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\54 ALS Removal S-TR02-03.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\54 ALS Removal S-TR02-03"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\58 ALS Removal S-TR05-03.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\58 ALS Removal S-TR05-03.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\58 ALS Removal S-TR05-03"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\59 ALS Removal S-TR06-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\59 ALS Removal S-TR06-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\59 ALS Removal S-TR06-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\60 ALS Removal S-TR06-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\60 ALS Removal S-TR06-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\60 ALS Removal S-TR06-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\61 ALS Removal S-TR06-03.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\61 ALS Removal S-TR06-03.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\61 ALS Removal S-TR06-03"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\62 ALS Removal S-TR07-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\62 ALS Removal S-TR07-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\62 ALS Removal S-TR07-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\63 ALS Removal S-TR07-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\63 ALS Removal S-TR07-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\63 ALS Removal S-TR07-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\64 ALS Removal S-TR07-03.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\64 ALS Removal S-TR07-03.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\64 ALS Removal S-TR07-03"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\65 ALS Removal S-TR08-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\65 ALS Removal S-TR08-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\65 ALS Removal S-TR08-01"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\66 ALS Removal S-TR11-02.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\66 ALS Removal S-TR11-02.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\66 ALS Removal S-TR11-02"),
    #     r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\67 ALS Removal S-TR12-01.NLA": (
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\67 ALS Removal S-TR12-01.st7",
    #         r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\ALS\Principal Axes Parquet\67 ALS Removal S-TR12-01")}
    #
    # p = "Something"
    #
    # for k, v in nla_dict.items():
    #     if not os.path.exists(v[1]):
    #         os.mkdir(v[1])
    #     extract_model_data(v[0], k, p, scratch_path=scratch_folder, parquet=parquet, directory=pathlib.Path(v[1]))
    #     time.sleep(1)


