import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the dataset
@st.cache
def load_data():
    try:
        df = pd.read_csv('shopping_behavior_updated.csv')
        return df
    except FileNotFoundError:
        st.error("Could not find the data file. Please make sure 'shopping_behavior_updated.csv' is in the same directory as this script.")

# Main function to run the app
def main():
    df = load_data()

    # Sidebar - Dashboard options
    st.sidebar.title('Dashboard Options')
    dashboard_selectbox = st.sidebar.selectbox(
        'Select Dashboard View:',
        ('Key Metrics', 'Product Preferences', 'Sales Trend', 'Customer Analysis')
    )

    # Main content
    st.title('Retail Consumer Behavior Analysis')

    # Dashboard view
    if dashboard_selectbox == 'Key Metrics':
        key_metrics_dashboard(df)

    # Product preferences view
    elif dashboard_selectbox == 'Product Preferences':
        product_preferences_dashboard(df)

    # Sales trend view
    elif dashboard_selectbox == 'Sales Trend':
        sales_trend_dashboard()

    # Customer analysis view
    elif dashboard_selectbox == 'Customer Analysis':
        customer_analysis_dashboard(df)

# Dashboard view functions
def key_metrics_dashboard(df):
    st.header('Key Metrics')
    total_sales = df['Purchase Amount (USD)'].sum()
    avg_purchase_amount = df['Purchase Amount (USD)'].mean()
    st.subheader('Total Sales: ${:.2f}'.format(total_sales))
    st.subheader('Average Purchase Amount: ${:.2f}'.format(avg_purchase_amount))

    # Interactive 3D graph for customer demographics
    fig = px.scatter_3d(df, x='Age', y='Gender', z='Purchase Amount (USD)',
                         color='Gender', symbol='Gender', color_discrete_map={'Male': 'yellow', 'Female': 'blue'})
    st.plotly_chart(fig)

def product_preferences_dashboard(df):
    st.header('Product Preferences')

    # Bar chart for distribution of purchases by product category
    category_counts = df['Category'].value_counts()
    fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values,
                 labels={'x': 'Category', 'y': 'Count'}, title='Purchases by Product Category',
                 color_discrete_map={'Category': 'yellow'})
    st.plotly_chart(fig)

def sales_trend_dashboard():
    st.header('Sales Trend')

    # Generate sample sales data
    months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    sales_data = np.random.randint(1000, 5000, size=len(months))
    sales_over_time = pd.DataFrame({'Date': months, 'Total Sales': sales_data})

    # Line chart for trend in sales over time
    fig = px.line(sales_over_time, x='Date', y='Total Sales',
                  labels={'x': 'Date', 'y': 'Total Sales'}, title='Sales Trend Over Time')
    st.plotly_chart(fig)

def customer_analysis_dashboard(df):
    st.header('Customer Analysis')

    # Scatter plot for relationship between customer age and average purchase amount
    fig = px.scatter(df, x='Age', y='Purchase Amount (USD)', color='Gender',
                     labels={'x': 'Age', 'y': 'Purchase Amount (USD)'}, title='Age vs. Purchase Amount',
                     color_discrete_map={'Male': 'yellow', 'Female': 'blue'})
    st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
