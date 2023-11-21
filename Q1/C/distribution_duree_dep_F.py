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

bins = range(0, int(merged_df['DUREE_ACTIVITE'].max()) + 2, 60)
labels = [f"{i}-{i+1}" for i in bins[:-1]]
merged_df['DUREE_ACTIVITE_BIN'] = pd.cut(merged_df['DUREE_ACTIVITE'], bins=bins, labels=labels, include_lowest=True)

select_columns = ["NUM_PERS", "FACPER_x", "DUREE_ACTIVITE_BIN"]

duree_df = merged_df[select_columns]

occurrences_counts = duree_df.groupby('DUREE_ACTIVITE_BIN')['FACPER_x'].sum().reset_index()
occurrences_counts = occurrences_counts.rename(columns={"FACPER_x": "NOMBRE_PERSONNES"})

occurrences_counts['DUREE_ACTIVITE_HOURS'] = occurrences_counts['DUREE_ACTIVITE_BIN'].apply(lambda x: int(x.split('-')[0]) / 60)
total_personnes = occurrences_counts['NOMBRE_PERSONNES'].sum()
occurrences_counts['POURCENTAGE'] = (occurrences_counts['NOMBRE_PERSONNES'] / total_personnes) * 100

plt.figure(figsize=(10, 6))
plt.bar(occurrences_counts['DUREE_ACTIVITE_HOURS'], occurrences_counts['POURCENTAGE'], color='orange', width=1.0)

plt.xlabel('DUREE_ACTIVITE (heures)')
plt.ylabel('POURCENTAGE')
plt.title('Distribution durée activité')

# Ajuster les étiquettes de l'axe x pour afficher toutes les valeurs entières
plt.xticks(occurrences_counts['DUREE_ACTIVITE_HOURS'])

plt.grid(axis='y')
plt.show()
