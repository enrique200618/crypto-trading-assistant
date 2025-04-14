import yfinance as yf
import pandas as pd
import ta  # Técnicas de análisis (RSI, SMA, etc.)
import streamlit as st  # Para crear la app web

# Función para obtener datos históricos de las criptomonedas
def get_crypto_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Añadir indicadores técnicos
def add_technical_indicators(data):
    # Asegurarse de que la columna 'Close' esté en formato unidimensional
    close_data = data['Close'].values.flatten()
    
    # Calculando RSI (Relative Strength Index)
    rsi = ta.momentum.RSIIndicator(close_data, window=14).rsi()
    data['RSI'] = rsi

    # Calculando SMA (Simple Moving Average)
    sma = ta.trend.SMAIndicator(close_data, window=50).sma_indicator()
    data['SMA50'] = sma
    
    return data

# Función para generar recomendaciones de compra/venta
def generate_recommendations(data):
    recommendations = []
    for i in range(len(data)):
        # Si el RSI es menor a 30 y el precio está por encima de la SMA, es una señal de compra
        if data['RSI'][i] < 30 and data['Close'][i] > data['SMA50'][i]:
            recommendations.append('Comprar')
        # Si el RSI es mayor a 70 y el precio está por debajo de la SMA, es una señal de venta
        elif data['RSI'][i] > 70 and data['Close'][i] < data['SMA50'][i]:
            recommendations.append('Vender')
        else:
            recommendations.append('Mantener')  # Si no hay una señal clara, mantener la posición

    data['Recomendación'] = recommendations
    return data

# Función para mostrar las alertas en tiempo real
def show_alerts(data):
    last_signal = data['Recomendación'].iloc[-1]  # Obtenemos la última señal
    
    if last_signal == 'Comprar':
        st.markdown(f"### 🚨 **¡Es momento de comprar!** 🚨")
    elif last_signal == 'Vender':
        st.markdown(f"### 🚨 **¡Es momento de vender!** 🚨")
    else:
        st.markdown(f"### **Mantener** por el momento. No hay señal clara.")

# Ejemplo de uso con una criptomoneda (Bitcoin, por ejemplo)
crypto_data = get_crypto_data("BTC-USD", "2023-01-01", "2024-01-01")
crypto_data_with_indicators = add_technical_indicators(crypto_data)
crypto_data_with_recommendations = generate_recommendations(crypto_data_with_indicators)

# Mostrar las alertas en tiempo real
st.title("Crypto Trading Assistant")
show_alerts(crypto_data_with_recommendations)

# Mostrar la tabla con los datos e indicadores
st.write(crypto_data_with_recommendations[['Close', 'RSI', 'SMA50', 'Recomendación']].tail())
