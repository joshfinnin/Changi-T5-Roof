import pandas as pd
import pprint
from inputs import TOP_OF_COLUMN_EXTREMA_OUTPUT_FP, CRUCIFORM_OUTPUT_FP, NODAL_OUTPUT_FP


fp = [TOP_OF_COLUMN_EXTREMA_OUTPUT_FP, CRUCIFORM_OUTPUT_FP, NODAL_OUTPUT_FP]

target_combinations = []

for i in fp:
    df = pd.read_csv(i)
    pairs = list(zip(df.iloc[:,1], df.iloc[:,2]) )
    target_combinations.extend(pairs)
    
    
print("[\n" + ",\n".join(
    f"(\"'{a}'\", \"'{b}'\")" for a, b in target_combinations
) + "\n]")
