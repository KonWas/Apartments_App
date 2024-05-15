import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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
            "Lokalizacja": ttk.Button(form_frame, text="Wybierz lokację z mapy"),
            "Powierzchnia": ttk.Entry(form_frame),
            "Liczba pokoi": ttk.Entry(form_frame),
            "Rok budowy": ttk.Entry(form_frame),
            "Piętro": ttk.Spinbox(form_frame, from_=0, to=50),
            "Liczba pięter": ttk.Spinbox(form_frame, from_=1, to=50),
            "Parking": ttk.Checkbutton(form_frame, text="Tak"),
            "Rynek": ttk.Combobox(form_frame, values=["wtórny", "pierwotny"]),
            "Umeblowany": ttk.Checkbutton(form_frame, text="Tak"),
            "Stan": ttk.Combobox(form_frame, values=["bardzo dobry", "wysoki standard", "do wykończenia", "deweloperski", "dobry", "do remontu", "nowe wykończone", "do odświeżenia"])
        }

        for i, (text, widget) in enumerate(self.widgets.items()):
            label = ttk.Label(form_frame, text=text)
            label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            widget.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)

        # Save button
        save_button = ttk.Button(form_frame, text="Zapisz", command=self.save_data)
        save_button.grid(row=len(self.widgets), column=0, columnspan=2, pady=10)

    def validate_data(self):
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

    def save_data(self):
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
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                self.data[dict_translations[key]] = widget.get()
            elif isinstance(widget, ttk.Checkbutton):
                self.data[dict_translations[key]] = 1 if widget.instate(['selected']) else 0
            elif isinstance(widget, ttk.Button):
                self.data[dict_translations[key]] = "Button clicked"
        print(self.data)  # Print data to check if it is saved correctly

    def go_back(self):
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
