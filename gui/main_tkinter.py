import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui.map import start_pyqt, show_saved_location
from shapely.geometry import Point, Polygon
from prediction_models import input_pred


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja GUI")
        self.geometry("800x600")
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
        ChartsWindow(self)

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

class ChartsWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        ttk.Label(self, text="Wykresy", font=("Helvetica", 18)).grid(column=0, row=0, pady=10)
        ttk.Button(self, text="Powrót do Menu", command=self.go_back).grid(column=0, row=1, pady=10)

    def go_back(self):
        self.destroy()
        self.master.show_main_frame()

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
        self.buttonReturn = ttk.Button(content_frame, text="Powrót", command=self.go_back)
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
            "Powierzchnia": ttk.Entry(form_frame),
            "Liczba pokoi": ttk.Entry(form_frame),
            "Rok budowy": ttk.Entry(form_frame),
            "Piętro": ttk.Spinbox(form_frame, from_=0, to=50),
            "Liczba pięter": ttk.Spinbox(form_frame, from_=1, to=50),
            "Parking": ttk.Checkbutton(form_frame, text="Tak"),
            "Rynek": ttk.Combobox(form_frame, values=["wtórny", "pierwotny"]),
            "Umeblowany": ttk.Checkbutton(form_frame, text="Tak"),
            "Stan": ttk.Combobox(form_frame, values=["bardzo dobry", "do wykończenia", "deweloperski", "dobry", "do remontu"])
        }

        for i, (text, widget) in enumerate(self.widgets.items()):
            label = ttk.Label(form_frame, text=text)
            label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)

        self.current_location_label = ttk.Label(form_frame, text="Wybierz lokalizację z mapy")
        self.current_location_label.grid(row=0, column=2, columnspan=2, pady=10)

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
            self.current_location_label.config(text=f"{district} ({location[0]:.4f}, {location[1]:.4f})")
            # CZEMU TO SIE AKTUALIZUJE DOPIERO PO PONOWNYM KLIKNIECIU W PRZYCISK?
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

        # districts = {
        #     "Krzyki": Polygon([
        #         (51.061, 17.019), (51.066, 17.024), (51.070, 17.028), (51.073, 17.032),
        #         (51.075, 17.038), (51.080, 17.040), (51.085, 17.045), (51.090, 17.048),
        #         (51.092, 17.050), (51.095, 17.054), (51.098, 17.060), (51.100, 17.063),
        #         (51.105, 17.067), (51.110, 17.070), (51.115, 17.075), (51.120, 17.078),
        #         (51.125, 17.080), (51.130, 17.085), (51.135, 17.088), (51.140, 17.090),
        #         (51.145, 17.095), (51.150, 17.100), (51.155, 17.105), (51.160, 17.110),
        #         (51.165, 17.115), (51.170, 17.120), (51.175, 17.125), (51.180, 17.130),
        #         (51.185, 17.135), (51.190, 17.140), (51.195, 17.145), (51.200, 17.150),
        #         (51.205, 17.155), (51.210, 17.160), (51.215, 17.165), (51.220, 17.170),
        #         (51.225, 17.175), (51.230, 17.180), (51.235, 17.185), (51.240, 17.190),
        #         (51.245, 17.195), (51.250, 17.200)
        #     ]),
        #     "Stare Miasto": Polygon([
        #         (51.107, 17.024), (51.110, 17.029), (51.113, 17.032), (51.116, 17.035),
        #         (51.119, 17.038), (51.122, 17.041), (51.125, 17.044), (51.128, 17.047),
        #         (51.131, 17.050), (51.134, 17.053), (51.137, 17.056), (51.140, 17.059),
        #         (51.143, 17.062), (51.146, 17.065), (51.149, 17.068), (51.152, 17.071),
        #         (51.155, 17.074), (51.158, 17.077), (51.161, 17.080), (51.164, 17.083),
        #         (51.167, 17.086), (51.170, 17.089), (51.173, 17.092), (51.176, 17.095),
        #         (51.179, 17.098), (51.182, 17.101), (51.185, 17.104), (51.188, 17.107),
        #         (51.191, 17.110), (51.194, 17.113), (51.197, 17.116), (51.200, 17.119),
        #         (51.203, 17.122), (51.206, 17.125), (51.209, 17.128), (51.212, 17.131),
        #         (51.215, 17.134), (51.218, 17.137), (51.221, 17.140), (51.224, 17.143),
        #         (51.227, 17.146), (51.230, 17.149), (51.233, 17.152), (51.236, 17.155),
        #         (51.239, 17.158), (51.242, 17.161)
        #     ]),
        #     "Fabryczna": Polygon([
        #         (51.107, 16.870), (51.110, 16.875), (51.113, 16.880), (51.116, 16.885),
        #         (51.119, 16.890), (51.122, 16.895), (51.125, 16.900), (51.128, 16.905),
        #         (51.131, 16.910), (51.134, 16.915), (51.137, 16.920), (51.140, 16.925),
        #         (51.143, 16.930), (51.146, 16.935), (51.149, 16.940), (51.152, 16.945),
        #         (51.155, 16.950), (51.158, 16.955), (51.161, 16.960), (51.164, 16.965),
        #         (51.167, 16.970), (51.170, 16.975), (51.173, 16.980), (51.176, 16.985),
        #         (51.179, 16.990), (51.182, 16.995), (51.185, 17.000), (51.188, 17.005),
        #         (51.191, 17.010), (51.194, 17.015), (51.197, 17.020), (51.200, 17.025),
        #         (51.203, 17.030), (51.206, 17.035), (51.209, 17.040), (51.212, 17.045),
        #         (51.215, 17.050), (51.218, 17.055), (51.221, 17.060), (51.224, 17.065),
        #         (51.227, 17.070), (51.230, 17.075), (51.233, 17.080), (51.236, 17.085),
        #         (51.239, 17.090), (51.242, 17.095)
        #     ]),
        #     "Psie Pole": Polygon([
        #         (51.120, 17.040), (51.125, 17.045), (51.130, 17.050), (51.135, 17.055),
        #         (51.140, 17.060), (51.145, 17.065), (51.150, 17.070), (51.155, 17.075),
        #         (51.160, 17.080), (51.165, 17.085), (51.170, 17.090), (51.175, 17.095),
        #         (51.180, 17.100), (51.185, 17.105), (51.190, 17.110), (51.195, 17.115),
        #         (51.200, 17.120), (51.205, 17.125), (51.210, 17.130), (51.215, 17.135),
        #         (51.220, 17.140), (51.225, 17.145), (51.230, 17.150), (51.235, 17.155),
        #         (51.240, 17.160), (51.245, 17.165), (51.250, 17.170), (51.255, 17.175),
        #         (51.260, 17.180), (51.265, 17.185), (51.270, 17.190), (51.275, 17.195),
        #         (51.280, 17.200), (51.285, 17.205), (51.290, 17.210), (51.295, 17.215),
        #         (51.300, 17.220), (51.305, 17.225), (51.310, 17.230), (51.315, 17.235),
        #         (51.320, 17.240), (51.325, 17.245), (51.330, 17.250)
        #     ]),
        #     "Śródmieście": Polygon([
        #         (51.112, 17.034), (51.115, 17.037), (51.118, 17.040), (51.121, 17.043),
        #         (51.124, 17.046), (51.127, 17.049), (51.130, 17.052), (51.133, 17.055),
        #         (51.136, 17.058), (51.139, 17.061), (51.142, 17.064), (51.145, 17.067),
        #         (51.148, 17.070), (51.151, 17.073), (51.154, 17.076), (51.157, 17.079),
        #         (51.160, 17.082), (51.163, 17.085), (51.166, 17.088), (51.169, 17.091),
        #         (51.172, 17.094), (51.175, 17.097), (51.178, 17.100), (51.181, 17.103),
        #         (51.184, 17.106), (51.187, 17.109), (51.190, 17.112), (51.193, 17.115),
        #         (51.196, 17.118), (51.199, 17.121), (51.202, 17.124), (51.205, 17.127),
        #         (51.208, 17.130), (51.211, 17.133), (51.214, 17.136), (51.217, 17.139),
        #         (51.220, 17.142), (51.223, 17.145), (51.226, 17.148), (51.229, 17.151),
        #         (51.232, 17.154), (51.235, 17.157), (51.238, 17.160)
        #     ]),
        # }

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
        ttk.Label(self, text="Inwestycje", font=("Helvetica", 18)).grid(column=0, row=0, pady=10)
        ttk.Button(self, text="Powrót do Menu", command=self.go_back).grid(column=0, row=1, pady=10)

    def go_back(self):
        self.destroy()
        self.master.show_main_frame()

if __name__ == "__main__":
    app = App()
    app.mainloop()
