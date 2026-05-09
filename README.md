Pipeline de Dados Financeiros — B3

Pipeline de engenharia de dados para ingestão, transformação e enriquecimento de dados do mercado acionário brasileiro, utilizando arquitetura medalhão (Bronze / Silver / Gold) para processamento analítico e geração de indicadores financeiros.

Arquitetura do Projeto
PIPELINE_DADOS/
├── config/
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── notebooks/
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── analytics/
│   └── storage/
├── tests/
└── run_pipeline.py
Stack Utilizada
Python
pandas
NumPy
PyArrow
SQLite
pytest
yfinance
Pipeline de Processamento

Bronze

Coleta de dados brutos de mercado para as 20 maiores empresas da B3.

Silver

Padronização, limpeza, tipagem e validação estrutural.

Gold

Enriquecimento analítico com:

Médias móveis
Indicadores técnicos
Filtros fundamentalistas
Screener automatizado
Funcionalidades
Ingestão resiliente

Tratamento de falhas em ativos indisponíveis.

Validação de esquema

Garantia de integridade antes das transformações.

Persistência otimizada

Armazenamento em formato parquet para alta performance.

Testes automatizados

Cobertura de regras de transformação e consistência.

Como executar
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_pipeline.py
Exemplo de saída
[INFO] Dados coletados
[INFO] Bronze salvo
[INFO] Silver processado
[INFO] Gold gerado
Próximos passos
Integração com dashboard em Microsoft Power BI
Expansão para novos provedores
Orquestração automatizada