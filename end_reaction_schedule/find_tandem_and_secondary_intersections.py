import duckdb
import pathlib

beam_properties_parq = r"E:\Projects\Changi\beam_properties.parquet"

with duckdb.connect() as conn:
    query = f"""WITH SECONDARY_TRUSS_NODES AS 
                (SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%SecondaryTop%'
                OR GroupName LIKE '%SecondaryBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%SecondaryTop%'
                OR GroupName LIKE '%SecondaryBot%'),

                PRIMARY_TRUSS_NODES AS (
                SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%PrimaryTop%'
                OR GroupName LIKE '%PrimaryBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%PrimaryTop%'
                OR GroupName LIKE '%PrimaryBot%')

                SELECT DISTINCT PTN.NodeNumber
                FROM PRIMARY_TRUSS_NODES AS PTN
                JOIN SECONDARY_TRUSS_NODES AS STN ON PTN.NodeNumber = STN.NodeNumber
                ORDER BY PTN.NodeNumber
                """

    results = conn.execute(query).fetchall()

    for result in results:
        print("\t".join(str(r) for r in result))

    print(";".join(str(r[0]) for r in results))
