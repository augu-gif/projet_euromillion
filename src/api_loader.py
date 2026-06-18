import json
import re
import urllib.error
import urllib.request
from typing import Any, Dict, List


class EuroMillionsAPIClient:
    """Client pour charger les tirages EuroMillions depuis une API JSON."""

    def __init__(self, api_url: str, timeout: int = 15):
        self.api_url = api_url.strip()
        self.timeout = timeout

    def fetch_draws(self) -> List[Dict[str, Any]]:
        """Récupère la liste des tirages depuis l'API."""
        if not self.api_url:
            raise ValueError("URL de l'API manquante")

        try:
            request = urllib.request.Request(
                self.api_url,
                headers={
                    'User-Agent': 'EuroMillionsApp/1.0',
                    'Accept': 'application/json',
                }
            )
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                content = response.read()
                data = json.loads(content.decode('utf-8'))
        except urllib.error.HTTPError as e:
            raise ValueError(f"Erreur HTTP lors de la requête API : {e.code} {e.reason}")
        except urllib.error.URLError as e:
            raise ValueError(f"Impossible de se connecter à l'API : {e.reason}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Réponse API invalide (JSON attendu) : {e}")

        if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
            data = data['data']

        if not isinstance(data, list):
            raise ValueError("Le format JSON de l'API doit être une liste de tirages")

        return [self._normalize_draw(draw) for draw in data]

    def save_to_local(self, file_path: str) -> None:
        """Sauvegarde les tirages récupérés dans un fichier local JSON."""
        draws = self.fetch_draws()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(draws, f, ensure_ascii=False, indent=2)

    def _normalize_draw(self, draw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalise les clés de tirage pour correspondre au traitement existant."""
        return {
            'date': self._get_value(draw, ['date', 'draw_date', 'drawDate']),
            'numbers': self._normalize_number_list(self._get_value(draw, ['numbers', 'main_numbers', 'balls', 'result'])),
            'stars': self._normalize_number_list(self._get_value(draw, ['stars', 'lucky_stars', 'luckyStars'])),
            'prize': self._get_value(draw, ['prize', 'jackpot', 'amount']),
            'has_winner': self._get_value(draw, ['has_winner', 'hasWinner'], default=False),
        }

    @staticmethod
    def _get_value(draw: Dict[str, Any], keys: List[str], default=None):
        for key in keys:
            if key in draw:
                return draw[key]
        return default

    @staticmethod
    def _normalize_number_list(value: Any) -> List[Any]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            cleaned = re.split(r'[\s,;\|]+', value.strip())
            return [item for item in cleaned if item]
        return []
