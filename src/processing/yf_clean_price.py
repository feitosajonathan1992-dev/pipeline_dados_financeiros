import pandas as pd


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza dados de preços.
    """

    df = df.copy()

    # Padronizar nomes de colunas
    df.columns = [col.lower() for col in df.columns]

    # Converter tipos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remover nulos críticos
    df = df.dropna(subset=["date", "ticker", "close"])

    # Remover duplicados
    df = df.drop_duplicates(subset=["date", "ticker"])

    # Ordenar
    df = df.sort_values(["ticker", "date"])
    
    print("[INFO] preços limpos com sucesso.")

    return df


# # def clean_fundamentals(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Limpa e padroniza dados fundamentalistas.
#     """

#     df = df.copy()

#     # Padronizar nomes
#     df.columns = [col.lower() for col in df.columns]

#     # Converter data
#     df["date"] = pd.to_datetime(df["date"], errors="coerce")

#     # Converter métricas
#     numeric_cols = ["revenue", "ebitda", "net_income"]
#     for col in numeric_cols:
#         if col in df.columns:
#             df[col] = pd.to_numeric(df[col], errors="coerce")

#     # Remover linhas sem dados essenciais
#     df = df.dropna(subset=["date", "ticker"])

#     # Remover duplicados
#     df = df.drop_duplicates(subset=["date", "ticker"])

#     # Ordenar
#     df = df.sort_values(["ticker", "date"])

#   #  return df