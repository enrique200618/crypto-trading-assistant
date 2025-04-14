import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Asistente de Trading de Criptomonedas")

# Lista de criptomonedas populares
cryptos = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Binance Coin": "BNB-USD",
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD"
}

# Selección de criptomoneda
crypto_name = st.selectbox("Selecciona una criptomoneda", list(cryptos.keys()))
crypto_symbol = cryptos[crypto_name]

# Rango de fechas
start_date = st.date_input("Desde", pd.to_datetime("2023-01-01"))
end_date = st.date_input("Hasta", pd.to_datetime("today"))

# Obtener datos
@st.cache_data
def get_crypto_data(symbol, start, end):
    return yf.download(symbol, start=start, end=end)

data = get_crypto_data(crypto_symbol, start_date, end_date)

# Verificamos que hay datos
if data.empty:
    st.error("No se pudieron obtener los datos de esta criptomoneda.")
    st.stop()

# Añadir indicadores técnicos
def add_technical_indicators(data):
    close_data = data['Close']  # Asegúrate de que sea un Series
    rsi = ta.momentum.RSIIndicator(close_data, window=14).rsi()
    ema = ta.trend.EMAIndicator(close_data, window=14).ema_indicator()
    data['RSI'] = rsi
    data['EMA'] = ema
    return data

data = add_technical_indicators(data)

# Mostrar datos
st.subheader("Datos históricos")
st.dataframe(data.tail())

# Visualizar precios y EMA
st.subheader("Precio vs. EMA")
fig, ax = plt.subplots()
ax.plot(data.index, data['Close'], label='Precio Cierre')
ax.plot(data.index, data['EMA'], label='EMA 14', linestyle='--')
ax.set_title(f"{crypto_name} Precio y EMA")
ax.legend()
st.pyplot(fig)

# Estrategia simple de compra/venta
st.subheader("Recomendación de Trading")
latest_rsi = data['RSI'].iloc[-1]
latest_price = data['Close'].iloc[-1]
latest_ema = data['EMA'].iloc[-1]

if latest_rsi < 30 and latest_price > latest_ema:
    st.success("📈 Señal de COMPRA: RSI bajo y el precio está sobre la EMA")
elif latest_rsi > 70 and latest_price < latest_ema:
    st.error("📉 Señal de VENTA: RSI alto y el precio está por debajo de la EMA")
else:
    st.info("🤔 Sin señal clara de compra o venta.")


