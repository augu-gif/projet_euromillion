import random
import numpy as np
from typing import List, Tuple, Dict
from collections import Counter

class GridGenerator:
    """Classe pour générer des grilles EuroMillions"""

    def __init__(self, number_freq: Counter = None, star_freq: Counter = None):
        self.number_freq = number_freq or Counter({i: 1 for i in range(1, 51)})  # Uniforme par défaut
        self.star_freq = star_freq or Counter({i: 1 for i in range(1, 13)})  # Uniforme par défaut

    def generate_uniform_grid(self) -> Tuple[List[int], List[int]]:
        """Génère une grille avec tirage uniforme (non pondéré)"""
        numbers = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))
        return numbers, stars

    def generate_weighted_grid(self, mode: str = 'frequent') -> Tuple[List[int], List[int]]:
        """
        Génère une grille pondérée selon les fréquences historiques

        Args:
            mode: 'frequent' pour favoriser les plus fréquents,
                  'rare' pour favoriser les moins fréquents,
                  'neutral' pour distribution uniforme
        """
        if mode == 'neutral':
            return self.generate_uniform_grid()

        # Préparer les poids pour les numéros
        if mode == 'frequent':
            number_weights = [self.number_freq.get(i, 1) for i in range(1, 51)]
        elif mode == 'rare':
            max_freq = max(self.number_freq.values()) if self.number_freq else 1
            number_weights = [max_freq - self.number_freq.get(i, 0) + 1 for i in range(1, 51)]
        else:
            raise ValueError("Mode doit être 'frequent', 'rare' ou 'neutral'")

        # Normaliser les poids
        number_weights = np.array(number_weights)
        number_weights = number_weights / number_weights.sum()

        # Préparer les poids pour les étoiles
        if mode == 'frequent':
            star_weights = [self.star_freq.get(i, 1) for i in range(1, 13)]
        elif mode == 'rare':
            max_star_freq = max(self.star_freq.values()) if self.star_freq else 1
            star_weights = [max_star_freq - self.star_freq.get(i, 0) + 1 for i in range(1, 13)]

        star_weights = np.array(star_weights)
        star_weights = star_weights / star_weights.sum()

        # Générer les numéros
        numbers = set()
        while len(numbers) < 5:
            num = np.random.choice(range(1, 51), p=number_weights)
            numbers.add(num)
        numbers = sorted(list(numbers))

        # Générer les étoiles
        stars = set()
        while len(stars) < 2:
            star = np.random.choice(range(1, 13), p=star_weights)
            stars.add(star)
        stars = sorted(list(stars))

        return numbers, stars

    def generate_multiple_grids(self, count: int, mode: str = 'uniform') -> List[Tuple[List[int], List[int]]]:
        """Génère plusieurs grilles"""
        grids = []
        for _ in range(count):
            if mode == 'uniform':
                grid = self.generate_uniform_grid()
            else:
                grid = self.generate_weighted_grid(mode)
            grids.append(grid)
        return grids

    def update_frequencies(self, number_freq: Counter, star_freq: Counter):
        """Met à jour les fréquences pour la génération pondérée"""
        self.number_freq = number_freq
        self.star_freq = star_freq