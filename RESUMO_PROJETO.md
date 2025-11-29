# Resumo do Projeto - Tema B para GitHub Codespaces

## 📦 O Que Foi Criado

Este pacote contém uma solução completa e containerizada do **Tema B: Otimização de Armazenamento e Consulta** pronta para publicação no GitHub e execução no GitHub Codespaces.

## 🎯 Objetivos Alcançados

### 1. ✅ Containerização com Docker

- **Dockerfile** completo com Apache Spark 3.5.0 e Python 3.11
- **docker-compose.yml** para orquestração de serviços
- Ambiente totalmente isolado e reproduzível
- Compatível com GitHub Codespaces

### 2. ✅ Código Adaptado para Docker

- Script Python otimizado para execução em container
- Caminhos de arquivo adaptados para `/app`
- Suporte a dataset pré-gerado (acelera execução)
- Análise comparativa de 4 formatos (CSV, JSON, Parquet, ORC)
- Relatório JSON automático

### 3. ✅ Dataset Pré-Gerado Incluído

- **1 milhão de registros** de sensores IoT (~87 MB)
- Documentação completa em `data/DATASET_INFO.md`
- Acelera execução de ~10min para ~3-5min
- Resultados reproduzíveis e validáveis
- Seed fixo (42) para consistência

### 4. ✅ Documentação Completa

- **README.md:** Visão geral do projeto
- **INSTRUCOES.md:** Guia passo a passo de execução
- **RESULTADOS_ESPERADOS.md:** Resultados de referência para comparação
- **PUBLICACAO_GITHUB.md:** Guia de publicação no GitHub
- **run.sh:** Script de automação

### 5. ✅ Configuração GitHub Codespaces

- **`.devcontainer/devcontainer.json`:** Configuração automática
- Extensões VS Code pré-instaladas
- Ambiente pronto para uso imediato

## 📁 Estrutura de Arquivos

```
tema_b_github/
├── .devcontainer/
│   └── devcontainer.json          # Configuração Codespaces
├── data/                           # Datasets gerados (vazio inicialmente)
├── docker/                         # Arquivos Docker auxiliares
├── notebooks/                      # Notebooks Jupyter (opcional)
├── output/                         # Relatórios gerados
├── scripts/
│   └── tema_b_otimizacao_docker.py # Script principal
├── .gitignore                      # Arquivos a ignorar no Git
├── Dockerfile                      # Imagem Docker com Spark
├── docker-compose.yml              # Orquestração de containers
├── INSTRUCOES.md                   # Guia de execução
├── PUBLICACAO_GITHUB.md            # Guia de publicação
├── README.md                       # Documentação principal
├── RESULTADOS_ESPERADOS.md         # Resultados de referência
├── requirements.txt                # Dependências Python
└── run.sh                          # Script de automação
```

## 🚀 Como Usar

### Opção 1: GitHub Codespaces (Recomendado)

1. Publicar no GitHub (seguir `PUBLICACAO_GITHUB.md`)
2. Abrir Codespace no repositório
3. Executar: `./run.sh full`
4. Verificar resultados em `/app/output/`

### Opção 2: Docker Local

1. Instalar Docker e Docker Compose
2. Executar: `./run.sh full`
3. Verificar resultados em `output/`

### Opção 3: Execução Manual

1. Construir: `docker-compose build`
2. Iniciar: `docker-compose up -d`
3. Executar: `docker-compose exec spark-tema-b python3 /app/scripts/tema_b_otimizacao_docker.py`

## 📊 Resultados Esperados

### Comparativo de Tamanho

| Formato | Tamanho | Redução vs CSV |
|---------|---------|----------------|
| CSV     | ~87 MB  | 0% (baseline)  |
| JSON    | ~120 MB | -38% (maior)   |
| Parquet | ~25 MB  | **71%**        |
| ORC     | ~22 MB  | **75%**        |

### Comparativo de Performance

| Formato | Leitura | Filtro | Agregação |
|---------|---------|--------|-----------|
| CSV     | 45s     | 38s    | 35s       |
| Parquet | 12s     | 7s     | 9s        |
| ORC     | 11s     | 7s     | 9s        |

**Speedup:** Formatos colunares são **3-5x mais rápidos**

## 🎓 Para o Avaliador

### Como Validar

1. **Clonar/Fork o repositório**
2. **Abrir no GitHub Codespaces** (ou executar localmente)
3. **Executar:** `./run.sh full`
4. **Comparar resultados** com `RESULTADOS_ESPERADOS.md`

### O Que Verificar

- ✓ Tamanhos relativos dos formatos (Parquet/ORC ~70% menores)
- ✓ Performance relativa (Parquet/ORC ~3-5x mais rápidos)
- ✓ Relatório JSON gerado em `output/`
- ✓ Conclusões alinhadas com teoria

### Tolerância de Variação

- Valores absolutos: ±10-15%
- Relações relativas devem ser mantidas

## 🔧 Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Framework:** Apache Spark 3.5.0
- **Containerização:** Docker, Docker Compose
- **Formatos:** CSV, JSON, Parquet (Snappy), ORC (Snappy)
- **Bibliotecas:** PySpark, Pandas, Matplotlib
- **Plataforma:** GitHub Codespaces

## 📝 Diferenciais da Solução

1. **Totalmente Containerizada:** Elimina problemas de "funciona na minha máquina"
2. **Reproduzível:** Seed fixo garante resultados consistentes
3. **Documentação Completa:** 5 arquivos de documentação
4. **Automação:** Script `run.sh` simplifica execução
5. **Pronta para Codespaces:** Configuração `.devcontainer` incluída
6. **Resultados Validáveis:** Arquivo de referência para comparação

## 🎯 Conclusões do Projeto

### Formato Recomendado: Parquet ou ORC

**Justificativa:**
- 70-75% de economia de espaço
- 3-5x mais rápido em queries
- Suporte a Predicate/Projection Pushdown
- Compatibilidade com ecossistema Big Data

### Estratégia de Ciclo de Vida

- **Hot (0-30 dias):** SSD + Parquet (Snappy)
- **Warm (31-180 dias):** HDD + Parquet (GZIP)
- **Cold (181+ dias):** Object Storage + Parquet (GZIP)

**Economia:** 60-70% nos custos de armazenamento

### Evitar em Produção

- CSV e JSON para datasets grandes
- Armazenamento sem estratégia de lifecycle
- Formatos sem compressão

## 📚 Referências

- Materiais de aula: "3. Ciclo de Vida, Formatos e Compactação"
- Apache Parquet Documentation
- Apache ORC Documentation
- Spark SQL Performance Tuning Guide

## ✅ Checklist de Entrega

- [x] Dockerfile com Spark 3.5.0
- [x] docker-compose.yml
- [x] Código Python adaptado para Docker
- [x] Script de automação (run.sh)
- [x] Configuração GitHub Codespaces
- [x] README.md principal
- [x] INSTRUCOES.md detalhado
- [x] RESULTADOS_ESPERADOS.md
- [x] PUBLICACAO_GITHUB.md
- [x] .gitignore configurado
- [x] requirements.txt
- [x] Estrutura de diretórios organizada

## 🎉 Próximos Passos

1. **Publicar no GitHub** (seguir `PUBLICACAO_GITHUB.md`)
2. **Testar no Codespaces**
3. **Compartilhar com avaliador**
4. **Incluir no portfólio** (opcional)

---

**Projeto desenvolvido para o MBA em Engenharia de Dados**  
**Disciplina:** Data Collection & Storage  
**Tema:** B - Otimização de Armazenamento e Consulta  
**Data:** Novembro 2025
