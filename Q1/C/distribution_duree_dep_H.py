import pandas as pd
import matplotlib.pyplot as plt
import os

def filter_dataframe(df, age_range: list, p_statut: int, sexe: int):
    filtered_df = df[
        (df["AGE"] >= age_range[0]) & 
        (df["AGE"] <= age_range[1]) & 
        (df["P_STATUT"] == p_statut) & 
        (df["SEXE"] == sexe)
        ]
    return filtered_df


age_range = (15, 19)
p_statut_etude =  3
sexe_homme = 1

csv_file_2013 = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

df = pd.read_csv(csv_file_2013)

filtered_df = filter_dataframe(df, age_range, p_statut_etude, sexe_homme)

filtered_df = filtered_df[(filtered_df["HREDE"] >= 1600) & (filtered_df["HREDE"] <= 1700)]
print(df.head(10))