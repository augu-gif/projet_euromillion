import pandas as pd
from typing import Dict, Any
from .stats import StatisticsCalculator

class InsightsCalculator:
    """Classe pour calculer les insights avancés des données EuroMillions"""

    def __init__(self, stats_calculator: StatisticsCalculator):
        self.stats = stats_calculator

    def get_overview_insights(self) -> Dict[str, Any]:
        """Retourne les insights d'ensemble"""
        prize_stats = self.stats.get_prize_stats()
        winner_stats = self.stats.get_winner_stats()

        return {
            'total_tirages': winner_stats['total_tirages'],
            'periode': self._get_period_string(),
            'prix_moyen': prize_stats['moyen'],
            'prix_median': prize_stats['median'],
            'jackpot_min': prize_stats['min'],
            'jackpot_max': prize_stats['max'],
            'tirages_avec_gagnant': winner_stats['avec_gagnant'],
            'tirages_sans_gagnant': winner_stats['sans_gagnant'],
            'pourcentage_avec_gagnant': winner_stats['pourcentage_avec_gagnant'],
            'pourcentage_sans_gagnant': winner_stats['pourcentage_sans_gagnant']
        }

    def get_frequency_insights(self) -> Dict[str, Any]:
        """Retourne les insights sur les fréquences"""
        number_freq = self.stats.get_number_frequencies()
        star_freq = self.stats.get_star_frequencies()

        return {
            'top_5_numeros': self.stats.get_top_numbers(5).to_dict('records'),
            'bottom_5_numeros': self.stats.get_bottom_numbers(5).to_dict('records'),
            'top_5_etoiles': self.stats.get_top_stars(5).to_dict('records'),
            'bottom_5_etoiles': self.stats.get_bottom_stars(5).to_dict('records'),
            'frequence_moyenne_numeros': number_freq['frequence'].mean(),
            'frequence_moyenne_etoiles': star_freq['frequence'].mean()
        }

    def get_regularity_insights(self) -> Dict[str, Any]:
        """Retourne les insights sur la régularité et les retards"""
        delays = self.stats.get_number_delays()
        recent = self.stats.get_recent_draws()

        return {
            'plus_grand_retard_numeros': delays.head(5).to_dict('records'),
            'numeros_plus_recents': recent.to_dict('records'),
            'retard_moyen': delays['retard_max'].mean(),
            'retard_max': delays['retard_max'].max()
        }

    def get_distribution_insights(self) -> Dict[str, Any]:
        """Retourne les insights sur les répartitions"""
        decade_dist = self.stats.get_number_distribution_by_decade()
        parity_stats = self.stats.get_parity_stats()
        sum_stats = self.stats.get_sum_stats()

        return {
            'distribution_par_dizaines': decade_dist.to_dict('records'),
            'statistiques_parite': parity_stats,
            'statistiques_sommes': sum_stats,
            'dizaine_plus_frequente': decade_dist.loc[decade_dist['frequence'].idxmax()]['decade']
        }

    def get_probability_insights(self) -> Dict[str, Any]:
        """Retourne les insights sur les probabilités empiriques"""
        number_freq = self.stats.get_number_frequencies()
        star_freq = self.stats.get_star_frequencies()

        return {
            'probabilite_theorique_numero': 5/50,  # 5 numéros sur 50
            'probabilite_theorique_etoile': 2/12,  # 2 étoiles sur 12
            'probabilite_empirique_moyenne_numero': number_freq['probabilite_empirique'].mean(),
            'probabilite_empirique_moyenne_etoile': star_freq['probabilite_empirique'].mean(),
            'numeros_sur_reprensentes': number_freq[number_freq['probabilite_empirique'] > 5/50]['numero'].tolist(),
            'numeros_sous_reprensentes': number_freq[number_freq['probabilite_empirique'] < 5/50]['numero'].tolist()
        }

    def get_all_insights(self) -> Dict[str, Any]:
        """Retourne tous les insights"""
        return {
            'overview': self.get_overview_insights(),
            'frequencies': self.get_frequency_insights(),
            'regularity': self.get_regularity_insights(),
            'distribution': self.get_distribution_insights(),
            'probabilities': self.get_probability_insights()
        }

    def _get_period_string(self) -> str:
        """Retourne la période sous forme de chaîne"""
        if self.stats.df is None or self.stats.df.empty:
            return "Non disponible"

        min_date = self.stats.df['date'].min()
        max_date = self.stats.df['date'].max()

        if pd.isna(min_date) or pd.isna(max_date):
            return "Non disponible"

        return f"{min_date.strftime('%d/%m/%Y')} - {max_date.strftime('%d/%m/%Y')}"