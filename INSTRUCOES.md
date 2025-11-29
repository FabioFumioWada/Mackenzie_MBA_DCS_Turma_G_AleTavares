# Instruções Detalhadas - Tema B no GitHub Codespaces

Este documento fornece instruções passo a passo para executar o Tema B no GitHub Codespaces e comparar os resultados com os apresentados no relatório.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração Inicial](#configuração-inicial)
3. [Execução no GitHub Codespaces](#execução-no-github-codespaces)
4. [Execução Local com Docker](#execução-local-com-docker)
5. [Interpretação dos Resultados](#interpretação-dos-resultados)
6. [Comparação com Resultados Apresentados](#comparação-com-resultados-apresentados)
7. [Troubleshooting](#troubleshooting)

---

## 1. Pré-requisitos

### Para GitHub Codespaces:
- Conta no GitHub
- Acesso ao GitHub Codespaces (incluído em contas gratuitas com limite mensal)

### Para Execução Local:
- Docker Desktop instalado (Windows/Mac) ou Docker Engine (Linux)
- Docker Compose instalado
- Mínimo de 8GB de RAM disponível
- 10GB de espaço em disco livre

---

## 2. Configuração Inicial

### 2.1. Fork ou Clone do Repositório

**Opção A: Fork (Recomendado)**
1. Acesse o repositório no GitHub
2. Clique no botão **"Fork"** no canto superior direito
3. Aguarde a criação do fork na sua conta

**Opção B: Clone Local**
```bash
git clone https://github.com/SEU_USUARIO/tema-b-otimizacao.git
cd tema-b-otimizacao
```

---

## 3. Execução no GitHub Codespaces

### 3.1. Criar Codespace

1. No repositório (fork ou original), clique no botão verde **"Code"**
2. Selecione a aba **"Codespaces"**
3. Clique em **"Create codespace on main"**
4. Aguarde a criação do ambiente (pode levar 2-5 minutos)

### 3.2. Verificar Ambiente

Após a criação do Codespace, você verá um VS Code no navegador. Verifique se o ambiente está pronto:

```bash
# Verificar versão do Python
python3 --version
# Esperado: Python 3.11.x

# Verificar versão do Java
java -version
# Esperado: OpenJDK 11.x

# Verificar instalação do Spark
ls -la /opt/spark
# Esperado: Diretório com arquivos do Spark 3.5.0
```

### 3.3. Dataset Pré-Gerado

Este projeto inclui um dataset pré-gerado de 1 milhão de registros em `data/tema_b_sensores_iot.csv`.

**Vantagens:**
- Execução mais rápida (~3-5 minutos vs ~10 minutos)
- Resultados consistentes e reproduzíveis
- Facilita validação pelo avaliador

**Detalhes do Dataset:**
- Veja `data/DATASET_INFO.md` para documentação completa
- 1.000.000 registros de sensores IoT
- 10 colunas (sensor_id, sensor_type, location, city, timestamp, value, unit, battery_level, signal_strength, status)
- Tamanho: ~87 MB

### 3.3. Executar a Análise

**Método 1: Script Automatizado (Recomendado)**

```bash
# Dar permissão de execução ao script
chmod +x run.sh

# Executar pipeline completo
./run.sh full
```

**Método 2: Execução Manual**

```bash
# Construir imagem Docker
docker-compose build

# Iniciar container
docker-compose up -d

# Aguardar 5 segundos para Spark inicializar
sleep 5

# Executar análise
docker-compose exec spark-tema-b python3 /app/scripts/tema_b_otimizacao_docker.py
```

### 3.4. Acompanhar Execução

A execução completa leva aproximadamente **5-10 minutos** dependendo dos recursos do Codespace.

Você verá no console:
1. ✓ Iniciando Spark Session
2. ✓ Gerando dataset (1.000.000 registros)
3. ✓ Salvando em CSV, JSON, Parquet, ORC
4. ✓ Analisando performance de cada formato
5. ✓ Gerando relatório comparativo

### 3.5. Verificar Resultados

```bash
# Listar arquivos gerados
ls -lh /app/data/
ls -lh /app/output/

# Visualizar relatório JSON
cat /app/output/relatorio_comparativo.json

# Visualizar tamanhos dos arquivos
du -sh /app/data/*
```

---

## 4. Execução Local com Docker

### 4.1. Preparar Ambiente

```bash
# Navegar até o diretório do projeto
cd tema-b-otimizacao

# Verificar se Docker está rodando
docker --version
docker-compose --version
```

### 4.2. Executar Pipeline

**Opção A: Script Automatizado**

```bash
./run.sh full
```

**Opção B: Comandos Manuais**

```bash
# 1. Construir imagem
docker-compose build

# 2. Iniciar container
docker-compose up -d

# 3. Executar análise
docker-compose exec spark-tema-b python3 /app/scripts/tema_b_otimizacao_docker.py

# 4. Verificar resultados
docker-compose exec spark-tema-b ls -lh /app/data/
docker-compose exec spark-tema-b cat /app/output/relatorio_comparativo.json

# 5. Parar container
docker-compose down
```

### 4.3. Acessar Shell do Container (Opcional)

```bash
# Abrir shell interativo
./run.sh shell

# Ou manualmente:
docker-compose exec spark-tema-b /bin/bash

# Dentro do container, você pode:
# - Explorar os dados gerados
# - Executar queries personalizadas
# - Verificar logs do Spark
```

---

## 5. Interpretação dos Resultados

### 5.1. Estrutura do Relatório

O arquivo `output/relatorio_comparativo.json` contém:

```json
{
  "CSV": {
    "read_time": 45.2,
    "filter_time": 38.1,
    "select_time": 12.3,
    "agg_time": 35.4,
    "size_mb": 87.5
  },
  "JSON": { ... },
  "Parquet": { ... },
  "ORC": { ... }
}
```

### 5.2. Métricas Importantes

- **size_mb:** Tamanho total em disco (MB)
- **read_time:** Tempo de leitura completa (segundos)
- **filter_time:** Tempo de query com filtro WHERE (segundos)
- **select_time:** Tempo de seleção de colunas (segundos)
- **agg_time:** Tempo de agregação GROUP BY (segundos)

### 5.3. Console Output

O console exibirá tabelas comparativas:

```
TAMANHO EM DISCO:
--------------------------------------------------------------------------------
Formato         Tamanho (MB)    Redução vs CSV
--------------------------------------------------------------------------------
CSV             87.50                    0.0%
JSON            120.30                  -37.5%
Parquet         25.20                   71.2%
ORC             22.10                   74.7%

PERFORMANCE DE LEITURA:
--------------------------------------------------------------------------------
Formato         Leitura (s)     Filtro (s)      Agregação (s)
--------------------------------------------------------------------------------
CSV             45.20           38.10           35.40
JSON            52.30           42.50           39.80
Parquet         12.10           7.20            9.10
ORC             11.30           6.80            8.50
```

---

## 6. Comparação com Resultados Apresentados

### 6.1. Resultados Esperados (Relatório Original)

| Formato | Tamanho (MB) | Redução | Leitura (s) | Filtro (s) |
|---------|--------------|---------|-------------|------------|
| CSV     | ~87          | 0%      | ~45         | ~38        |
| JSON    | ~120         | -38%    | ~52         | ~42        |
| Parquet | ~25          | 71%     | ~12         | ~7         |
| ORC     | ~22          | 75%     | ~11         | ~7         |

### 6.2. Tolerância de Variação

Os resultados podem variar em **±10-15%** devido a:
- Recursos de CPU/RAM do ambiente
- Carga do sistema
- Versão exata do Spark
- Otimizações de JVM

**Exemplo de variação aceitável:**
- CSV: 80-95 MB (esperado: ~87 MB)
- Parquet: 22-28 MB (esperado: ~25 MB)
- Leitura CSV: 40-50s (esperado: ~45s)

### 6.3. Validação dos Resultados

Para validar que a execução foi bem-sucedida, verifique:

1. **Tamanhos Relativos:**
   - Parquet deve ser ~70% menor que CSV
   - ORC deve ser ~75% menor que CSV
   - JSON deve ser ~35% maior que CSV

2. **Performance Relativa:**
   - Parquet/ORC devem ser ~3-4x mais rápidos na leitura
   - Parquet/ORC devem ser ~5-6x mais rápidos em queries com filtro

3. **Conclusões:**
   - Formatos colunares (Parquet/ORC) devem ser superiores em todos os aspectos
   - JSON deve ser o pior em tamanho e performance

---

## 7. Troubleshooting

### 7.1. Erro: "Docker not found"

**Solução:**
- GitHub Codespaces: Docker já está pré-instalado. Recarregue a página.
- Local: Instale o Docker Desktop ou Docker Engine.

### 7.2. Erro: "Out of memory"

**Solução:**
```bash
# Editar docker-compose.yml e reduzir memória:
deploy:
  resources:
    limits:
      memory: 4G  # Reduzir de 8G para 4G
```

### 7.3. Erro: "Permission denied"

**Solução:**
```bash
# Dar permissão de execução aos scripts
chmod +x run.sh
chmod +x scripts/*.py
```

### 7.4. Execução Muito Lenta

**Solução:**
- Reduzir número de registros no script:
  ```python
  NUM_RECORDS = 100_000  # Ao invés de 1_000_000
  ```

### 7.5. Container não Inicia

**Solução:**
```bash
# Verificar logs
docker-compose logs

# Reconstruir imagem
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 8. Comandos Úteis

```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar tudo
docker-compose down

# Limpar volumes e recomeçar
docker-compose down -v
rm -rf data/* output/*

# Verificar uso de recursos
docker stats

# Listar containers rodando
docker ps

# Abrir Spark UI (se disponível)
# Acesse: http://localhost:8080
```

---

## 9. Próximos Passos

Após executar com sucesso:

1. **Explorar os Dados:**
   - Abra os arquivos gerados em `data/`
   - Compare visualmente os tamanhos

2. **Personalizar a Análise:**
   - Modifique `NUM_RECORDS` para testar com datasets maiores/menores
   - Adicione novos formatos ou compressões

3. **Criar Visualizações:**
   - Use os dados do relatório JSON para criar gráficos
   - Gere apresentações com os resultados

4. **Documentar Aprendizados:**
   - Anote as diferenças observadas
   - Compare com a teoria dos materiais de aula

---

## 10. Suporte

Para dúvidas ou problemas:

1. Verifique a seção de [Troubleshooting](#troubleshooting)
2. Consulte os logs: `docker-compose logs`
3. Revise o código em `scripts/tema_b_otimizacao_docker.py`
4. Abra uma issue no repositório GitHub

---

**Bom trabalho! 🚀**
