from datetime import datetime


def validate_date(date_str: str) -> None:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Неверный формат даты") from exc


def parse_temperature(temperature_str: str) -> float:
    try:
        return float(temperature_str)
    except ValueError as exc:
        raise ValueError("Температура должна быть числом") from exc


def validate_description(description: str) -> None:
    if not description or not description.strip():
        raise ValueError("Описание не может быть пустым")
