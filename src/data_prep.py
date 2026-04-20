import json
import pandas as pd
import numpy as np
from collections import Counter
from dateutil import parser as dateparser

class EuroMillionsDataPrep:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None
        self.df = None
        self.number_freq = None
        self.star_freq = None

    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement des données : {e}")

    def create_dataframe(self):
        """Crée un DataFrame pandas à partir des données"""
        if self.data is None:
            self.load_data()

        rows = []
        for draw in self.data:
            # Conversion de la date
            date_str = draw.get('date', '')
            try:
                date_obj = dateparser.parse(date_str)
                date_obj = pd.to_datetime(date_obj)
            except:
                date_obj = pd.NaT

            # Extraction des numéros et étoiles
            numbers = []
            for n in draw.get('numbers', []):
                try:
                    numbers.append(int(n))
                except:
                    pass
            stars = []
            for s in draw.get('stars', []):
                try:
                    stars.append(int(s))
                except:
                    pass

            rows.append({
                'date': date_obj,
                'year': date_obj.year if pd.notna(date_obj) else None,
                'numbers': numbers,
                'stars': stars,
                'has_winner': draw.get('has_winner', False),
                'prize': float(draw.get('prize')) if draw.get('prize') else np.nan
            })

        self.df = pd.DataFrame(rows)
        self.df = self.df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)

    def calculate_frequencies(self):
        """Calcule les fréquences des numéros et étoiles"""
        if self.df is None:
            self.create_dataframe()

        # Fréquences des numéros
        all_numbers = []
        for nums in self.df['numbers']:
            all_numbers.extend(nums)
        self.number_freq = Counter(all_numbers)

        # Fréquences des étoiles
        all_stars = []
        for stars in self.df['stars']:
            all_stars.extend(stars)
        self.star_freq = Counter(all_stars)

    def get_total_draws(self):
        """Retourne le nombre total de tirages"""
        return len(self.df) if self.df is not None else 0

    def get_period(self):
        """Retourne la période couverte par les données"""
        if self.df is None:
            return "Non disponible"
        min_date = self.df['date'].min()
        max_date = self.df['date'].max()
        return f"{min_date.strftime('%d/%m/%Y')} - {max_date.strftime('%d/%m/%Y')}"

    def get_number_frequencies_df(self):
        """Retourne un DataFrame avec les fréquences des numéros"""
        if self.number_freq is None:
            self.calculate_frequencies()

        freq_df = pd.DataFrame({
            'numero': range(1, 51),
            'frequence': [self.number_freq.get(i, 0) for i in range(1, 51)]
        })
        freq_df['pourcentage'] = freq_df['frequence'] / freq_df['frequence'].sum() * 100
        return freq_df

    def get_star_frequencies_df(self):
        """Retourne un DataFrame avec les fréquences des étoiles"""
        if self.star_freq is None:
            self.calculate_frequencies()

        freq_df = pd.DataFrame({
            'etoile': range(1, 13),
            'frequence': [self.star_freq.get(i, 0) for i in range(1, 13)]
        })
        freq_df['pourcentage'] = freq_df['frequence'] / freq_df['frequence'].sum() * 100
        return freq_df

    def get_top_numbers(self, n=10):
        """Retourne les n numéros les plus fréquents"""
        freq_df = self.get_number_frequencies_df()
        return freq_df.nlargest(n, 'frequence')

    def get_bottom_numbers(self, n=10):
        """Retourne les n numéros les moins fréquents"""
        freq_df = self.get_number_frequencies_df()
        return freq_df.nsmallest(n, 'frequence')

    def filter_by_year(self, year):
        """Filtre les données par année"""
        if self.df is None:
            return None
        try:
            year_int = int(year)
            return self.df[self.df['year'] == year_int]
        except ValueError:
            return None
