import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional, Tuple
from .apartments_classes import Apartment, ApartmentsList

class InvestmentsWindow(ttk.Frame):
    def __init__(self, master):
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
        self.geometry("450x300")
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