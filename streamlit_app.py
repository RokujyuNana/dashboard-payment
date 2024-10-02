from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Payment Type Analysis",
    page_icon=":bar_chart:",  # This is an emoji shortcode. Could be a URL too.
)

# ----------------------------------------------------------------------------- 
# Load your dataset. Here, we're using CSV instead of SQLite for simplicity.
@st.cache_data
def load_data():
    file_path = 'https://github.com/RokujyuNana/dashboard-payment/blob/main/order_payments_dataset.csv'
    data = pd.read_csv(file_path)
    return data

data = load_data()

# ----------------------------------------------------------------------------- 
# Business Question 1: Which payment type contributes the most to total revenue?

st.title("Exploratory Data Analysis (EDA) on Payment Data")

st.subheader("Business Question 1: Which payment type contributes the most to total revenue?")

# Grouping by payment type and calculating total revenue
payment_revenue = data.groupby('payment_type')['payment_value'].sum().reset_index()
payment_revenue = payment_revenue.sort_values(by='payment_value', ascending=False)

# Display results
st.dataframe(payment_revenue)

# Visualization using Altair
chart1 = alt.Chart(payment_revenue).mark_bar().encode(
    x=alt.X('payment_value:Q', title='Total Revenue'),
    y=alt.Y('payment_type:N', sort='-x', title='Payment Type')
).properties(
    title="Total Revenue by Payment Type"
)

st.altair_chart(chart1, use_container_width=True)

# ----------------------------------------------------------------------------- 
# Business Question 2: What is the relationship between payment installments and order value?

st.subheader("Business Question 2: What is the relationship between payment installments and order value?")

# Grouping by payment installments and calculating average order value
installments_order_value = data.groupby('payment_installments')['payment_value'].mean().reset_index()

# Display results
st.dataframe(installments_order_value)

# Visualization using Seaborn and Matplotlib
fig, ax = plt.subplots()
sns.lineplot(x='payment_installments', y='payment_value', data=installments_order_value, marker='o', ax=ax)
ax.set_title('Average Order Value by Payment Installments')
ax.set_xlabel('Payment Installments')
ax.set_ylabel('Average Order Value')

# Display the plot in Streamlit
st.pyplot(fig)

# ----------------------------------------------------------------------------- 
# Conclusion
st.subheader("Conclusions")

st.write("""
1. **Total Revenue by Payment Type**: Credit cards contribute the highest to total revenue, followed by boleto.
2. **Installments and Order Value**: Higher installments tend to be associated with higher average order values.
""")
