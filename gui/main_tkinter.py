import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.map import start_pyqt, show_saved_location
from gui.graphs import price_vs_area, avg_price_per_district, price_distribution, price_vs_rooms, price_vs_year, price_vs_floor
from shapely.geometry import Point, Polygon
from prediction_models import input_pred
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog


class Apartment:
    def __init__(self, location, price, area, rooms, floor, total_floors, year, parking, state, furnished, market):
        self.location = location
        self.price = price
        self.area = area
        self.rooms = rooms
        self.floor = floor
        self.total_floors = total_floors
        self.year = year
        self.parking = parking
        self.state = state
        self.furnished = furnished
        self.market = market

    def __str__(self):
        return f"Apartment: {self.location}, {self.price}, {self.area}, {self.rooms}, {self.floor}, {self.total_floors}, {self.year}, {self.parking}, {self.state}, {self.furnished}, {self.market}"
    

class ApartmentsList:
    def __init__(self):
        self.apartments = []

    def __len__(self):
        return len(self.apartments)

    def __iter__(self):
        return iter(self.apartments)

    def __contains__(self, apartment):
        return apartment in self.apartments

    def append(self, apartment):
        self.apartments.append(apartment)

    def get_apartments_by_criteria(self, **kwargs):
        filtered_apartments = self.apartments
        if 'location' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.location == kwargs['location']]
        if 'price_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.price >= kwargs['price_min']]
        if 'price_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.price <= kwargs['price_max']]
        if 'area_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.area >= kwargs['area_min']]
        if 'area_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.area <= kwargs['area_max']]
        if 'rooms_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.rooms >= kwargs['rooms_min']]
        if 'rooms_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.rooms <= kwargs['rooms_max']]
        if 'floor_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.floor >= kwargs['floor_min']]
        if 'floor_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.floor <= kwargs['floor_max']]
        if 'total_floors_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.total_floors >= kwargs['total_floors_min']]
        if 'total_floors_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.total_floors <= kwargs['total_floors_max']]
        if 'year_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.year >= kwargs['year_min']]
        if 'year_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.year <= kwargs['year_max']]
        if 'parking' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.parking == kwargs['parking']]
        if 'state' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.state == kwargs['state']]
        if 'furnished' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.furnished == kwargs['furnished']]
        if 'market' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.market == kwargs['market']]
        return filtered_apartments


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja GUI")
        self.geometry("580x600")
        self.create_menu()

    def create_menu(self):
        self.main_frame = ttk.Frame(self, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Center the main frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center the title
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        title = ttk.Label(self.main_frame, text="Menu Główne", font=("Helvetica", 18))
        title.grid(column=0, row=0, pady=10)

        # Create buttons below the title
        self.main_frame.grid_rowconfigure(1, weight=1)
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(column=0, row=1, pady=10)

        self.create_button(buttons_frame, "Wykresy", self.open_charts_window)
        self.create_button(buttons_frame, "Przewidywanie Ceny Mieszkania", self.open_prediction_window)
        self.create_button(buttons_frame, "Inwestycje", self.open_investments_window)

        # Add exit button in the top left corner
        exit_button = ttk.Button(self, text="Zamknij", command=self.quit_app)
        exit_button.place(x=10, y=10)

    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(pady=10, fill=tk.X)

    def open_charts_window(self):
        self.hide_main_frame()
        ChartsWindowMenu(self)

    def open_prediction_window(self):
        self.hide_main_frame()
        PredictionWindow(self)

    def open_investments_window(self):
        self.hide_main_frame()
        InvestmentsWindow(self)

    def hide_main_frame(self):
        self.main_frame.grid_forget()

    def show_main_frame(self):
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def quit_app(self):
        self.quit()

class ChartsWindowMenu(ttk.Frame):
    def __init__(self, master):
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

    def create_button(self, parent, text, command, row, column):
        button = ttk.Button(parent, text=text, command=command)
        button.grid(row=row, column=column, padx=10, pady=10, sticky=tk.EW)

    def open_chart_1(self):
        self.open_chart_window("Cena vs Powierzchnia", price_vs_area)

    def open_chart_2(self):
        self.open_chart_window("Przykładowe przewidywania", avg_price_per_district)

    def open_chart_3(self):
        self.open_chart_window("Rozkład cen", price_distribution)

    def open_chart_4(self):
        self.open_chart_window("Cena vs Liczba Pokoi", price_vs_rooms)

    def open_chart_5(self):
        self.open_chart_window("Cena vs Rok Budowy", price_vs_year)

    def open_chart_6(self):
        self.open_chart_window("Cena vs Piętro", price_vs_floor)

    def open_chart_window(self, chart_title, chart_function):
        ChartWindow(self.master, chart_title, chart_function)

    def go_back(self):
        self.destroy()
        self.master.show_main_frame()

class ChartWindow(tk.Toplevel):
    def __init__(self, master, chart_title, chart_function):
        super().__init__(master)
        self.title(chart_title)
        self.geometry("800x600")
        self.create_widgets(chart_title, chart_function)

    def create_widgets(self, chart_title, chart_function):
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
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_widgets()

    def create_widgets(self):
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
        self.widgets = {
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

    def validate_data(self):
        """Validate the data from the form fields."""
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

    def open_predictions_results(self, data):
        """Open a new window with predictions results.
        :param data: Dictionary with the form data.
        """
        converted_data = [value for key, value in data.items()]
        location = converted_data[0]
        area = converted_data[1]
        rooms = converted_data[2]
        year = converted_data[3]
        floor = converted_data[4]
        total_floors = converted_data[5]
        parking = converted_data[6]
        market = converted_data[7]
        furnished = converted_data[8]
        state = converted_data[9]
        predictions = input_pred(location, area, rooms, floor, total_floors, year, parking, state, furnished, market)

        PredictionResultsWindow(self.master, predictions, self)

        # for testing purposes
        # for model, prediction in predictions.items():
        #     print(f"{model}: {prediction:.2f}")

    def clear_inputs(self):
        for key, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Spinbox):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, ttk.Checkbutton):
                widget.state(['!selected'])

    def save_data(self):
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
        self.data = {}
        for key, widget in self.widgets.items():
            if key == "":
                continue
            if isinstance(widget, ttk.Entry):
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Spinbox):
                self.data[dict_translations[key]] = int(widget.get())
            elif isinstance(widget, ttk.Combobox):
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Checkbutton):
                self.data[dict_translations[key]] = 1 if widget.instate(['selected']) else 0
            elif isinstance(widget, ttk.Button):
                self.data[dict_translations[key]] = self.coords_to_district(show_saved_location())
                print(show_saved_location())

        self.data['market'] = "primary" if self.data['market'] == "pierwotny" else "secondary"

        # print(self.data)  # Print data to check if it is saved correctly

        self.open_predictions_results(self.data)


    def open_map(self):
        """Open the map window to select the location."""
        start_pyqt()
        self.update_location()

    def update_location(self):
        """Update the location field after the map window is closed."""
        location = show_saved_location()
        if location:
            district = self.coords_to_district(location)
            self.current_location_label.config(text=f"{district} ({location[0]:.2f}, {location[1]:.2f})")
        else:
            self.widgets["Lokalizacja"].config(text="Wybierz lokalizację z mapy")

    def coords_to_district(self, coords):
        """Convert coordinates to district name.
        :param coords: Tuple with latitude and longitude.
        :return: District name.
        """
        lat, lon = coords

        districts = {
            "Krzyki": Polygon([(51.060, 16.960), (51.060, 17.080), (51.020, 17.080), (51.020, 17.060), (51.000, 17.060), (51.000, 16.960)]),
            "Stare Miasto": Polygon([(51.120, 17.000), (51.120, 17.040), (51.090, 17.040), (51.090, 17.000), (51.070, 17.000), (51.070, 17.020), (51.090, 17.020), (51.090, 17.000)]),
            "Fabryczna": Polygon([(51.140, 16.870), (51.140, 17.020), (51.060, 17.020), (51.060, 16.960),(51.000, 16.960), (51.000, 16.870)]),
            "Psie Pole": Polygon([(51.220, 17.040), (51.220, 17.160), (51.150, 17.160), (51.150, 17.100),(51.110, 17.100), (51.110, 17.040)]),
            "Śródmieście": Polygon([(51.140, 17.040), (51.140, 17.080), (51.090, 17.080), (51.090, 17.040),(51.070, 17.040), (51.070, 17.080), (51.090, 17.080), (51.090, 17.040)])
        }

        point = Point(lat, lon)
        
        for district, polygon in districts.items():
            if polygon.contains(point):
                return district
        
        return "Inne"

    def go_back(self):
        self.destroy()
        self.master.show_main_frame()


