import streamlit as st
import pandas as pd
import yfinance as yf
import ta
from datetime import datetime, timedelta

# Función para obtener datos cripto con columnas limpias
@st.cache_data
def get_crypto_data(ticker):
    end = datetime.today()
    start = end - timedelta(days=180)
    df = yf.Ticker(ticker).history(start=start, end=end)
    df = df.reset_index()
    df.set_index("Date", inplace=True)
    return df

# Añadir indicadores técnicos
def add_technical_indicators(df):
    if 'Close' not in df.columns:
        raise KeyError("La columna 'Close' no existe en los datos.")
    
    close = df['Close']
    df['RSI'] = ta.momentum.RSIIndicator(close, window=14).rsi()
    df['EMA20'] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
    df['MACD'] = ta.trend.MACD(close).macd()
    return df

# Señal de trading simple
def trading_signal(df):
    latest = df.dropna().iloc[-1]
    if latest['RSI'] < 30 and latest['Close'] > latest['EMA20']:
        return "COMPRAR"
    elif latest['RSI'] > 70 and latest['Close'] < latest['EMA20']:
        return "VENDER"
    else:
        return "MANTENER"

# Configurar Streamlit
st.set_page_config(page_title="Asistente de Trading Cripto", layout="centered")
st.title("📊 Asistente de Trading Cripto (Corto Plazo)")

# Criptomonedas sugeridas
cryptos = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Cardano (ADA)": "ADA-USD",
    "Ripple (XRP)": "XRP-USD"
}

opcion = st.selectbox("Selecciona una criptomoneda", list(cryptos.keys()))
ticker = cryptos[opcion]

# Obtener y procesar datos
data = get_crypto_data(ticker)
data = add_technical_indicators(data)
signal = trading_signal(data)

# Mostrar señal de compra/venta
st.subheader(f"📌 Señal actual para {opcion}")
if signal == "COMPRAR":
    st.success("📈 Señal: COMPRAR")
elif signal == "VENDER":
    st.error("📉 Señal: VENDER")
else:
    st.info("⏳ Señal: MANTENER")

# Mostrar gráficos
st.subheader("📉 Gráfico de precios y EMA20")
st.line_chart(data[['Close', 'EMA20']])

st.subheader("📊 RSI y MACD")
st.line_chart(data[['RSI', 'MACD']])
