import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(layout="wide", page_title="TRADEX - Painel Forex", initial_sidebar_state="collapsed")

# Logo (arquivo na mesma pasta: loho2.png)
try:
    logo = Image.open("loho2.png")
    st.image(logo, width=250)
except FileNotFoundError:
    st.warning("Logo não encontrada. Suba 'loho2.png' na mesma pasta do app.")

# Título
st.markdown("<h1 style='text-align: center;'>Painel Forex - TRADEX</h1>", unsafe_allow_html=True)

# Lista de pares de moedas
pairs = [
    "OANDA:EURUSD", "OANDA:USDJPY", "OANDA:GBPUSD",
    "OANDA:AUDUSD", "OANDA:USDCAD", "OANDA:USDCHF", "OANDA:NZDUSD"
]

# Função para embed TradingView
def tradingview_chart(symbol):
    widget_code = f"""
    <div class="tradingview-widget-container" style="height:100%; width:100%">
      <div id="tradingview_{symbol.replace(':','')}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
          "width": "100%",
          "height": 350,
          "symbol": "{symbol}",
          "interval": "60",
          "timezone": "Etc/UTC",
          "theme": "dark",
          "style": "1",
          "locale": "br",
          "toolbar_bg": "#000000",
          "enable_publishing": false,
          "hide_legend": false,
          "save_image": false,
          "studies": [],
          "container_id": "tradingview_{symbol.replace(':','')}"
      }});
      </script>
    </div>
    """
    components.html(widget_code, height=350)

# Layout dinâmico - 3 colunas por linha
for i in range(0, len(pairs), 3):
    cols = st.columns(3)
    for col, pair in zip(cols, pairs[i:i+3]):
        with col:
            st.subheader(pair.replace("OANDA:", ""))
            tradingview_chart(pair)

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align:center;'>Desenvolvido por TRADEX | 2025</p>", unsafe_allow_html=True)