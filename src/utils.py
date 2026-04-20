import pandas as pd
from typing import Optional

class Utils:
    """Classe utilitaire pour les opérations communes"""

    @staticmethod
    def format_currency(amount: float) -> str:
        """Formate un montant en euros"""
        if pd.isna(amount):
            return "N/A"
        return f"{amount:,.0f} €"

    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Formate un pourcentage"""
        return f"{value:.{decimals}f}%"

    @staticmethod
    def format_number(value: float, decimals: int = 0) -> str:
        """Formate un nombre avec séparateur de milliers"""
        if pd.isna(value):
            return "N/A"
        return f"{value:,.{decimals}f}"

    @staticmethod
    def get_years_list(df: pd.DataFrame) -> list:
        """Retourne la liste des années disponibles"""
        if df is None or 'year' not in df.columns:
            return []
        return sorted(df['year'].dropna().unique().astype(int).tolist())

    @staticmethod
    def filter_by_year(df: pd.DataFrame, year: int) -> Optional[pd.DataFrame]:
        """Filtre un DataFrame par année"""
        if df is None or 'year' not in df.columns:
            return None
        try:
            return df[df['year'] == year].copy()
        except:
            return None

    @staticmethod
    def filter_by_date_range(df: pd.DataFrame, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Filtre un DataFrame par plage de dates"""
        if df is None or 'date' not in df.columns:
            return None
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            return df[(df['date'] >= start) & (df['date'] <= end)].copy()
        except:
            return None

    @staticmethod
    def validate_grid(numbers: list, stars: list) -> bool:
        """Valide qu'une grille respecte les règles EuroMillions"""
        # 5 numéros distincts entre 1 et 50
        if len(numbers) != 5 or len(set(numbers)) != 5:
            return False
        if not all(1 <= n <= 50 for n in numbers):
            return False

        # 2 étoiles distinctes entre 1 et 12
        if len(stars) != 2 or len(set(stars)) != 2:
            return False
        if not all(1 <= s <= 12 for s in stars):
            return False

        return True