class PredictionResultsWindow(tk.Toplevel):
    def __init__(self, master, predictions, prediction_window):
        super().__init__(master)
        self.master = master
        self.prediction_window = prediction_window
        self.title("Wyniki Predykcji")
        self.geometry("400x300")
        self.create_widgets(predictions)

    def create_widgets(self, predictions):
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

    def close_window(self):
        self.prediction_window.clear_inputs()
        self.destroy()
        self.master.show_main_frame()


class InvestmentsWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.apartments_list = ApartmentsList()
        self.current_apartments = []
        self.create_widgets()

    def create_widgets(self):
        # Create the main layout
        main_layout = ttk.Frame(self)
        main_layout.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Load button
        load_button = ttk.Button(main_layout, text="Wczytaj predefiniowany plik mieszkań", command=self.load_predefined_file)
        load_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Listbox for apartments
        self.apartment_listbox = tk.Listbox(main_layout, width=50, height=20)
        self.apartment_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.apartment_listbox.bind("<<ListboxSelect>>", self.show_details)

        # Detail section
        detail_frame = ttk.Frame(main_layout, padding="10 10 10 10")
        detail_frame.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        detail_labels = ["Lokalizacja:", "Cena:", "Powierzchnia:", "Liczba pokoi:", "Rok budowy:", "Piętro:", "Liczba pięter:", "Parking:", "Stan:", "Rynek:", "Umeblowany:"]
        self.detail_widgets = {}
        for i, label in enumerate(detail_labels):
            ttk.Label(detail_frame, text=label).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.detail_widgets[label] = ttk.Label(detail_frame, text="-")
            self.detail_widgets[label].grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)

        # Filters section
        filter_frame = ttk.Frame(main_layout, padding="10 10 10 10")
        filter_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        ttk.Label(filter_frame, text="Filtry", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        self.filters = {
            "Cena od": tk.IntVar(),
            "Cena do": tk.IntVar(),
            "Powierzchnia od": tk.IntVar(),
            "Powierzchnia do": tk.IntVar(),
            "Liczba pokoi od": tk.IntVar(),
            "Liczba pokoi do": tk.IntVar(),
            "Rok budowy od": tk.IntVar(),
            "Rok budowy do": tk.IntVar()
        }

        row = 1
        for label, var in self.filters.items():
            ttk.Label(filter_frame, text=label).grid(row=row, column=0, sticky=tk.E, padx=5, pady=5)
            ttk.Scale(filter_frame, from_=0, to=1000, orient=tk.HORIZONTAL, variable=var).grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
            row += 1

        apply_filters_button = ttk.Button(filter_frame, text="Zastosuj filtry", command=self.apply_filters)
        apply_filters_button.grid(row=row, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self, text="Powrót do Menu", command=self.go_back)
        back_button.grid(row=3, column=0, pady=10, sticky=tk.W)

    def load_predefined_file(self):
        filepath = r"/Users/konwas/Documents/university/MSiD/msid_projekt/data_cleaned_formated.csv"
        self.load_apartments(filepath)

    def load_apartments(self, filepath):
        # Load apartments from file
        with open(filepath, 'r') as file:
            for line in file:
                apartment_data = line.strip().split(',')
                if len(apartment_data) == 11:
                    apartment = Apartment(*apartment_data)
                    self.apartments_list.append(apartment)
                    self.apartment_listbox.insert(tk.END, str(apartment)[:50] + "...")

    def show_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            apartment = self.current_apartments[index]
            details = [
                apartment.location,
                apartment.price,
                apartment.area,
                apartment.rooms,
                apartment.year,
                apartment.floor,
                apartment.total_floors,
                "Tak" if apartment.parking else "Nie",
                apartment.state,
                apartment.market,
                "Tak" if apartment.furnished else "Nie"
            ]
            for label, detail in zip(self.detail_widgets.keys(), details):
                self.detail_widgets[label].config(text=detail)

    def apply_filters(self):
        # Apply filters to the apartment list
        filtered_apartments = self.apartments_list.get_apartments_by_criteria(
            price_min=self.filters["Cena od"].get(),
            price_max=self.filters["Cena do"].get(),
            area_min=self.filters["Powierzchnia od"].get(),
            area_max=self.filters["Powierzchnia do"].get(),
            rooms_min=self.filters["Liczba pokoi od"].get(),
            rooms_max=self.filters["Liczba pokoi do"].get(),
            year_min=self.filters["Rok budowy od"].get(),
            year_max=self.filters["Rok budowy do"].get()
        )
        self.current_apartments = filtered_apartments
        self.apartment_listbox.delete(0, tk.END)
        for apartment in filtered_apartments:
            self.apartment_listbox.insert(tk.END, str(apartment)[:50] + "...")

    def go_back(self):
        self.destroy()
        self.master.show_main_frame()


def main_tkinter():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
