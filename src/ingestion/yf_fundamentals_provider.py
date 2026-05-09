import yfinance as yf
import pandas as pd


def get_fundamentals_4y(tickers):
    """
    Coleta dados fundamentalistas dos últimos 4 anos.

    Retorna:
        DataFrame com:
        - date
        - ticker
        - ebitda
        - net_income
        - revenue
    """

    all_data = []

    net_income_aliases = [
        "Net Income",
        "Net Income Common Stockholders"
    ]

    revenue_aliases = [
        "Total Revenue",
        "Revenue"
    ]

    for ticker in tickers:
        try:
            ticker = str(ticker).strip().upper()
            print(f"[INFO] Coletando fundamentos: {ticker}")

            stock = yf.Ticker(ticker)
            df = stock.financials

            if df.empty:
                print(f"[WARN] Sem dados para {ticker}")
                continue

            # formato long
            df = df.T

            net_income_col = next(
                (c for c in net_income_aliases if c in df.columns),
                None
            )

            revenue_col = next(
                (c for c in revenue_aliases if c in df.columns),
                None
            )

            if not all([
                "EBITDA" in df.columns,
                net_income_col,
                revenue_col
            ]):
                print(f"[WARN] Fundamentais incompletos: {ticker}")
                continue

            df = df[
                ["EBITDA", net_income_col, revenue_col]
            ].head(4)

            df = df.reset_index()

            df.columns = [
                "date",
                "ebitda",
                "net_income",
                "revenue"
            ]

            df["ticker"] = ticker

            all_data.append(df)

        except Exception as e:
            print(f"[ERROR] {ticker}: {e}")

    if not all_data:
        raise ValueError("Nenhum dado fundamental coletado.")

    return pd.concat(all_data, ignore_index=True)