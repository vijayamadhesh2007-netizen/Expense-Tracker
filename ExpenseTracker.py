
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# Colours
NAVY = "#142D4E"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
GREEN = "#16A34A"
RED = "#DC2626"
GREY = "#64748B"
BG = "#F1F5F9"

# Application data
transactions = []

# Main window
app = tk.Tk()
app.title("My Expense Tracker")
app.geometry("1000x680")
app.resizable(False, False)
app.configure(bg=BG)

# Configure styles
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    padding=8,
    font=("Arial", 12)
)


# Clear previous screen
def clear_page():
    for widget in app.winfo_children():
        widget.destroy()


# Create label
def make_label(parent, text, size=14, color=NAVY, bold=False):
    return tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold" if bold else "normal"),
        fg=color,
        bg=parent.cget("bg")
    )


# Create button
def make_button(parent, text, command, color=BLUE, width=20):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        width=width,
        height=2
    )


# Welcome screen
def show_welcome():
    clear_page()

    card = tk.Frame(
        app,
        bg=NAVY,
        width=650,
        height=420
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(
        card,
        text="MY EXPENSE TRACKER",
        font=("Arial", 34, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(pady=(85, 20))

    tk.Label(
        card,
        text="Manage your money. Track your future.",
        font=("Arial", 18),
        fg="#CBD5E1",
        bg=NAVY
    ).pack(pady=10)

    make_button(
        card,
        "GET STARTED",
        show_login
    ).pack(pady=45)


# Login screen
def show_login():
    clear_page()

    card = tk.Frame(
        app,
        bg=WHITE,
        width=450,
        height=430
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(
        card,
        text="Welcome Back!",
        font=("Arial", 30, "bold"),
        fg=NAVY,
        bg=WHITE
    ).pack(pady=(45, 10))

    tk.Label(
        card,
        text="Login to manage your expenses",
        font=("Arial", 15),
        fg=GREY,
        bg=WHITE
    ).pack(pady=5)

    username = tk.Entry(
        card,
        width=30,
        font=("Arial", 13),
        relief="solid",
        bd=1
    )
    username.pack(ipady=10, pady=15)

    password = tk.Entry(
        card,
        width=30,
        font=("Arial", 13),
        relief="solid",
        bd=1,
        show="*"
    )
    password.pack(ipady=10, pady=10)

    def login():
        if not username.get().strip() or not password.get():
            messagebox.showwarning(
                "Login",
                "Please enter username and password."
            )
        else:
            show_dashboard()

    make_button(card, "LOGIN", login).pack(pady=25)


# Calculate totals
def calculate_totals():
    income = sum(
        t["amount"] for t in transactions
        if t["type"] == "Income"
    )

    expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "Expense"
    )

    balance = income - expenses

    return income, expenses, balance


# Add income or expense
def add_transaction(transaction_type):

    window = tk.Toplevel(app)
    window.title("Add " + transaction_type)
    window.geometry("400x430")
    window.resizable(False, False)
    window.configure(bg=WHITE)
    window.transient(app)
    window.grab_set()

    tk.Label(
        window,
        text="Add " + transaction_type,
        font=("Arial", 25, "bold"),
        fg=NAVY,
        bg=WHITE
    ).pack(pady=25)

    amount_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 13),
        relief="solid",
        bd=1
    )
    amount_entry.pack(ipady=10, pady=15)

    amount_entry.insert(0, "")

    tk.Label(
        window,
        text="Select Category",
        font=("Arial", 12),
        fg=NAVY,
        bg=WHITE
    ).pack(pady=5)

    category = ttk.Combobox(
        window,
        values=[
            "Food",
            "Travel",
            "Shopping",
            "Salary",
            "Bills",
            "Education",
            "Other"
        ],
        width=27,
        font=("Arial", 12),
        state="readonly"
    )
    category.pack(ipady=5, pady=10)
    category.set("Food")

    def save_transaction():

        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount greater than zero."
            )
            return

        transactions.append({
            "type": transaction_type,
            "amount": amount,
            "category": category.get(),
            "date": date.today().strftime("%d %b %Y")
        })

        window.destroy()
        show_dashboard()

    make_button(
        window,
        "SAVE TRANSACTION",
        save_transaction
    ).pack(pady=30)


