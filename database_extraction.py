
"""
database_extractor.py

Module to extract the analysis results from a Strand7 model into a SQLite database.
Have added support for producing parquet files of results.
"""

__version__ = "1.1.0"

import ctypes
from sqlite3 import Connection, Cursor, connect
import pyarrow as pa
import pyarrow.parquet as pq
import os
import time
import tkinter as tk
from tkinter import filedialog
import pathlib
from getpass import getuser

# Import the St7API module
import St7API as St7

_BEAM_FORCE_SCHEMA = pa.schema([
    ("ResultId", pa.string()),
    ("BeamNumber", pa.int32()),
    ("ResultCase", pa.int32()),
    ("ResultCaseName", pa.string()),
    ("Position", pa.float16()),
    ("Fx", pa.float32()),
    ("Fy", pa.float32()),
    ("Fz", pa.float32()),
    ("Mx", pa.float32()),
    ("My", pa.float32()),
    ("Mz", pa.float32())
])

_BEAM_PROPERTIES_SCHEMA = pa.schema([
    ("BeamNumber", pa.int32()),
    ("N1", pa.int32()),
    ("N2", pa.int32()),
    ("Length", pa.float32()),
    ("PropertyName", pa.string()),
    ("GroupName", pa.string()),
    ("BeamIDNumber", pa.int32()),
    ("Dir1_X", pa.float32()),
    ("Dir1_Y", pa.float32()),
    ("Dir1_Z", pa.float32()),
    ("Dir2_X", pa.float32()),
    ("Dir2_Y", pa.float32()),
    ("Dir2_Z", pa.float32()),
    ("Dir3_X", pa.float32()),
    ("Dir3_Y", pa.float32()),
    ("Dir3_Z", pa.float32())
])

_NODAL_REACTIONS_SCHEMA = pa.schema([
    ("ResultId", pa.string()),
    ("NodeNumber", pa.int32()),
    ("ResultCase", pa.int32()),
    ("ResultCaseName", pa.string()),
    ("Rx", pa.float32()),
    ("Ry", pa.float32()),
    ("Rz", pa.float32()),
    ("Rxx", pa.float32()),
    ("Ryy", pa.float32()),
    ("Rzz", pa.float32())
])

_NODAL_DISPLACEMENTS_SCHEMA = pa.schema([
    ("ResultId", pa.string()),
    ("NodeNumber", pa.int32()),
    ("ResultCase", pa.int32()),
    ("ResultCaseName", pa.string()),
    ("Dx", pa.float32()),
    ("Dy", pa.float32()),
    ("Dz", pa.float32()),
    ("Dxx", pa.float32()),
    ("Dyy", pa.float32()),
    ("Dzz", pa.float32())
])

_NODAL_COORDINATES_SCHEMA = pa.schema([
    ("NodeNumber", pa.int32()),
    ("X", pa.float32()),
    ("Y", pa.float32()),
    ("Z", pa.float32())
])

SCHEMAS = {"BeamForces": _BEAM_FORCE_SCHEMA,
           "BeamProperties": _BEAM_PROPERTIES_SCHEMA,
           "NodalReactions": _NODAL_REACTIONS_SCHEMA,
           "NodalDisplacements": _NODAL_DISPLACEMENTS_SCHEMA,
           "NodalCoordinates": _NODAL_COORDINATES_SCHEMA}


