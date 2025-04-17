
"""
database_extractor.py

Module to extract the analysis results from a Strand7 model into a SQLite database.
"""

import ctypes
from sqlite3 import Connection, Cursor, connect
import os
import tkinter as tk
from tkinter import filedialog

# Import the St7API module
import St7API as St7


# Function to create a database and table
def create_database(conn: Connection, cursor: Cursor):

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
            GroupName TEXT
        )
    ''')

    cursor.execute("""CREATE INDEX idx_beam_attributes_propertyname ON BeamProperties(PropertyName, GroupName);""")

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
def insert_nodal_reactions(conn: Connection, cursor: Cursor, nodal_results: list):

    insertion_query = """
            INSERT INTO NodalReactions (ResultId, NodeNumber, ResultCase, ResultCaseName, ReactionX, ReactionY, ReactionZ, ReactionXX, ReactionYY, ReactionZZ)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    cursor.executemany(insertion_query, nodal_results)

    conn.commit()


# Function to insert nodal displacements into the database
def insert_nodal_displacements(conn: Connection, cursor: Cursor, nodal_results: list):

    insertion_query = """
        INSERT INTO NodalDisplacements (ResultId, NodeNumber, ResultCase, ResultCaseName, DisplacementX, DisplacementY, DisplacementZ, RotationXX, RotationYY, RotationZZ)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insertion_query, nodal_results)
    conn.commit()


# Function to insert nodal coordinates into the database
def insert_nodal_coordinates(conn: Connection, cursor: Cursor, nodal_results: list):

    insertion_query = """INSERT INTO NodalCoordinates (NodeNumber, X, Y, Z)
    VALUES (?, ?, ?, ?)"""
    cursor.executemany(insertion_query, nodal_results)
    conn.commit()


# Function to insert element properties into the database
def insert_beam_properties(conn: Connection, cursor: Cursor, beam_results: list):

    insertion_query = """INSERT INTO BeamProperties (BeamNumber, N1, N2, Length, PropertyName, GroupName)
    VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insertion_query, beam_results)
    conn.commit()


# Function to insert element forces into the database
def insert_beam_forces(conn: Connection, cursor: Cursor, beam_results: list):

    insertion_query = """INSERT INTO BeamForces (ResultId, BeamNumber, ResultCase, ResultCaseName, Position, Fx, Fy, Fz, Mx, My, Mz)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insertion_query, beam_results)

    conn.commit()


# Function to insert element displacements into the database
def insert_beam_displacements(conn: Connection, cursor: Cursor, beam_results: list):

    insertion_query = """INSERT INTO BeamDisplacements (ResultId, BeamNumber, ResultCase, ResultCaseName, Position, Dx, Dy, Dz, Rx, Ry, Rz)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insertion_query, beam_results)

    conn.commit()


# Initialize Strand7 model
def initialize_model(model_file: str, result_file: str):
    uID = ctypes.c_int(1)  # Unique identifier for the model
    St7.St7Init()
    p_combo_count = ctypes.c_int(0)
    s_combo_count = ctypes.c_int(0)
    try:  # This try block is essential for avoiding getting stuck if the API call fails
        St7.St7OpenFile(uID, model_file.encode('utf-8'), r'C:\Users\Josh.Finnin\Documents\Projects\Changi T5\Database Files'.encode())
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
def extract_nodal_reactions(conn: Connection, cursor: Cursor, uID, primary_combo_count: ctypes.c_int,
                            secondary_combo_count: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    nodal_results = []
    for result_case in range(1, primary_combo_count.value + secondary_combo_count.value + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, result_case, case_name, St7.kMaxStrLen)

        print(f"Extracting node reactions for load case {case_name.value.decode()}...")

        for node in range(1, nNodes.value + 1):

            reaction_array = ctypes.c_double * 6
            reactions = reaction_array()

            St7.St7GetNodeResult(uID, St7.rtNodeReact, node, result_case, reactions)
            result_id = f"{node}-{result_case}"
            fx = reactions[0]
            fy = reactions[1]
            fz = reactions[2]
            mx = reactions[3]
            my = reactions[4]
            mz = reactions[5]

            nodal_results.append((result_id, node, result_case, case_name.value.decode(), fx, fy, fz, mx, my, mz))

    # Insert the reactions into the SQLite database
    insert_nodal_reactions(conn, cursor, nodal_results)
    print("Nodal reactions written to DB.")

    # Having issues running into memory limits, so let's try deleting the nodal results after they are written to the DB
    del nodal_results


# Function to extract nodal displacements
def extract_nodal_displacements(conn: Connection, cursor: Cursor, uID, primary_combo_count: ctypes.c_int,
                                secondary_combo_count: ctypes.c_int):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    nLoadCases = ctypes.c_int(0)
    St7.St7GetNumLoadCase(uID, ctypes.byref(nLoadCases))

    nodal_results = []
    for result_case in range(1, primary_combo_count.value + secondary_combo_count.value + 1):

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
            rx = displacements[3]
            ry = displacements[4]
            rz = displacements[5]

            nodal_results.append((result_id, node, result_case, case_name.value.decode(), dx, dy, dz, rx, ry, rz))

    # Insert the reactions into the SQLite database
    insert_nodal_displacements(conn, cursor, nodal_results)
    print("Nodal displacements written to DB.")

    # Having issues running into memory limits, so let's try deleting the nodal results after they are written to the DB
    del nodal_results


# Function to extract nodal coordinates
def extract_nodal_coordinates(conn: Connection, cursor: Cursor, uID):

    nNodes = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyNODE, ctypes.byref(nNodes))

    print("Extracting nodal coordinates...")

    node_coordinate_array = ctypes.c_double * 3
    node_coordinates = node_coordinate_array()

    node_results = []
    for node in range(1, nNodes.value + 1):
        St7.St7GetNodeXYZ(uID, node, node_coordinates)

        x_coord = node_coordinates[0]
        y_coord = node_coordinates[1]
        z_coord = node_coordinates[2]

        result = (node, x_coord, y_coord, z_coord)
        node_results.append(result)

    if len(node_results) == 0:
        pass
    else:
        insert_nodal_coordinates(conn, cursor, node_results)

    print("Nodal coordinates written to DB.")


# Function to extract beam attributes and properties
def extract_beam_properties(conn: Connection, cursor: Cursor, uID):

    nBeams = ctypes.c_int(0)
    St7.St7GetTotal(uID, St7.tyBEAM, ctypes.byref(nBeams))

    print("Extracting beam attributes and properties...")

    beam_results = []
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

        # Access the beam geometric data
        element_data = ctypes.c_double * 3
        element_data_array = element_data()
        St7.St7GetElementData(uID, St7.tyBEAM, beam, 0, element_data_array)

        node1 = connections[1]
        node2 = connections[2]
        length = element_data_array[0]

        result = (beam, node1, node2, length, property_name.value.decode(), group_name.value.decode())
        beam_results.append(result)

    # Insert the beam force results into the database
    if len(beam_results) == 0:
        pass
    else:
        insert_beam_properties(conn, cursor, beam_results)

    print("Beam attributes and properties written to DB.")


# Function to extract the beam force results
def extract_beam_forces(conn: Connection, cursor: Cursor, uID, primary_combo_count: ctypes.c_int,
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

    for result_case in range(1, primary_combo_count.value + secondary_combo_count.value + 1):

        case_name = ctypes.create_string_buffer(St7.kMaxStrLen)
        St7.St7GetResultCaseName(uID, result_case, case_name, St7.kMaxStrLen)
        print(f"Extracting beam forces for result case {case_name.value.decode()}...")

        for beam in range(1, nBeams.value + 1):

            # Number of result columns (i.e. fields)
            number_columns = ctypes.c_int(0)

            force_array = ctypes.c_double * (num_stations_requested * St7.kMaxBeamResult)
            forces = force_array()

            # Station positions along the element for querying loads
            position_values = [0.0, 0.25, 0.5, 0.75, 1.0]
            position_values_c = [ctypes.c_double(p) for p in position_values]
            pos_array = ctypes.c_double * len(position_values_c)
            positions = pos_array(*position_values_c)

            # Get the beam results using the Strand API
            St7.St7GetBeamResultArrayPos(uID, St7.rtBeamForce, St7.stBeamLocal, beam, result_case,
                                         num_stations_requested, positions, ctypes.byref(number_columns), forces)

            # Access the forces from each beam at each station position, and add these to the result list
            for i in range(num_stations_requested):
                position = f"{position_values[i]:.2f}"
                fx = forces[(i * 6) + St7.ipBeamAxialF]
                fy = forces[(i * 6) + St7.ipBeamSFx]
                fz = forces[(i * 6) + St7.ipBeamSFy]
                mx = forces[(i * 6) + St7.ipBeamTorque]
                my = forces[(i * 6) + St7.ipBeamBMy]
                mz = forces[(i * 6) + St7.ipBeamBMx]
                sid = f"{beam}-{result_case}-{position}"
                result = (sid, beam, result_case, case_name.value.decode(), float(position), fx, fy, fz, mx, my, mz)
                beam_results.append(result)

    # Insert the beam force results into the database
    if len(beam_results) == 0:
        print("Warning: Beam force result set is empty.")
    else:
        insert_beam_forces(conn, cursor, beam_results)

    print("Beam force results written to DB.")


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

    for result_case in range(1, primary_combo_count.value + secondary_combo_count.value + 1):

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
            St7.St7GetBeamResultArrayPos(uID, St7.rtBeamDisp, St7.stBeamLocal, beam, result_case,
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

    # Insert the beam force results into the database
    if len(beam_results) == 0:
        print("Warning: Beam displacement result set is empty.")
    else:
        insert_beam_displacements(conn, cursor, beam_results)

    print("Beam displacement results written to DB.")


# Main function for extracting results
def extract_model_data(model_file: str, result_file: str, db_fp: str):

    conn = connect(db_fp)
    cursor = conn.cursor()

    # Ensure the database is ready
    create_database(conn, cursor)

    # Initialize the Strand7 model
    uID, primary_combo_count, secondary_combo_count = initialize_model(model_file, result_file)

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
        extract_beam_properties(conn, cursor, uID)

        # Extract beam forces and store them in the database
        extract_beam_forces(conn, cursor, uID, primary_combo_count, secondary_combo_count)

        # Extract beam displacements and store them in the database
        extract_beam_displacements(conn, cursor, uID, primary_combo_count, secondary_combo_count)

        # Close the Strand7 model
        St7.St7CloseResultFile(uID)
        St7.St7CloseFile(uID)
        St7.St7Release()

    conn.close()


if __name__ == '__main__':

    root = tk.Tk()
    root.withdraw()
    model_file = filedialog.askopenfilename(title="Select your model file.")
    result_file = filedialog.askopenfilename(title="Select your results file.")

    # Provide the path for the output SQLite database file
    result_name = os.path.splitext(os.path.split(result_file)[1])[0]
    db_fp = filedialog.asksaveasfilename(title="Save Database File As", defaultextension=".db")

    extract_model_data(model_file, result_file, db_fp)


