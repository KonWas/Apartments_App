import tkinter as tk
from tkinter import ttk
import threading
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from geopy.geocoders import Nominatim
import folium

location_coords = None

# Global instances
app = None
map_window = None

def create_map(filename='gui/wroclaw_map.html'):
    if not os.path.exists(filename):
        start_coords = (51.107883, 17.038538)
        map = folium.Map(location=start_coords, zoom_start=14, min_zoom=12, max_zoom=17)
        folium.Marker(start_coords, popup='Centrum Wrocławia').add_to(map)
        map.save(filename)

class MapWindow(QMainWindow):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.initUI()

    def initUI(self):
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

    def search_location(self):
        address = self.address_input.text()
        geolocator = Nominatim(user_agent="konwas")
        location = geolocator.geocode(address)
        if location:
            self.update_map(location.latitude, location.longitude)

    def update_map(self, lat, lng):
        script = f'''
            addOrUpdateMarker('searchResult', {lat}, {lng});
        '''
        self.browser.page().runJavaScript(script)
        self.current_coords = (lat, lng)

    def save_location(self):
        global location_coords
        location_coords = self.current_coords
        self.hide()
        if self.callback:
            self.callback()

def start_pyqt():
    global app, map_window
    create_map()
    if app is None:
        app = QApplication(sys.argv)
    if map_window is None:
        map_window = MapWindow()
    map_window.show()

def open_map():
    threading.Thread(target=start_pyqt).start()

def show_saved_location():
    return location_coords

def main():
    root = tk.Tk()
    root.title("Główne Okno Tkinter")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Button(mainframe, text="Otwórz Mapę", command=open_map).grid(column=1, row=1, sticky=tk.W)

    root.mainloop()

if __name__ == '__main__':
    main()
