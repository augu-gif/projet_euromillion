# Projet EuroMillions

## Lancer l'application 
<p align="center">
  <a href="https://augu-gif-projet-euromillion-generateur-streamlit-vkeyxo.streamlit.app/">
    <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit App" width="200"/>
  </a>
</p>

Ce projet permet d'analyser les tirages EuroMillions et de générer des combinaisons de numéros probables ou aléatoires, avec visualisations statistiques.


## Fonctionnalités
- Analyse des fréquences des numéros et étoiles
- Analyse des associations (paires, triplets, quadruplets)
- Visualisation de la dispersion des tirages
- Générateur de grilles EuroMillions pondéré par les statistiques
- Interface web avec Streamlit

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/augu-gif/projet_euromillion.git
   cd projet_euromillion
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
- **Analyse complète** :
  ```bash
  python analyse_euromillions.py
  ```
- **Générateur de numéros avec interface web** :
  ```bash
  streamlit run generateur_streamlit.py
  ```

## Fichiers principaux
- `analyse_euromillions.py` : analyse statistique complète
- `generateur_streamlit.py` : interface web pour générer des grilles
- `resultat.json` : historique des tirages EuroMillions

[Retour au portfolio](https://github.com/augu-gif/mon-portfolio-data/blob/main/README.md)
