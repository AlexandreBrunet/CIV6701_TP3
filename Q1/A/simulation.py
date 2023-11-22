import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pourcentages = {
    'Pourcentage_2003': [20.779453, 75.970497, 3.250050, 0.000000],
    'Pourcentage_2013': [18.034529, 75.770002, 5.531028, 0.664441]
}

# Activités
activites = [0, 1, 2, 3]

# Créer un dictionnaire
data = {'activite': activites}
data.update(pourcentages)

# Créer un DataFrame
df = pd.DataFrame(data)

# Nombre total d'individus dans la simulation
nombre_individus = 1000

# Répéter la simulation plusieurs fois (par exemple, 1000 fois)
nombre_simulations = 1000

# Stocker les résultats simulés
simulated_results_2003 = pd.DataFrame()
simulated_results_2013 = pd.DataFrame()

for i in range(nombre_simulations):
    # Générer des fréquences aléatoires pour chaque activité
    frequencies = np.random.rand(len(df))

    # Normaliser les fréquences pour qu'elles ajoutent à 1
    frequencies /= np.sum(frequencies)

    # Ajuster les résultats simulés pour correspondre aux pourcentages initiaux de 2003
    adjusted_results_2003 = frequencies * df['Pourcentage_2003'].values / 100 * nombre_individus
    adjusted_results_2003 *= df['Pourcentage_2003'].sum() / adjusted_results_2003.sum()
    simulated_results_2003['Simulated_{}'.format(i)] = adjusted_results_2003.astype(int)

    # Ajuster les résultats simulés pour correspondre aux pourcentages initiaux de 2013
    adjusted_results_2013 = frequencies * df['Pourcentage_2013'].values / 100 * nombre_individus
    adjusted_results_2013 *= df['Pourcentage_2013'].sum() / adjusted_results_2013.sum()
    simulated_results_2013['Simulated_{}'.format(i)] = adjusted_results_2013.astype(int)

# Calculer la moyenne des simulations pour chaque année
df['Mean_Simulated_2003'] = simulated_results_2003.mean(axis=1).astype(int)
df['Mean_Simulated_2013'] = simulated_results_2013.mean(axis=1).astype(int)

# Afficher le résultat
print(df[['activite', 'Pourcentage_2003', 'Pourcentage_2013', 'Mean_Simulated_2003', 'Mean_Simulated_2013']])
df['RMSE_2003'] = np.square(df['Mean_Simulated_2003'] - df['Pourcentage_2003'])
df['RMSE_2013'] = np.square(df['Mean_Simulated_2013'] - df['Pourcentage_2013'])

rmse_2003 = np.sqrt(df['RMSE_2003'].mean())
print(rmse_2003)
rmse_2013 = np.sqrt(df['RMSE_2013'].mean())
print(rmse_2013)


activitee = df['activite']
simulation_2003 = df['Mean_Simulated_2003']
simulation_2013 = df['Mean_Simulated_2013']

ind = np.arange(len(activitee))

# Largeur des barres
width = 0.35

# Création du bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bar1 = ax.bar(ind - width/2, simulation_2003, width, label='Simulation 2003')
bar2 = ax.bar(ind + width/2, simulation_2013, width, label='Simulation 2013')

# Ajout des étiquettes, titres, etc.
ax.set_xlabel('Nombre d\'ocurrences du déplacement')
ax.set_ylabel('Pourcentage')
ax.set_title('Simulation Distribution fréquentielle du nombre d\'activité')
ax.set_xticks(ind)
ax.set_xticklabels(activitee)

# Ajout des pourcentages sur chaque barre
for i, v in enumerate(simulation_2003):
    ax.text(i - width/2, v + 0.5, f'{v/100:.2%}', ha='center', va='bottom')

for i, v in enumerate(simulation_2013):
    ax.text(i + width/2, v + 0.5, f'{v/100:.2%}', ha='center', va='bottom')

ax.legend()

# Affichage du bar chart
plt.show()
