import json
from collections import Counter
import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Chemin du fichier JSON
json_path = "resultat.json"

# Lire le fichier JSON
with open(json_path, "r", encoding="utf-8") as f:
    all_draws = json.load(f)

# Compter les fréquences des numéros et des étoiles (tous tirages)
number_counter = Counter()
star_counter = Counter()

for draw in all_draws:
    number_counter.update(draw["numbers"])
    star_counter.update(draw["stars"])

# Afficher les numéros les plus fréquents
print("Numéros les plus fréquents :")
for num, count in number_counter.most_common():
    print(f"Numéro {num}: {count} fois")

print("\nÉtoiles les plus fréquentes :")
for star, count in star_counter.most_common():
    print(f"Étoile {star}: {count} fois")

# Afficher la combinaison optimale (5 numéros + 2 étoiles les plus fréquents)
combinaison_numeros = [num for num, _ in number_counter.most_common(5)]
combinaison_etoiles = [star for star, _ in star_counter.most_common(2)]

print("\nLa combinaison la plus probable serait :")
print(f"Numéros : {', '.join(combinaison_numeros)}")
print(f"Étoiles : {', '.join(combinaison_etoiles)}")

# Tirage aléatoire pondéré
all_numbers = list(number_counter.keys())
all_stars = list(star_counter.keys())
number_weights = [number_counter[num] for num in all_numbers]
star_weights = [star_counter[star] for star in all_stars]

def tirage_aleatoire_pondere():
    numeros = random.choices(all_numbers, weights=number_weights, k=100)
    numeros_uniques = []
    for n in numeros:
        if n not in numeros_uniques:
            numeros_uniques.append(n)
        if len(numeros_uniques) == 5:
            break
    etoiles = random.choices(all_stars, weights=star_weights, k=50)
    etoiles_uniques = []
    for e in etoiles:
        if e not in etoiles_uniques:
            etoiles_uniques.append(e)
        if len(etoiles_uniques) == 2:
            break
    return numeros_uniques, etoiles_uniques

num_tirage, etoile_tirage = tirage_aleatoire_pondere()
print("\nTirage aléatoire pondéré :")
print(f"Numéros : {', '.join(num_tirage)}")
print(f"Étoiles : {', '.join(etoile_tirage)}")

# --- Analyse spécifique pour 2025 ---
# Isoler les tirages de 2025
all_draws_2025 = [draw for draw in all_draws if draw["date"].split()[-3] == "2025"]
number_counter_2025 = Counter()
star_counter_2025 = Counter()
for draw in all_draws_2025:
    number_counter_2025.update(draw["numbers"])
    star_counter_2025.update(draw["stars"])

print("\n--- Analyse des tirages de 2025 ---")
print(f"Nombre de tirages en 2025 : {len(all_draws_2025)}")
print("Numéros les plus fréquents en 2025 :")
for num, count in number_counter_2025.most_common():
    print(f"Numéro {num}: {count} fois")
print("\nÉtoiles les plus fréquentes en 2025 :")
for star, count in star_counter_2025.most_common():
    print(f"Étoile {star}: {count} fois")

# --- Comparaison des moyennes ---
total_tirages = len(all_draws)
total_tirages_2025 = len(all_draws_2025)
print("\n--- Moyenne d'apparition par tirage (tous vs 2025) ---")
print("Numéro | Moyenne tous tirages | Moyenne 2025")
for num in sorted(set(list(number_counter.keys()) + list(number_counter_2025.keys())), key=int):
    moy_all = number_counter[num] / total_tirages if total_tirages else 0
    moy_2025 = number_counter_2025[num] / total_tirages_2025 if total_tirages_2025 else 0
    print(f"{num:>6} | {moy_all:>20.3f} | {moy_2025:>11.3f}")
print("\nÉtoile | Moyenne tous tirages | Moyenne 2025")
for star in sorted(set(list(star_counter.keys()) + list(star_counter_2025.keys())), key=int):
    moy_all = star_counter[star] / total_tirages if total_tirages else 0
    moy_2025 = star_counter_2025[star] / total_tirages_2025 if total_tirages_2025 else 0
    print(f"{star:>6} | {moy_all:>20.3f} | {moy_2025:>11.3f}")

