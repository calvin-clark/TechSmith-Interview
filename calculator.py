from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from PySide6.QtWidgets import QApplication
import sys

from enum import Enum, auto

#define digits and operations used
DIGITS = set("0123456789")
OPERATIONS = set("+-/*")

"""Enumeration of the button types"""
class ButtonType(Enum):
    DIGIT = auto()
    OPERATION = auto()
    EQUALS = auto()
    CLEAR = auto()
    DECIMAL = auto()

"""Class that represents a button"""
class CalcButton:
    def __init__(self, val: str):
        self.val = val
        self.type = self.find_type(val)
    
    def find_type(self, val):
        """Get the type of the button on its creation"""
        if val in DIGITS:
            return ButtonType.DIGIT
        if val in OPERATIONS:
            return ButtonType.OPERATION
        if val == "=":
            return ButtonType.EQUALS
        if val == "C":
            return ButtonType.CLEAR
        if val == ".":
            return ButtonType.DECIMAL

"""Class that contains the UI and functionality of a calculator"""
class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_number = "0"
        self.current_expression = []
        self.start_new_num = True
        self.has_decimal = False

        self.build_ui()


    def build_ui(self):
        """Builds the calculator's UI"""

        self.setWindowTitle("Calculator")
        self.setMinimumHeight(306)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        #initialize the output display
        self.display_label = QLabel("0")
        self.display_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display_label.setMaximumHeight(64)
        self.display_label.setStyleSheet("""
        background-color: black;
        color: white;
        font-family: Titillium;
        font-size: 24px;
        """)
        self.display_label.setMargin(10)
        layout.addWidget(self.display_label)

        #initialize the buttons grid
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignCenter)
        grid.setSpacing(6)
        layout.addLayout(grid)

        buttons = [
        [CalcButton("7"), CalcButton("8"), CalcButton("9"), CalcButton("/")],
        [CalcButton("4"), CalcButton("5"), CalcButton("6"), CalcButton("*")],
        [CalcButton("1"), CalcButton("2"), CalcButton("3"), CalcButton("-")],
        [CalcButton("0"), CalcButton("C"), CalcButton("="), CalcButton("+")],
        [CalcButton(".")]
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, btn in enumerate(row):
                button = QPushButton(btn.val)
                button.setFixedSize(60, 48)
                button.clicked.connect(lambda checked=False, b=btn: self.on_button_click(b))
                grid.addWidget(button, row_idx, col_idx)

    def set_display(self, value: str):
        """Updates the display"""
        self.display_label.setText(value)

    def on_button_click(self, button: CalcButton):
        """Handler for when any button is pressed"""

        if button.type == ButtonType.DIGIT:
            self.handle_digit(button.val)
        elif button.type == ButtonType.OPERATION:
            self.handle_operation(button.val)
        elif button.type == ButtonType.EQUALS:
            self.handle_calculation()
        elif button.type == ButtonType.CLEAR:
            self.handle_clear()
        elif button.type == ButtonType.DECIMAL:
            self.handle_decimal()

    def handle_digit(self, num):
        """Handler for when a digit is pressed"""

        #if there was just a calculation, reset the number
        if self.start_new_num:
            if self.current_number == "0" and num == "0":
                return
            self.current_number = num
            self.start_new_num = False
        else:
            self.current_number += num
        
        self.set_display(self.current_number)

    def handle_decimal(self):
        """Handler for when the decimal is pressed"""

        if self.has_decimal:
            return
        
        self.has_decimal = True
        self.start_new_num = False
        self.current_number += "."
        self.set_display(self.current_number)


    def handle_operation(self, operation):
        """Handler for when an operation is selected"""

        if self.current_number == "" or self.current_number == "0":
            return

        #add the current number and operation to the expression list
        num = self.trim_whole_number(self.current_number)
        self.current_expression.append(num)
        self.current_expression.append(operation)

        #reset the displayed number
        self.current_number = ""
        self.set_display(operation)


    def handle_calculation(self):
        """Performs the calculation on the list of inputs"""

        num = self.trim_whole_number(self.current_number)
        self.current_expression.append(num)

        #first pass - multiplication and division
        i = 1
        while i < len(self.current_expression):
            
            if self.current_expression[i] == "*" or self.current_expression[i] == "/":

                if self.current_expression[i] == "*":
                    result = self.current_expression[i - 1] * self.current_expression[i + 1]

                elif self.current_expression[i] == "/":

                    
                    if self.current_expression[i + 1] == 0:
                        self.handle_clear(error=True)
                        return

                    result = self.current_expression[i - 1] / self.current_expression[i + 1]

                self.current_expression[i - 1] = result
                self.current_expression.pop(i)
                self.current_expression.pop(i)

                continue

            i += 1

        #second pass - add and subtract
        total = self.current_expression[0]
        i = 1
        while i < len(self.current_expression):

            operation = self.current_expression[i]
            next_num = self.current_expression[i + 1]

            if operation == "+":
                total += next_num
            elif operation == "-":
                total -= next_num

            i += 2

        if float(total) % 1 != 0:
            self.has_decimal = True

        display_str = str(self.trim_whole_number(str(total)))
        self.set_display(display_str)
        self.current_expression = []
        self.current_number = display_str
        self.start_new_num = True

    def trim_whole_number(self, num: str):
        """Gets rid of trailing zero decimal"""
        
        if float(num) % 1 == 0:

            if num[-2:] == ".0":
                return int(num[:-2])
            return int(num)
        
        else:
            return float(num)
        

    def handle_clear(self, error=False):
        """Clears the calculator"""

        if error:
            self.set_display("Error")
        else:
            self.set_display("0")
        
        self.start_new_num = True
        self.has_decimal = False
        self.current_number = "0"
        self.current_expression = []
    


if __name__ == "__main__":
    app = QApplication([])

    window = CalculatorApp()
    window.show()

    sys.exit(app.exec())