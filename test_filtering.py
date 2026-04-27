from pathlib import Path

import pytest

from services.repository import WeatherRepository
from services.weather_service import WeatherService


@pytest.fixture
def service(tmp_path: Path) -> WeatherService:
    repository = WeatherRepository(tmp_path / "data.json")
    svc = WeatherService(repository)
    svc.add_record("2026-04-20", "5", "Пасмурно", True)
    svc.add_record("2026-04-21", "12.3", "Солнечно", False)
    svc.add_record("2026-04-21", "-1", "Снег", True)
    return svc


def test_filter_by_date(service: WeatherService) -> None:
    records = service.filter_records(date="2026-04-21")
    assert len(records) == 2
    assert all(r.date == "2026-04-21" for r in records)


def test_filter_by_temperature_above(service: WeatherService) -> None:
    records = service.filter_records(min_temperature_text="0")
    assert len(records) == 2
    assert all(r.temperature > 0 for r in records)


def test_filter_combined(service: WeatherService) -> None:
    records = service.filter_records(date="2026-04-21", min_temperature_text="10")
    assert len(records) == 1
    assert records[0].description == "Солнечно"


def test_filter_with_invalid_temp(service: WeatherService) -> None:
    with pytest.raises(ValueError, match="Температура должна быть числом"):
        service.filter_records(min_temperature_text="холодно")
