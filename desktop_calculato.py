import tkinter as tk
import ast
import operator

# Window setup
root = tk.Tk()
root.title("Mini Calculator")
root.geometry("340x470")
root.resizable(False, False)
root.configure(bg="#202124")

expression = tk.StringVar(value="")

# Safe arithmetic evaluation
def evaluate(node):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    if isinstance(node, ast.Expression):
        return evaluate(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in operations:
        left = evaluate(node.left)
        right = evaluate(node.right)
        return operations[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        value = evaluate(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value

    raise ValueError("Invalid expression")


def press(value):
    if value == "AC":
        expression.set("")

    elif value == "⌫":
        expression.set(expression.get()[:-1])

    elif value == "=":
        calculate()

    else:
        expression.set(expression.get() + value)


def calculate():
    text = expression.get().strip()

    if not text:
        return

    try:
        tree = ast.parse(text, mode="eval")
        result = evaluate(tree)
        expression.set(str(result))

    except ZeroDivisionError:
        expression.set("Cannot divide by zero")

    except (ValueError, SyntaxError, OverflowError):
        expression.set("Error")


# Display
display = tk.Entry(
    root,
    textvariable=expression,
    font=("Arial", 24),
    justify="right",
    bg="#303134",
    fg="white",
    insertbackground="white",
    bd=0
)
display.pack(fill="x", padx=12, pady=16, ipady=15)

# Calculator buttons
buttons = [
    ["AC", "⌫", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

button_frame = tk.Frame(root, bg="#202124")
button_frame.pack(expand=True, fill="both", padx=8, pady=4)

for r, row in enumerate(buttons):
    for c, value in enumerate(row):
        color = "#3c4043"
        foreground = "white"

        if value in ["+", "-", "*", "/", "="]:
            color = "#8ab4f8"
            foreground = "#202124"

        elif value in ["AC", "⌫"]:
            color = "#5f6368"

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 16, "bold"),
            bg=color,
            fg=foreground,
            activebackground="#bdc1c6",
            activeforeground="#202124",
            relief="flat",
            bd=0,
            command=lambda v=value: press(v)
        )
        button.grid(
            row=r, column=c, sticky="nsew",
            padx=4, pady=4
        )

for r in range(5):
    button_frame.rowconfigure(r, weight=1)

for c in range(4):
    button_frame.columnconfigure(c, weight=1)

# Keyboard shortcuts
def keyboard_press(event):
    if event.keysym in ("Return", "KP_Enter"):
        calculate()
        return "break"

    if event.keysym == "Escape":
        expression.set("")
        return "break"

    if event.keysym == "BackSpace":
        press("⌫")
        return "break"


root.bind("<Return>", keyboard_press)
root.bind("<Escape>", keyboard_press)
root.bind("<BackSpace>", keyboard_press)

root.mainloop()