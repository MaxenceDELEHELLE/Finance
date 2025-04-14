### Pour lancer ce programme, taper streamlit run dashboard_streamlit.py et
### copier coller l'adresse dans un navigateur web


import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Marché Financier", layout="wide")

st.title("Dashboard Marché Financier")

tickers = st.multiselect("Sélectionnez les actions :", ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"], default=["AAPL", "MSFT"])
start = st.date_input("Date de début", pd.to_datetime("2022-01-01"))
end = st.date_input("Date de fin", pd.to_datetime("today"))

if tickers:
    data = yf.download(tickers, start=start, end=end)["Close"]

    st.subheader("Prix des actions")
    fig = go.Figure()
    for ticker in tickers:
        fig.add_trace(go.Scatter(x=data.index, y=data[ticker], name=ticker))
    fig.update_layout(height=400, legend_title="Tickers")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Statistiques")
    returns = data.pct_change().dropna()
    stats = pd.DataFrame({
        "Rendement Annuel (%)": returns.mean() * 252 * 100,
        "Volatilité (%)": returns.std() * np.sqrt(252) * 100,
        "Max Drawdown (%)": ((data / data.cummax() - 1).min()) * 100
    })
    st.dataframe(stats.style.format("{:.2f}"))

    st.subheader("Corrélation")
    corr = returns.corr()
    st.dataframe(corr.style.background_gradient(cmap='coolwarm'))

    st.subheader("Indicateurs techniques (SMA)")
    selected_ticker = st.selectbox("Choisissez une action :", tickers)
    sma_window = st.slider("Fenêtre SMA (jours)", 5, 100, 20)
    sma = data[selected_ticker].rolling(window=sma_window).mean()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data.index, y=data[selected_ticker], name=selected_ticker))
    fig2.add_trace(go.Scatter(x=data.index, y=sma, name=f"SMA {sma_window}"))
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
