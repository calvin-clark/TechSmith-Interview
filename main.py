from PySide6.QtWidgets import QApplication
from calculator import CalculatorApp
import sys


if __name__ == "__main__":
    app = QApplication([])

    window = CalculatorApp()
    window.show()

    sys.exit(app.exec())
