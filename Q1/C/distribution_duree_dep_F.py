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

fig, ax = plt.subplots(figsize=(10, 6))
legend_labels = []

csv_file_2003 = "./data/OD03/od03_Regdomi8_6_MTLLAVAL.csv"
csv_file_2013 = "./data/OD13/od13_Regdomi8_6_MTLLAVAL.csv"

# csv_file_2003 = "./data/OD03/od03_Regdomi8_7_CNORD.csv"
# csv_file_2013 = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

age_range = (50, 54)
p_statut_travail =  1
sexe_femme = 2


csv_files = [csv_file_2003, csv_file_2013]

for idx, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file)

    if os.path.exists(csv_file):
        if "OD03" in csv_file:
            df = df[["feuillet", "rang", "age", "sexe", "p_statut", "hrede", "motif", "facper"]]
            df.columns = df.columns.str.upper()
            legend_label = "2003: F , 50-54 ans, Travailleur"
        elif "OD13" in csv_file:
            df = df[["FEUILLET", "RANG", "AGE", "SEXE", "P_STATUT", "HREDE", "MOTIF", "FACPER"]]
            legend_label = "2013: F , 50-54 ans, Travailleur"

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

    width = 0.4
    x = [i + width * idx for i in range(len(occurrences_counts))]
    bars = ax.bar(x, occurrences_counts['POURCENTAGE'], width=width, label=f'{csv_file[-8:-4]}')

    for bar, percentage in zip(bars, occurrences_counts['POURCENTAGE']):
        height = bar.get_height()
        # ax.annotate(f'{percentage:.2f}%', (bar.get_x() + bar.get_width() / 2, height), ha='center', va='bottom')

    legend_labels.append(legend_label)

ax.set_xticks([i + width for i in range(len(occurrences_counts))])
ax.set_xticklabels(occurrences_counts['DUREE_ACTIVITE_HOURS'], rotation='vertical')

ax.legend(legend_labels)

ax.set_xlabel('Durée de l\'activite')
ax.set_ylabel('Pourcentage')
ax.set_title("Distribution de la durée pour l'activité: Travail")

plt.show()
