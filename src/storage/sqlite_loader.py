import sqlite3
from pathlib import Path

class SQLiteLoader:
    def __init__(self, db_name="financial.br_data.db"):
        # Isso pega a pasta raiz do projeto (PIPELINE_DADOS) 
        # subindo 3 níveis a partir de src/storage/sqlite_loader.py
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        
        # Define o caminho final na pasta data da raiz
        self.db_path = self.root_dir / "data" / db_name

        # Garante que a pasta 'data' exista na raiz
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # PRINT DE DEBUG: Isso vai te mostrar exatamente onde o arquivo está sendo salvo
        print(f"[DEBUG] Banco de dados em: {self.db_path}")

    def save_table(self, df, table_name):
        if df is None or df.empty:
            print(f"[AVISO] Tabela '{table_name}' não salva: DataFrame vazio.")
            return

        conn = sqlite3.connect(self.db_path)
        try:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists="replace",
                index=False
            )
            conn.commit() # Garante a persistência física no disco
            print(f"[INFO] Tabela '{table_name}' salva ({len(df)} linhas).")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar '{table_name}': {e}")
        finally:
            conn.close()