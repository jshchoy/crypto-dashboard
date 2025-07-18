import streamlit as st
import requests
import matplotlib.pyplot as plt

# Your portfolio - coin name and quantity
portfolio = {
    'bitcoin': 0.5,
    'ethereum': 2,
    'solana': 10
}

# Fetch current prices from CoinGecko
@st.cache_data
def fetch_prices():
    ids = ','.join(portfolio.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price"
    response = requests.get(url, params={'ids': ids, 'vs_currencies': 'usd'})
    return response.json()

# Calculate portfolio value
def calculate_value(prices):
    total = 0
    values = {}
    for coin, amount in portfolio.items():
        price = prices[coin]['usd']
        value = price * amount
        values[coin] = value
        total += value
    return total, values

# Streamlit UI
st.title("💰 Crypto Investment Dashboard")

prices = fetch_prices()
total, values = calculate_value(prices)

st.header("📦 Portfolio Overview")
st.write(f"**Total Portfolio Value:** ${total:,.2f}")

# Table of holdings
st.subheader("Holdings:")
for coin, value in values.items():
    st.write(f"{coin.capitalize()}: ${value:,.2f} (at ${prices[coin]['usd']:,}/coin)")

# Pie chart
st.subheader("📊 Portfolio Distribution")
fig, ax = plt.subplots()
ax.pie(values.values(), labels=values.keys(), autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)
