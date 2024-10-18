import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# Define the main window class
class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        # Set window title
        self.setWindowTitle('Simple PyQt5 App')

        # Create a button
        self.button = QPushButton('Click Me', self)
        self.button.clicked.connect(self.on_button_click)

        # Set layout and add button
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window size
        self.resize(300, 200)

    def on_button_click(self):
        print("Button clicked!")

# Main function to run the application
def main():
    app = QApplication(sys.argv)

    # Create an instance of the application window
    window = SimpleApp()
    window.show()

    # Run the application loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
