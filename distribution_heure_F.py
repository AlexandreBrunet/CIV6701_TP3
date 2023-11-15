import pandas as pd
import matplotlib.pyplot as plt

def filter_dataframe(df, age_range: list, p_statut: int, sexe: int):
    filtered_df = df[
        (df["AGE"] >= age_range[0]) & 
        (df["AGE"] <= age_range[1]) & 
        (df["P_STATUT"] == p_statut) & 
        (df["SEXE"] == sexe)
        ]
    return filtered_df

csv_file = "./data/OD13/od13_Regdomi8_7_CNORD.csv"

df = pd.read_csv(csv_file)

df = df[["FEUILLET", "RANG", "AGE", "SEXE", "P_STATUT", "HREDE" ,"MOTIF", "FACPER"]]

age_range = (50, 54)
p_statut_travail =  1
sexe_femme = 2

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

plt.figure(figsize=(12, 6))
bar_width = 0.8
plt.bar(occurrences_counts["HREDE_HOUR"], occurrences_counts["PERCENTAGE"], width=bar_width, align='edge')
plt.xlabel("Heure de Départ")
plt.ylabel("Pourcentage")
plt.title("Distribution du Pourcentage de Personnes par Heure de Départ")
plt.xticks(rotation=45, ha='right') 
plt.show()




