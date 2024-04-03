import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create a DataFrame to store expenses
expenses_df = pd.DataFrame(columns=['Date', 'Amount', 'Category'])
opening_balance = 0

# Function to display the expense form and add expenses to the DataFrame
def add_expense():
    date = st.date_input("Date", pd.Timestamp.today())
    amount = st.number_input("Amount")
    category = st.selectbox("Category", ["Food", "Transportation", "Utilities", "Entertainment", "Other"])
    
    if st.button("Add Expense"):
        global opening_balance
        expenses_df.loc[len(expenses_df)] = [date, amount, category]
        opening_balance -= amount

# Function to display expenses summary
def show_summary():
    st.subheader("Expenses Summary")
    st.write(expenses_df)
    
    # Grouping expenses by category
    grouped_expenses = expenses_df.groupby('Category').sum()
    
    # Plotting expenses by category
    plt.figure(figsize=(10, 6))
    sns.barplot(x=grouped_expenses.index, y='Amount', data=grouped_expenses)
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.title('Total Expenses by Category')
    st.pyplot()

# Function to add opening balance
def add_opening_balance():
    global opening_balance
    opening_balance = st.number_input("Opening Balance", value=opening_balance)

# Function to calculate and display remaining balance
def show_remaining_balance():
    global opening_balance
    remaining_balance = opening_balance - expenses_df['Amount'].sum()
    st.subheader("Remaining Balance")
    st.write(f"${remaining_balance}")

# Main function to run the app
def main():
    st.title("Personal Expense Tracker")
    
    add_opening_balance()
    menu = ["Add Expense", "Expenses Summary", "Remaining Balance"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add Expense":
        add_expense()
    elif choice == "Expenses Summary":
        show_summary()
    elif choice == "Remaining Balance":
        show_remaining_balance()

if __name__ == "__main__":
    main()
