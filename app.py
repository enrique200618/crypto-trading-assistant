import streamlit as st
import pandas as pd
import yfinance as yf
import ta
from datetime import datetime, timedelta

# Función para obtener los datos de la criptomoneda
@st.cache_data
def get_crypto_data(ticker):
    end = datetime.today()
    start = end - timedelta(days=180)
    data = yf.download(ticker, start=start, end=end)
    # Aseguramos que el índice esté limpio y sin multi-índices
    data.columns = [col if isinstance(col, str) else col[1] for col in data.columns.values]
    return data

# Añadir indicadores técnicos
def add_technical_indicators(data):
    close_series = data['Close'].squeeze()

    if close_series.ndim != 1:
        raise ValueError("La columna 'Close' debe ser un Series de una sola dimensión")

    data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    data['EMA20'] = ta.trend.EMAIndicator(close_series, window=20).ema_indicator()
    data['MACD'] = ta.trend.MACD(close_series).macd()
    return data

# Lógica de trading simple
def trading_signal(data):
    latest = data.iloc[-1]
    if latest['RSI'] < 30 and latest['Close'] > latest['EMA20']:
        return "COMPRAR"
    elif latest['RSI'] > 70 and latest['Close'] < latest['EMA20']:
        return "VENDER"
    else:
        return "MANTENER"

# Configuración de la app
st.set_page_config(page_title="Asistente de Trading Cripto", layout="centered")
st.title("📊 Asistente de Trading Cripto (Corto Plazo)")

# Lista de criptomonedas
cryptos = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Cardano (ADA)": "ADA-USD",
    "Ripple (XRP)": "XRP-USD"
}

seleccion = st.selectbox("Selecciona una criptomoneda", list(cryptos.keys()))
ticker = cryptos[seleccion]

# Obtener datos y mostrar resultados
data = get_crypto_data(ticker)
data = add_technical_indicators(data)
signal = trading_signal(data)

# Mostrar señal
st.subheader(f"📌 Señal para {seleccion}")
if signal == "COMPRAR":
    st.success("📈 Señal actual: COMPRAR")
elif signal == "VENDER":
    st.error("📉 Señal actual: VENDER")
else:
    st.info("⏳ Señal actual: MANTENER")

# Mostrar gráficos
st.subheader("📉 Gráfico de precios y EMA20")
st.line_chart(data[['Close', 'EMA20']])

st.subheader("📊 RSI y MACD")
st.line_chart(data[['RSI', 'MACD']])

