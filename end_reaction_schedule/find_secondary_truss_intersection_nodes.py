import duckdb

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
                OR GroupName LIKE '%SecondaryBot%')

                SELECT NodeNumber, Count(NodeNumber) AS Chords
                FROM SECONDARY_TRUSS_NODES
                GROUP BY NodeNumber
                HAVING Chords > 2
                ORDER BY NodeNumber
                """

    results = conn.execute(query).fetchall()

    for result in results:
        print("\t".join(str(r) for r in result))

    print(";".join(str(r[0]) for r in results))
