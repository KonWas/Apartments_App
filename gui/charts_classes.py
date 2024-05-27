import tkinter as tk
from tkinter import ttk
from typing import Callable
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.graphs import price_vs_area, avg_price_per_district, price_distribution, price_vs_rooms, price_vs_year, price_vs_floor

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
    def __init__(self, master, chart_title: str, chart_function: Callable):
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
