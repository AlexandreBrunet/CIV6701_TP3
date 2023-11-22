import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#on va regarder proportion homme possedant un permis MTLCENTRE vs MTLLAVAL
csv_file_2003 = "./data/OD03/od03_Regdomi8_2_MTLCENTRE.csv"
csv_file_2013 = "./data/OD13/od13_Regdomi8_2_MTLCENTRE.csv"

# csv_file_2003 = "./data/OD03/od03_Regdomi8_6_MTLLAVAL.csv"
# csv_file_2013 = "./data/OD13/od13_Regdomi8_6_MTLLAVAL.csv"


csv_files = [csv_file_2003, csv_file_2013]
result_df = pd.DataFrame()

for csv_file in csv_files:

    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.upper()

    #regarder seulement les hommes >= 15 ans
    sexe_homme = 1
    age = 15

    filtered_df = df[(
        df["SEXE"] == sexe_homme) & 
        (df["AGE"] > age)
        ]
    #creation de la colonne numero de personne
    filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

    select_columns = ["NUM_PERS", "FACPER", "AGE", "PERMIS"]


    filtered_df = filtered_df[select_columns].drop_duplicates(subset="NUM_PERS")

    permis_mapping = {1: 'Permis', 2: 'Pas de permis', 3: 'Ne sait pas', 4: 'Refus', 5: 'Non applicable'}
    filtered_df['PERMIS'] = filtered_df['PERMIS'].replace(permis_mapping)

    age_bins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, float('inf')]
    age_labels = ['16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65', '66-70', '71-75', '75+']
    filtered_df['AGE_GROUP'] = pd.cut(filtered_df['AGE'], bins=age_bins, labels=age_labels, right=False)

    occurences_counts = filtered_df.groupby(['AGE_GROUP', 'PERMIS'])['FACPER'].sum().reset_index()
    occurences_counts = occurences_counts.rename(columns={"FACPER": "NB_PERS"})

    total_by_age_group = occurences_counts.groupby('AGE_GROUP')['NB_PERS'].sum().reset_index()
    occurences_counts = pd.merge(occurences_counts, total_by_age_group, on='AGE_GROUP', suffixes=('', '_TOTAL'))
    occurences_counts['TAUX'] = occurences_counts['NB_PERS'] / occurences_counts['NB_PERS_TOTAL']
    occurences_counts = occurences_counts.drop('NB_PERS_TOTAL', axis=1)

    pivot_df = occurences_counts.pivot(index='AGE_GROUP', columns='PERMIS', values='TAUX').reset_index()
    year = csv_file.split("/")[-2][-4:]
    permis_column_name = f"Permis_{year}"
    result_df = pd.concat([result_df, pivot_df[['AGE_GROUP', 'Permis']].rename(columns={'Permis': permis_column_name})], axis=1)
    duplicate_columns = result_df.columns[result_df.columns.duplicated()]
    result_df = result_df.loc[:, ~result_df.columns.duplicated()]

print(result_df)

age_groups = result_df['AGE_GROUP']
permis_od03 = result_df['Permis_OD03']
permis_od13 = result_df['Permis_OD13']
ind = np.arange(len(age_groups))

# Largeur des barres
width = 0.35

# Création du bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bar1 = ax.bar(ind - width/2, permis_od03, width, label='2003: Homme > 15 ans')
bar2 = ax.bar(ind + width/2, permis_od13, width, label='2013: Homme > 15 ans')

# Ajout des étiquettes, titres, etc.
ax.set_xlabel('Groupe d\'âge')
ax.set_ylabel('Pourcentage')
ax.set_title('Taux de possession permis par groupe d\'âge')
ax.set_xticks(ind)
ax.set_xticklabels(age_groups)
ax.legend()

# Affichage du bar chart
plt.show()