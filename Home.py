import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime
from statementParser import BankStatement

# Initialize session state if not already initialized
if 'categorized_df' not in st.session_state:
    st.session_state['categorized_df'] = None
if 'fixed_exp' not in st.session_state:
    st.session_state['fixed_exp'] = set()
if 'variable_exp' not in st.session_state:
    st.session_state['variable_exp'] = set()

# Define your page configurations
st.set_page_config(
    page_title="Expense Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Expense Tracker")

# Date input for start and end dates
start_date = st.date_input('Start Date', datetime.now().date().replace(month=1, day=1))
end_date = st.date_input('End Date')

# Store start and end dates in session state
st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date

# Select bank option
bank_option = st.selectbox("Select Bank", ("Kotak Bank",))

# Button to proceed to the next step
if st.button('Next'):
    st.session_state['selected_bank'] = bank_option
    switch_page("Create_Categories")

# Display selected bank if available in session state
if 'selected_bank' in st.session_state:
    selected_bank = st.session_state['selected_bank']
    st.write(f"Selected Bank: {selected_bank}")

# Add file upload option
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Parse statement and display expenses and amounts
if uploaded_file is not None:
    statement_parser = BankStatement(uploaded_file)
    df = statement_parser.parse_statement_as_df()

    st.write("Expenses:")
    st.write(df['Description'])

    st.write("Amounts:")
    st.write(df['Debit'])

    # # Button to navigate to the visualization page
    # if st.button("Visualize"):
    #     switch_page("Visualize")

    # Store parsed data in session state
    st.session_state['categorized_df'] = df

# Done button to finish categorizing expenses
if st.button("Done"):
    # Validate fixed and variable expenses
    fixed_exp = st.session_state['fixed_exp']
    variable_exp = st.session_state['variable_exp']

    if not fixed_exp and not variable_exp:
        st.error("Both Fixed and Variable expenses are empty. Please categorize your expenses properly.")
    elif fixed_exp & variable_exp:
        st.error("Fixed and Variable expenses cannot have common values between them. Please review your categorization.")
    else:
        switch_page("Home")

# Dropdown menu for selecting categories
categories = ["Groceries", "Utilities", "Transportation", "Entertainment", "Healthcare", "Education", "Other"]
selected_category = st.selectbox("Select a category", categories)

# Add button to assign selected category to expenses
if st.button("Assign Category"):
    # Assign selected category to expenses
    selected_expenses = st.multiselect("Select expenses to assign category", df['Description'].unique())
    if selected_category:
        if selected_category == "Fixed":
            st.session_state['fixed_exp'].update(selected_expenses)
        elif selected_category == "Variable":
            st.session_state['variable_exp'].update(selected_expenses)
        st.success("Category assigned successfully!")
