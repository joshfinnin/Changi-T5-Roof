
import duckdb

beam_properties_parq = r"E:\Projects\Changi\beam_properties.parquet"
bif_parq = r"E:\Projects\Changi\MUC\Strand7 Model\V1_4_5\Tandem Truss Splice Reactions\Parquet Files\12 ALS Removal P-TR03a-01_BIF_filtered.parquet"

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

                EDGE_TRUSS_NODES AS (
                SELECT N1 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP1
                WHERE GroupName LIKE '%EdgeTrussTop%'
                OR GroupName LIKE '%EdgeTrussBot%'

                UNION ALL

                SELECT N2 AS NodeNumber
                FROM '{beam_properties_parq}' AS BP2
                WHERE GroupName LIKE '%EdgeTrussTop%'
                OR GroupName LIKE '%EdgeTrussBot%')

                SELECT DISTINCT ETN.NodeNumber
                FROM EDGE_TRUSS_NODES AS ETN
                JOIN PRIMARY_TRUSS_NODES AS PTN ON ETN.NodeNumber = PTN.NodeNumber
                ORDER BY ETN.NodeNumber
                """

    results = conn.execute(query).fetchall()

    for result in results:
        print("\t".join(str(r) for r in result))

    print(";".join(str(r[0]) for r in results))
