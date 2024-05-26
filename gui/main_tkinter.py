import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, List, Optional, Tuple
from gui.map import start_pyqt, show_saved_location
from gui.graphs import price_vs_area, avg_price_per_district, price_distribution, price_vs_rooms, price_vs_year, price_vs_floor
from shapely.geometry import Point, Polygon
from prediction_models import input_pred
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from .apartments_classes import ApartmentsList, Apartment
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja GUI")
        self.geometry("800x700")
        self.create_menu()
        self.set_window_icon()

    def create_menu(self) -> None:
        """Create the main menu with buttons and logo."""
        self.main_frame = ttk.Frame(self, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Center the main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center the title
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Add logo
        self.add_logo(self.main_frame)

        # title = ttk.Label(self.main_frame, text="Menu Główne", font=("Helvetica", 18))
        # title.grid(column=0, row=1, pady=10)

        # Create buttons below the title
        self.main_frame.grid_rowconfigure(2, weight=1)
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(column=0, row=2, pady=10)

        self.create_button(buttons_frame, "Wykresy", self.open_charts_window)
        self.create_button(buttons_frame, "Przewidywanie Ceny Mieszkania", self.open_prediction_window)
        self.create_button(buttons_frame, "Inwestycje", self.open_investments_window)

        # Add exit button in the top left corner
        exit_button = ttk.Button(self, text="Zamknij", command=self.quit_app)
        exit_button.place(x=10, y=10)

    def set_window_icon(self) -> None:
        """Set the window icon."""

    def create_button(self, parent: ttk.Frame, text: str, command: Callable) -> None:
        """Helper method to create a button.
        :param parent: Parent frame for the button
        :param text: Text displayed on the button
        :param command: Function to call when the button is clicked
        """
        button = ttk.Button(parent, text=text, command=command)
        button.pack(pady=10, fill=tk.X)

    def add_logo(self, parent: ttk.Frame) -> None:
        """Add the logo to the main menu.
        :param parent: Parent frame to add the logo to
        """
        image_path = os.path.join(os.path.dirname(__file__), "APPartments.png")
        image = Image.open(image_path)

        # Remove the white background
        image = image.convert("RGBA")
        datas = image.getdata()

        new_data = []
        for item in datas:
            # Change all white (also shades of whites)
            # pixels to transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        image.putdata(new_data)

        self.logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(parent, image=self.logo, background="#f0f0f0")
        logo_label.grid(column=0, row=0, pady=10)

    def open_charts_window(self) -> None:
        """Open the window with chart options."""
        self.hide_main_frame()
        ChartsWindowMenu(self)

    def open_prediction_window(self) -> None:
        """Open the prediction window."""
        self.hide_main_frame()
        PredictionWindow(self)

    def open_investments_window(self) -> None:
        """Open the investments window."""
        self.hide_main_frame()
        InvestmentsWindow(self)

    def hide_main_frame(self) -> None:
        """Hide the main frame."""
        self.main_frame.grid_forget()

    def show_main_frame(self) -> None:
        """Show the main frame."""
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def quit_app(self) -> None:
        """Quit the application."""
        self.quit()


class ChartsWindowMenu(ttk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid to center the content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title label centered
        title = ttk.Label(self, text="Wykresy", font=("Helvetica", 18))
        title.grid(row=0, column=0, pady=10)

        # Create a frame for the buttons
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(column=0, row=1, pady=10)

        # Create buttons for different charts in 2 columns, 3 rows
        self.create_button(buttons_frame, "Cena vs Powierzchnia", self.open_chart_1, 0, 0)
        self.create_button(buttons_frame, "Przykładowe przewidywania", self.open_chart_2, 0, 1)
        self.create_button(buttons_frame, "Rozkład cen", self.open_chart_3, 1, 0)
        self.create_button(buttons_frame, "Cena vs Liczba Pokoi", self.open_chart_4, 1, 1)
        self.create_button(buttons_frame, "Cena vs Rok Budowy", self.open_chart_5, 2, 0)
        self.create_button(buttons_frame, "Cena vs Piętro", self.open_chart_6, 2, 1)

        # Return button in top left corner
        back_button = ttk.Button(self, text="Powrót do Menu", command=self.go_back)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    def create_button(self, parent: ttk.Frame, text: str, command: Callable, row: int, column: int) -> None:
        """Helper method to create a button for chart selection.
        :param parent: Parent frame for the button
        :param text: Text displayed on the button
        :param command: Function to call when the button is clicked
        :param row: Row position of the button
        :param column: Column position of the button
        """
        button = ttk.Button(parent, text=text, command=command)
        button.grid(row=row, column=column, padx=10, pady=10, sticky=tk.EW)

    def open_chart_1(self) -> None:
        self.open_chart_window("Cena vs Powierzchnia", price_vs_area)

    def open_chart_2(self) -> None:
        self.open_chart_window("Przykładowe przewidywania", avg_price_per_district)

    def open_chart_3(self) -> None:
        self.open_chart_window("Rozkład cen", price_distribution)

    def open_chart_4(self) -> None:
        self.open_chart_window("Cena vs Liczba Pokoi", price_vs_rooms)

    def open_chart_5(self) -> None:
        self.open_chart_window("Cena vs Rok Budowy", price_vs_year)

    def open_chart_6(self) -> None:
        self.open_chart_window("Cena vs Piętro", price_vs_floor)

    def open_chart_window(self, chart_title: str, chart_function: Callable) -> None:
        """Open a new window to display the selected chart.
        :param chart_title: Title of the chart window
        :param chart_function: Function to generate the chart
        """
        ChartWindow(self.master, chart_title, chart_function)

    def go_back(self) -> None:
        """Return to the main menu."""
        self.destroy()
        self.master.show_main_frame()


class ChartWindow(tk.Toplevel):
    def __init__(self, master: App, chart_title: str, chart_function: Callable):
        super().__init__(master)
        self.title(chart_title)
        self.geometry("800x600")
        self.create_widgets(chart_title, chart_function)

    def create_widgets(self, chart_title: str, chart_function: Callable) -> None:
        """Create the widgets for the chart window.
        :param chart_title: Title of the chart window
        :param chart_function: Function to generate the chart
        """
        content_frame = ttk.Frame(self, padding="10 10 10 10")
        content_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        title = ttk.Label(content_frame, text=chart_title, font=("Helvetica", 18))
        title.grid(row=0, column=0, pady=10)

        chart_frame = ttk.Frame(content_frame)
        chart_frame.grid(row=1, column=0, pady=10)

        fig = chart_function()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        close_button = ttk.Button(content_frame, text="Zamknij", command=self.destroy)
        close_button.grid(row=2, column=0, pady=10)


class PredictionWindow(ttk.Frame):
    def __init__(self, master: App):
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

        districts = {
            "Krzyki": Polygon([(51.060, 16.960), (51.060, 17.080), (51.020, 17.080), (51.020, 17.060), (51.000, 17.060), (51.000, 16.960)]),
            "Stare Miasto": Polygon([(51.120, 17.000), (51.120, 17.040), (51.090, 17.040), (51.090, 17.000), (51.070, 17.000), (51.070, 17.020), (51.090, 17.020), (51.090, 17.000)]),
            "Fabryczna": Polygon([(51.140, 16.870), (51.140, 17.020), (51.060, 17.020), (51.060, 16.960), (51.000, 16.960), (51.000, 16.870)]),
            "Psie Pole": Polygon([(51.220, 17.040), (51.220, 17.160), (51.150, 17.160), (51.150, 17.100), (51.110, 17.100), (51.110, 17.040)]),
            "Śródmieście": Polygon([(51.140, 17.040), (51.140, 17.080), (51.090, 17.080), (51.090, 17.040), (51.070, 17.040), (51.070, 17.080), (51.090, 17.080), (51.090, 17.040)])
        }

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
    def __init__(self, master: App, predictions: Dict[str, float], prediction_window: PredictionWindow):
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


class InvestmentsWindow(ttk.Frame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.apartments_list = ApartmentsList()
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create the widgets for the investments window."""
        # Create the main layout
        main_layout = ttk.Frame(self)
        main_layout.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Return button in top left corner
        back_button = ttk.Button(main_layout, text="Powrót do Menu", command=self.go_back)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Navigation buttons frame
        nav_frame = ttk.Frame(main_layout)
        nav_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=tk.E)

        # Previous and next buttons
        self.prev_button = ttk.Button(nav_frame, text="Poprzednie", command=self.prev_apartment)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.prev_button.config(state=tk.DISABLED)

        self.next_button = ttk.Button(nav_frame, text="Następne", command=self.next_apartment)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.config(state=tk.DISABLED)

        # Listbox for apartments with scrollbar
        listbox_frame = ttk.Frame(main_layout)
        listbox_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.apartment_listbox = tk.Listbox(listbox_frame, width=50, height=20)
        self.apartment_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.apartment_listbox.bind("<<ListboxSelect>>", self.show_details)

        self.scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.apartment_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.apartment_listbox.config(yscrollcommand=self.scrollbar.set)

        # Load apartments from file
        apartments_file = os.path.join(os.path.dirname(__file__), "apartments.txt")
        self.load_apartments(apartments_file)

        # Detail section
        detail_frame = ttk.Frame(main_layout, padding="10 10 10 10")
        detail_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        detail_labels = ["Id:", "Lokalizacja:", "Cena:", "Powierzchnia:", "Liczba pokoi:", "Rok budowy:", "Piętro:", "Liczba pięter:", "Parking:", "Stan:", "Rynek:", "Umeblowany:"]
        self.detail_widgets: Dict[str, ttk.Label] = {}
        for i, label in enumerate(detail_labels):
            ttk.Label(detail_frame, text=label).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.detail_widgets[label] = ttk.Label(detail_frame, text="-")
            self.detail_widgets[label].grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)

        # Filters section
        filter_frame = ttk.Frame(main_layout, padding="10 10 10 10")
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        ttk.Label(filter_frame, text="Filtry", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=5)

        self.filters: Dict[str, Tuple[tk.IntVar, tk.BooleanVar]] = {
            "Cena od": (tk.IntVar(), tk.BooleanVar()),
            "Cena do": (tk.IntVar(), tk.BooleanVar()),
            "Powierzchnia od": (tk.IntVar(), tk.BooleanVar()),
            "Powierzchnia do": (tk.IntVar(), tk.BooleanVar()),
            "Liczba pokoi od": (tk.IntVar(), tk.BooleanVar()),
            "Liczba pokoi do": (tk.IntVar(), tk.BooleanVar()),
            "Rok budowy od": (tk.IntVar(), tk.BooleanVar()),
            "Rok budowy do": (tk.IntVar(), tk.BooleanVar())
        }

        # Create filter widgets
        row = 1

        # Filters for 'Cena od' and 'Cena do'
        for i, (label, (var, chk_var)) in enumerate(list(self.filters.items())[:2]):
            ttk.Label(filter_frame, text=label).grid(row=row + i, column=0, sticky=tk.E, padx=5, pady=5)
            checkbutton = ttk.Checkbutton(filter_frame, variable=chk_var, command=lambda v=var, c=chk_var: self.toggle_filter(v, c))
            checkbutton.grid(row=row + i, column=1, padx=5, pady=5)
            scale = ttk.Scale(filter_frame, from_=0, to=1250000, orient=tk.HORIZONTAL, variable=var, command=lambda v, sv=var: self.update_text_field(sv))
            scale.grid(row=row + i, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
            entry = ttk.Entry(filter_frame, textvariable=var)
            entry.grid(row=row + i, column=3, padx=5, pady=5)

        # Filters for 'Powierzchnia od' and 'Powierzchnia do'
        for i, (label, (var, chk_var)) in enumerate(list(self.filters.items())[2:4]):
            ttk.Label(filter_frame, text=label).grid(row=row + i, column=4, sticky=tk.E, padx=5, pady=5)
            checkbutton = ttk.Checkbutton(filter_frame, variable=chk_var, command=lambda v=var, c=chk_var: self.toggle_filter(v, c))
            checkbutton.grid(row=row + i, column=5, padx=5, pady=5)
            scale = ttk.Scale(filter_frame, from_=0, to=80, orient=tk.HORIZONTAL, variable=var, command=lambda v, sv=var: self.update_text_field(sv))
            scale.grid(row=row + i, column=6, padx=5, pady=5, sticky=(tk.W, tk.E))
            entry = ttk.Entry(filter_frame, textvariable=var)
            entry.grid(row=row + i, column=7, padx=5, pady=5)

        # Filters for 'Liczba pokoi od' and 'Liczba pokoi do'
        for i, (label, (var, chk_var)) in enumerate(list(self.filters.items())[4:6]):
            ttk.Label(filter_frame, text=label).grid(row=row + 2 + i, column=0, sticky=tk.E, padx=5, pady=5)
            checkbutton = ttk.Checkbutton(filter_frame, variable=chk_var, command=lambda v=var, c=chk_var: self.toggle_filter(v, c))
            checkbutton.grid(row=row + 2 + i, column=1, padx=5, pady=5)
            scale = ttk.Scale(filter_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=var, command=lambda v, sv=var: self.update_text_field(sv))
            scale.grid(row=row + 2 + i, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
            entry = ttk.Entry(filter_frame, textvariable=var)
            entry.grid(row=row + 2 + i, column=3, padx=5, pady=5)

        # Filters for 'Rok budowy od' and 'Rok budowy do'
        for i, (label, (var, chk_var)) in enumerate(list(self.filters.items())[6:]):
            ttk.Label(filter_frame, text=label).grid(row=row + 2 + i, column=4, sticky=tk.E, padx=5, pady=5)
            checkbutton = ttk.Checkbutton(filter_frame, variable=chk_var, command=lambda v=var, c=chk_var: self.toggle_filter(v, c))
            checkbutton.grid(row=row + 2 + i, column=5, padx=5, pady=5)
            scale = ttk.Scale(filter_frame, from_=1900, to=2024, orient=tk.HORIZONTAL, variable=var, command=lambda v, sv=var: self.update_text_field(sv))
            scale.grid(row=row + 2 + i, column=6, padx=5, pady=5, sticky=(tk.W, tk.E))
            entry = ttk.Entry(filter_frame, textvariable=var)
            entry.grid(row=row + 2 + i, column=7, padx=5, pady=5)

        apply_filters_button = ttk.Button(filter_frame, text="Zastosuj filtry", command=self.apply_filters)
        apply_filters_button.grid(row=row + 4, column=0, columnspan=8, pady=10)

        invest_button = ttk.Button(filter_frame, text="Zainwestuj", command=self.invest)
        invest_button.grid(row=row + 5, column=0, columnspan=8, pady=10)

    def update_text_field(self, var: tk.IntVar) -> None:
        """Update the text field with the value from the scale.
        :param var: Integer variable bound to the scale and text field
        """
        var.set(int(float(var.get())))

    def toggle_filter(self, var: tk.IntVar, chk_var: tk.BooleanVar) -> None:
        """Enable or disable the filter based on the checkbox state.
        :param var: Integer variable bound to the scale and text field
        :param chk_var: Boolean variable bound to the checkbox
        """
        state = 'normal' if chk_var.get() else 'disabled'
        for widget in self.master.winfo_children():
            if isinstance(widget, ttk.Entry) and widget.cget('textvariable') == str(var):
                widget.config(state=state)
            elif isinstance(widget, ttk.Scale) and widget.cget('variable') == str(var):
                widget.config(state=state)

    def load_apartments(self, filepath: str) -> None:
        """Load apartments from the file and populate the listbox.
        :param filepath: Path to the file containing apartment data
        """
        with open(filepath, 'r') as file:
            for line in file:
                apartment_data = line.strip().split('\t')
                if len(apartment_data) == 12:
                    apartment = Apartment(*apartment_data)
                    self.apartments_list.append(apartment)
                    self.apartment_listbox.insert(tk.END, str(apartment)[:50] + "...")

        self.current_apartments = self.apartments_list.apartments

    def show_details(self, event: Optional[tk.Event] = None) -> None:
        """Show details of the selected apartment.
        :param event: Tkinter event object
        """
        selection = self.apartment_listbox.curselection()
        if selection:
            index = selection[0]
            apartment = self.current_apartments[index]
            details = [
                apartment.id,
                apartment.location,
                apartment.price,
                apartment.area,
                apartment.rooms,
                apartment.year,
                apartment.floor,
                apartment.total_floors,
                apartment.parking,
                apartment.state,
                apartment.market,
                apartment.furnished
            ]
            for label, detail in zip(self.detail_widgets.keys(), details):
                self.detail_widgets[label].config(text=detail)
        self.update_navigation_buttons()

    def apply_filters(self) -> None:
        """Apply the selected filters to the list of apartments."""
        translations = {
            "Cena od": "price_min",
            "Cena do": "price_max",
            "Powierzchnia od": "area_min",
            "Powierzchnia do": "area_max",
            "Liczba pokoi od": "rooms_min",
            "Liczba pokoi do": "rooms_max",
            "Rok budowy od": "year_min",
            "Rok budowy do": "year_max"
        }
        criteria = {}
        for label, (var, chk_var) in self.filters.items():
            if chk_var.get():
                criteria[translations[label]] = var.get()
        filtered_apartments = self.apartments_list.get_apartments_by_criteria(**criteria)

        self.current_apartments = filtered_apartments
        self.apartment_listbox.delete(0, tk.END)
        for apartment in filtered_apartments:
            self.apartment_listbox.insert(tk.END, str(apartment)[:50] + "...")
        self.update_navigation_buttons()

    def prev_apartment(self) -> None:
        """Navigate to the previous apartment in the list."""
        current_row = self.apartment_listbox.curselection()[0]
        if current_row > 0:
            self.apartment_listbox.selection_clear(0, tk.END)
            self.apartment_listbox.selection_set(current_row - 1)
            self.apartment_listbox.see(current_row - 1)
            self.show_details()

    def next_apartment(self) -> None:
        """Navigate to the next apartment in the list."""
        current_row = self.apartment_listbox.curselection()[0]
        if current_row < self.apartment_listbox.size() - 1:
            self.apartment_listbox.selection_clear(0, tk.END)
            self.apartment_listbox.selection_set(current_row + 1)
            self.apartment_listbox.see(current_row + 1)
            self.show_details()

    def update_navigation_buttons(self) -> None:
        """Update the state of the navigation buttons based on the current selection."""
        if not self.apartment_listbox.curselection():
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
        else:
            current_row = self.apartment_listbox.curselection()[0]
            self.prev_button.config(state=tk.NORMAL if current_row > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if current_row < self.apartment_listbox.size() - 1 else tk.DISABLED)

    def go_back(self) -> None:
        """Return to the main menu."""
        self.destroy()
        self.master.show_main_frame()

    def invest(self) -> None:
        """Open the investment window for the selected apartment."""
        InvestWindow(self, self.current_apartments[self.apartment_listbox.curselection()[0]])


class InvestWindow(tk.Toplevel):
    def __init__(self, master: InvestmentsWindow, apartment: Apartment):
        super().__init__(master)
        self.master = master
        self.apartment = apartment
        self.title("Zainwestuj")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create the widgets for the investment window."""
        content_frame = ttk.Frame(self, padding="10 10 10 10")
        content_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        title = ttk.Label(content_frame, text="Zainwestuj", font=("Helvetica", 18))
        title.grid(row=0, column=0, pady=10, columnspan=2)

        # Investment duration label and entry
        duration_label = ttk.Label(content_frame, text="Okres inwestycji (w latach):")
        duration_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.duration_entry = ttk.Entry(content_frame)
        self.duration_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Monthly rental income label and entry
        rental_income_label = ttk.Label(content_frame, text="Miesięczny dochód z najmu:")
        rental_income_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.rental_income_entry = ttk.Entry(content_frame)
        self.rental_income_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Annual expenses label and entry
        annual_expenses_label = ttk.Label(content_frame, text="Roczne koszty:")
        annual_expenses_label.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.annual_expenses_entry = ttk.Entry(content_frame)
        self.annual_expenses_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Calculate ROI button
        calculate_button = ttk.Button(content_frame, text="Oblicz ROI", command=self.calculate_roi)
        calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Close button
        close_button = ttk.Button(content_frame, text="Zamknij", command=self.close_window)
        close_button.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_roi(self) -> None:
        """Calculate and display the ROI based on the provided investment details."""
        try:
            price = self.apartment.price
            duration = float(self.duration_entry.get())
            rental_income = float(self.rental_income_entry.get())
            annual_expenses = float(self.annual_expenses_entry.get())

            if duration <= 0 or rental_income <= 0 or annual_expenses < 0:
                raise ValueError

            annual_net_income = (rental_income * 12) - annual_expenses
            roi = (annual_net_income / price) * 100

            messagebox.showinfo("Wynik ROI", f"Zysk z inwestycji: {roi:.2f}% rocznie")
        except ValueError:
            messagebox.showerror("Błąd", "Wszystkie wartości muszą być poprawnymi liczbami większymi od zera.")

    def close_window(self) -> None:
        """Close the investment window."""
        self.destroy()


def main_tkinter() -> None:
    """Start the Tkinter application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
