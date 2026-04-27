from dataclasses import dataclass


@dataclass
class WeatherRecord:
    date: str
    temperature: float
    description: str
    precipitation: bool

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "temperature": self.temperature,
            "description": self.description,
            "precipitation": self.precipitation,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WeatherRecord":
        return cls(
            date=str(data["date"]),
            temperature=float(data["temperature"]),
            description=str(data["description"]),
            precipitation=bool(data["precipitation"]),
        )
