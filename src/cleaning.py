import pandas as pd
import numpy as np
from dateutil import parser as dateparser
from typing import List, Dict, Any

class DataCleaner:
    """Classe pour nettoyer et normaliser les données des tirages EuroMillions"""

    def __init__(self, raw_data: List[Dict[str, Any]]):
        self.raw_data = raw_data
        self.df = None

    def clean_and_normalize(self) -> pd.DataFrame:
        """Nettoie et normalise les données brutes en DataFrame"""
        rows = []

        for draw in self.raw_data:
            # Conversion de la date
            date_str = draw.get('date', '')
            try:
                date_obj = dateparser.parse(date_str)
                date_obj = pd.to_datetime(date_obj)
            except:
                date_obj = pd.NaT

            # Extraction et validation des numéros (1-50)
            numbers = []
            for n in draw.get('numbers', []):
                try:
                    num = int(n)
                    if 1 <= num <= 50:
                        numbers.append(num)
                except:
                    pass
            numbers = sorted(list(set(numbers)))  # Supprimer doublons et trier

            # Extraction et validation des étoiles (1-12)
            stars = []
            for s in draw.get('stars', []):
                try:
                    star = int(s)
                    if 1 <= star <= 12:
                        stars.append(star)
                except:
                    pass
            stars = sorted(list(set(stars)))  # Supprimer doublons et trier

            # Prix et gagnant
            prize = None
            try:
                prize_raw = draw.get('prize')
                if prize_raw is not None and prize_raw != 'N/A':
                    if isinstance(prize_raw, str):
                        prize_str = prize_raw.replace(' ', '').replace('€', '').replace(',', '.')
                        prize = float(prize_str)
                    else:
                        # Si c'est déjà un nombre
                        prize = float(prize_raw)
            except:
                prize = np.nan

            has_winner = draw.get('has_winner', False)
            if isinstance(has_winner, str):
                has_winner = has_winner.lower() in ['true', '1', 'yes']

            rows.append({
                'date': date_obj,
                'year': date_obj.year if pd.notna(date_obj) else None,
                'month': date_obj.month if pd.notna(date_obj) else None,
                'numbers': numbers,
                'stars': stars,
                'has_winner': has_winner,
                'prize': prize,
                'numbers_count': len(numbers),
                'stars_count': len(stars)
            })

        self.df = pd.DataFrame(rows)

        # Nettoyage final
        self.df = self.df.dropna(subset=['date']).sort_values('date').reset_index(drop=True)

        # Validation : seulement les tirages avec 5 numéros et 2 étoiles
        self.df = self.df[
            (self.df['numbers_count'] == 5) &
            (self.df['stars_count'] == 2)
        ].copy()

        return self.df

    def get_cleaned_data(self) -> pd.DataFrame:
        """Retourne les données nettoyées"""
        if self.df is None:
            self.clean_and_normalize()
        return self.df