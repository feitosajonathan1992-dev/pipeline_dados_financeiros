import pandas as pd


def clean_fundamentals(df):
    """
    Limpeza e padronização dos fundamentos.

    - Conversão numérica
    - Conversão para milhões
    - Tratamento de datas
    - Remoção de nulos essenciais
    - Deduplicação
    """

    if df is None or df.empty:
        raise ValueError("DataFrame fundamentalista vazio.")

    df = df.copy()

    required_cols = ["date", "ticker", "revenue", "ebitda", "net_income"]

    existing_cols = [
        col for col in required_cols
        if col in df.columns
    ]

    if not existing_cols:
        raise ValueError("Nenhuma coluna fundamental encontrada.")

    # date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # métricas numéricas
    numeric_cols = ["revenue", "ebitda", "net_income"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

            df[col] = df[col].fillna(0) / 1_000_000

    # limpeza estrutural
    df = df.dropna(subset=["date", "ticker"])

    df = df.drop_duplicates(subset=["ticker", "date"])

    df = df.sort_values(["ticker", "date"])

    print("[INFO] Fundamentos limpos com sucesso.")

    return df