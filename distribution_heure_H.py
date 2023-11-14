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

age_range = (15, 19)
etudiant =  3
homme = 1

#creer mon dataframe pour les homme, age de 15 a 19 ans, statut etudiant
filtered_df = filter_dataframe(df, age_range, etudiant, homme)

#filtrer le dataframe pour garder seulement les deplacements etude
filtered_df = filtered_df[(filtered_df["MOTIF"] == 2)]
filtered_df['NUM_PERS'] = filtered_df['FEUILLET'].astype(str) + '_' + filtered_df['RANG'].astype(str)

#Calculter le nombre de fois que le deplacement etude est fait
count_motif_per_person = filtered_df[filtered_df["MOTIF"] == 2].groupby("NUM_PERS")["MOTIF"].count()
#Trouver les personnes où le nombre de déplacement = 1
selected_num_pers = count_motif_per_person[count_motif_per_person == 1].index

#garder seulement les lignes que le nombre de deplacement étude = 1
filtered_df = filtered_df[filtered_df["NUM_PERS"].isin(selected_num_pers)]

select_columns = ["NUM_PERS", "FACPER", "HREDE"]

hrede_df = filtered_df[select_columns]

print(hrede_df.head(10))

occurrences_counts = hrede_df.groupby('HREDE')['FACPER'].sum().reset_index()
occurrences_counts = occurrences_counts.rename(columns={"FACPER": "NOMBRE_PERSONNES"})
occurrences_counts = occurrences_counts.sort_values(by="NOMBRE_PERSONNES", ascending=False)
print(occurrences_counts.head(10))

total = occurrences_counts['NOMBRE_PERSONNES'].sum()
print(total)

occurrences_counts["PERCENTAGE"] = (occurrences_counts["NOMBRE_PERSONNES"] / total) * 100


plt.figure(figsize=(12, 6))
bar_width = 20.0
plt.bar(occurrences_counts["HREDE"], occurrences_counts["PERCENTAGE"], width=bar_width, align='edge')
plt.xlabel("Heure de Départ (HREDE)")
plt.ylabel("Nombre de Personnes")
plt.title("Distribution du Nombre de Personnes par Heure de Départ")
plt.ylim(0, 20)
plt.show()




