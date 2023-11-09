import sqlite3
import os
import matplotlib.pyplot as plt
import db_management

csv_file = "./data/OD13/od13_Regdomi8_7_CNORD.csv"
database = "student_15_19_m.db"
table_name = "student_15_19_m"

conn = sqlite3.connect(database)
cursor = conn.cursor()

db_management.create_database(table_name, cursor)
db_management.insert_csv(csv_file, table_name, cursor)

conn.commit()

query = f"""
SELECT
  CASE MOTIF
    WHEN 1 THEN 'Travail'
    WHEN 2 THEN 'Étude'
    WHEN 3 THEN 'Retour au domicile'
    WHEN 4 THEN 'Loisir'
    WHEN 5 THEN 'Magasinage'
    WHEN 6 THEN 'Autre'
    WHEN 7 THEN 'Sans déplacement'
    WHEN 8 THEN 'Indéterminé'
  END AS MOTIF_Description,
  COUNT(*) AS Count
FROM {table_name}
WHERE SEXE = 1
  AND AGE BETWEEN 15 AND 19
  AND P_STATUT = 3
GROUP BY MOTIF_Description
ORDER BY MOTIF_Description;
"""


result = cursor.execute(query).fetchall()

motif = [row[0] for row in result]
deplacement = [row[1] for row in result]

plt.bar(motif, deplacement, width=0.4, label='M Étudiant 15-19 ans', color='blue')

plt.xlabel('Type de déplacement')
plt.ylabel('Nombre de déplacement')
plt.title('Répartition nombre de déplacement - MTL COURONNE NORD')
plt.legend()

plt.show()

for row in result:
    motif, deplacement = row
    print(f"{motif}, Nombre de déplacement: {deplacement}")


if os.path.exists(database):
    os.remove(database)
    print(f"Database file '{database}' has been deleted.")
else:
    print(f"Database file '{database}' does not exist.")



conn.close()