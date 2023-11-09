import sqlite3
import csv
import os
import matplotlib.pyplot as plt

csv_file = "./data/OD13/od13_Regdomi8_7_CNORD.csv"
database = "population_data.db"

conn = sqlite3.connect(database)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS population (
        FEUILLET INTEGER,
        RANG INTEGER,
        XDOMI INTEGER,
        YDOMI INTEGER,
        SDOMI100 INTEGER,
        REGDOMI8 INTEGER,
        PERSLOGI INTEGER,
        AUTOLOGI INTEGER,
        AGE INTEGER,
        SEXE INTEGER,
        P_STATUT INTEGER,
        PERMIS INTEGER,
        P_MOBIL INTEGER,
        NODEPLAC INTEGER,
        HREDE INTEGER,
        MOTIF INTEGER,
        SORIG100 INTEGER,
        REGORIG8 INTEGER,
        SDEST100 INTEGER,
        REGDEST8 INTEGER,
        FACPER REAL,
        F_MENAGE TEXT,
        F_PERS TEXT
    )
''')

with open(csv_file, 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Ignore the header row
    for row in csv_reader:
        cursor.execute('INSERT INTO population VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

conn.commit()


query = """
    SELECT
        CASE
            WHEN AGE BETWEEN 0 AND 4 THEN '0-4'
            WHEN AGE BETWEEN 5 AND 9 THEN '5-9'
            WHEN AGE BETWEEN 10 AND 14 THEN '10-14'
            WHEN AGE BETWEEN 15 AND 19 THEN '15-19'
            WHEN AGE BETWEEN 20 AND 24 THEN '20-24'
            WHEN AGE BETWEEN 25 AND 29 THEN '25-29'
            WHEN AGE BETWEEN 30 AND 34 THEN '30-34'
            WHEN AGE BETWEEN 35 AND 39 THEN '35-39'
            WHEN AGE BETWEEN 40 AND 44 THEN '40-44'
            WHEN AGE BETWEEN 45 AND 49 THEN '45-49'
            WHEN AGE BETWEEN 50 AND 54 THEN '50-54'
            WHEN AGE BETWEEN 55 AND 59 THEN '55-59'
            WHEN AGE BETWEEN 60 AND 64 THEN '60-64'
            WHEN AGE BETWEEN 65 AND 69 THEN '65-69'
            WHEN AGE BETWEEN 70 AND 74 THEN '70-74'
            ELSE '75+'
        END AS age_group,
        SUM(CASE WHEN SEXE = 1 THEN 1 ELSE 0 END) as hommes,
        SUM(CASE WHEN SEXE = 2 THEN 1 ELSE 0 END) as femmes
    FROM population
    WHERE P_STATUT = 1
    GROUP BY age_group
"""

result = cursor.execute(query).fetchall()

age_groups = [row[0] for row in result]
hommes = [row[1] for row in result]
femmes = [row[2] for row in result]

plt.figure(figsize=(12, 6))
plt.bar(age_groups, hommes, width=0.4, label='Hommes', color='blue')
plt.bar(age_groups, femmes, width=0.4, label='Femmes', color='pink', bottom=hommes)


plt.xlabel('Catégorie d\'âge')
plt.ylabel('Nombre de personnes')
plt.title('Répartition par âge et sexe - MTL COURONNE NORD')
plt.legend()

plt.show()

for row in result:
    age_group, hommes, femmes = row
    print(f"{age_group:6s}: Hommes: {hommes}, Femmes: {femmes}")


if os.path.exists(database):
    os.remove(database)
    print(f"Database file '{database}' has been deleted.")
else:
    print(f"Database file '{database}' does not exist.")



conn.close()
