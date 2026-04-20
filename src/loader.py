import json
import os

class DataLoader:
    """Classe pour charger les données JSON des tirages EuroMillions"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None

    def load(self) -> list:
        """Charge les données depuis le fichier JSON"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Fichier {self.file_path} introuvable")

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON : {e}")
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement : {e}")

    def get_data(self) -> list:
        """Retourne les données chargées"""
        if self.data is None:
            self.load()
        return self.data