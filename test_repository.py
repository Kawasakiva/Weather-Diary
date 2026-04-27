import json
from pathlib import Path

from models.weather_record import WeatherRecord
from services.repository import WeatherRepository


def test_save_and_load_records(tmp_path: Path) -> None:
    data_file = tmp_path / "data.json"
    repository = WeatherRepository(data_file)
    records = [
        WeatherRecord(
            date="2026-04-27",
            temperature=12.0,
            description="Ясно",
            precipitation=False,
        )
    ]

    repository.save(records)
    loaded = repository.load()

    assert len(loaded) == 1
    assert loaded[0].date == "2026-04-27"
    assert loaded[0].temperature == 12.0
    assert loaded[0].description == "Ясно"
    assert loaded[0].precipitation is False


def test_load_missing_file_returns_empty(tmp_path: Path) -> None:
    data_file = tmp_path / "missing.json"
    repository = WeatherRepository(data_file)
    assert repository.load() == []


def test_load_corrupted_json_returns_empty(tmp_path: Path) -> None:
    data_file = tmp_path / "data.json"
    data_file.write_text("{not valid json}", encoding="utf-8")
    repository = WeatherRepository(data_file)
    assert repository.load() == []


def test_saved_json_is_list(tmp_path: Path) -> None:
    data_file = tmp_path / "data.json"
    repository = WeatherRepository(data_file)
    repository.save([])
    data = json.loads(data_file.read_text(encoding="utf-8"))
    assert isinstance(data, list)
