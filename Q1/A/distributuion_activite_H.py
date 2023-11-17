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


csv_file_2003 = "./data/OD03/od03_Regdomi8_7_CNORD.csv"
csv_file_2013 = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

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
            legend_label = f"2003: H , {age_range} ans, Etudiant"
        elif "OD13" in csv_file:
            df = df[["FEUILLET", "RANG", "AGE", "SEXE", "P_STATUT", "MOTIF", "FACPER"]]
            legend_label = f"2013: H , {age_range}, Etudiant"

    filtered_df = filter_dataframe(df, age_range, p_statut_etudiant, sexe_homme)

    filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

    pivot_df = filtered_df.groupby(['NUM_PERS', 'FACPER', 'MOTIF']).size().unstack(fill_value=0).reset_index()
    pivot_df.columns.name = None

    pivot_df.columns = ['NUM_PERS', 'FACPER'] + [f'COUNT_MOTIF_{col}' for col in pivot_df.columns[2:]]

    pivot_df = pivot_df.rename(columns=columns_mapping)
    print(pivot_df.head(10))

    etude_df = pivot_df.loc[:, ['NUM_PERS', 'FACPER', 'Etude']]

    occurrences_counts = etude_df.groupby('Etude')['FACPER'].sum().reset_index()
    occurrences_counts.columns = ['Nombre d\'occurrences du déplacement etude', 'Total pondéré']
    total_pondere_total = occurrences_counts['Total pondéré'].sum()
    occurrences_counts['Pourcentage'] = (occurrences_counts['Total pondéré'] / total_pondere_total) * 100

    occurrences_counts = occurrences_counts.sort_values('Nombre d\'occurrences du déplacement etude')

    total_count = occurrences_counts['Total pondéré'].sum()
    total_percentage = occurrences_counts['Pourcentage'].sum()

    width = 0.4
    x = [i + width * idx for i in range(len(occurrences_counts))]
    bars = ax.bar(x, occurrences_counts['Pourcentage'], width=width, label=f'{csv_file[-8:-4]}')

    for bar, percentage in zip(bars, occurrences_counts['Pourcentage']):
        height = bar.get_height()
        ax.annotate(f'{percentage:.2f}%', (bar.get_x() + bar.get_width() / 2, height), ha='center', va='bottom')

    legend_labels.append(legend_label)


ax.set_xticks([i + width for i in range(len(occurrences_counts))])
ax.set_xticklabels(occurrences_counts['Nombre d\'occurrences du déplacement etude'])

ax.legend(legend_labels)

ax.set_xlabel('Nombre d\'occurrences du déplacement etude')
ax.set_ylabel('Pourcentage')
ax.set_title('Distribution en pourcentage du nombre de déplacement etude')

plt.show()
    