# Analyse de la dispersion des tirages
spreads = []
for draw in all_draws:
    nums = [int(n) for n in draw["numbers"]]
    spreads.append(np.std(nums))

moyenne_dispersion = np.mean(spreads)
print("\n--- Analyse de la dispersion des tirages ---")
print(f"Écart-type moyen des numéros par tirage : {moyenne_dispersion:.2f}")
print("En général, les tirages Euromillions sont plus souvent dispersés (numéros éloignés les uns des autres) que resserrés.")
print("Il est donc plus probable d'obtenir une combinaison avec des numéros répartis sur toute la grille qu'une combinaison de numéros proches.")

# --- Règle de probabilité et loi uniforme discrète ---
print("\n--- Règle de probabilité et loi uniforme discrète ---")
print("Le tirage EuroMillions suit une loi uniforme discrète sur un espace combinatoire.")
print("Il y a environ 139 millions de combinaisons possibles (5 numéros parmi 50 et 2 étoiles parmi 12). Chaque tirage a donc exactement la même probabilité d'être tiré, quelle que soit la combinaison.")
print("Même si certains motifs semblent plus fréquents, la probabilité réelle de chaque combinaison reste identique.")

# Analyse des paires de numéros qui sortent le plus souvent ensemble
pair_counter = Counter()
for draw in all_draws:
    nums = draw["numbers"]
    for pair in combinations(sorted(nums, key=int), 2):
        pair_counter[pair] += 1

print("\n--- Paires de numéros les plus fréquentes ---")
for pair, count in pair_counter.most_common(10):
    print(f"Paire {pair[0]} et {pair[1]} : {count} fois ensemble")

# Analyse des triplets et quadruplets de numéros
triplet_counter = Counter()
quadruplet_counter = Counter()
for draw in all_draws:
    nums = draw["numbers"]
    for triplet in combinations(sorted(nums, key=int), 3):
        triplet_counter[triplet] += 1
    for quadruplet in combinations(sorted(nums, key=int), 4):
        quadruplet_counter[quadruplet] += 1

# Analyse des paires d'étoiles
star_pair_counter = Counter()
for draw in all_draws:
    stars = draw["stars"]
    for pair in combinations(sorted(stars, key=int), 2):
        star_pair_counter[pair] += 1

print("\n--- Triplets de numéros les plus fréquents ---")
for triplet, count in triplet_counter.most_common(10):
    print(f"Triplet {triplet} : {count} fois ensemble")

print("\n--- Quadruplets de numéros les plus fréquents ---")
for quadruplet, count in quadruplet_counter.most_common(10):
    print(f"Quadruplet {quadruplet} : {count} fois ensemble")

print("\n--- Paires d'étoiles les plus fréquentes ---")
for pair, count in star_pair_counter.most_common(10):
    print(f"Paire d'étoiles {pair[0]} et {pair[1]} : {count} fois ensemble")

# Synthèse finale
print("\n--- Synthèse des sorties les plus fréquentes ---")
print("Numéros les plus fréquents :", ', '.join([num for num, _ in number_counter.most_common(10)]))
print("Étoiles les plus fréquentes :", ', '.join([star for star, _ in star_counter.most_common(5)]))
print("Paires les plus fréquentes :", ', '.join([f"({a},{b})" for (a,b), _ in pair_counter.most_common(5)]))
print("Triplets les plus fréquents :", ', '.join([str(triplet) for triplet, _ in triplet_counter.most_common(3)]))
print("Quadruplets les plus fréquents :", ', '.join([str(quadruplet) for quadruplet, _ in quadruplet_counter.most_common(2)]))
print("Paires d'étoiles les plus fréquentes :", ', '.join([f"({a},{b})" for (a,b), _ in star_pair_counter.most_common(3)]))

# Proposition du prochain tirage le plus probable (basé sur la fréquence conjointe)
# On prend les 5 numéros et 2 étoiles les plus fréquents individuellement
prochain_numeros = [num for num, _ in number_counter.most_common(5)]
prochain_etoiles = [star for star, _ in star_counter.most_common(2)]
print("\n--- Proposition du prochain tirage le plus probable (statistiquement) ---")
print(f"Numéros : {', '.join(prochain_numeros)}")
print(f"Étoiles : {', '.join(prochain_etoiles)}") 