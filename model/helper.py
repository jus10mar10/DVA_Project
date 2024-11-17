import pandas as pd

def circut_names():
    df = pd.read_csv("model/F1_Final_Table_with_RaceName.csv")
    return list(df.circuit_short_name.unique())