# Dashboard screen
def show_dashboard():
    clear_page()

    tk.Label(
        app,
        text="MY DASHBOARD",
        font=("Arial", 30, "bold"),
        fg=NAVY,
        bg=BG
    ).pack(pady=(20, 5))

    tk.Label(
        app,
        text="Overview of your money",
        font=("Arial", 15),
        fg=GREY,
        bg=BG
    ).pack(pady=(0, 15))

    income, expenses, balance = calculate_totals()

    # Balance card
    balance_card = tk.Frame(
        app,
        bg=NAVY,
        height=115
    )
    balance_card.pack(fill="x", padx=35, pady=8)
    balance_card.pack_propagate(False)

    tk.Label(
        balance_card,
        text="TOTAL BALANCE",
        font=("Arial", 16, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(pady=(15, 5))

    tk.Label(
        balance_card,
        text=f"₹ {balance:.2f}",
        font=("Arial", 28, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack()

    # Income and expense cards
    small_cards = tk.Frame(app, bg=BG)
    small_cards.pack(fill="x", padx=35, pady=8)

    income_card = tk.Frame(
        small_cards,
        bg=WHITE,
        height=100
    )
    income_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 8)
    )
    income_card.pack_propagate(False)

    tk.Label(
        income_card,
        text="TOTAL INCOME",
        font=("Arial", 14, "bold"),
        fg=GREEN,
        bg=WHITE
    ).pack(pady=(15, 5))

    tk.Label(
        income_card,
        text=f"₹ {income:.2f}",
        font=("Arial", 22, "bold"),
        fg=NAVY,
        bg=WHITE
    ).pack()

    expense_card = tk.Frame(
        small_cards,
        bg=WHITE,
        height=100
    )
    expense_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(8, 0)
    )
    expense_card.pack_propagate(False)

    tk.Label(
        expense_card,
        text="TOTAL EXPENSES",
        font=("Arial", 14, "bold"),
        fg=RED,
        bg=WHITE
    ).pack(pady=(15, 5))

    tk.Label(
        expense_card,
        text=f"₹ {expenses:.2f}",
        font=("Arial", 22, "bold"),
        fg=NAVY,
        bg=WHITE
    ).pack()

    # Action buttons
    buttons = tk.Frame(app, bg=BG)
    buttons.pack(pady=15)

    make_button(
        buttons,
        "+ ADD INCOME",
        lambda: add_transaction("Income"),
        GREEN,
        20
    ).pack(side="left", padx=10)

    make_button(
        buttons,
        "+ ADD EXPENSE",
        lambda: add_transaction("Expense"),
        RED,
        20
    ).pack(side="left", padx=10)

    # Recent transactions
    tk.Label(
        app,
        text="RECENT TRANSACTIONS",
        font=("Arial", 20, "bold"),
        fg=NAVY,
        bg=BG
    ).pack(pady=(5, 5))

    history = tk.Frame(
        app,
        bg=WHITE
    )
    history.pack(
        padx=35,
        pady=5,
        fill="both",
        expand=True
    )

    if not transactions:
        tk.Label(
            history,
            text="No transactions yet. Add your first income or expense!",
            font=("Arial", 13),
            fg=GREY,
            bg=WHITE
        ).pack(pady=20)

    else:
        for item in reversed(transactions[-4:]):

            row = tk.Frame(
                history,
                bg=BG
            )
            row.pack(fill="x", padx=8, pady=4)

            amount_color = (
                GREEN if item["type"] == "Income" else RED
            )

            tk.Label(
                row,
                text=(
                    f'{item["date"]} | '
                    f'{item["category"]} | '
                    f'{item["type"]}'
                ),
                font=("Arial", 12),
                fg=NAVY,
                bg=BG
            ).pack(side="left", padx=12, pady=8)

            tk.Label(
                row,
                text=f'₹ {item["amount"]:.2f}',
                font=("Arial", 12, "bold"),
                fg=amount_color,
                bg=BG
            ).pack(side="right", padx=12, pady=8)


# Start application
show_welcome()

app.mainloop()
