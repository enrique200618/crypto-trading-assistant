import streamlit as st
import pandas as pd
import yfinance as yf
import ta
from datetime import datetime, timedelta

# Función para descargar datos de criptomonedas
@st.cache_data
def get_crypto_data(ticker):
    end = datetime.today()
    start = end - timedelta(days=180)
    data = yf.download(ticker, start=start, end=end)
    return data

# Añadir indicadores técnicos
def add_technical_indicators(data):
    # Asegurar que 'Close' sea un Series 1D
    if isinstance(data['Close'], pd.DataFrame):
        close_series = data['Close'].squeeze()
    else:
        close_series = data['Close']
    
    if close_series.ndim != 1:
        raise ValueError("La columna 'Close' debe ser un Series de una sola dimensión")

    rsi = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    ema = ta.trend.EMAIndicator(close_series, window=20).ema_indicator()
    macd = ta.trend.MACD(close_series).macd()

    data['RSI'] = rsi
    data['EMA20'] = ema
    data['MACD'] = macd
    return data

# Estrategia de trading simple
def trading_signal(data):
    if data['RSI'].iloc[-1] < 30 and data['Close'].iloc[-1] > data['EMA20'].iloc[-1]:
        return "COMPRAR"
    elif data['RSI'].iloc[-1] > 70 and data['Close'].iloc[-1] < data['EMA20'].iloc[-1]:
        return "VENDER"
    else:
        return "MANTENER"

# Streamlit UI
st.set_page_config(page_title="Crypto Trading Assistant", layout="centered")
st.title("🤖 Asistente de Trading Cripto (Corto Plazo)")

st.markdown("Este asistente analiza criptomonedas y recomienda **comprar**, **mantener** o **vender** según indicadores técnicos.")

# Criptomonedas populares para mostrar
cryptos = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Cardano (ADA)": "ADA-USD",
    "Ripple (XRP)": "XRP-USD"
}

selected = st.selectbox("Selecciona una criptomoneda", list(cryptos.keys()))

# Obtener datos
ticker = cryptos[selected]
data = get_crypto_data(ticker)
data = add_technical_indicators(data)
signal = trading_signal(data)

# Mostrar datos y señal
st.subheader(f"Señal para {selected}:")
if signal == "COMPRAR":
    st.success("📈 Señal: COMPRAR")
elif signal == "VENDER":
    st.error("📉 Señal: VENDER")
else:
    st.info("⏳ Señal: MANTENER")

st.line_chart(data[['Close', 'EMA20']])
st.line_chart(data[['RSI', 'MACD']])
