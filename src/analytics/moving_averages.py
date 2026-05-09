import pandas as pd

def calculate_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Trabalhar com uma cópia para evitar warnings de SettingWithCopy
    df = df.copy()

    # 2. transformar a coluna de data para datetime para a ordenação funcionar
    df["date"] = pd.to_datetime(df["date"])
    
    # 3. Ordenar por ticker e data (importante para o calculo)
    df = df.sort_values(["ticker", "date"])

    # 4. Calcular as médias com min_periods=1
    # O transform garante que o resultado mantenha o mesmo número de linhas do DF original
    df["ma7"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    
    df["ma30"] = df.groupby("ticker")["close"].transform(
        lambda x: x.rolling(window=30, min_periods=1).mean()
    )

    return df