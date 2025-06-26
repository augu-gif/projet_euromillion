import streamlit as st
import json
import random
from collections import Counter

st.title("Générateur de numéros EuroMillions")

# Charger les données
try:
    with open("resultat.json", "r", encoding="utf-8") as f:
        all_draws = json.load(f)
except Exception as e:
    st.error(f"Erreur lors de la lecture de resultat.json : {e}")
    st.stop()

number_counter = Counter()
star_counter = Counter()
for draw in all_draws:
    number_counter.update(draw["numbers"])
    star_counter.update(draw["stars"])

all_numbers = list(map(str, range(1, 51)))
all_stars = list(map(str, range(1, 13)))
number_weights = [number_counter.get(num, 1) for num in all_numbers]
star_weights = [star_counter.get(star, 1) for star in all_stars]

def tirage_aleatoire_pondere():
    nums = random.choices(all_numbers, weights=number_weights, k=100)
    nums_uniques = []
    for n in nums:
        if n not in nums_uniques:
            nums_uniques.append(n)
        if len(nums_uniques) == 5:
            break
    etoiles = random.choices(all_stars, weights=star_weights, k=50)
    etoiles_uniques = []
    for e in etoiles:
        if e not in etoiles_uniques:
            etoiles_uniques.append(e)
        if len(etoiles_uniques) == 2:
            break
    return nums_uniques, etoiles_uniques

def tirage_aleatoire_pur():
    nums = random.sample(all_numbers, 5)
    etoiles = random.sample(all_stars, 2)
    return sorted(nums, key=int), sorted(etoiles, key=int)

mode = st.radio("Mode de génération :", ("Pondéré par les fréquences", "Aléatoire pur"))

if st.button("Générer une grille"):
    if mode == "Pondéré par les fréquences":
        nums, etoiles = tirage_aleatoire_pondere()
        st.success(f"Grille pondérée : Numéros {', '.join(nums)} | Étoiles {', '.join(etoiles)}")
    else:
        nums, etoiles = tirage_aleatoire_pur()
        st.success(f"Grille aléatoire : Numéros {', '.join(nums)} | Étoiles {', '.join(etoiles)}")

st.markdown("---")
st.write("Basé sur l'historique du fichier resultat.json.") 
