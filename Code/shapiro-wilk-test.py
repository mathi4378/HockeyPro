import numpy as np
import pandas as pd
from scipy import stats
import os

# Pfad zur CSV-Datei (bitte anpassen)
csv_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment1\\E8_V2\\result"
csv_file = os.path.join(csv_path, "grouped_hits.csv")

# CSV-Datei laden
data = pd.read_csv(csv_file)

# Extrahieren der x- und y-Koordinaten
# Annahme: Die Spalte 'Position (x, y) in cm' enthält die Koordinaten im Format "(x, y)"
data['Position'] = data['Position (x, y) in cm'].apply(lambda pos: eval(pos))  # Umwandlung der String-Position in Tupel
data['x'], data['y'] = zip(*data['Position'])  # Entpacken der Tupel in x und y

# Shapiro-Wilk-Test für x und y durchführen
statistic_x, p_value_x = stats.shapiro(data['x'])
statistic_y, p_value_y = stats.shapiro(data['y'])

# Ergebnisse für x-Koordinaten
print(f"Shapiro-Wilk Test für x-Koordinaten:")
print(f"Statistik: {statistic_x}, p-Wert: {p_value_x}")

# Ergebnisse für y-Koordinaten
print(f"\nShapiro-Wilk Test für y-Koordinaten:")
print(f"Statistik: {statistic_y}, p-Wert: {p_value_y}")

# Entscheidung basierend auf dem p-Wert
alpha = 0.05  # Signifikanzniveau
print("\nEntscheidung basierend auf dem p-Wert:")
if p_value_x > alpha:
    print("Die Nullhypothese wird nicht abgelehnt: Die x-Daten folgen einer Normalverteilung.")
else:
    print("Die Nullhypothese wird abgelehnt: Die x-Daten folgen nicht einer Normalverteilung.")

if p_value_y > alpha:
    print("Die Nullhypothese wird nicht abgelehnt: Die y-Daten folgen einer Normalverteilung.")
else:
    print("Die Nullhypothese wird abgelehnt: Die y-Daten folgen nicht einer Normalverteilung.")
