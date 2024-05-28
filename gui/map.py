import sys
import os
from typing import Optional, Tuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from geopy.geocoders import Nominatim
import folium

location_coords = None
app = None
map_window = None

def create_map(filename: str = 'gui/wroclaw_map.html') -> None:
    """Create a map of Wrocław and save it to a file if it does not already exist."""
    if not os.path.exists(filename):
        start_coords = (51.107883, 17.038538)
        map = folium.Map(location=start_coords, zoom_start=14, min_zoom=12, max_zoom=17)
        folium.Marker(start_coords, popup='Centrum Wrocławia').add_to(map)
        map.save(filename)

class MapWindow(QMainWindow):
    def __init__(self) -> None:
        """Initialize the MapWindow."""
        super().__init__()
        self.current_coords = None
        self.initUI()

    def initUI(self) -> None:
        """Set up the user interface for the MapWindow."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.address_input = QLineEdit(self)
        self.search_button = QPushButton('Szukaj', self)
        self.search_button.clicked.connect(self.search_location)

        self.browser = QWebEngineView()
        self.browser.load(QUrl.fromLocalFile(os.path.abspath("gui/wroclaw_map.html")))

        layout.addWidget(self.address_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.browser)

        self.save_button = QPushButton('Zapisz', self)
        self.save_button.clicked.connect(self.save_location)
        layout.addWidget(self.save_button)

        self.setWindowTitle('Interaktywna Mapa Wrocławia')
        self.setGeometry(600, 300, 800, 600)

    def search_location(self) -> None:
        """Search for a location using the address provided by the user."""
        address = self.address_input.text()
        geolocator = Nominatim(user_agent="konwas")
        location = geolocator.geocode(address)
        if location:
            self.update_map(location.latitude, location.longitude)

    def update_map(self, lat: float, lng: float) -> None:
        """Update the map to show a marker at the specified latitude and longitude."""
        script = f'''
            addOrUpdateMarker('searchResult', {lat}, {lng});
        '''
        self.browser.page().runJavaScript(script)
        self.current_coords = (lat, lng)

    def save_location(self) -> None:
        """Save the current location coordinates and hide the map window."""
        global location_coords
        location_coords = self.current_coords
        self.hide()

def start_pyqt() -> None:
    """Start the PyQt application and display the map window."""
    global app, map_window
    create_map()
    if app is None:
        app = QApplication(sys.argv)
    if map_window is None:
        map_window = MapWindow()
    map_window.show()

# TESTING PURPOSES
# def open_map() -> None:
#     """Open the map in a new thread to avoid blocking the Tkinter main loop."""
#     threading.Thread(target=start_pyqt).start()

def show_saved_location() -> Optional[Tuple[float, float]]:
    """Return the saved location coordinates."""
    return location_coords

# TESTING PURPOSES
# def main() -> None:
#     """Main function to start the Tkinter application."""
#     root = tk.Tk()
#     root.title("Główne Okno Tkinter")

#     mainframe = ttk.Frame(root, padding="3 3 12 12")
#     mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#     ttk.Button(mainframe, text="Otwórz Mapę", command=open_map).grid(column=1, row=1, sticky=tk.W)

#     root.mainloop()

# if __name__ == '__main__':
#     main()