# Tema B: Otimização de Armazenamento e Consulta com PySpark

**MBA em Engenharia de Dados - Data Collection & Storage**

Este projeto realiza uma comparação entre formatos de arquvivos para demonstrar a importância da otimização de armazenamento e consulta em um ambiente de Big Data, propondo uma estratégia de ciclo de vida de dados. A solução foi totalmente desenvolvida com Docker e GitHub Codespaces.

**Alunos:**
**Fabio Fumio Wada – RA 10741479** /
**Sweeli Suzuki – RA 10423319** /
**Tatiane Silva Santos  – RA 10747108**

**Prof: Alexandre Tavares**


## 🚀 Objetivos

- **Comparar Formatos:** Analisar o impacto de formatos de arquivo (CSV, JSON, Parquet, ORC) no tamanho de armazenamento e na performance de queries.
- **Analisar Performance:** Medir o tempo de leitura, filtro e agregação para cada formato.
- **Propor Ciclo de Vida:** Desenvolver uma estratégia de ciclo de vida (Hot, Warm, Cold) para otimizar custos.
- **Containerizar Solução:** Empacotar a aplicação com Docker para execução em qualquer ambiente, incluindo GitHub Codespaces.

## 📊 Dataset Incluído

Este projeto inclui um **dataset pré-gerado** de 1 milhão de registros (~87 MB) para acelerar a execução:

- **Arquivo:** `data/tema_b_sensores_iot.csv`
- **Registros:** 1.000.000 leituras de sensores IoT
- **Tamanho:** 87 MB
- **Documentação:** `data/DATASET_INFO.md` 

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Processamento:** Apache Spark 3.5.0
- **Containerização:** Docker, Docker Compose
- **Formatos Analisados:** CSV, JSON, Parquet, ORC
- **Bibliotecas Python:** PySpark, Pandas, Matplotlib, Seaborn

## 📁 Estrutura de Diretórios

```
/tema_b_github
├── Dockerfile             # Define a imagem Docker com Spark e dependências
├── docker-compose.yml     # Orquestra o container de serviço
├── README.md              # Este arquivo
├── requirements.txt       # Dependências Python
├── scripts/
│   └── tema_b_otimizacao_docker.py  # Script principal da análise
├── data/                  # Diretório para armazenar os datasets gerados
├── output/                # Diretório para salvar relatórios e gráficos
├── notebooks/             # (Opcional) Para análises interativas em Jupyter
└── .devcontainer/         # Configuração para GitHub Codespaces
    └── devcontainer.json
```

## 🚀 Como Executar no GitHub Codespaces

EXECUÇÃO RÁPIDA (LOCAL):
------------------------
Se você tem Docker instalado, pode testar localmente:

1. **Executar a Análise:**
  cd tema_b_github
  ./run.sh full

   Este comando executará dentro do container o comnando:
      python3 /app/scripts/tema_b_otimizacao_docker.py

2. **Verificar os Resultados:**
   - Os resultados estarão nos diretórios `data/` e `output/`.

3. **Gerar gráficos:**
   - Executar no terminal os comandos do arquivo "pre_geracao_graficos_tema_b.txt"
   - Excutar no terminal o comando "python3 /workspace/gerar_graficos.py"


## 📈 Resultados Esperados

O script irá gerar um relatório detalhado no console e um arquivo JSON com os seguintes resultados:

- **Comparativo de Tamanho:**
  - **CSV:** ~87 MB
  - **JSON:** ~120 MB
  - **Parquet:** ~25 MB (redução de ~71%)
  - **ORC:** ~22 MB (redução de ~75%)

- **Comparativo de Performance:**
  - **Leitura Completa:** Formatos colunares (Parquet/ORC) são ~3-4x mais rápidos.
  - **Queries com Filtro:** Formatos colunares são ~5-10x mais rápidos devido ao Predicate Pushdown.
  - **Queries com Agregação:** Formatos colunares são ~3-5x mais rápidos.

## 🔄 Estratégia de Ciclo de Vida

O projeto também propõe uma estratégia de ciclo de vida para otimização de custos:

- **Hot Storage (0-30 dias):**
  - **Mídia:** SSD/NVMe
  - **Formato:** Parquet (Snappy)
  - **Custo:** Alto
  - **Uso:** Dashboards e análises em tempo real.

- **Warm Storage (31-180 dias):**
  - **Mídia:** HDD
  - **Formato:** Parquet (GZIP - maior compressão)
  - **Custo:** Médio
  - **Uso:** Relatórios mensais e análises de tendência.

- **Cold Storage (181+ dias):**
  - **Mídia:** Object Storage (AWS S3 Glacier, Azure Archive)
  - **Formato:** Parquet (GZIP)
  - **Custo:** Baixo
  - **Uso:** Conformidade regulatória e auditorias.
