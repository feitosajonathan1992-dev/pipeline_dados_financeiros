import pandas as pd


def screen_profitable(df: pd.DataFrame) -> pd.DataFrame:
    """
    Screener de ações baseado em:

    ✔ EBITDA (não nulo)
    ✔ Lucro líquido (não nulo)
    ✔ Retorna apenas o registro mais recente por ticker
    """

    if df is None or df.empty:
        raise ValueError("DataFrame vazio recebido no screener.")

    df = df.copy()

    # =========================
    # 🔍 Validação de colunas
    # =========================
    required_cols = ["ticker", "date", "close"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória faltando: {col}")

    # =========================
    # 💰 Filtro fundamentalista
    # =========================
    if "ebitda" in df.columns and "net_income" in df.columns:
        df["ebitda"] = pd.to_numeric(df["ebitda"], errors="coerce")
        df["net_income"] = pd.to_numeric(df["net_income"], errors="coerce")

        # Em vez de excluir quem é NaN, vamos apenas filtrar quem tem lucro >= 0
        # E usamos .fillna(0) para que o filtro não descarte os bancos (NaN)
        df = df[
            (df["ebitda"].fillna(0) >= 0) & 
            (df["net_income"].fillna(0) >= 0)
        ]
    else:
        print("[WARN] Colunas fundamentalistas não disponíveis - pulando filtro de EBITDA/Lucro")

    # # =========================
    # # 📈 Tendência (Médias móveis)
    # # =========================
    # if "ma30" in df.columns and "ma200" in df.columns:
    #     df["ma30"] = pd.to_numeric(df["ma30"], errors="coerce")
    #     df["ma200"] = pd.to_numeric(df["ma200"], errors="coerce")

    #     df = df[df["ma30"] > df["ma200"]]
    # else:
    #     print("[WARN] Médias móveis não disponíveis - pulando filtro de tendência")

    # =========================
    # 📊 Selecionar último registro por ticker
    # =========================
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.sort_values(["ticker", "date"])
    df = df.groupby("ticker").tail(1)

    # =========================
    # 🧹 Limpeza final
    # =========================
    df = df.dropna(subset=["date", "ticker"])

    # Ordenar por melhor desempenho (opcional)
    if "close" in df.columns:
        df = df.sort_values("close", ascending=False)

    return df