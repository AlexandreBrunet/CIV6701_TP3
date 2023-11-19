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


age_range = (50, 54)
p_statut_travail =  1
sexe_femme = 2

csv_file_2013 = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

df = pd.read_csv(csv_file_2013)

filtered_df = filter_dataframe(df, age_range, p_statut_travail, sexe_femme)

depart_df = filtered_df[(filtered_df["HREDE"] >= 700) & ((filtered_df["MOTIF"] == 1))]
depart_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

retour_df = filtered_df[(filtered_df["HREDE"] >= 700) & ((filtered_df["MOTIF"] == 3))]
retour_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

select_columns = ["NUM_PERS", "FACPER", "HREDE", "MOTIF"]

depart_df = depart_df[select_columns]
retour_df = retour_df[select_columns]


merged_df = pd.merge(depart_df, retour_df, on="NUM_PERS", how="inner")
merged_df = merged_df[merged_df['HREDE_x'] < merged_df['HREDE_y']]

columns_mapping = {
    'HREDE_x': 'HEURE_DEPART',
    'HREDE_y': 'HEURE_RETOUR',
    'MOTIF_x': 'DEPART_ECOLE',
    'MOTIF_y': 'RETOUR_MAISON',
}

merged_df = merged_df.rename(columns=columns_mapping)

merged_df['HEURE_DEPART'] = pd.to_datetime(merged_df['HEURE_DEPART'], format='%H%M', errors='coerce')
merged_df['HEURE_RETOUR'] = pd.to_datetime(merged_df['HEURE_RETOUR'], format='%H%M', errors='coerce')

merged_df['DUREE_ACTIVITE'] = merged_df['HEURE_RETOUR'] - merged_df['HEURE_DEPART']

merged_df['HEURE_DEPART'] = merged_df['HEURE_DEPART'].dt.time
merged_df['HEURE_RETOUR'] = merged_df['HEURE_RETOUR'].dt.time
#calcule duree de l'activite en minute
merged_df['DUREE_ACTIVITE'] = merged_df['DUREE_ACTIVITE'].dt.total_seconds() / 60


select_columns = ["NUM_PERS", "FACPER_x", "DUREE_ACTIVITE"]

duree_df = merged_df[select_columns]

occurrences_counts = duree_df.groupby('DUREE_ACTIVITE')['FACPER_x'].sum().reset_index()
occurrences_counts = occurrences_counts.rename(columns={"FACPER_x": "NOMBRE_PERSONNES"})

occurrences_counts['DUREE_ACTIVITE_HOURS'] = occurrences_counts['DUREE_ACTIVITE'] / 60

plt.figure(figsize=(10, 6))
plt.bar(occurrences_counts['DUREE_ACTIVITE_HOURS'], occurrences_counts['NOMBRE_PERSONNES'], color='skyblue')

plt.xlabel('DUREE_ACTIVITE (hours)')
plt.ylabel('NOMBRE_PERSONNES')
plt.title('Distribution duree activitee')

plt.grid(axis='y')
plt.show()
