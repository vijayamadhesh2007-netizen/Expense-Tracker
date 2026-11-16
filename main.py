
import customtkinter as ctk
from tkinter import messagebox
from datetime import date

# Appearance settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Main window
app = ctk.CTk()
app.title("My Expense Tracker")
app.geometry("1000x680")
app.resizable(False, False)
app.configure(fg_color="#F1F5F9")

# Colours
NAVY = "#142D4E"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
GREEN = "#16A34A"
RED = "#DC2626"
GREY = "#64748B"

# Application data
transactions = []
page = None

# Clear previous screen
def clear_page():
    global page

    if page is not None:
        page.destroy()

    page = ctk.CTkFrame(app, fg_color="#F1F5F9")
    page.pack(fill="both", expand=True)

# Welcome screen
def show_welcome():
    clear_page()

    card = ctk.CTkFrame(
        page,
        width=650,
        height=420,
        corner_radius=25,
        fg_color=NAVY
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        card,
        text="MY EXPENSE TRACKER",
        font=("Arial", 34, "bold"),
        text_color=WHITE
    ).pack(pady=(75, 20))

    ctk.CTkLabel(
        card,
        text="Manage your money. Track your future.",
        font=("Arial", 18),
        text_color="#CBD5E1"
    ).pack(pady=10)

    ctk.CTkButton(
        card,
        text="GET STARTED",
        width=200,
        height=48,
        corner_radius=12,
        fg_color=BLUE,
        command=show_login
    ).pack(pady=45)


# Login screen
def show_login():
    clear_page()

    card = ctk.CTkFrame(
        page,
        width=450,
        height=430,
        corner_radius=20,
        fg_color=WHITE
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        card,
        text="Welcome Back!",
        font=("Arial", 30, "bold"),
        text_color=NAVY
    ).pack(pady=(45, 10))

    ctk.CTkLabel(
        card,
        text="Login to manage your expenses",
        text_color=GREY,
        font=("Arial", 15)
    ).pack(pady=5)

    username = ctk.CTkEntry(
        card,
        width=300,
        height=42,
        placeholder_text="Username"
    )
    username.pack(pady=15)

    password = ctk.CTkEntry(
        card,
        width=300,
        height=42,
        placeholder_text="Password",
        show="*"
    )
    password.pack(pady=10)

    def login():
        if not username.get().strip() or not password.get():
            messagebox.showwarning(
                "Login",
                "Please enter username and password."
            )
        else:
            show_dashboard()

    ctk.CTkButton(
        card,
        text="LOGIN",
        width=200,
        height=45,
        fg_color=BLUE,
        command=login
    ).pack(pady=25)


# Calculate income, expenses and balance
def calculate_totals():
    total_income = sum(
        t["amount"] for t in transactions
        if t["type"] == "Income"
    )

    total_expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "Expense"
    )

    balance = total_income - total_expenses

    return total_income, total_expenses, balance


