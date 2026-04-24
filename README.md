# EuroMillions - Analyse statistique

Une application Streamlit pour analyser les données historiques des tirages EuroMillions et explorer les probabilités.

## Avertissement important

**Cette application est strictement pédagogique et exploratoire.** Elle ne prétend pas prédire les tirages futurs ni optimiser les chances de gagner. Chaque tirage EuroMillions est indépendant et les fréquences passées n'influencent pas les résultats futurs.

## Fonctionnalités

### Analyse statistique
- **Statistiques globales** : nombre de tirages, période couverte, prix moyens, taux de gagnants
- **Fréquences d'apparition** : numéros (1-50) et étoiles (1-12) avec visualisations interactives
- **Top/Bottom** : numéros et étoiles les plus/moins fréquents
- **Régularité** : retards maximums, numéros les plus récents

### Générateur de grilles
- **Générateur uniforme** : tirage aléatoire classique (toutes les combinaisons équiprobables)
- **Générateur pondéré** : exploration basée sur les fréquences historiques (fréquents/rare)
- **Générateur multiple** : création de 1 ou 5 grilles à la fois

### Analyse avancée
- **Probabilités empiriques** : comparaison avec les probabilités théoriques
- **Répartition** : analyse par dizaines, pairs/impairs, sommes des numéros
- **Évolution temporelle** : analyse par périodes et années

### Contrôles
- **Filtrage temporel** : par année ou période personnalisée
- **Interface intuitive** : sidebar avec tous les contrôles
- **Visualisations riches** : graphiques Plotly interactifs

## Données

- **Source** : fichier `data/resultat_trie.json`
- **Période** : 2004 à 2026
- **Tirages** : ~1,945 tirages validés
- **Format** : JSON avec dates, numéros, étoiles, prix, gagnants

## Technologies

- **Streamlit** : Interface web interactive
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques
- **Python-dateutil** : Parsing des dates

## Métriques disponibles

- Nombre total de tirages
- Période d'analyse
- Prix moyen, médian, min/max
- Taux de tirages avec/sans gagnant
- Fréquences par numéro et étoile
- Probabilités empiriques
- Retards et régularité
- Répartition statistique

## Générateur

Le générateur propose trois modes :
1. **Uniforme** : chaque combinaison a la même probabilité (recommandé)
2. **Fréquents** : favorise les numéros/étoiles sortis souvent (exploratoire)
3. **Rares** : favorise les numéros/étoiles sortis peu souvent (exploratoire)

**Important :** Aucun mode n'améliore réellement les chances de gagner !

---



