import duckdb

beam_properties_parq = r"E:\Projects\Changi\beam_properties.parquet"

with duckdb.connect() as conn:
    query = f"""WITH PRIMARY_TRUSS_NODES AS 
                (SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%PrimaryTop%'
                OR GroupName LIKE '%PrimaryBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%PrimaryTop%'
                OR GroupName LIKE '%PrimaryBot%'),
                
                BRACING_PURLIN_NODES AS (SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%BracingPlanTop%'
                OR GroupName LIKE '%BracingPlanBot%'
                OR GroupName LIKE '%PurlinTop%'
                OR GroupName LIKE '%PurlinBot%'
                OR GroupName LIKE '%LiftingBeam%'
                
                UNION ALL
                
                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%BracingPlanTop%'
                OR GroupName LIKE '%BracingPlanBot%'
                OR GroupName LIKE '%PurlinTop%'
                OR GroupName LIKE '%PurlinBot%'
                OR GroupName LIKE '%LiftingBeam%'),

                EDGE_TRUSS_NODES AS (
                SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%EdgeTrussTop%'
                OR GroupName LIKE '%EdgeTrussBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%EdgeTrussTop%'
                OR GroupName LIKE '%EdgeTrussBot%'),

                SECONDARY_TRUSS_NODES AS (
                SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%SecondaryTop%'
                OR GroupName LIKE '%SecondaryBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%SecondaryTop%'
                OR GroupName LIKE '%SecondaryBot%'),

                INTERSECTION_NODES AS (
                SELECT PTN.NodeNumber
                FROM PRIMARY_TRUSS_NODES AS PTN
                JOIN SECONDARY_TRUSS_NODES AS STN ON STN.NodeNumber = PTN.NodeNumber

                UNION ALL

                SELECT PTN.NodeNumber
                FROM PRIMARY_TRUSS_NODES AS PTN
                JOIN EDGE_TRUSS_NODES AS ETN ON ETN.NodeNumber = PTN.NodeNumber
                ),
                
                TANDEM_TRUSS_CHORDS AS 
                (SELECT NodeNumber, COUNT(NodeNumber) AS Chords FROM (SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%PrimaryTop%'
                OR GroupName LIKE '%PrimaryBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%PrimaryTop%'
                OR GroupName LIKE '%PrimaryBot%')
                GROUP BY NodeNumber
                HAVING Chords > 2
                ),

                TANDEM_TRUSS_DIAGS AS 
                (SELECT NodeNumber, COUNT(NodeNumber) AS Members FROM (SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%PrimaryDiag%'
                OR GroupName LIKE '%PrimaryVert%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%PrimaryDiag%'
                OR GroupName LIKE '%PrimaryVert%')
                GROUP BY NodeNumber
                )

                SELECT PTN.NodeNumber, COUNT(PTN.NodeNumber) AS Members
                FROM PRIMARY_TRUSS_NODES AS PTN
                WHERE PTN.NodeNumber NOT IN (SELECT * FROM INTERSECTION_NODES)
                AND PTN.NodeNumber NOT IN (SELECT NodeNumber FROM TANDEM_TRUSS_DIAGS)
                AND PTN.NodeNumber IN (SELECT * FROM BRACING_PURLIN_NODES)
                AND PTN.NodeNumber NOT IN (SELECT NodeNumber FROM TANDEM_TRUSS_CHORDS)
                GROUP BY PTN.NodeNumber
                ORDER BY PTN.NodeNumber
                """

    results = conn.execute(query).fetchall()

    for result in results:
        print("\t".join(str(r) for r in result))

    print(";".join(str(r[0]) for r in results))


