import sys
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

def create_map():
    # Coordinates of the center of Wrocław
    start_coords = (51.107883, 17.038538)
    # Create a map centered around Wrocław
    map = folium.Map(location=start_coords, zoom_start=13)
    
    # You can add additional features like markers or lines here
    folium.Marker(start_coords, popup='Wrocław City Center').add_to(map)
    
    # Save the map as an HTML file
    map.save('wroclaw_map.html')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set the layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create a QWebEngineView widget to display the map
        self.browser = QWebEngineView()
        
        # Load the HTML file
        file_path = 'wroclaw_map.html'
        self.browser.load(QUrl.fromLocalFile(file_path))
        
        # Add the browser to the layout
        layout.addWidget(self.browser)
        
        # Set the window properties
        self.setWindowTitle('Map of Wrocław')
        self.setGeometry(300, 300, 800, 600)
        self.show()

if __name__ == '__main__':
    create_map()  # Create the map HTML file
    
    # Create the application object
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
