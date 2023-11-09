import sqlite3
import os
import matplotlib.pyplot as plt
import db_management

csv_file = "./data/OD13/od13_Regdomi8_7_CNORD.csv"
database = "worker_50_54_f.db"
table_name = "worker_50_54_f"

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
WHERE SEXE = 2
  AND AGE BETWEEN 50 AND 54
  AND P_STATUT = 1
GROUP BY MOTIF_Description
ORDER BY MOTIF_Description;
"""


result = cursor.execute(query).fetchall()

motif = [row[0] for row in result]
deplacement = [row[1] for row in result]

plt.bar(motif, deplacement, width=0.4, label='F Travailleur 50-54 ans', color='orange')

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