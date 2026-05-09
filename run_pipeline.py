from pathlib import Path
import pandas as pd

# ingestion
from src.ingestion.yf_price_provider import get_prices
from src.ingestion.yf_fundamentals_provider import get_fundamentals_4y

# processing
from src.processing.yf_clean_price import clean_prices
from src.processing.yf_clear_fundamentals import clean_fundamentals

# analytics
from src.analytics.moving_averages import calculate_moving_averages
from src.analytics.screener import screen_profitable

# storage
from src.storage.parquet_writer import save_parquet
from src.storage.sqlite_loader import SQLiteLoader

# tests
from tests.test_schema import validate_price_schema

# config
from config.tickers import B3_TICKERS

#inicia o pipeline
def run():
    try:
        # =========================
        # 🥉 BRONZE
        # =========================
        print("🚀 Iniciando Pipeline: BRONZE")

        # preços
        df_prices = get_prices(B3_TICKERS)
        save_parquet(df_prices, "bronze", "br", "raw_prices.parquet")

        # fundamentos
        df_fund = get_fundamentals_4y(B3_TICKERS)
        save_parquet(df_fund, "bronze","br","fundamentals.parquet")

        print("✅ Bronze completo")

        # =========================
        # 🥈 SILVER
        # =========================
        print("🥈 Iniciando Pipeline: SILVER")

        # limpeza preços
        df_prices_silver = clean_prices(df_prices)
        # validação-testes
        validate_price_schema(df_prices_silver)

        save_parquet(
        df_prices_silver,"silver","br", "prices.parquet")

        # limpeza fundamentos
        df_fund_silver = clean_fundamentals(df_fund)

        save_parquet(
        df_fund_silver,"silver","br","fundamentals.parquet")

        print("✅ Silver completo")

        # =========================
        # 🥇 GOLD
        # =========================
        print("🥇 Iniciando Pipeline: GOLD")

        # 🔥 alinhar granularidade por ano, ajusta o merge()
        df_prices_silver["year"] = df_prices_silver["date"].dt.year
        df_fund_silver["year"] = pd.to_datetime(
            df_fund_silver["date"]
        ).dt.year

        # 🔗 mesclar
        # Forçamos as colunas de união a serem do mesmo tipo (string)
        df_prices_silver['ticker'] = df_prices_silver['ticker'].astype(str)
        df_fund_silver['ticker'] = df_fund_silver['ticker'].astype(str)
        df_gold = df_prices_silver.merge(
            df_fund_silver,
            on=["ticker", "year"],
            how="left"
        )
        df_gold = df_gold.reset_index()
        if "date_x" in df_gold.columns: # Caso o merge tenha gerado sufixos
            df_gold = df_gold.rename(columns={"date_x": "date"})
        # 📈 indicadores
        df_gold = calculate_moving_averages(df_gold)

        # 🔎 screener
        df_filtered = screen_profitable(df_gold)

        # salvar
        save_parquet(
            df_gold,"gold","br","metrics.parquet")

        save_parquet(
            df_filtered,"gold","br","filtered.parquet")
        
         # salvar SQLite
        loader = SQLiteLoader()

        loader.save_table(df_gold, "gold_metrics")
        loader.save_table(df_filtered, "gold_filtered")

        print("✅ Gold completo")
        print("🎯 Pipeline finalizado com sucesso!")

    except Exception as e:
        print(f"❌ Erro no pipeline: {e}")
        raise

if __name__ == "__main__":
    run()