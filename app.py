from pathlib import Path
from tkinter import ttk

import customtkinter as ctk
from tkinter import messagebox

from services.repository import WeatherRepository
from services.weather_service import WeatherService


class WeatherDiaryApp:
    def __init__(self) -> None:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Дневник погоды")
        self.root.geometry("950x620")

        data_path = Path(__file__).resolve().parent.parent / "data" / "data.json"
        repository = WeatherRepository(data_path)
        self.service = WeatherService(repository)

        self._build_ui()
        self._refresh_table(self.service.get_all_records())

    def _build_ui(self) -> None:
        title = ctk.CTkLabel(
            self.root,
            text="Дневник погоды",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.pack(pady=14)

        add_frame = ctk.CTkFrame(self.root)
        add_frame.pack(fill="x", padx=16, pady=8)
        add_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.date_entry = self._entry_with_label(add_frame, "Дата (YYYY-MM-DD)", 0, 0)
        self.temperature_entry = self._entry_with_label(add_frame, "Температура", 0, 1)
        self.description_entry = self._entry_with_label(add_frame, "Описание погоды", 0, 2)

        precip_label = ctk.CTkLabel(add_frame, text="Осадки")
        precip_label.grid(row=0, column=3, padx=8, pady=(10, 2), sticky="w")
        self.precipitation_var = ctk.BooleanVar(value=False)
        self.precipitation_checkbox = ctk.CTkCheckBox(
            add_frame,
            text="Да",
            variable=self.precipitation_var,
        )
        self.precipitation_checkbox.grid(row=1, column=3, padx=8, pady=(0, 10), sticky="w")

        add_button = ctk.CTkButton(
            add_frame,
            text="Добавить запись",
            command=self._on_add_record,
        )
        add_button.grid(row=2, column=0, columnspan=4, pady=(0, 12))

        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.pack(fill="x", padx=16, pady=8)
        filter_frame.grid_columnconfigure((0, 1), weight=1)

        self.filter_date_entry = self._entry_with_label(
            filter_frame, "Фильтр по дате (YYYY-MM-DD)", 0, 0
        )
        self.filter_temp_entry = self._entry_with_label(
            filter_frame, "Температура выше чем", 0, 1
        )

        filter_buttons = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_buttons.grid(row=2, column=0, columnspan=2, pady=(0, 12))
        filter_button = ctk.CTkButton(
            filter_buttons,
            text="Фильтровать",
            command=self._on_filter,
        )
        filter_button.pack(side="left", padx=8)

        reset_button = ctk.CTkButton(
            filter_buttons,
            text="Сбросить фильтры",
            command=self._on_reset_filters,
        )
        reset_button.pack(side="left", padx=8)

        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(8, 16))

        columns = ("date", "temperature", "description", "precipitation")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14,
        )
        self.table.heading("date", text="Дата")
        self.table.heading("temperature", text="Температура")
        self.table.heading("description", text="Описание")
        self.table.heading("precipitation", text="Осадки")

        self.table.column("date", width=140, anchor="center")
        self.table.column("temperature", width=140, anchor="center")
        self.table.column("description", width=420, anchor="w")
        self.table.column("precipitation", width=120, anchor="center")
        self.table.pack(fill="both", expand=True, padx=12, pady=12)

    @staticmethod
    def _entry_with_label(parent, label_text: str, row: int, column: int) -> ctk.CTkEntry:
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=column, padx=8, pady=(10, 2), sticky="w")
        entry = ctk.CTkEntry(parent)
        entry.grid(row=row + 1, column=column, padx=8, pady=(0, 10), sticky="ew")
        return entry

    def _on_add_record(self) -> None:
        try:
            self.service.add_record(
                date=self.date_entry.get(),
                temperature_text=self.temperature_entry.get(),
                description=self.description_entry.get(),
                precipitation=self.precipitation_var.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))
            return

        self._refresh_table(self.service.get_all_records())
        self._clear_input_fields()
        messagebox.showinfo("Успех", "Запись успешно добавлена")

    def _on_filter(self) -> None:
        try:
            records = self.service.filter_records(
                date=self.filter_date_entry.get(),
                min_temperature_text=self.filter_temp_entry.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))
            return

        self._refresh_table(records)

    def _on_reset_filters(self) -> None:
        self.filter_date_entry.delete(0, "end")
        self.filter_temp_entry.delete(0, "end")
        self._refresh_table(self.service.get_all_records())

    def _clear_input_fields(self) -> None:
        self.date_entry.delete(0, "end")
        self.temperature_entry.delete(0, "end")
        self.description_entry.delete(0, "end")
        self.precipitation_var.set(False)

    def _refresh_table(self, records) -> None:
        for item in self.table.get_children():
            self.table.delete(item)

        for record in records:
            self.table.insert(
                "",
                "end",
                values=(
                    record.date,
                    record.temperature,
                    record.description,
                    "Да" if record.precipitation else "Нет",
                ),
            )

    def run(self) -> None:
        self.root.mainloop()
