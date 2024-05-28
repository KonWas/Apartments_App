import tkinter as tk
from tkinter import ttk
from typing import Callable
import os
from PIL import Image, ImageTk
from .charts_classes import ChartsWindowMenu
from .predictions_classes import PredictionWindow
from .investments_classes import InvestmentsWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("APPartments")
        # On windows, 800x700
        self.geometry("950x740")
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
            # Change all white pixels to transparent
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


def main_tkinter() -> None:
    """Start the Tkinter application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
