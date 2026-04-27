from models.weather_record import WeatherRecord
from services.repository import WeatherRepository
from services.validation import parse_temperature, validate_date, validate_description


class WeatherService:
    def __init__(self, repository: WeatherRepository) -> None:
        self.repository = repository
        self.records = self.repository.load()

    def add_record(
        self,
        date: str,
        temperature_text: str,
        description: str,
        precipitation: bool,
    ) -> WeatherRecord:
        validate_date(date)
        temperature = parse_temperature(temperature_text)
        validate_description(description)

        record = WeatherRecord(
            date=date,
            temperature=temperature,
            description=description.strip(),
            precipitation=precipitation,
        )
        self.records.append(record)
        self.repository.save(self.records)
        return record

    def get_all_records(self) -> list[WeatherRecord]:
        return list(self.records)

    def filter_records(
        self,
        date: str = "",
        min_temperature_text: str = "",
    ) -> list[WeatherRecord]:
        filtered = self.records

        if date.strip():
            validate_date(date.strip())
            filtered = [record for record in filtered if record.date == date.strip()]

        if min_temperature_text.strip():
            min_temp = parse_temperature(min_temperature_text.strip())
            filtered = [record for record in filtered if record.temperature > min_temp]

        return filtered
