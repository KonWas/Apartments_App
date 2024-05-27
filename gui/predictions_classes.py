import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple
from shapely.geometry import Polygon, Point
from prediction_models import input_pred
from gui.map import start_pyqt, show_saved_location
from gui.districts import districts


class PredictionWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create the widgets for the prediction window."""
        # Create main frame to center the content
        content_frame = ttk.Frame(self, padding="10 10 10 10")
        content_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        # Configure grid to center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # Return button in top left corner
        self.buttonReturn = ttk.Button(content_frame, text="Powrót do Menu", command=self.go_back)
        self.buttonReturn.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Title label
        self.label = ttk.Label(content_frame, text="Predykcja ceny mieszkania", font=("Helvetica", 18))
        self.label.grid(row=0, column=0, pady=10, columnspan=2)

        # Create a frame for the form fields
        form_frame = ttk.Frame(content_frame, padding="10 10 10 10")
        form_frame.grid(row=1, column=0, pady=10)

        # Labels and entry fields in a single column
        self.widgets: Dict[str, tk.Widget] = {
            "Lokalizacja": ttk.Button(form_frame, text="Wybierz lokację z mapy", command=self.open_map),
            "": ttk.Button(form_frame, text="Zobacz lokalizację", command=self.update_location),
            "Powierzchnia": ttk.Entry(form_frame),
            "Liczba pokoi": ttk.Entry(form_frame),
            "Rok budowy": ttk.Entry(form_frame),
            "Piętro": ttk.Spinbox(form_frame, from_=0, to=50),
            "Liczba pięter": ttk.Spinbox(form_frame, from_=1, to=50),
            "Parking": ttk.Checkbutton(form_frame, text="Tak"),
            "Rynek": ttk.Combobox(form_frame, values=["pierwotny", "wtórny"]),
            "Umeblowany": ttk.Checkbutton(form_frame, text="Tak"),
            "Stan": ttk.Combobox(form_frame, values=["bardzo dobry", "dobry", "deweloperski", "do remontu", "do wykończenia"])
        }

        for i, (text, widget) in enumerate(self.widgets.items()):
            label = ttk.Label(form_frame, text=text)
            label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)

        self.current_location_label = ttk.Label(form_frame, text="Wybierz lokalizację z mapy")
        self.current_location_label.grid(row=1, column=2, columnspan=2, pady=10)

        # Save button
        save_button = ttk.Button(form_frame, text="Zapisz", command=self.save_data)
        save_button.grid(row=len(self.widgets), column=0, columnspan=2, pady=10)

    def validate_data(self) -> List[str]:
        """Validate the data from the form fields.
        :return: List of error messages if any validation fails
        """
        errors = []

        # Validate Powierzchnia
        area = self.widgets["Powierzchnia"].get()
        if not area.isdigit() or int(area) <= 0:
            errors.append("Powierzchnia musi być liczbą większą od 0.")

        # Validate Liczba pokoi
        rooms = self.widgets["Liczba pokoi"].get()
        if not rooms.isdigit() or int(rooms) <= 0 or int(rooms) > 10:
            errors.append("Liczba pokoi musi być liczbą większą od 0 i mniejszą od 10.")

        # Validate Rok budowy
        year = self.widgets["Rok budowy"].get()
        if not year.isdigit() or not (1925 <= int(year) <= 2024):
            errors.append("Rok budowy musi być liczbą z zakresu 1925-2024.")

        # Validate Piętro
        floor = self.widgets["Piętro"].get()
        if not floor.isdigit() or int(floor) < 0 or int(floor) > 50 or int(floor) > int(self.widgets["Liczba pięter"].get()):
            errors.append("Piętro musi być liczbą większą lub równą 0, mniejszą od 50 i mniejszą od liczby wszystkich pięter.")

        # Validate Liczba pięter
        total_floors = self.widgets["Liczba pięter"].get()
        if not total_floors.isdigit() or int(total_floors) <= 0 or int(total_floors) > 50:
            errors.append("Liczba pięter musi być liczbą większą od 0 i mniejszą od 50.")

        return errors

    def open_predictions_results(self, data: Dict[str, str]) -> None:
        """Open a new window with predictions results.
        :param data: Dictionary with the form data
        """
        converted_data = [value for key, value in data.items()]
        location, area, rooms, year, floor, total_floors, parking, market, furnished, state = converted_data
        predictions = input_pred(location, float(area), int(rooms), int(floor), int(total_floors), int(year), int(parking), state, int(furnished), market)

        PredictionResultsWindow(self.master, predictions, self)

    def clear_inputs(self) -> None:
        """Clear all input fields in the form."""
        for key, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Spinbox):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, ttk.Checkbutton):
                widget.state(['!selected'])

    def save_data(self) -> None:
        """Save the data from the form fields and validate it."""
        errors = self.validate_data()
        if errors:
            messagebox.showerror("Błąd", "\n".join(errors))
            return

        dict_translations = {
            "Lokalizacja": "location",
            "": "",
            "Powierzchnia": "area",
            "Liczba pokoi": "rooms",
            "Rok budowy": "year",
            "Piętro": "floor",
            "Liczba pięter": "total_floors",
            "Parking": "parking",
            "Rynek": "market",
            "Umeblowany": "furnished",
            "Stan": "state"
        }
        self.data: Dict[str, str] = {}
        for key, widget in self.widgets.items():
            if key == "":
                continue
            if isinstance(widget, ttk.Entry):
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Spinbox):
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Checkbutton):
                self.data[dict_translations[key]] = '1' if widget.instate(['selected']) else '0'
            elif isinstance(widget, ttk.Button):
                location = show_saved_location()
                if location:
                    self.data[dict_translations[key]] = self.coords_to_district(location)
                    self.current_location_label.config(text=f"{self.data[dict_translations[key]]} ({location[0]:.2f}, {location[1]:.2f})")

        self.data['market'] = "primary" if self.data['market'] == "pierwotny" else "secondary"

        self.open_predictions_results(self.data)

    def open_map(self) -> None:
        """Open the map window to select the location."""
        start_pyqt()
        self.update_location()

    def update_location(self) -> None:
        """Update the location field after the map window is closed."""
        location = show_saved_location()
        if location:
            district = self.coords_to_district(location)
            self.current_location_label.config(text=f"{district} ({location[0]:.2f}, {location[1]:.2f})")
        else:
            self.widgets["Lokalizacja"].config(text="Wybierz lokalizację z mapy")

    def coords_to_district(self, coords: Tuple[float, float]) -> str:
        """Convert coordinates to district name.
        :param coords: Tuple with latitude and longitude
        :return: District name
        """
        lat, lon = coords

        # districts = {
        #     "Krzyki": Polygon([(51.060, 16.960), (51.060, 17.080), (51.020, 17.080), (51.020, 17.060), (51.000, 17.060), (51.000, 16.960)]),
        #     "Stare Miasto": Polygon([(51.120, 17.000), (51.120, 17.040), (51.090, 17.040), (51.090, 17.000), (51.070, 17.000), (51.070, 17.020), (51.090, 17.020), (51.090, 17.000)]),
        #     "Fabryczna": Polygon([(51.140, 16.870), (51.140, 17.020), (51.060, 17.020), (51.060, 16.960), (51.000, 16.960), (51.000, 16.870)]),
        #     "Psie Pole": Polygon([(51.220, 17.040), (51.220, 17.160), (51.150, 17.160), (51.150, 17.100), (51.110, 17.100), (51.110, 17.040)]),
        #     "Śródmieście": Polygon([(51.140, 17.040), (51.140, 17.080), (51.090, 17.080), (51.090, 17.040), (51.070, 17.040), (51.070, 17.080), (51.090, 17.080), (51.090, 17.040)])
        # }

        point = Point(lat, lon)

        for district, polygon in districts.items():
            if polygon.contains(point):
                return district

        return "Inne"

    def go_back(self) -> None:
        """Return to the main menu."""
        self.destroy()
        self.master.show_main_frame()


class PredictionResultsWindow(tk.Toplevel):
    def __init__(self, master, predictions: Dict[str, float], prediction_window: PredictionWindow):
        super().__init__(master)
        self.master = master
        self.prediction_window = prediction_window
        self.title("Wyniki Predykcji")
        self.geometry("400x300")
        self.create_widgets(predictions)

    def create_widgets(self, predictions: Dict[str, float]) -> None:
        """Create the widgets for the predictions results window.
        :param predictions: Dictionary with model names and predicted prices
        """
        content_frame = ttk.Frame(self, padding="10 10 10 10")
        content_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        title = ttk.Label(content_frame, text="Wyniki Predykcji", font=("Helvetica", 18))
        title.grid(row=0, column=0, pady=10, columnspan=2)

        results_frame = ttk.Frame(content_frame, padding="10 10 10 10")
        results_frame.grid(row=1, column=0, pady=10)

        for i, (model, prediction) in enumerate(predictions.items()):
            model_label = ttk.Label(results_frame, text=f"{model}:")
            model_label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            prediction_label = ttk.Label(results_frame, text=f"{prediction:.2f} PLN")
            prediction_label.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)

        close_button = ttk.Button(content_frame, text="Zamknij", command=self.close_window)
        close_button.grid(row=2, column=0, pady=10)

    def close_window(self) -> None:
        """Close the window and clear the prediction form inputs."""
        self.prediction_window.clear_inputs()
        self.destroy()
        self.master.show_main_frame()
