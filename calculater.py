import tkinter as tk
from tkinter import messagebox


class Calculator:

    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x440")
        self.root.resizable(False, False)
        self.root.configure(bg="#222f3e")

        # Current calculation expression
        self.expression = ""

        self.setup_ui()

    def setup_ui(self):
        # Display screen
        self.display_var = tk.StringVar(value="0")

        display_frame = tk.Frame(self.root, bg="#222f3e", padx=12, pady=16)
        display_frame.pack(fill=tk.X)

        self.display_screen = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 26, "bold"),
            bg="#10ac84",
            fg="#ffffff",
            anchor="e",
            padx=12,
            pady=12,
            relief="sunken",
            bd=2,
        )
        self.display_screen.pack(fill=tk.X)

        # Keypad container
        buttons_frame = tk.Frame(self.root, bg="#222f3e", padx=10, pady=5)
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        # Button layout definition: (label, row, col, colspan, bg_color)
        btn_layout = [
            ("C", 0, 0, 3, "#ee5253"),
            ("/", 0, 3, 1, "#ff9f43"),
            ("7", 1, 0, 1, "#576574"),
            ("8", 1, 1, 1, "#576574"),
            ("9", 1, 2, 1, "#576574"),
            ("*", 1, 3, 1, "#ff9f43"),
            ("4", 2, 0, 1, "#576574"),
            ("5", 2, 1, 1, "#576574"),
            ("6", 2, 2, 1, "#576574"),
            ("-", 2, 3, 1, "#ff9f43"),
            ("1", 3, 0, 1, "#576574"),
            ("2", 3, 1, 1, "#576574"),
            ("3", 3, 2, 1, "#576574"),
            ("+", 3, 3, 1, "#ff9f43"),
            ("0", 4, 0, 2, "#576574"),
            (".", 4, 2, 1, "#576574"),
            ("=", 4, 3, 1, "#10ac84"),
        ]

        # Configure equal spacing for grid
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)

        # Create all keypad buttons
        for label, r, c, span, color in btn_layout:
            action = lambda x=label: self.on_button_click(x)
            btn = tk.Button(
                buttons_frame,
                text=label,
                font=("Arial", 14, "bold"),
                bg=color,
                fg="white",
                relief="flat",
                cursor="hand2",
                command=action,
            )
            btn.grid(row=r, column=c, columnspan=span, sticky="nsew", padx=3, pady=3)

    # ---------------- Calculator Logic ----------------
    def on_button_click(self, char):
        if char == "C":
            self.clear()
        elif char == "=":
            self.calculate()
        elif char in ["+", "-", "*", "/"]:
            self.handle_operator(char)
        elif char == ".":
            self.handle_decimal()
        else:
            self.handle_digit(char)

    def handle_digit(self, digit):
        if self.expression == "0" or self.display_var.get() == "Error":
            self.expression = digit
        else:
            self.expression += digit
        self.display_var.set(self.expression)

    def handle_decimal(self):
        if self.display_var.get() == "Error":
            self.expression = "0."
            self.display_var.set(self.expression)
            return

        if not self.expression or self.expression[-1] in "+-*/":
            self.expression += "0."
            self.display_var.set(self.expression)
            return

        # Check if the current active number already contains a dot
        parts = []
        current = ""
        for ch in self.expression:
            if ch in "+-*/":
                parts.append(current)
                current = ""
            else:
                current += ch
        parts.append(current)

        if "." not in parts[-1]:
            self.expression += "."
            self.display_var.set(self.expression)

    def handle_operator(self, op):
        if self.display_var.get() == "Error":
            return

        if not self.expression:
            # Allow starting negative numbers
            if op == "-":
                self.expression = "-"
                self.display_var.set(self.expression)
            return

        # If user clicks another operator back-to-back, update to the latest operator
        if self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op

        self.display_var.set(self.expression)

    def calculate(self):
        if not self.expression or self.display_var.get() == "Error":
            return

        # Do nothing if the expression ends with an incomplete operator
        if self.expression[-1] in "+-*/":
            return

        try:
            # Check for division by zero manually
            if "/0" in self.expression:
                # Handle cases like /0 or /0.0
                tokens = self.expression.replace("+", " ").replace("-", " ").replace("*", " ").split()
                # Check directly in evaluation
                pass

            result = eval(self.expression)

            # Round precision and eliminate trailing zeroes if integer
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 6)

            self.expression = str(result)
            self.display_var.set(self.expression)

        except ZeroDivisionError:
            self.expression = ""
            self.display_var.set("Error")
            messagebox.showerror("Math Error", "Cannot divide by zero!")
        except Exception:
            self.expression = ""
            self.display_var.set("Error")

    def clear(self):
        self.expression = ""
        self.display_var.set("0")


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()