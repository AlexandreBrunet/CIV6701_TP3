import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

fig, ax = plt.subplots(figsize=(10, 6))
legend_labels = []

#on va regarder proportion homme possedant un permis MTLCENTRE vs MTLLAVAL
csv_file_2013 = "./data/OD13/od13_Regdomi8_2_MTLCENTRE.csv"
csv_file_2003 = "./data/OD03/od03_Regdomi8_2_MTLCENTRE.csv"

#regarder seulement les hommes >= 15 ans
sexe_femme = 2
age = 15

csv_files = [csv_file_2003, csv_file_2013]

for idx, csv_file in enumerate(csv_files):
    
    df = pd.read_csv(csv_file)

    if os.path.exists(csv_file):
        if "OD03" in csv_file:
            df = df[["feuillet", "rang", "age", "sexe", "p_statut", "motif", "facper", "permis", "autologi"]]
            df.columns = df.columns.str.upper()
            legend_label = "2003: Centre de Montréal, femme > 15 ans"
        elif "OD13" in csv_file:
            df = df[["FEUILLET", "RANG", "AGE", "SEXE", "P_STATUT", "MOTIF", "FACPER", "PERMIS", "AUTOLOGI"]]
            legend_label = "2013: Centre de Montréal, femme > 15 ans"

    filtered_df = df[
        (df["SEXE"] == sexe_femme) & 
        (df["AGE"] > age)
        ]
    #creation de la colonne numero de personne
    filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

    select_columns = ["FEUILLET", "NUM_PERS", "FACPER", "PERMIS", "AUTOLOGI"]


    filtered_df = filtered_df[select_columns].drop_duplicates(subset="NUM_PERS")
    filtered_df['NB_PERS'] = filtered_df.groupby('FEUILLET')['NUM_PERS'].transform('count')

    filtered_df['NB_PERMIS'] = filtered_df.groupby('FEUILLET')['PERMIS'].transform(lambda x: (x == 1).sum())

    select_columns = ["FEUILLET", "FACPER", "AUTOLOGI", "NB_PERS", "NB_PERMIS"]

    auto_df = filtered_df[select_columns]
    auto_df = auto_df.groupby('FEUILLET').agg({'FACPER': 'sum', 'AUTOLOGI': 'first', 'NB_PERS': 'first', 'NB_PERMIS': 'first'}).reset_index()
    auto_df['TAUX_ACCES_AUTO'] = (auto_df['AUTOLOGI'] / auto_df['NB_PERMIS']) * 100
    auto_df = auto_df.replace([np.inf, -np.inf], np.nan).dropna(subset=['TAUX_ACCES_AUTO'])
    print(auto_df)

    total_taux = auto_df.groupby('TAUX_ACCES_AUTO')['NB_PERS'].sum().reset_index()
    total = auto_df['NB_PERS'].sum()
    print(total)
    total_taux['TAUX'] = (total_taux['NB_PERS'] / total) * 100
    print(total_taux)

    taux_significatif = total_taux[
        (total_taux["TAUX"] > 1.0)
        ]
    
    width = 0.4
    x = [i + width * idx for i in range(len(taux_significatif))]
    bars = ax.bar(x, taux_significatif['TAUX'], width=width, label=f'{csv_file[-8:-4]}')

    for bar, percentage in zip(bars, taux_significatif['TAUX']):
        height = bar.get_height()
        ax.annotate(f'{percentage:.2f}%', (bar.get_x() + bar.get_width() / 2, height), ha='center', va='bottom')

    legend_labels.append(legend_label)

ax.set_xticks([i + width for i in range(len(taux_significatif))])
ax.set_xticklabels(taux_significatif['TAUX_ACCES_AUTO'])

ax.legend(legend_labels)

ax.set_xlabel('Taux accès à l\'automobile')
ax.set_ylabel('Pourcentage')
ax.set_title('Distribution taux d\'accès à l\'automobile pour les personnes avec un permis')

plt.show()