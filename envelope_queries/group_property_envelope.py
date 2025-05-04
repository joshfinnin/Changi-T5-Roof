""""
Script to export the envelope results for each property from the Strand7 analysis result databases.
"""

from sqlite3 import *
import os
import csv


def process_result(value: float) -> float:
    result = round(value, 2)
    return result


def process_absolute(value: float) -> float:
    result = abs(round(value, 2))
    return result


if __name__ == '__main__':
    # ----------------------------------------------------------------------
    # SPECIFY INPUT FILE PATHS
    # ----------------------------------------------------------------------

    input_directory = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.9"
    db_files = [r"V1_3_9_LB_Gmax.db",
                r"V1_3_9_LB_Gmin.db",
                r"V1_3_9_UB_Gmax.db",
                r"V1_3_9_UB_Gmin.db"]

    output_fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.9\2025-05-04 Group_Property_Envelope_Results.csv"

    file_paths = [os.path.join(input_directory, db) for db in db_files]

    # ----------------------------------------------------------------------
    # ESTABLISH CONNECTION WITH DATABASE FILES
    # ----------------------------------------------------------------------

    # Envelope query called on the combined SQLite connection
    envelope_query = """ WITH ABS_ENV AS (
    SELECT
    GroupName,
    PropertyName,
    MAX(Fx) AS Fx,
    MAX(Fy) AS Fy,
    MAX(Fz) AS Fz,
    MAX(Mx) AS Mx,
    MAX(My) AS My,
    MAX(Mz) AS Mz
    FROM BeamForces AS BF
    JOIN BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL

    SELECT
    GroupName,
    PropertyName,
    MIN(Fx) AS Fx,
    MIN(Fy) AS Fy,
    MIN(Fz) AS Fz,
    MIN(Mx) AS Mx,
    MIN(My) AS My,
    MIN(Mz) AS Mz
    FROM BeamForces AS BF
    JOIN BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL 

    SELECT
    GroupName,
    PropertyName,
    MAX(Fx) AS Fx,
    MAX(Fy) AS Fy,
    MAX(Fz) AS Fz,
    MAX(Mx) AS Mx,
    MAX(My) AS My,
    MAX(Mz) AS Mz
    FROM db2.BeamForces AS BF
    JOIN db2.BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL 

    SELECT
    GroupName,
    PropertyName,
    MIN(Fx) AS Fx,
    MIN(Fy) AS Fy,
    MIN(Fz) AS Fz,
    MIN(Mx) AS Mx,
    MIN(My) AS My,
    MIN(Mz) AS Mz
    FROM db2.BeamForces AS BF
    JOIN db2.BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL

    SELECT
    GroupName,
    PropertyName,
    MAX(Fx) AS Fx,
    MAX(Fy) AS Fy,
    MAX(Fz) AS Fz,
    MAX(Mx) AS Mx,
    MAX(My) AS My,
    MAX(Mz) AS Mz
    FROM db3.BeamForces AS BF
    JOIN db3.BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL

    SELECT
    GroupName,
    PropertyName,
    MIN(Fx) AS Fx,
    MIN(Fy) AS Fy,
    MIN(Fz) AS Fz,
    MIN(Mx) AS Mx,
    MIN(My) AS My,
    MIN(Mz) AS Mz
    FROM db3.BeamForces AS BF
    JOIN db3.BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL

    SELECT
    GroupName,
    PropertyName,
    MAX(Fx) AS Fx,
    MAX(Fy) AS Fy,
    MAX(Fz) AS Fz,
    MAX(Mx) AS Mx,
    MAX(My) AS My,
    MAX(Mz) AS Mz
    FROM db4.BeamForces AS BF
    JOIN db4.BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName

    UNION ALL

    SELECT
    GroupName,
    PropertyName,
    MIN(Fx) AS Fx,
    MIN(Fy) AS Fy,
    MIN(Fz) AS Fz,
    MIN(Mx) AS Mx,
    MIN(My) AS My,
    MIN(Mz) AS Mz
    FROM db4.BeamForces AS BF
    JOIN db4.BeamProperties AS BP ON BP.BeamNumber = BF.BeamNumber 
    GROUP BY GroupName, PropertyName
    )

    SELECT
    GroupName,
    PropertyName,
    process_result(MAX(Fx)),
    process_result(MAX(Fy)),
    process_result(MAX(Fz)),
    process_result(MAX(Mx)),
    process_result(MAX(My)),
    process_result(MAX(Mz))
    FROM ABS_ENV
    GROUP BY GroupName, PropertyName

    UNION ALL

    SELECT
    GroupName,
    PropertyName,
    process_result(MIN(Fx)),
    process_result(MIN(Fy)),
    process_result(MIN(Fz)),
    process_result(MIN(Mx)),
    process_result(MIN(My)),
    process_result(MIN(Mz))
    FROM ABS_ENV
    GROUP BY GroupName, PropertyName
    ;
    """

    with open(output_fp, 'w+', newline="", encoding='utf-8') as out_file:

        connection = connect(file_paths[0])
        connection.create_function("process_result", 1, process_result)

        cursor = connection.cursor()

        # Priorize RAM if possible to speed up the query
        cursor.execute("""PRAGMA temp_store=1;""")

        # Attach all of the additional databases to the first database
        for i, fp in enumerate(file_paths[1:]):
            attach_query = f"ATTACH DATABASE '{fp}' AS db{i + 2};"
            cursor.execute(attach_query)

        results = cursor.execute(envelope_query).fetchall()

        # Write the results of the envelope query to a CSV file
        headers = ["GroupName", "PropertyName", "Fx", "Fy", "Fz", "Mx", "My", "Mz"]
        writer = csv.writer(out_file)
        writer.writerow(headers)
        writer.writerows(results)


