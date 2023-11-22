import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import ks_2samp
import numpy as np
from scipy.stats import chi2_contingency

def filter_dataframe(df, age_range: list, p_statut: int, sexe: int):
    filtered_df = df[
        (df["AGE"] >= age_range[0]) & 
        (df["AGE"] <= age_range[1]) & 
        (df["P_STATUT"] == p_statut) & 
        (df["SEXE"] == sexe)
        ]
    return filtered_df


columns_mapping = {
    'COUNT_MOTIF_1': 'Travail',
    'COUNT_MOTIF_2': 'Etude',
    'COUNT_MOTIF_3': 'Retour au domicile',
    'COUNT_MOTIF_4': 'Loisir',
    'COUNT_MOTIF_5': 'Magasinage',
    'COUNT_MOTIF_6': 'Autre',
    'COUNT_MOTIF_7': 'Sans deplacement',
    'COUNT_MOTIF_8': 'Indetermine'
}

fig, ax = plt.subplots(figsize=(10, 6))
legend_labels = []

extracted_data = pd.DataFrame()

csv_file_2003 = "./data/OD03/od03_Regdomi8_6_MTLLAVAL.csv"
csv_file_2013 = "./data/OD13/od13_Regdomi8_6_MTLLAVAL.csv"

# csv_file_2003 = "./data/OD03/od03_Regdomi8_7_CNORD.csv"
# csv_file_2013 = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

#################################################
## Analyse des hommes entre 15-19 ans Étudiant ##
#################################################
age_range = (15, 19)
p_statut_etudiant =  3
sexe_homme = 1

csv_files = [csv_file_2003, csv_file_2013]

for idx, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file)

    if os.path.exists(csv_file):
        if "OD03" in csv_file:
            df = df[["feuillet", "rang", "age", "sexe", "p_statut", "motif", "facper"]]
            df.columns = df.columns.str.upper()
            legend_label = f"2003: H , 15-19 ans, Etudiant"
        elif "OD13" in csv_file:
            df = df[["FEUILLET", "RANG", "AGE", "SEXE", "P_STATUT", "MOTIF", "FACPER"]]
            legend_label = f"2013: H , 15-19 ans, Etudiant"

    filtered_df = filter_dataframe(df, age_range, p_statut_etudiant, sexe_homme)

    filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

    pivot_df = filtered_df.groupby(['NUM_PERS', 'FACPER', 'MOTIF']).size().unstack(fill_value=0).reset_index()
    pivot_df.columns.name = None

    pivot_df.columns = ['NUM_PERS', 'FACPER'] + [f'COUNT_MOTIF_{col}' for col in pivot_df.columns[2:]]

    pivot_df = pivot_df.rename(columns=columns_mapping)
    print(pivot_df.head(10))

    etude_df = pivot_df.loc[:, ['NUM_PERS', 'FACPER', 'Etude']]

    occurrences_counts = etude_df.groupby('Etude')['FACPER'].sum().reset_index()
    occurrences_counts.columns = ['Nombre d\'occurrences du déplacement étude', 'Total pondéré']
    total_pondere_total = occurrences_counts['Total pondéré'].sum()
    occurrences_counts['Pourcentage'] = (occurrences_counts['Total pondéré'] / total_pondere_total) * 100

    occurrences_counts = occurrences_counts.sort_values('Nombre d\'occurrences du déplacement étude')

    total_count = occurrences_counts['Total pondéré'].sum()
    total_percentage = occurrences_counts['Pourcentage'].sum()

    width = 0.4
    x = [i + width * idx for i in range(len(occurrences_counts))]
    bars = ax.bar(x, occurrences_counts['Pourcentage'], width=width, label=f'{csv_file[-8:-4]}')

    for bar, percentage in zip(bars, occurrences_counts['Pourcentage']):
        height = bar.get_height()
        ax.annotate(f'{percentage:.2f}%', (bar.get_x() + bar.get_width() / 2, height), ha='center', va='bottom')

    legend_labels.append(legend_label)

    extracted_data = pd.concat([extracted_data, occurrences_counts.add_suffix(f'_{csv_file[-8:-4]}')], axis=1)


ax.set_xticks([i + width for i in range(len(occurrences_counts))])
ax.set_xticklabels(occurrences_counts['Nombre d\'occurrences du déplacement étude'])

ax.legend(legend_labels)

ax.set_xlabel('Nombre d\'occurrences du déplacement étude')
ax.set_ylabel('Pourcentage')
ax.set_title('Distribution en pourcentage du nombre de déplacement: Étude')

plt.show()

print(extracted_data)

extracted_data.columns = [
    'Nombre_occurrences_2003', 'Total_pondere_2003', 'Pourcentage_2003',
    'Nombre_occurrences_2013', 'Total_pondere_2013', 'Pourcentage_2013'
]

print(extracted_data)

columns_to_drop = ['Nombre_occurrences_2003', 'Nombre_occurrences_2013']
extracted_data = extracted_data.drop(columns=columns_to_drop)
print(extracted_data)

columns_2003 = ['Pourcentage_2003']
columns_2013 = ['Pourcentage_2013']

observed = pd.concat([extracted_data[columns_2003].fillna(0), extracted_data[columns_2013].fillna(0)], axis=1)
print(observed)
chi2, p_value, _, _ = chi2_contingency(observed)
print(f"Statistique du test du Chi-squared : {chi2}")
print(f"p-valeur : {p_value}")

hypothese_null = "Il n'y a pas suffisamment de preuves pour rejeter l'hypothèse nulle. Les distributions sont similaires."
hypothese_alternative = "La différence entre les distributions est statistiquement significative. Rejetez l'hypothèse nulle."
alpha = 0.05 # 5%

if p_value < alpha:
    print(hypothese_alternative)
else:
    print(hypothese_null)
    


