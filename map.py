import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from geopy.geocoders import Nominatim
import folium

def create_map(filename='wroclaw_map.html'):
    if not os.path.exists(filename):
        start_coords = (51.107883, 17.038538)
        map = folium.Map(location=start_coords, zoom_start=14, min_zoom=12, max_zoom=17)
        folium.Marker(start_coords, popup='Centrum Wrocławia').add_to(map)
        map.save(filename)

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.address_input = QLineEdit(self)
        self.search_button = QPushButton('Szukaj', self)
        self.search_button.clicked.connect(self.search_location)

        self.browser = QWebEngineView()
        self.browser.load(QUrl.fromLocalFile(r"/Users/konwas/Documents/university/MSiD/msid_projekt/wroclaw_map.html"))

        layout.addWidget(self.address_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.browser)

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

if __name__ == '__main__':
    create_map()
    app = QApplication(sys.argv)
    ex = MapWindow()
    ex.show()
    sys.exit(app.exec_())