# Dashboard screen
def show_dashboard():
    clear_page()

    # Heading
    ctk.CTkLabel(
        page,
        text="MY DASHBOARD",
        font=("Arial", 30, "bold"),
        text_color=NAVY
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        page,
        text="Overview of your money",
        font=("Arial", 15),
        text_color=GREY
    ).pack(pady=(0, 20))

    # Calculate totals
    income, expenses, balance = calculate_totals()

    # Summary cards container
    cards = ctk.CTkFrame(
        page,
        fg_color="transparent"
    )
    cards.pack(fill="x", padx=35, pady=10)

    # Balance card
    balance_card = ctk.CTkFrame(
        cards,
        fg_color=NAVY,
        corner_radius=15,
        height=130
    )
    balance_card.pack(fill="x", pady=8)
    balance_card.pack_propagate(False)

    ctk.CTkLabel(
        balance_card,
        text="TOTAL BALANCE",
        font=("Arial", 16, "bold"),
        text_color=WHITE
    ).pack(pady=(18, 5))

    ctk.CTkLabel(
        balance_card,
        text=f"₹ {balance:.2f}",
        font=("Arial", 28, "bold"),
        text_color=WHITE
    ).pack()

    # Income and expense cards
    small_cards = ctk.CTkFrame(
        cards,
        fg_color="transparent"
    )
    small_cards.pack(fill="x", pady=8)

    income_card = ctk.CTkFrame(
        small_cards,
        fg_color=WHITE,
        corner_radius=15,
        height=110
    )
    income_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 8)
    )
    income_card.pack_propagate(False)

    ctk.CTkLabel(
        income_card,
        text="TOTAL INCOME",
        font=("Arial", 14, "bold"),
        text_color=GREEN
    ).pack(pady=(18, 5))

    ctk.CTkLabel(
        income_card,
        text=f"₹ {income:.2f}",
        font=("Arial", 22, "bold"),
        text_color=NAVY
    ).pack()

    expense_card = ctk.CTkFrame(
        small_cards,
        fg_color=WHITE,
        corner_radius=15,
        height=110
    )
    expense_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(8, 0)
    )
    expense_card.pack_propagate(False)

    ctk.CTkLabel(
        expense_card,
        text="TOTAL EXPENSES",
        font=("Arial", 14, "bold"),
        text_color=RED
    ).pack(pady=(18, 5))

    ctk.CTkLabel(
        expense_card,
        text=f"₹ {expenses:.2f}",
        font=("Arial", 22, "bold"),
        text_color=NAVY
    ).pack()

    # Action buttons
    buttons = ctk.CTkFrame(
        page,
        fg_color="transparent"
    )
    buttons.pack(pady=20)

    ctk.CTkButton(
        buttons,
        text="+ ADD INCOME",
        width=180,
        height=42,
        fg_color=GREEN,
        command=lambda: add_transaction("Income")
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        buttons,
        text="+ ADD EXPENSE",
        width=180,
        height=42,
        fg_color=RED,
        command=lambda: add_transaction("Expense")
    ).pack(side="left", padx=10)

    # Transaction history heading
    ctk.CTkLabel(
        page,
        text="RECENT TRANSACTIONS",
        font=("Arial", 20, "bold"),
        text_color=NAVY
    ).pack(pady=(10, 5))

    # Transaction history area
    history = ctk.CTkScrollableFrame(
        page,
        width=850,
        height=130,
        fg_color=WHITE,
        corner_radius=12
    )
    history.pack(padx=35, pady=(5, 15), fill="x")

    if not transactions:
        ctk.CTkLabel(
            history,
            text="No transactions yet. Add your first income or expense!",
            text_color=GREY,
            font=("Arial", 14)
        ).pack(pady=20)

    else:
        for item in reversed(transactions):
            transaction_row = ctk.CTkFrame(
                history,
                fg_color="#F1F5F9",
                corner_radius=8
            )
            transaction_row.pack(
                fill="x",
                padx=8,
                pady=5
            )

            amount_color = (
                GREEN if item["type"] == "Income" else RED
            )

            ctk.CTkLabel(
                transaction_row,
                text=f'{item["date"]}  |  {item["category"]}  |  {item["type"]}',
                text_color=NAVY,
                font=("Arial", 13)
            ).pack(side="left", padx=12, pady=10)

            ctk.CTkLabel(
                transaction_row,
                text=f'₹ {item["amount"]:.2f}',
                text_color=amount_color,
                font=("Arial", 13, "bold")
            ).pack(side="right", padx=12, pady=10)


# Add income or expense
def add_transaction(transaction_type):

    window = ctk.CTkToplevel(app)
    window.title("Add " + transaction_type)
    window.geometry("400x430")
    window.resizable(False, False)
    window.configure(fg_color=WHITE)

    window.transient(app)
    window.grab_set()

    ctk.CTkLabel(
        window,
        text="Add " + transaction_type,
        font=("Arial", 25, "bold"),
        text_color=NAVY
    ).pack(pady=25)

    amount_entry = ctk.CTkEntry(
        window,
        width=280,
        height=42,
        placeholder_text="Enter Amount (₹)"
    )
    amount_entry.pack(pady=15)

    category = ctk.CTkOptionMenu(
        window,
        width=280,
        height=42,
        values=[
            "Food",
            "Travel",
            "Shopping",
            "Salary",
            "Bills",
            "Education",
            "Other"
        ]
    )
    category.pack(pady=15)

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

    ctk.CTkButton(
        window,
        text="SAVE TRANSACTION",
        width=220,
        height=45,
        fg_color=BLUE,
        command=save_transaction
    ).pack(pady=30)


# Start the application
show_welcome()
app.mainloop()
