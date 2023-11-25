import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel

class Homepage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        

        welcome_label = QLabel("Welcome to ReviewAnnotator!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #BEFEFB;")

        self.button1 = QPushButton("Annotate existing Reviews", self)
        self.button2 = QPushButton("Scrape More Reviews", self)
        self.button1.setStyleSheet(
            "font-size: 16px; background-color: #008CBA;font-family: Poppins ;padding: 5px; color: white;font-weight:bold;"
        )
        self.button2.setStyleSheet(
            "font-size: 16px; background-color: #008CBA;font-family: Poppins ;padding: 5px; color: white;font-weight:bold;"
        )

        main_layout.addWidget(welcome_label)
        main_layout.addWidget(self.button1)
        main_layout.addWidget(self.button2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 800, 600)

        homepage = Homepage()
        self.setCentralWidget(homepage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
