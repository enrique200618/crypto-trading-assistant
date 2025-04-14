import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# ====== Función para obtener datos ======
def get_crypto_data(symbol, period='90d', interval='1h'):
    df = yf.download(tickers=symbol, period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No se pudo obtener datos para {symbol}")
    df = df[['Close']].copy()  # Solo usamos la columna 'Close'
    df.dropna(inplace=True)
    return df

# ====== Añadir indicadores ======
def add_technical_indicators(data):
    if 'Close' not in data.columns:
        raise ValueError("La columna 'Close' no está en los datos")

    close_series = data['Close']
    if not isinstance(close_series, pd.Series):
        raise ValueError("La columna 'Close' debe ser un Series 1D")

    data['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    data['EMA'] = ta.trend.EMAIndicator(close_series, window=14).ema_indicator()
    data.dropna(inplace=True)
    return data

# ====== Señal de compra/venta ======
def get_signal(data):
    last_rsi = data['RSI'].iloc[-1]
    last_price = data['Close'].iloc[-1]
    last_ema = data['EMA'].iloc[-1]

    if last_rsi < 30 and last_price > last_ema:
        return "Comprar"
    elif last_rsi > 70 and last_price < last_ema:
        return "Vender"
    else:
        return "Sin señal"

# ====== Interfaz con Streamlit ======
st.title("Asistente de Trading Cripto 📈")
st.markdown("Analiza RSI y EMA para recomendar **Comprar** o **Vender** en criptomonedas.")

cryptos = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'AVAX-USD']
selected = st.selectbox("Selecciona una criptomoneda:", cryptos)

try:
    data = get_crypto_data(selected)
    data = add_technical_indicators(data)
    signal = get_signal(data)

    st.subheader(f"Recomendación para {selected}")
    st.write(f"**{signal}**")

    st.line_chart(data[['Close', 'EMA']])
    st.area_chart(data[['RSI']])

except Exception as e:
    st.error(f"Ocurrió un error: {str(e)}")
