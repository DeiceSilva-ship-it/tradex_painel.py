# TRADEX - Painel Forex (Streamlit + TradingView)

## Rodar localmente
```bash
pip install -r requirements.txt
streamlit run tradex_painel.py
```

## Deploy (Streamlit Community Cloud)
1. Suba estes arquivos para um repositório no GitHub (incluindo `loho2.png`).
2. Vá em https://share.streamlit.io/ (Streamlit Community Cloud) e clique em **New app**.
3. Selecione seu repositório e arquivo principal `tradex_painel.py`. Clique **Deploy**.
4. Seu app ficará acessível em `https://<seu-projeto>.streamlit.app`.

## Deploy (Render.com - com domínio próprio)
1. Crie conta no https://render.com e clique em **New +** > **Web Service**.
2. Conecte seu GitHub e selecione o repositório.
3. **Runtime**: *Python 3* — **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `streamlit run tradex_painel.py --server.port $PORT --server.address 0.0.0.0`
5. Após o deploy, adicione seu domínio em **Settings > Custom Domains** e siga as instruções de DNS.