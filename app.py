import pandas as pd
import ta
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

# Función para obtener los datos históricos de criptomonedas
def get_crypto_data(crypto_symbol, start_date, end_date):
    crypto_data = yf.download(crypto_symbol, start=start_date, end=end_date)
    return crypto_data

# Función para agregar indicadores técnicos
def add_technical_indicators(data):
    close_data = data['Close']
    
    # Verificar que close_data sea un pandas.Series unidimensional
    if not isinstance(close_data, pd.Series):
        raise ValueError(f"La columna 'Close' debe ser un pandas.Series, pero es de tipo {type(close_data)}")
    
    # Verificar si hay valores nulos
    if close_data.isnull().any():
        raise ValueError("La columna 'Close' contiene valores nulos (NaN), por favor limpia los datos antes de procesarlos.")
    
    # Verificar que haya suficientes datos
    if len(close_data) < 14:
        raise ValueError("No hay suficientes datos para calcular el RSI (se requieren al menos 14 puntos de datos).")
    
    # Calcular el RSI
    rsi = ta.momentum.RSIIndicator(close_data, window=14).rsi()
    data['RSI'] = rsi
    
    # Otros indicadores técnicos pueden ser añadidos aquí
    
    return data

# Función para mostrar las gráficas
def plot_data(data):
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    
    # Gráfico de precios
    ax[0].plot(data['Close'], label='Precio de Cierre', color='blue')
    ax[0].set_title('Precio de Cierre de la Criptomoneda')
    ax[0].legend()
    
    # Gráfico RSI
    ax[1].plot(data['RSI'], label='RSI', color='red')
    ax[1].set_title('RSI - Relative Strength Index')
    ax[1].legend()
    
    plt.tight_layout()
    plt.show()

# Función principal de la app web en Streamlit
def main():
    st.title('Asistente de Trading de Criptomonedas')
    
    # Obtener las entradas del usuario
    crypto_symbol = st.text_input('Símbolo de Criptomoneda (Ejemplo: BTC-USD, ETH-USD):', 'BTC-USD')
    start_date = st.date_input('Fecha de inicio:', pd.to_datetime('2023-01-01'))
    end_date = st.date_input('Fecha de finalización:', pd.to_datetime('2023-12-31'))
    
    # Obtener los datos históricos
    if crypto_symbol:
        st.write(f"Obteniendo datos históricos para {crypto_symbol} desde {start_date} hasta {end_date}...")
        crypto_data = get_crypto_data(crypto_symbol, start_date, end_date)
        
        if not crypto_data.empty:
            st.write(crypto_data.tail())  # Mostrar las últimas filas del DataFrame
            
            # Añadir indicadores técnicos
            try:
                crypto_data_with_indicators = add_technical_indicators(crypto_data)
                st.write(crypto_data_with_indicators.tail())  # Mostrar las últimas filas con indicadores añadidos
                
                # Mostrar los gráficos
                plot_data(crypto_data_with_indicators)
                
                # Análisis de señales de compra/venta (por ejemplo, RSI)
                latest_rsi = crypto_data_with_indicators['RSI'].iloc[-1]
                st.write(f"RSI más reciente: {latest_rsi:.2f}")
                
                if latest_rsi > 70:
                    st.write("¡Señal de sobrecompra! Podrías considerar vender.")
                elif latest_rsi < 30:
                    st.write("¡Señal de sobreventa! Podrías considerar comprar.")
                else:
                    st.write("RSI en rango normal, sigue monitoreando.")
            except ValueError as e:
                st.write(f"Error: {e}")
        else:
            st.write("No se encontraron datos para esta criptomoneda en el rango de fechas seleccionado.")
    else:
        st.write("Por favor ingresa el símbolo de una criptomoneda.")

if __name__ == '__main__':
    main()