def _clear_lists(lists_to_clear: tuple):
    """Convenience function for clearing lists."""
    for lst in lists_to_clear:
        lst.clear()


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
def sql_insert_nodal_reactions(conn: Connection, cursor: Cursor, uID, primary_combo_count: ctypes.c_int,
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
def sql_insert_nodal_displacements(conn: Connection, cursor: Cursor, uID, primary_combo_count, secondary_combo_count):

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
def sql_insert_nodal_coordinates(conn: Connection, cursor: Cursor, uID):

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
def sql_insert_beam_properties(conn: Connection, cursor: Cursor, uID):

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
def sql_insert_beam_forces(conn: Connection, cursor: Cursor, uID, primary_combo_count, secondary_combo_count):
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


def parquet_insert_nodal_coordinates(uID, directory: pathlib.Path):

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
                array = list(pa.array(data) for data in lists_to_process)
                table = pa.Table.from_arrays(array, schema=SCHEMAS["NodalCoordinates"])
                writer.write_table(table)
                _clear_lists(lists_to_process)

        array = list(pa.array(data) for data in lists_to_process)
        table = pa.Table.from_arrays(array, schema=SCHEMAS["NodalCoordinates"])
        writer.write_table(table)
        _clear_lists(lists_to_process)

    print("Nodal coordinates written to DB.")


def parquet_insert_nodal_reactions(uID, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int,
                                   directory: pathlib.Path):

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
                array = list(pa.array(data) for data in lists_to_process)
                table = pa.Table.from_arrays(array, schema=SCHEMAS["NodalReactions"])
                writer.write_table(table)
                _clear_lists(lists_to_process)

        array = list(pa.array(data) for data in lists_to_process)
        table = pa.Table.from_arrays(array, schema=SCHEMAS["NodalReactions"])
        writer.write_table(table)
        _clear_lists(lists_to_process)

        print("Nodal reactions written to DB.")


def parquet_insert_nodal_displacements(uID, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int,
                                       directory: pathlib.Path):

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
                array = list(pa.array(data) for data in lists_to_process)
                table = pa.Table.from_arrays(array, schema=SCHEMAS["NodalDisplacements"])
                writer.write_table(table)
                _clear_lists(lists_to_process)

        array = list(pa.array(data) for data in lists_to_process)
        table = pa.Table.from_arrays(array, schema=SCHEMAS["NodalDisplacements"])
        writer.write_table(table)
        _clear_lists(lists_to_process)

    print("Nodal displacements written to DB.")


def parquet_insert_beam_properties(uID, directory: pathlib.Path):
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
                array = list(pa.array(data) for data in lists_to_process)
                table = pa.Table.from_arrays(array, schema=SCHEMAS["BeamProperties"])
                writer.write_table(table)
                _clear_lists(lists_to_process)

        # We write one last time for any remaining data in the lists
        array = list(pa.array(data) for data in lists_to_process)
        table = pa.Table.from_arrays(array, schema=SCHEMAS["BeamProperties"])
        writer.write_table(table)
        _clear_lists(lists_to_process)

    print("Beam attributes and properties written to DB.")


def parquet_insert_beam_forces(uID, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int,
                               directory: pathlib.Path):
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
                array = list(pa.array(data) for data in lists_to_process)
                table = pa.Table.from_arrays(array, schema=SCHEMAS["BeamForces"])
                writer.write_table(table)
                _clear_lists(lists_to_process)

        # We write one last time for any remaining data in the lists
        array = list(pa.array(data) for data in
                     (result_ids, beam_numbers, case_numbers, case_names, position_results, fxs, fys, fzs, mxs, mys, mzs))
        table = pa.Table.from_arrays(array, schema=SCHEMAS["BeamForces"])
        writer.write_table(table)
        _clear_lists(lists_to_process)

    print("Beam force results written to DB.")


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
def extract_nodal_reactions(uID, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for result_case in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, result_case, case_name, St7.kMaxStrLen)

        case_name_string = str(case_name.value.decode())
        print(f"Extracting node reactions for load case {case_name_string}...")

        for node in range(1, nNodes.value + 1):

            reaction_array = ctypes.c_double * 6
            reactions = reaction_array()

            St7.St7GetNodeResult(uID, St7.rtNodeReact, node, result_case, reactions)
            result_id = f"{node}-{result_case}"
            fx = float(reactions[0])
            fy = float(reactions[1])
            fz = float(reactions[2])
            mx = float(reactions[3])
            my = float(reactions[4])
            mz = float(reactions[5])

            result = (result_id, node, result_case, case_name_string, fx, fy, fz, mx, my, mz)

            yield result

    print("Nodal reactions written to DB.")


# Function to extract nodal displacements
def extract_nodal_displacements(uID, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for result_case in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, result_case, case_name, St7.kMaxStrLen)
        print(f"Extracting node displacements for load case {case_name.value.decode()}...")

        for node in range(1, nNodes.value + 1):

            displacement_array = ctypes.c_double * 6
            displacements = displacement_array()

            St7.St7GetNodeResult(uID, St7.rtNodeDisp, node, result_case, displacements)
            result_id = f"{node}-{result_case}"
            dx = displacements[0]
            dy = displacements[1]
            dz = displacements[2]
            dxx = displacements[3]
            dyy = displacements[4]
            dzz = displacements[5]

            result = (result_id, node, result_case, case_name.value.decode(), dx, dy, dz, dxx, dyy, dzz)
            yield result


# Function to extract nodal coordinates
def extract_nodal_coordinates(uID):

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
def extract_beam_properties(uID):

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

        result = (beam, node1, node2, length, property_name.value.decode(),
                  group_name.value.decode(), id_number.value, dir1_x, dir1_y, dir1_z,
                  dir2_x, dir2_y, dir2_z, dir3_x, dir3_y, dir3_z)
        yield result


# Function to extract the beam force results
def extract_beam_forces(uID, primary_combo_count: ctypes.c_int, secondary_combo_count: ctypes.c_int):

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
def extract_beam_displacements(conn: Connection, cursor: Cursor, uID, primary_combo_count: ctypes.c_int,
                               secondary_combo_count: ctypes.c_int):
    nBeams = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyBEAM, ctypes.byref(nBeams))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    # The following ensures that the result positions are output as a ratio of the overall member length (0.0...1.0)
    St7.St7SetBeamResultPosMode(uID, St7.bpParam)

    num_stations_requested = 5

    # Shifted beam results outside the result case loop - transactions will occur once at the end rather than after
    # every result case, which should enhance performance
    beam_results = []
    number_of_cases = primary_combo_count.value + secondary_combo_count.value
    for result_case in range(1, number_of_cases + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, result_case, case_name, St7.kMaxStrLen)
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
            St7.St7GetBeamResultArrayPos(uID, St7.rtBeamDisp, St7.stBeamPrincipal, beam, result_case,
                                         num_stations_requested, positions, ctypes.byref(number_columns), displacements)

            # Access the forces from each beam at each station position, and add these to the result list
            for i in range(num_stations_requested):
                position = f"{position_values[i]:.2f}"
                dx = displacements[(i * 6) + 0]
                dy = displacements[(i * 6) + 1]
                dz = displacements[(i * 6) + 2]
                rx = displacements[(i * 6) + 3]
                ry = displacements[(i * 6) + 4]
                rz = displacements[(i * 6) + 5]
                sid = f"{beam}-{result_case}-{position}"
                result = (sid, beam, result_case, case_name.value.decode(), float(position), dx, dy, dz, rx, ry, rz)
                beam_results.append(result)

        # Insert the beam dispalcement results into the database
        if len(beam_results) == 0:
            print("Warning: Beam displacement result set is empty.")
        else:
            # Implementing smarter batching
            if result_case % 100 == 0 or result_case == number_of_cases:
                sql_insert_beam_displacements(conn, cursor, beam_results)
                beam_results.clear()

    print("Beam displacement results written to DB.")


