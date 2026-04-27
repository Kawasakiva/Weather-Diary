import pytest

from services.validation import parse_temperature, validate_date, validate_description


def test_validate_date_valid() -> None:
    validate_date("2026-04-27")


def test_validate_date_invalid() -> None:
    with pytest.raises(ValueError, match="Неверный формат даты"):
        validate_date("27-04-2026")


def test_parse_temperature_valid() -> None:
    assert parse_temperature("-3.5") == -3.5


def test_parse_temperature_invalid() -> None:
    with pytest.raises(ValueError, match="Температура должна быть числом"):
        parse_temperature("тепло")


def test_validate_description_invalid() -> None:
    with pytest.raises(ValueError, match="Описание не может быть пустым"):
        validate_description("   ")
