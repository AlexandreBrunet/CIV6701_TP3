import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_city_from_path(csv_file_path):
    if "MTLCENTRE" in csv_file_path:
        return "mtl"
    elif "MTLLAVAL" in csv_file_path:
        return "laval"
    else:
        return None

#on va regarder proportion homme possedant un permis MTLCENTRE vs MTLLAVAL
csv_file_2013_mtl = "./data/OD13/od13_Regdomi8_2_MTLCENTRE.csv"
csv_file_2003_mtl = "./data/OD03/od03_Regdomi8_2_MTLCENTRE.csv"

# csv_file_2013_laval = "./data/OD13/od13_Regdomi8_6_MTLLAVAL.csv"
# csv_file_2003_laval = "./data/OD03/od03_Regdomi8_6_MTLLAVAL.csv"

#regarder seulement les hommes >= 15 ans
sexe_homme = 1
age = 15

csv_files = [csv_file_2013_mtl, csv_file_2003_mtl]
result_df = pd.DataFrame()

for idx, csv_file in enumerate(csv_files):
    city = extract_city_from_path(csv_file)
    df = pd.read_csv(csv_file)

    if os.path.exists(csv_file):
        if "OD03" in csv_file:
            df = df[["feuillet", "rang", "age", "sexe", "p_statut", "motif", "facper", "permis", "autologi"]]
            df.columns = df.columns.str.upper()
            legend_label = "2003: Centre de Montréal, homme > 15 ans"
        elif "OD13" in csv_file:
            df = df[["FEUILLET", "RANG", "AGE", "SEXE", "P_STATUT", "MOTIF", "FACPER", "PERMIS", "AUTOLOGI"]]
            legend_label = "2013: Centre de Montréal, homme > 15 ans"

    filtered_df = df[
        (df["SEXE"] == sexe_homme) & 
        (df["AGE"] > age)
        ]
    #creation de la colonne numero de personne
    filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

    select_columns = ["FEUILLET", "NUM_PERS", "AGE", "FACPER", "PERMIS", "AUTOLOGI"]


    filtered_df = filtered_df[select_columns].drop_duplicates(subset="NUM_PERS")
    filtered_df['NB_PERS'] = filtered_df.groupby('FEUILLET')['NUM_PERS'].transform('count')

    filtered_df['NB_PERMIS'] = filtered_df.groupby('FEUILLET')['PERMIS'].transform(lambda x: (x == 1).sum())

    select_columns = ["FEUILLET", "FACPER", "AGE" ,"AUTOLOGI", "NB_PERS", "NB_PERMIS"]

    auto_df = filtered_df[select_columns]
    auto_df = auto_df.groupby('FEUILLET').agg({'FACPER': 'sum', 'AGE': 'first', 'AUTOLOGI': 'first', 'NB_PERS': 'first', 'NB_PERMIS': 'first'}).reset_index()
    auto_df['TAUX_ACCES_AUTO'] = (auto_df['AUTOLOGI'] / auto_df['NB_PERMIS']) * 100
    auto_df = auto_df.replace([np.inf, -np.inf], np.nan).dropna(subset=['TAUX_ACCES_AUTO'])

    auto_df_pond = auto_df.groupby(['AGE', 'TAUX_ACCES_AUTO'])['FACPER'].sum().reset_index()

    auto_df_pond = auto_df_pond.groupby('AGE').agg({'TAUX_ACCES_AUTO': 'mean', 'FACPER': 'sum'}).reset_index()
    auto_df_pond = auto_df_pond.rename(columns={"FACPER": "NB_PERS"})

    auto_df_pond['AGE_GROUP'] = pd.cut(auto_df_pond['AGE'], bins=range(16, 76, 5), right=False)

# Calculer la moyenne de TAUX_ACCES_AUTO et la somme de NB_PERS pour chaque groupe d'âge
    auto_df_pond = auto_df_pond.groupby('AGE_GROUP').agg({'TAUX_ACCES_AUTO': 'mean'}).reset_index()
    auto_df_pond['AGE_GROUP'] = auto_df_pond['AGE_GROUP'].apply(lambda x: f"{x.left}-{x.right-1}" if x.right != 75 else '75+')

    auto_df_pond = auto_df_pond.rename(columns={"TAUX_ACCES_AUTO": "ACCES_NB_VOITURE"})
    auto_df_pond['ACCES_NB_VOITURE'] = auto_df_pond['ACCES_NB_VOITURE'] / 100
    auto_df_pond['ACCES_NB_VOITURE'] = auto_df_pond['ACCES_NB_VOITURE'].round(2)
    year = csv_file.split("/")[-2][-4:]
    acces_nb_voiture_year = f"ACCES_NB_VOITURE_{year}"
    # acces_nb_voiture_city = f"ACCES_NB_VOITURE_{city.upper()}"
    result_df = pd.concat([result_df, auto_df_pond[['AGE_GROUP', 'ACCES_NB_VOITURE']].rename(columns={'ACCES_NB_VOITURE': acces_nb_voiture_year})], axis=1)
    duplicate_columns = result_df.columns[result_df.columns.duplicated()]
    result_df = result_df.loc[:, ~result_df.columns.duplicated()]

print(result_df)

age_groups = result_df['AGE_GROUP']
acces_auto_2003 = result_df['ACCES_NB_VOITURE_OD03']
acces_auto_2013 = result_df['ACCES_NB_VOITURE_OD13']
ind = np.arange(len(age_groups))

# Largeur des barres
width = 0.35

# Création du bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bar1 = ax.bar(ind - width/2, acces_auto_mtl, width, label='Centre de Mtl 2013: Homme > 15 ans')
bar2 = ax.bar(ind + width/2, acces_auto_laval, width, label='Laval 2013: Homme > 15 ans')

# Ajout des étiquettes, titres, etc.
ax.set_xlabel('Groupe d\'âge')
ax.set_ylabel('Nombre de véhicules')
ax.set_title('Nombre de véhicules disponibles par permis dans les ménages')
ax.set_xticks(ind)
ax.set_xticklabels(age_groups)
ax.legend()

# Affichage du bar chart
plt.show()