# Main function for extracting results
def extract_model_data(model_file: str, result_file: str, db_fp: str, scratch_path: str, parquet=False, directory=None):

    # Initialize the Strand7 model
    uID, primary_combo_count, secondary_combo_count = initialize_model(model_file, result_file, scratch_path)

    # Logic for creating the parquet files
    if parquet:
        parquet_insert_nodal_coordinates(uID, directory)
        parquet_insert_nodal_reactions(uID, primary_combo_count, secondary_combo_count, directory)
        parquet_insert_nodal_displacements(uID, primary_combo_count, secondary_combo_count, directory)
        parquet_insert_beam_forces(uID, primary_combo_count, secondary_combo_count, directory)
        parquet_insert_beam_properties(uID, directory)

    # If not running the parquet extraction, the program will extract to a SQLite db
    else:
        with connect(db_fp) as conn:

            cursor = conn.cursor()

            # Ensure the database is ready
            create_sqlite_database(conn, cursor)

            if uID is None:
                pass

            else:

                # Extract nodal reactions and store them in the database
                extract_nodal_reactions(conn, cursor, uID, primary_combo_count, secondary_combo_count)

                # Extract nodal displacements and store them in the database
                extract_nodal_displacements(conn, cursor, uID, primary_combo_count, secondary_combo_count)

                # Extract nodal coordinates and store them in the database
                extract_nodal_coordinates(conn, cursor, uID)

                # Extract the beam properties and store them in the database
                sql_insert_beam_properties(conn, cursor, uID)

                # Extract beam forces and store them in the database
                # Let's change the below logic to use a generator pattern instead
                # This should be efficient
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
    # make sure to delete the empty database cruciform_output_file that it created before
    # rerunning the script.
    # ----------------------------------------------------------------------

    # Do you want it to extract in parquet format?
    parquet = True
    directory = pathlib.Path(r"C:\Users\Josh.Finnin\OneDrive - Arup\Desktop\ALS Versioning Factors\V1_4_4_ALS_Base_Parquet")

    # Create scratch path if not exists
    scratch_folder = f"C:\\Users\\{getuser()}\\Documents\\Changi T5_Database_Scratch"
    if not os.path.exists(scratch_folder):
        os.mkdir(scratch_folder)

    root = tk.Tk()
    root.withdraw()
    model_file = filedialog.askopenfilename(title="Select your Strand7 model file.")
    result_file = filedialog.askopenfilename(title="Select your Strand7 results file.")

    # Provide the path for the output SQLite database cruciform_output_file
    result_name = os.path.splitext(os.path.split(result_file)[1])[0]
    db_fp = filedialog.asksaveasfilename(title="Save Database File As", defaultextension=".db")

    extract_model_data(model_file, result_file, db_fp, scratch_path=scratch_folder, parquet=parquet, directory=directory)

