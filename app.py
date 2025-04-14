import yfinance as yf
import ta
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Función para obtener datos históricos de criptomonedas
def get_crypto_data(crypto_symbol, start_date, end_date):
    data = yf.download(crypto_symbol, start=start_date, end=end_date)
    return data

# Función para añadir indicadores técnicos
def add_technical_indicators(data):
    data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()
    data['SMA_50'] = ta.trend.SMAIndicator(close=data['Close'], window=50).sma_indicator()
    return data

# Función para generar señales de compra/venta
def generate_signal(data):
    last_row = data.dropna().iloc[-1]  # Última fila con datos completos
    price = last_row['Close']
    rsi = last_row['RSI']
    sma50 = last_row['SMA_50']
    
    if rsi < 30 and price > sma50:
        return "COMPRAR"
    elif rsi > 70 and price < sma50:
        return "VENDER"
    else:
        return "MANTENER"

# Lista de criptomonedas a evaluar
cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD"]

# Rango de fechas: últimos 180 días
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')

# Configuración de la app web
st.title("🧠 Asistente de Trading de Criptomonedas")
st.write("A continuación se muestran las recomendaciones de compra/venta para las criptomonedas seleccionadas.")

# Resultados de las señales de trading
results = []
for crypto in cryptos:
    try:
        data = get_crypto_data(crypto, start_date, end_date)
        
        if data.empty:
            results.append((crypto, "Sin datos"))
            continue
        
        data = add_technical_indicators(data)
        signal = generate_signal(data)
        results.append((crypto, signal))
    except Exception as e:
        results.append((crypto, f"Error: {e}"))

# Mostrar las recomendaciones
df_signals = pd.DataFrame(results, columns=["Cripto", "Recomendación"])
st.write(df_signals)

# Mostrar gráficos interactivos para cada criptomoneda
for crypto in cryptos:
    try:
        data = get_crypto_data(crypto, start_date, end_date)
        st.write(f"### Gráfico de {crypto}")
        st.line_chart(data['Close'])
    except Exception as e:
        st.write(f"Error al mostrar gráfico para {crypto}: {e}")
