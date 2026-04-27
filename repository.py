import json
from json import JSONDecodeError
from pathlib import Path

from models.weather_record import WeatherRecord


class WeatherRepository:
    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[WeatherRecord]:
        if not self.data_file.exists():
            return []

        try:
            raw = json.loads(self.data_file.read_text(encoding="utf-8"))
        except JSONDecodeError:
            return []

        if not isinstance(raw, list):
            return []

        records: list[WeatherRecord] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            try:
                records.append(WeatherRecord.from_dict(item))
            except (KeyError, TypeError, ValueError):
                continue
        return records

    def save(self, records: list[WeatherRecord]) -> None:
        payload = [record.to_dict() for record in records]
        self.data_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
