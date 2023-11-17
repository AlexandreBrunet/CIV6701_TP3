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


csv_file_2003 = "./data/OD03/od03_Regdomi8_7_CNORD.csv"
csv_file_2013 = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

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

    #creer mon dataframe pour les femmes, age de 50 a 54 ans, statut travailß
    filtered_df = filter_dataframe(df, age_range, p_statut_travail, sexe_femme)

    #filtrer le dataframe pour garder seulement les deplacements travail
    filtered_df = filtered_df[(filtered_df["MOTIF"] == 1)]
    filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

    #Calculer le nombre de fois que le deplacement travail est fait
    count_motif_per_person = filtered_df[filtered_df["MOTIF"] == 1].groupby("NUM_PERS")["MOTIF"].count()
    #Trouver les personnes où le nombre de déplacement = 1 (deplacement le plus commun)
    selected_num_pers = count_motif_per_person[count_motif_per_person == 1].index

    #garder seulement les lignes que le nombre de deplacement étude = 1
    filtered_df = filtered_df[filtered_df["NUM_PERS"].isin(selected_num_pers)]

    select_columns = ["NUM_PERS", "FACPER", "HREDE"]

    hrede_df = filtered_df[select_columns]
    hrede_df['HREDE'] = pd.to_datetime(hrede_df['HREDE'], format='%H%M').dt.time

    print(hrede_df.head(10))
    bins = list(range(0, 25, 1))  # Bins for each hour
    hrede_df['HREDE_BIN'] = pd.cut(hrede_df['HREDE'].apply(lambda x: x.hour), bins=bins, right=False)

    # Calculate the sum and percentage for each hour bin
    occurrences_counts = hrede_df.groupby('HREDE_BIN')['FACPER'].sum().reset_index()
    occurrences_counts = occurrences_counts.rename(columns={"FACPER": "NOMBRE_PERSONNES"})

    total = occurrences_counts['NOMBRE_PERSONNES'].sum()
    occurrences_counts["PERCENTAGE"] = (occurrences_counts["NOMBRE_PERSONNES"] / total) * 100
    occurrences_counts["HREDE_HOUR"] = occurrences_counts["HREDE_BIN"].apply(lambda x: f'{x.left}-{x.right}')

    width = 0.4
    x = [i + width * idx for i in range(len(occurrences_counts))]
    bars = ax.bar(x, occurrences_counts['PERCENTAGE'], width=width, label=f'{csv_file[-8:-4]}')

    for bar, percentage in zip(bars, occurrences_counts['PERCENTAGE']):
        height = bar.get_height()
        # ax.annotate(f'{percentage:.2f}%', (bar.get_x() + bar.get_width() / 2, height), ha='center', va='bottom')

    legend_labels.append(legend_label)


ax.set_xticks([i + width for i in range(len(occurrences_counts))])
ax.set_xticklabels(occurrences_counts['HREDE_HOUR'], rotation='vertical')

ax.legend(legend_labels)

ax.set_xlabel('HREDE_HOUR')
ax.set_ylabel('Pourcentage')
ax.set_title("Heure de départ pour l'activité étude")

plt.show()




