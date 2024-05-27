import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple
from shapely.geometry import Polygon, Point
from prediction_models import input_pred
from gui.map import start_pyqt, show_saved_location


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

        districts = {
            "Śródmieście": Polygon([
                (51.12544483948943, 17.021441096800885),
                (51.12216439556502, 17.02160048342887),
                (51.118189675105924, 17.017740392186965),
                (51.115733657001215, 17.01954401620324),
                (51.11468115270256, 17.024328412328714),
                (51.11394027234101, 17.02886562911715),
                (51.115071014171775, 17.033783814017454),
                (51.114525063777506, 17.037130649696167),
                (51.11358969579484, 17.04035995479262),
                (51.113746131446845, 17.043338558036425),
                (51.11234307048804, 17.047682828694008),
                (51.11023858259068, 17.053270184275277),
                (51.10743248673211, 17.055132720164465),
                (51.10680888537206, 17.0582365777488),
                (51.10579693344218, 17.06258332623551),
                (51.10166374922923, 17.07387989331835),
                (51.09651865595214, 17.090267531698686),
                (51.093945628624624, 17.102682523907447),
                (51.09558416839192, 17.108267099468065),
                (51.098549130159654, 17.115833431845545),
                (51.10096243265886, 17.124781519157807),
                (51.11101758162289, 17.112372394489967),
                (51.118967874187746, 17.100697367237103),
                (51.12535725557967, 17.092625936280115),
                (51.12691756867588, 17.085551959299494),
                (51.12777715011853, 17.067919333039157),
                (51.12659896550679, 17.063777053601683),
                (51.1301776047701, 17.05662153465829),
                (51.12847674412208, 17.050429487412543),
                (51.126294124582756, 17.040960880095128),
                (51.126293516753634, 17.033230172702133),
                (51.12653673759135, 17.026368808691416),
                (51.12544483948943, 17.021441096800885)
            ]),
            "Stare Miasto": Polygon([
                (51.10976639915023, 17.051953395766162),
                (51.11332238735105, 17.042039665660894),
                (51.114902625124756, 17.03543135971637),
                (51.113126610360155, 17.03007808309053),
                (51.11470767261639, 17.020004198628556),
                (51.118858698318576, 17.016696317282708),
                (51.12093279626481, 17.01905913591608),
                (51.12448735661991, 17.02016358319429),
                (51.128740845770835, 17.014647592384705),
                (51.130817650160026, 17.00441121713024),
                (51.12122811313472, 17.00009950251639),
                (51.11307652550579, 16.997783851686258),
                (51.10709874873845, 17.001596478450978),
                (51.10334533079967, 17.014350125957378),
                (51.102159876386935, 17.02284558891884),
                (51.09840479811277, 17.03983685601611),
                (51.10334429773968, 17.041567847186116),
                (51.10779058850363, 17.04487129187123),
                (51.10976639915023, 17.051953395766162)
            ]),
            "Psie Pole": Polygon([
                (51.15946371043469, 16.963796820660747),
                (51.15487029676265, 16.9776415340111),
                (51.143134927277316, 16.987393698146604),
                (51.13445702735254, 16.99633119514803),
                (51.1298628719, 17.012197860503733),
                (51.126034144623446, 17.02013001084849),
                (51.12629154460336, 17.03620238829842),
                (51.128589834574996, 17.051658832668522),
                (51.130374585487544, 17.061417136215596),
                (51.12909866551868, 17.088667646280697),
                (51.11352728565481, 17.11428967191162),
                (51.102037480314664, 17.129336485365343),
                (51.090800630683674, 17.143569415544505),
                (51.08083881066034, 17.149261685970544),
                (51.08850020480273, 17.16431262850159),
                (51.11378044334961, 17.18953776249404),
                (51.14364576866839, 17.198032926000394),
                (51.16914648419038, 17.17485964753763),
                (51.18265532695236, 17.093951138102028),
                (51.178848509234484, 17.0235859451534),
                (51.17247210114046, 16.983927762791453),
                (51.15946371043469, 16.963796820660747)
            ]),
            "Fabryczna": Polygon([
                (51.109657914324174, 17.05201110202998),
                (51.10786445267709, 17.04453983066469),
                (51.09834398212914, 17.039925555058232),
                (51.099586058591086, 17.033334360786853),
                (51.103504831226985, 17.01347778712028),
                (51.090953613587914, 17.001117301194768),
                (51.07444969647358, 16.991265033301033),
                (51.04944295042358, 16.97412018102267),
                (51.00140388865435, 17.038383935430744),
                (51.0202167963395, 17.152888061930298),
                (51.05513999893128, 17.18501640007426),
                (51.07749305422507, 17.16662483848623),
                (51.08063023282335, 17.14790645483916),
                (51.09042834944054, 17.141345003391848),
                (51.10042283800985, 17.12449795684904),
                (51.09219393376617, 17.098914201873697),
                (51.10727871441483, 17.056164745665626),
                (51.109657914324174, 17.05201110202998)
            ]),
            "Krzyki": Polygon([
                (51.10409029044584, 17.012865036238964),
                (51.106242813623254, 17.002252882022276),
                (51.113558018349664, 16.997788516272436),
                (51.13031881282134, 17.00227390875847),
                (51.136553358694584, 16.98993648384038),
                (51.14321616925116, 16.977604011219427),
                (51.15116585690828, 16.977937535071845),
                (51.155464790119396, 16.9714387587928),
                (51.156539021557734, 16.9546530053197),
                (51.1672796376663, 16.941292329364472),
                (51.17544113522425, 16.93033065584271),
                (51.18768213246554, 16.922109553250607),
                (51.18790372556694, 16.910118717957687),
                (51.1683402895556, 16.860821401743408),
                (51.15051780710627, 16.84610139915543),
                (51.124956863591564, 16.86866586149071),
                (51.089462219539655, 16.86939692018487),
                (51.050957248187075, 16.875591587239086),
                (51.03287901169125, 16.92419308554875),
                (51.02533308517158, 16.97176950294815),
                (51.04988960109162, 16.97382896391656),
                (51.08667226716105, 16.99676699202149),
                (51.10409029044584, 17.012865036238964)
            ])
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
