import yfinance as yf
import pandas as pd


# =========================
# 📊 PRICES
# =========================
def get_prices(tickers, period="4y"):
    all_data = []

    for ticker in tickers:
        try:
            if not isinstance(ticker, str):
                print(f"[ERRO] Tipo inválido: {ticker} ({type(ticker)})")
                continue

            ticker = ticker.strip().upper()

            print(f"[INFO] Coletando preços: {ticker}")

            df = yf.download(
                ticker,
                period=period,
                group_by="column",
                auto_adjust=True,
                progress=False
            )

            if df.empty:
                print(f"[WARN] Sem dados para {ticker}")
                continue

            # 🔥 Corrigir (evita) o MultiIndex
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df.reset_index(inplace=True)

            df = df.rename(columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            })

            df["ticker"] = ticker

            all_data.append(df)

        except Exception as e:
            print(f"[ERROR] Preço {ticker}: {e}")

    if not all_data:
        raise ValueError("Nenhum dado de preço coletado.")

    return pd.concat(all_data, ignore_index=True)

