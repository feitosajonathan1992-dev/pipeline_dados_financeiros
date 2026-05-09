import pandas as pd


def validate_price_schema(df: pd.DataFrame):
    required_columns = [
        "date",
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Colunas faltando: {missing}")

    print("✅ Schema de preços OK")


def validate_fundamental_schema(df: pd.DataFrame):
    required_columns = [
        "date",
        "ticker",
        "ebitda",
        "net_income"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        print(f"⚠️ Dados fundamentais ausentes: {missing}")
        return False

    print("✅ Schema de fundamentos OK")
    return True