
# app.py
# ------------------------------------------------------------
# TRADEx — Dashboard de Cripto (estilo Coin360, simples)
# - Heatmap por Market Cap (Plotly Treemap)
# - Cores por variação de 24h (verde/vermelho)
# - Dados gratuitos em tempo quase real (CoinGecko API)
# - Logo no topo e tela única (sem sidebar)
# - Atualização automática por JavaScript (configurável)
# ------------------------------------------------------------
import time
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="TRADEx — Crypto Heatmap", page_icon="📊", layout="wide")

# ---------------------------
# Estilos e barra superior com logo
# ---------------------------
st.markdown(
    '''
    <style>
        :root {
            --bg: #0b0f17;
            --panel: #121826;
            --text: #e5e7eb;
            --muted: #94a3b8;
            --accent: #ff4b6e;
            --radius: 18px;
        }
        html, body, [class^="css"]  {
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }
        .block-container { padding-top: 0.6rem; }
        .topbar { display:flex; align-items:center; gap:14px; margin: 8px 0 14px 0; }
        .topbar .title { font-weight:700; font-size: 1.3rem; letter-spacing: .3px; }
        .panel { background: var(--panel); border:1px solid rgba(255,255,255,0.06); border-radius: var(--radius); padding: 12px 14px; }
        .muted { color: var(--muted); font-size: 12px; }
        .footer-note { color: var(--muted); font-size: 12px; opacity:.9; margin-top:8px;}
        .refresh { display:flex; align-items:center; gap:8px; justify-content:flex-end; }
        .hide-header > header {visibility: hidden;}
    </style>
    ''',
    unsafe_allow_html=True,
)

# Barra superior
top_l, top_r = st.columns([0.75, 0.25])
with top_l:
    st.markdown('<div class="topbar">'
                '<img src="assets/logo.png" width="110">'
                '<div class="title">TRADEx • Heatmap de Criptos</div>'
                '</div>', unsafe_allow_html=True)
with top_r:
    st.markdown(f'<div class="refresh muted">Atualizado: {time.strftime("%d/%m/%Y %H:%M:%S")}</div>', unsafe_allow_html=True)

# ---------------------------
# Parâmetros
# ---------------------------
TOP_N = 120           # quantidade de moedas no heatmap
REFRESH_SEC = 60      # intervalo de auto refresh (segundos)
VS_CURRENCY = "usd"   # moeda base

# ---------------------------
# Função de dados — CoinGecko API (gratuita)
# ---------------------------
@st.cache_data(show_spinner=False, ttl=90)
def fetch_markets(top_n:int=TOP_N, vs_currency:str=VS_CURRENCY) -> pd.DataFrame:
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = dict(vs_currency=vs_currency,
                  order="market_cap_desc",
                  per_page=min(250, top_n),
                  page=1,
                  price_change_percentage="1h,24h,7d",
                  locale="en")
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    # renomeia e garante colunas
    rename_map = {
        "id":"id", "symbol":"symbol", "name":"name",
        "current_price":"price", "market_cap":"market_cap",
        "total_volume":"volume",
        "price_change_percentage_24h_in_currency":"chg24",
    }
    # Se a chave específica não vier, usa genérica
    if "price_change_percentage_24h_in_currency" not in df.columns and "price_change_percentage_24h" in df.columns:
        df["price_change_percentage_24h_in_currency"] = df["price_change_percentage_24h"]
    df = df.rename(columns=rename_map)
    needed = ["id","symbol","name","price","market_cap","volume","chg24"]
    for c in needed:
        if c not in df.columns:
            df[c] = None
    df["symbol"] = df["symbol"].str.upper()
    return df[needed].sort_values("market_cap", ascending=False).head(top_n)

def fmt_money(x: float) -> str:
    try:
        x = float(x)
        if x >= 1e12: return f"${x/1e12:.2f}T"
        if x >= 1e9:  return f"${x/1e9:.2f}B"
        if x >= 1e6:  return f"${x/1e6:.2f}M"
        if x >= 1e3:  return f"${x/1e3:.2f}K"
        return f"${x:.2f}"
    except Exception:
        return "-"

# ---------------------------
# Carrega dados
# ---------------------------
try:
    df = fetch_markets()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

if df.empty:
    st.warning("Sem dados no momento. Tente novamente em instantes.")
    st.stop()

# ---------------------------
# Heatmap (treemap) — tamanho por Market Cap, cor por variação 24h
# ---------------------------
heat = df.copy()
heat["label"] = heat.apply(lambda r: f"{r['symbol']}\n{fmt_money(r['market_cap'])}\n{(r['chg24'] or 0):+.2f}%", axis=1)

color_scale = ["#ef4444", "#f59e0b", "#22c55e"]  # vermelho -> amarelo -> verde
fig = px.treemap(
    heat,
    path=["label"],
    values="market_cap",
    color="chg24",
    color_continuous_scale=color_scale,
    color_continuous_midpoint=0,
    hover_data={
        "label": False,
        "name": True,
        "symbol": True,
        "price": ":$.4f",
        "market_cap": ":$,.0f",
        "volume": ":$,.0f",
        "chg24": ":+.2f%%",
    },
)
fig.update_traces(root_color="rgba(0,0,0,0)")
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    paper_bgcolor="#0b0f17",
    plot_bgcolor="#0b0f17",
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ---------------------------
# Rodapé + Auto refresh
# ---------------------------
st.markdown('<div class="footer-note">Fonte: CoinGecko API (gratuita). Atualiza automaticamente a cada '
            f'{REFRESH_SEC} segundos. | Este painel é informativo e não constitui recomendação de investimento.</div>', unsafe_allow_html=True)

# Auto-refresh via JS (sem dependências extras)
st.components.v1.html(f"""
    <script>
        setTimeout(() => window.location.reload(), {REFRESH_SEC * 1000});
    </script>
""", height=0)
