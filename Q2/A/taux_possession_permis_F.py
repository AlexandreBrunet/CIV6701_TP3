import pandas as pd
import matplotlib.pyplot as plt


#on va regarder proportion homme possedant un permis MTLCENTRE vs MTLLAVAL
csv_file = "./data/OD13/od13_Regdomi8_2_MTLCENTRE.csv"


df = pd.read_csv(csv_file)

#regarder seulement les hommes >= 15 ans
sexe_femme = 2
age = 15
filtered_df = df[(
    df["SEXE"] == sexe_femme) & 
    (df["AGE"] > age)
    ]
#creation de la colonne numero de personne
filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

select_columns = ["NUM_PERS", "FACPER", "AGE", "PERMIS"]


filtered_df = filtered_df[select_columns].drop_duplicates(subset="NUM_PERS")
print(filtered_df.head(10))

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
print(occurences_counts.head(10))
fig, ax = plt.subplots(figsize=(10, 6))

pivot_df = occurences_counts.pivot(index='AGE_GROUP', columns='PERMIS', values='TAUX')
pivot_df.plot(kind='bar', stacked=True, ax=ax)

ax.set_title('Number of Persons by Age Group and Driving License')
ax.set_xlabel('Age Group')
ax.set_ylabel('Number of Persons')
ax.legend(title='Driving License', bbox_to_anchor=(1, 1), loc='upper left')

plt.show()