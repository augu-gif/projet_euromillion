# 🎰 EuroMillions Analytics

Une application Streamlit pédagogique pour analyser les données historiques des tirages EuroMillions et explorer les probabilités.

## ⚠️ Avertissement important

**Cette application est strictement pédagogique et exploratoire.** Elle ne prétend pas prédire les tirages futurs ni optimiser les chances de gagner. Chaque tirage EuroMillions est indépendant et les fréquences passées n'influencent pas les résultats futurs.

## ✨ Fonctionnalités

### 📊 Analyse statistique
- **Statistiques globales** : nombre de tirages, période couverte, prix moyens, taux de gagnants
- **Fréquences d'apparition** : numéros (1-50) et étoiles (1-12) avec visualisations interactives
- **Top/Bottom** : numéros et étoiles les plus/moins fréquents
- **Régularité** : retards maximums, numéros les plus récents

### 🎲 Générateur de grilles
- **Générateur uniforme** : tirage aléatoire classique (toutes les combinaisons équiprobables)
- **Générateur pondéré** : exploration basée sur les fréquences historiques (fréquents/rare)
- **Générateur multiple** : création de 1 ou 5 grilles à la fois

### 🔍 Insights avancés
- **Probabilités empiriques** : comparaison avec les probabilités théoriques
- **Répartition** : analyse par dizaines, pairs/impairs, sommes des numéros
- **Évolution temporelle** : analyse par périodes et années

### 🎛️ Contrôles
- **Filtrage temporel** : par année ou période personnalisée
- **Interface intuitive** : sidebar avec tous les contrôles
- **Visualisations riches** : graphiques Plotly interactifs

## 🏗️ Architecture

```
euro-millions-analytics/
├── data/
│   └── resultat_trie.json      # Données historiques
├── src/
│   ├── __init__.py
│   ├── loader.py               # Chargement JSON
│   ├── cleaning.py             # Nettoyage et validation
│   ├── stats.py                # Calculs statistiques
│   ├── generators.py           # Génération de grilles
│   ├── insights.py             # Insights métier
│   └── utils.py                # Utilitaires
├── archive/                    # Anciens fichiers
├── app.py                      # Application Streamlit
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. **Clonez le dépôt et accédez au dossier :**
   ```bash
   git clone <url-du-repo>
   cd "Projet euro million"
   ```

2. **Créez et activez un environnement virtuel :**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
   ```

3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Utilisation

**Lancez l'application :**
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

## 📊 Données

- **Source** : fichier `data/resultat_trie.json`
- **Période** : 2004 à 2026
- **Tirages** : ~1,945 tirages validés
- **Format** : JSON avec dates, numéros, étoiles, prix, gagnants

## 🎓 Aspects pédagogiques

L'application explique :
- L'indépendance des tirages
- Les probabilités théoriques vs empiriques
- L'importance de la rigueur statistique
- Les limites de l'analyse rétrospective

## 🛠️ Technologies

- **Streamlit** : Interface web interactive
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques
- **Python-dateutil** : Parsing des dates

## 📈 Métriques disponibles

- Nombre total de tirages
- Période d'analyse
- Prix moyen, médian, min/max
- Taux de tirages avec/sans gagnant
- Fréquences par numéro et étoile
- Probabilités empiriques
- Retards et régularité
- Répartition statistique

## 🎲 Générateur

Le générateur propose trois modes :
1. **Uniforme** : chaque combinaison a la même probabilité (recommandé)
2. **Fréquents** : favorise les numéros/étoiles sortis souvent (exploratoire)
3. **Rares** : favorise les numéros/étoiles sortis peu souvent (exploratoire)

**Important :** Aucun mode n'améliore réellement les chances de gagner !

---

*"Les tirages passés n'influencent pas les tirages futurs"* 🎰

