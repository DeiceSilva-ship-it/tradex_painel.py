
# TRADEx — Crypto Heatmap (Coin360-like, gratuito)

Painel simples, fullscreen e intuitivo com **heatmap por capitalização de mercado** e **cores por variação 24h**, usando **dados gratuitos** da CoinGecko API.

**Stack:** Streamlit + Plotly + Requests  
**Dados:** CoinGecko (gratuito)  
**Atualização:** automática a cada 60s (ajuste em `app.py` via `REFRESH_SEC`).

---

## 🚀 Executar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

App abre em `http://localhost:8501`.

---

## ☁️ Publicar (Streamlit Community Cloud — grátis)
1. Crie um repositório no GitHub e envie os arquivos deste projeto.
2. Acesse https://streamlit.io/cloud e faça login com o GitHub.
3. Clique **New app** → selecione seu repositório e o arquivo `app.py` → **Deploy**.

---

## 🔧 Personalizações rápidas
- Logo: substitua `assets/logo.png` pelo seu arquivo (mesmo nome).
- Quantidade de moedas: ajuste `TOP_N` em `app.py`.
- Intervalo de atualização: ajuste `REFRESH_SEC` em `app.py`.
- Cores do heatmap: edite `color_scale` em `app.py`.

---

## ℹ️ Observações
- CoinGecko possui limites de taxa. Em alto tráfego, aumente `REFRESH_SEC`.
- Este painel é apenas informativo. Não é recomendação de investimento.
