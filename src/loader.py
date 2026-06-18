import json
import os
import re
from urllib import request, error
from datetime import datetime
from dateutil import parser as dateparser

class DataLoader:
    """Classe pour charger et mettre à jour les données JSON des tirages EuroMillions"""

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

    def save(self, data: list) -> None:
        """Enregistre les données dans le fichier JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise ValueError(f"Erreur lors de l'écriture du fichier : {e}")

    def update_from_external_source(self, external_url: str) -> list:
        """Mets à jour le fichier JSON en récupérant les résultats depuis une source externe."""
        raw_data = self._fetch_external_data(external_url)
        normalized = self._normalize_external_draws(raw_data)
        if not normalized:
            raise ValueError("Aucune donnée valide récupérée depuis la source externe.")

        existing = self.load()
        existing_by_date = {self._normalize_date(draw.get('date')): draw for draw in existing}
        added = 0
        for draw in normalized:
            date_key = self._normalize_date(draw.get('date'))
            if date_key and date_key not in existing_by_date:
                existing.append(draw)
                existing_by_date[date_key] = draw
                added += 1

        if added > 0:
            existing.sort(key=lambda x: self._normalize_date(x.get('date')) or '')
            self.save(existing)
        return existing

    def _fetch_external_data(self, url: str) -> list:
        req = request.Request(url, headers={
            'User-Agent': 'python-urllib/3.11',
            'Accept': 'application/json'
        })
        try:
            with request.urlopen(req, timeout=15) as resp:
                payload = resp.read().decode('utf-8')
                data = json.loads(payload)
                if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
                    return data['data']
                if isinstance(data, list):
                    return data
                raise ValueError('Format JSON inattendu pour la source externe.')
        except error.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e.code} {e.reason}")
        except error.URLError as e:
            raise RuntimeError(f"URL error: {e}")
        except Exception as e:
            raise RuntimeError(f"Impossible de récupérer la source externe : {e}")

    def _normalize_external_draws(self, draws: list) -> list:
        normalized = []
        for draw in draws:
            if not isinstance(draw, dict):
                continue
            date = self._normalize_date(draw.get('date') or draw.get('draw_date') or draw.get('drawDate'))
            numbers = self._extract_numbers(draw)
            stars = self._extract_stars(draw)
            prize = self._extract_prize(draw)
            has_winner = draw.get('has_winner', False)
            normalized.append({
                'date': date,
                'numbers': [str(n) for n in numbers],
                'stars': [str(s) for s in stars],
                'prize': prize,
                'has_winner': has_winner,
                'draw_id': draw.get('draw_id') or draw.get('id'),
                'id': draw.get('id') or draw.get('draw_id')
            })
        return normalized

    def _normalize_date(self, value):
        if value is None:
            return None
        try:
            dt = dateparser.parse(str(value))
            return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
        except:
            return None

    def _extract_numbers(self, draw):
        candidates = []
        for key in ['numbers', 'balls', 'winning_numbers', 'draw']:
            value = draw.get(key)
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                for n in value:
                    try:
                        num = int(n)
                        if 1 <= num <= 50:
                            candidates.append(num)
                    except:
                        pass
            elif isinstance(value, str):
                parts = re.findall(r'\d+', value)
                for p in parts:
                    try:
                        num = int(p)
                        if 1 <= num <= 50:
                            candidates.append(num)
                    except:
                        pass
        return sorted(set(candidates))[:5]

    def _extract_stars(self, draw):
        candidates = []
        for key in ['stars', 'lucky_stars', 'lucky_numbers']:
            value = draw.get(key)
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                for s in value:
                    try:
                        num = int(s)
                        if 1 <= num <= 12:
                            candidates.append(num)
                    except:
                        pass
            elif isinstance(value, str):
                parts = re.findall(r'\d+', value)
                for p in parts:
                    try:
                        num = int(p)
                        if 1 <= num <= 12:
                            candidates.append(num)
                    except:
                        pass
        return sorted(set(candidates))[:2]

    def _extract_prize(self, draw):
        prize = draw.get('prize') or draw.get('jackpot') or draw.get('estimated_jackpot')
        if prize is None:
            return None
        try:
            if isinstance(prize, str):
                prize = prize.replace(' ', '').replace('€', '').replace(',', '.')
            return float(prize)
        except:
            return None