#     nla_dict = {
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\40 ALS Removal S-TR04-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\40 ALS Removal S-TR04-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\40 ALS Removal S-TR04-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\41 ALS Removal S-TR11-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\41 ALS Removal S-TR11-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\41 ALS Removal S-TR11-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\42 ALS Removal S-TR13-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\42 ALS Removal S-TR13-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\42 ALS Removal S-TR13-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\43 ALS Removal S-TR13-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\43 ALS Removal S-TR13-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\43 ALS Removal S-TR13-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\44 ALS Removal S-TR13-03.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\44 ALS Removal S-TR13-03.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\44 ALS Removal S-TR13-03_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\45 ALS Removal S-TR13-04.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\45 ALS Removal S-TR13-04.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\45 ALS Removal S-TR13-04_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\46 ALS Removal S-TR14-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\46 ALS Removal S-TR14-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\46 ALS Removal S-TR14-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\47 ALS Removal S-TR14-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\47 ALS Removal S-TR14-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\47 ALS Removal S-TR14-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\48 ALS Removal S-TR14-03.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\48 ALS Removal S-TR14-03.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\48 ALS Removal S-TR14-03_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\49 ALS Removal S-TR14-04.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\49 ALS Removal S-TR14-04.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\49 ALS Removal S-TR14-04_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\50 ALS Removal S-TR01-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\50 ALS Removal S-TR01-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\50 ALS Removal S-TR01-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\51 ALS Removal S-TR01-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\51 ALS Removal S-TR01-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\51 ALS Removal S-TR01-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\52 ALS Removal S-TR01a-05.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\52 ALS Removal S-TR01a-05.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\52 ALS Removal S-TR01a-05_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\53 ALS Removal S-TR01b-05.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\53 ALS Removal S-TR01b-05.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\53 ALS Removal S-TR01b-05_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\54 ALS Removal S-TR02-03.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\54 ALS Removal S-TR02-03.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\54 ALS Removal S-TR02-03_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\55 ALS Removal S-TR02a-05.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\55 ALS Removal S-TR02a-05.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\55 ALS Removal S-TR02a-05_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\56 ALS Removal S-TR02b-05.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\56 ALS Removal S-TR02b-05.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\56 ALS Removal S-TR02b-05_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\57 ALS Removal S-TR04-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\57 ALS Removal S-TR04-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\57 ALS Removal S-TR04-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\58 ALS Removal S-TR05-03.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\58 ALS Removal S-TR05-03.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\58 ALS Removal S-TR05-03_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\59 ALS Removal S-TR06-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\59 ALS Removal S-TR06-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\59 ALS Removal S-TR06-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\60 ALS Removal S-TR06-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\60 ALS Removal S-TR06-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\60 ALS Removal S-TR06-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\61 ALS Removal S-TR06-03.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\61 ALS Removal S-TR06-03.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\61 ALS Removal S-TR06-03_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\62 ALS Removal S-TR07-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\62 ALS Removal S-TR07-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\62 ALS Removal S-TR07-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\63 ALS Removal S-TR07-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\63 ALS Removal S-TR07-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\63 ALS Removal S-TR07-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\64 ALS Removal S-TR07-03.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\64 ALS Removal S-TR07-03.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\64 ALS Removal S-TR07-03_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\65 ALS Removal S-TR08-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\65 ALS Removal S-TR08-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\65 ALS Removal S-TR08-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\66 ALS Removal S-TR11-02.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\66 ALS Removal S-TR11-02.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\66 ALS Removal S-TR11-02_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\67 ALS Removal S-TR12-01.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\67 ALS Removal S-TR12-01.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\67 ALS Removal S-TR12-01_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\68 ALS Removal TR01a-04.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\68 ALS Removal TR01a-04.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\68 ALS Removal TR01a-04_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\69 ALS Removal TR01b-04.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\69 ALS Removal TR01b-04.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\69 ALS Removal TR01b-04_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\70 ALS Removal TR02a-04.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\70 ALS Removal TR02a-04.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\70 ALS Removal TR02a-04_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\71 ALS Removal TR02b-04.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\71 ALS Removal TR02b-04.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\71 ALS Removal TR02b-04_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\72 ALS Removal CHB1-T1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\72 ALS Removal CHB1-T1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\72 ALS Removal CHB1-T1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\73 ALS Removal CHB1-T2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\73 ALS Removal CHB1-T2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\73 ALS Removal CHB1-T2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\74 ALS Removal CHB1-T3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\74 ALS Removal CHB1-T3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\74 ALS Removal CHB1-T3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\75 ALS Removal CHB1-T4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\75 ALS Removal CHB1-T4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\75 ALS Removal CHB1-T4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\76 ALS Removal CHB1-B1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\76 ALS Removal CHB1-B1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\76 ALS Removal CHB1-B1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\77 ALS Removal CHB1-B2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\77 ALS Removal CHB1-B2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\77 ALS Removal CHB1-B2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\78 ALS Removal CHB1-B3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\78 ALS Removal CHB1-B3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\78 ALS Removal CHB1-B3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\79 ALS Removal CHB1-B4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\79 ALS Removal CHB1-B4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\79 ALS Removal CHB1-B4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\80 ALS Removal CHB1-D1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\80 ALS Removal CHB1-D1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\80 ALS Removal CHB1-D1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\81 ALS Removal CHB1-D2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\81 ALS Removal CHB1-D2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\81 ALS Removal CHB1-D2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\82 ALS Removal CHB1-D3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\82 ALS Removal CHB1-D3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\82 ALS Removal CHB1-D3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\83 ALS Removal CHB1-D4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\83 ALS Removal CHB1-D4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\83 ALS Removal CHB1-D4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\84 ALS Removal CHB2-T1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\84 ALS Removal CHB2-T1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\84 ALS Removal CHB2-T1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\85 ALS Removal CHB2-T2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\85 ALS Removal CHB2-T2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\85 ALS Removal CHB2-T2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\86 ALS Removal CHB2-T3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\86 ALS Removal CHB2-T3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\86 ALS Removal CHB2-T3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\87 ALS Removal CHB2-T4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\87 ALS Removal CHB2-T4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\87 ALS Removal CHB2-T4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\88 ALS Removal CHB2-B1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\88 ALS Removal CHB2-B1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\88 ALS Removal CHB2-B1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\89 ALS Removal CHB2-B2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\89 ALS Removal CHB2-B2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\89 ALS Removal CHB2-B2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\90 ALS Removal CHB2-B3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\90 ALS Removal CHB2-B3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\90 ALS Removal CHB2-B3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\91 ALS Removal CHB2-B4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\91 ALS Removal CHB2-B4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\91 ALS Removal CHB2-B4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\92 ALS Removal CHB2-D1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\92 ALS Removal CHB2-D1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\92 ALS Removal CHB2-D1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\93 ALS Removal CHB2-D2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\93 ALS Removal CHB2-D2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\93 ALS Removal CHB2-D2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\94 ALS Removal CHB2-D3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\94 ALS Removal CHB2-D3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\94 ALS Removal CHB2-D3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\95 ALS Removal CHB2-D4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\95 ALS Removal CHB2-D4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\95 ALS Removal CHB2-D4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\96 ALS Removal CHC2-T1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\96 ALS Removal CHC2-T1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\96 ALS Removal CHC2-T1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\97 ALS Removal CHC2-T2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\97 ALS Removal CHC2-T2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\97 ALS Removal CHC2-T2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\98 ALS Removal CHC2-T3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\98 ALS Removal CHC2-T3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\98 ALS Removal CHC2-T3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\99 ALS Removal CHC2-T4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\99 ALS Removal CHC2-T4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\99 ALS Removal CHC2-T4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\100 ALS Removal CHC2-B1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\100 ALS Removal CHC2-B1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\100 ALS Removal CHC2-B1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\101 ALS Removal CHC2-B2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\101 ALS Removal CHC2-B2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\101 ALS Removal CHC2-B2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\102 ALS Removal CHC2-B3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\102 ALS Removal CHC2-B3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\102 ALS Removal CHC2-B3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\103 ALS Removal CHC2-B4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\103 ALS Removal CHC2-B4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\103 ALS Removal CHC2-B4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\104 ALS Removal CHC2-D1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\104 ALS Removal CHC2-D1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\104 ALS Removal CHC2-D1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\105 ALS Removal CHC2-D2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\105 ALS Removal CHC2-D2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\105 ALS Removal CHC2-D2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\106 ALS Removal CHC2-D3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\106 ALS Removal CHC2-D3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\106 ALS Removal CHC2-D3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\107 ALS Removal CHC2-D4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\107 ALS Removal CHC2-D4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\107 ALS Removal CHC2-D4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\108 ALS Removal CHC1-T1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\108 ALS Removal CHC1-T1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\108 ALS Removal CHC1-T1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\109 ALS Removal CHC1-T2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\109 ALS Removal CHC1-T2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\109 ALS Removal CHC1-T2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\110 ALS Removal CHC1-T3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\110 ALS Removal CHC1-T3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\110 ALS Removal CHC1-T3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\111 ALS Removal CHC1-T4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\111 ALS Removal CHC1-T4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\111 ALS Removal CHC1-T4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\112 ALS Removal CHC1-B1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\112 ALS Removal CHC1-B1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\112 ALS Removal CHC1-B1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\113 ALS Removal CHC1-B2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\113 ALS Removal CHC1-B2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\113 ALS Removal CHC1-B2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\114 ALS Removal CHC1-B3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\114 ALS Removal CHC1-B3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\114 ALS Removal CHC1-B3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\115 ALS Removal CHC1-B4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\115 ALS Removal CHC1-B4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\115 ALS Removal CHC1-B4_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\116 ALS Removal CHC1-D1.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\116 ALS Removal CHC1-D1.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\116 ALS Removal CHC1-D1_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\117 ALS Removal CHC1-D2.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\117 ALS Removal CHC1-D2.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\117 ALS Removal CHC1-D2_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\118 ALS Removal CHC1-D3.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\118 ALS Removal CHC1-D3.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\118 ALS Removal CHC1-D3_Parquet"),
# r"D:\Projects\Changi T5\MUC\Strand7 Model Data\119 ALS Removal CHC1-D4.NLA": (r"D:\Projects\Changi T5\MUC\Strand7 Model Data\119 ALS Removal CHC1-D4.st7", r"D:\Projects\Changi T5\MUC\Strand7 Model Data\119 ALS Removal CHC1-D4_Parquet")}
#
#     p = "Something"
#
#     for k, v in nla_dict.items():
#         if not os.path.exists(v[1]):
#             os.mkdir(v[1])
#         extract_model_data(v[0], k, p, scratch_path=scratch_folder, parquet=parquet, directory=pathlib.Path(v[1]))
#         time.sleep(1)


