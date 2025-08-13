import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    layout="wide",
    page_title="TRADEX - Painel Forex Completo",
    page_icon="💹"
)

# --- FUNÇÕES HELPERS ---

def tradingview_chart(symbol, interval, theme, studies):
    """Gera o código HTML para o widget de gráfico do TradingView."""
    interval_map = {
        "1 minuto": "1", "5 minutos": "5", "15 minutos": "15",
        "1 hora": "60", "4 horas": "240", "Diário": "D", "Semanal": "W"
    }
    tv_interval = interval_map.get(interval, "60")

    widget_code = f"""
    <div class="tradingview-widget-container" style="height:100%;width:100%">
      <div id="tradingview_{symbol.replace(':', '')}" style="height:calc(100% - 32px);width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
          "width": "100%", "height": 400, "symbol": "{symbol}", "interval": "{tv_interval}",
          "timezone": "America/Sao_Paulo", "theme": "{theme}", "style": "1", "locale": "br",
          "enable_publishing": false, "hide_side_toolbar": false, "allow_symbol_change": true,
          "save_image": true, "studies": {studies}, "container_id": "tradingview_{symbol.replace(':', '')}"
      }});
      </script>
    </div>
    """
    components.html(widget_code, height=400)

# --- BARRA LATERAL (SIDEBAR) ---
# A sidebar continua controlando a parte de "Análise Técnica"
st.sidebar.header("Painel de Controle")

try:
    logo = Image.open("loho2.png")
    st.sidebar.image(logo, width=200)
except FileNotFoundError:
    st.sidebar.warning("Logo (loho2.png) não encontrada.")

available_pairs = [
    "OANDA:EURUSD", "OANDA:USDJPY", "OANDA:GBPUSD", "OANDA:AUDUSD",
    "OANDA:USDCAD", "OANDA:USDCHF", "OANDA:NZDUSD", "OANDA:EURGBP",
    "OANDA:EURJPY", "OANDA:GBPJPY", "OANDA:AUDJPY", "OANDA:XAUUSD"
]

selected_pairs = st.sidebar.multiselect(
    "Escolha os pares (para Análise Técnica):",
    options=available_pairs,
    default=["OANDA:EURUSD", "OANDA:USDJPY", "OANDA:GBPUSD", "OANDA:XAUUSD"]
)

selected_interval = st.sidebar.selectbox(
    "Selecione o Timeframe:",
    options=["1 minuto", "5 minutos", "15 minutos", "1 hora", "4 horas", "Diário", "Semanal"],
    index=3
)

selected_theme = st.sidebar.selectbox(
    "Selecione o Tema:", options=["dark", "light"], index=0
)

num_columns = st.sidebar.slider(
    "Número de colunas:", min_value=1, max_value=4, value=3
)

selected_studies = st.sidebar.multiselect(
    "Adicionar Indicadores:",
    options=["MASimple@tv-basicstudies", "Volume@tv-basicstudies", "RSI@tv-basicstudies"],
    default=[]
)


# --- CONTEÚDO PRINCIPAL (PÁGINA ÚNICA) ---
st.markdown("<h1 style='text-align: center;'>Painel Forex - TRADEX</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- SEÇÃO 1: VISÃO GERAL (HEATMAP) ---
st.header("Visão Rápida do Mercado (Heatmap)")
st.caption("O tamanho do retângulo representa o volume de negociação (simulado) e a cor representa a variação nas últimas 24h.")

# Simular dados para o treemap (idealmente, viria de uma API)
heatmap_ativos = ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD", "USDCAD", "XAUUSD", "NZDUSD", "EURGBP"]
heatmap_dados = {
    'ativo': heatmap_ativos,
    'grupo': ['Majors', 'Majors', 'Majors', 'Majors', 'Majors', 'Commodities', 'Majors', 'Crosses'],
    'volume_negociacao_mm': [random.randint(500, 2000) for _ in heatmap_ativos],
    'variacao_24h': [random.uniform(-1.5, 1.5) for _ in heatmap_ativos]
}
df_heatmap = pd.DataFrame(heatmap_dados)

# Criar e exibir o gráfico treemap
fig = px.treemap(
    df_heatmap,
    path=[px.Constant("Todos"), 'grupo', 'ativo'],
    values='volume_negociacao_mm',
    color='variacao_24h',
    hover_data={'variacao_24h': ':.2f%'},
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=0
)
fig.update_layout(margin=dict(t=30, l=10, r=10, b=10), font=dict(size=16))
fig.update_traces(texttemplate="<b>%{label}</b><br>%{customdata[0]:.2f}%", textposition="middle center", textfont_size=18)
st.plotly_chart(fig, use_container_width=True)

# Adicionando um separador visual
st.markdown("<br><hr><br>", unsafe_allow_html=True)

# --- SEÇÃO 2: ANÁLISE TÉCNICA (GRÁFICOS) ---
st.header("Análise Técnica Detalhada")
st.caption("Use o painel de controle à esquerda para customizar os gráficos abaixo.")

if not selected_pairs:
    st.warning("Por favor, selecione pelo menos um par de moedas na barra lateral para ver os gráficos.")
else:
    for i in range(0, len(selected_pairs), num_columns):
        cols = st.columns(num_columns)
        row_pairs = selected_pairs[i : i + num_columns]
        for col, pair in zip(cols, row_pairs):
            with col:
                st.subheader(pair.replace("OANDA:", ""))
                tradingview_chart(pair, selected_interval, selected_theme, str(selected_studies))

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<p style='text-align:center; color: grey;'>Desenvolvido por TRADEX | 2025</p>", unsafe_allow_html=True)
