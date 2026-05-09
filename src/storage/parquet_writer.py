from pathlib import Path
import pandas as pd

def save_parquet(df: pd.DataFrame, layer: str, market: str, filename: str):
    """
    Salva o DataFrame seguindo a estrutura: data / camada / mercado / arquivo.parquet
    """
    # CORREÇÃO: Removidas as aspas de market e layer para usar as variáveis
    base_path = Path("data") / market / layer
    
    # Cria as pastas se não existirem
    base_path.mkdir(parents=True, exist_ok=True)

    file_path = base_path / filename

    try:
        df.to_parquet(file_path, index=False)
        print(f"[INFO] Arquivo salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"[ERROR] Erro ao salvar {filename}: {e}")
        raise