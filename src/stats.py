import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, Tuple, List

class StatisticsCalculator:
    """Classe pour calculer les statistiques des tirages EuroMillions"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.number_freq = None
        self.star_freq = None
        self._calculate_frequencies()

    def _calculate_frequencies(self):
        """Calcule les fréquences des numéros et étoiles"""
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

    def get_number_frequencies(self) -> pd.DataFrame:
        """Retourne les fréquences des numéros sous forme de DataFrame"""
        freq_df = pd.DataFrame({
            'numero': range(1, 51),
            'frequence': [self.number_freq.get(i, 0) for i in range(1, 51)]
        })
        total_draws = len(self.df)
        freq_df['probabilite_empirique'] = freq_df['frequence'] / (total_draws * 5)  # 5 numéros par tirage
        freq_df['pourcentage'] = freq_df['frequence'] / freq_df['frequence'].sum() * 100
        return freq_df

    def get_star_frequencies(self) -> pd.DataFrame:
        """Retourne les fréquences des étoiles sous forme de DataFrame"""
        freq_df = pd.DataFrame({
            'etoile': range(1, 13),
            'frequence': [self.star_freq.get(i, 0) for i in range(1, 13)]
        })
        total_draws = len(self.df)
        freq_df['probabilite_empirique'] = freq_df['frequence'] / (total_draws * 2)  # 2 étoiles par tirage
        freq_df['pourcentage'] = freq_df['frequence'] / freq_df['frequence'].sum() * 100
        return freq_df

    def get_top_numbers(self, n: int = 10) -> pd.DataFrame:
        """Retourne les n numéros les plus fréquents"""
        freq_df = self.get_number_frequencies()
        return freq_df.nlargest(n, 'frequence')

    def get_bottom_numbers(self, n: int = 10) -> pd.DataFrame:
        """Retourne les n numéros les moins fréquents"""
        freq_df = self.get_number_frequencies()
        return freq_df.nsmallest(n, 'frequence')

    def get_top_stars(self, n: int = 10) -> pd.DataFrame:
        """Retourne les n étoiles les plus fréquentes"""
        freq_df = self.get_star_frequencies()
        return freq_df.nlargest(n, 'frequence')

    def get_bottom_stars(self, n: int = 10) -> pd.DataFrame:
        """Retourne les n étoiles les moins fréquentes"""
        freq_df = self.get_star_frequencies()
        return freq_df.nsmallest(n, 'frequence')

    def get_number_delays(self) -> pd.DataFrame:
        """Calcule le nombre de tirages depuis la dernière apparition de chaque numéro"""
        delays = {}
        last_seen = {i: -1 for i in range(1, 51)}

        for idx, row in self.df.iterrows():
            for num in range(1, 51):
                if num in row['numbers']:
                    last_seen[num] = idx
                else:
                    if last_seen[num] == -1:
                        delays.setdefault(num, []).append(idx + 1)  # +1 car idx commence à 0
                    else:
                        delays.setdefault(num, []).append(idx - last_seen[num])

        # Pour chaque numéro, prendre le délai maximum
        max_delays = {}
        for num in range(1, 51):
            if num in delays:
                max_delays[num] = max(delays[num])
            else:
                max_delays[num] = 0

        delay_df = pd.DataFrame({
            'numero': list(max_delays.keys()),
            'retard_max': list(max_delays.values())
        })
        return delay_df.sort_values('retard_max', ascending=False)

    def get_recent_draws(self) -> pd.DataFrame:
        """Retourne les numéros sortis le plus récemment"""
        last_draw = self.df.iloc[-1]
        recent_df = pd.DataFrame({
            'numero': last_draw['numbers'],
            'derniere_apparition': last_draw['date']
        })
        return recent_df

    def get_prize_stats(self) -> Dict[str, float]:
        """Retourne les statistiques des prix"""
        prizes = self.df['prize'].dropna()
        if len(prizes) == 0:
            return {
                'moyen': np.nan,
                'median': np.nan,
                'min': np.nan,
                'max': np.nan
            }

        return {
            'moyen': prizes.mean(),
            'median': prizes.median(),
            'min': prizes.min(),
            'max': prizes.max()
        }

    def get_winner_stats(self) -> Dict[str, int]:
        """Retourne les statistiques des gagnants"""
        total_draws = len(self.df)
        draws_with_winner = self.df['has_winner'].sum()
        draws_without_winner = total_draws - draws_with_winner

        return {
            'total_tirages': total_draws,
            'avec_gagnant': draws_with_winner,
            'sans_gagnant': draws_without_winner,
            'pourcentage_avec_gagnant': (draws_with_winner / total_draws * 100) if total_draws > 0 else 0,
            'pourcentage_sans_gagnant': (draws_without_winner / total_draws * 100) if total_draws > 0 else 0
        }

    def get_number_distribution_by_decade(self) -> pd.DataFrame:
        """Distribution des numéros par dizaines"""
        decades = []
        for nums in self.df['numbers']:
            for num in nums:
                decade = ((num - 1) // 10) + 1
                decades.append(decade)

        decade_counter = Counter(decades)
        decade_df = pd.DataFrame({
            'decade': [f"{i*10-9:2d}-{i*10}" for i in range(1, 6)],
            'frequence': [decade_counter.get(i, 0) for i in range(1, 6)]
        })
        total = decade_df['frequence'].sum()
        decade_df['pourcentage'] = decade_df['frequence'] / total * 100
        return decade_df

    def get_parity_stats(self) -> Dict[str, float]:
        """Statistiques pairs/impairs"""
        all_numbers = []
        for nums in self.df['numbers']:
            all_numbers.extend(nums)

        pairs = sum(1 for n in all_numbers if n % 2 == 0)
        impairs = len(all_numbers) - pairs

        return {
            'pairs': pairs,
            'impairs': impairs,
            'pourcentage_pairs': pairs / len(all_numbers) * 100,
            'pourcentage_impairs': impairs / len(all_numbers) * 100
        }

    def get_sum_stats(self) -> Dict[str, float]:
        """Statistiques des sommes des numéros"""
        sums = []
        for nums in self.df['numbers']:
            sums.append(sum(nums))

        return {
            'moyenne': np.mean(sums),
            'mediane': np.median(sums),
            'minimum': min(sums),
            'maximum': max(sums)
        }