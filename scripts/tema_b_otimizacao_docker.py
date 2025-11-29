#!/usr/bin/env python3
"""
================================================================================
PROJETO FINAL - TEMA B: OTIMIZAÇÃO DE ARMAZENAMENTO E CONSULTA
================================================================================

Disciplina: Data Collection & Storage
MBA em Engenharia de Dados

Versão: Docker/GitHub Codespaces
Data: Novembro 2025

Objetivo:
---------
Comparar formatos de arquivo (CSV, JSON, Parquet, ORC) em termos de:
- Tamanho de armazenamento
- Performance de leitura
- Performance de queries analíticas
- Estratégia de ciclo de vida (Hot/Warm/Cold Storage)

Tecnologias:
------------
- Apache Spark 3.5.0
- Python 3.11
- Docker

Arquitetura:
------------
[Dataset] → [CSV/JSON] → [Conversão] → [Parquet/ORC]
                                              ↓
                                    [Análise Performance]
                                              ↓
                                    [Estratégia Lifecycle]

================================================================================
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, rand, expr
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, TimestampType
)

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# Diretórios (adaptados para Docker)
BASE_DIR = Path("/app")
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Criar diretórios se não existirem
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configurações do dataset
DATASET_SIZE_MB = 600  # Tamanho alvo do dataset em MB
NUM_RECORDS = 1_000_000  # Número de registros a gerar

print("=" * 80)
print("TEMA B - OTIMIZAÇÃO DE ARMAZENAMENTO E CONSULTA")
print("=" * 80)
print(f"Diretório base: {BASE_DIR}")
print(f"Diretório de dados: {DATA_DIR}")
print(f"Diretório de saída: {OUTPUT_DIR}")
print()

# ============================================================================
# CONFIGURAÇÃO DO SPARK
# ============================================================================

def criar_spark_session():
    """
    Cria SparkSession otimizada para ambiente Docker.
    """
    print("Iniciando Spark Session...")
    
    spark = SparkSession.builder \
        .appName("Tema B - Otimização Armazenamento (Docker)") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.files.maxPartitionBytes", "128MB") \
        .config("spark.driver.host", "localhost") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    print(f"✓ Spark {spark.version} iniciado com sucesso")
    print(f"✓ Adaptive Query Execution: Habilitado")
    print()
    
    return spark


# ============================================================================
# ETAPA 1: GERAÇÃO DE DATASET
# ============================================================================

def gerar_dataset_iot(spark, num_records=NUM_RECORDS):
    """
    Gera dataset de sensores IoT.
    
    Cenário: Rede de monitoramento ambiental com sensores de temperatura,
    umidade, pressão, CO2 e luminosidade.
    """
    print("=" * 80)
    print("ETAPA 1: GERAÇÃO DE DATASET")
    print("=" * 80)
    print(f"Gerando {num_records:,} registros de sensores IoT...")
    
    start_time = time.time()
    
    # Schema do dataset
    schema = StructType([
        StructField("sensor_id", StringType(), False),
        StructField("sensor_type", StringType(), False),
        StructField("location", StringType(), False),
        StructField("city", StringType(), False),
        StructField("timestamp", TimestampType(), False),
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),
        StructField("battery_level", IntegerType(), False),
        StructField("signal_strength", IntegerType(), False),
        StructField("status", StringType(), False)
    ])
    
    # Gerar dados usando Spark SQL
    df = spark.range(0, num_records) \
        .withColumn("sensor_id", expr("concat('SENSOR_', lpad(cast(id % 1000 as string), 4, '0'))")) \
        .withColumn("sensor_type", 
            expr("case when rand() < 0.2 then 'TEMPERATURE' " +
                 "when rand() < 0.4 then 'HUMIDITY' " +
                 "when rand() < 0.6 then 'PRESSURE' " +
                 "when rand() < 0.8 then 'CO2' " +
                 "else 'LIGHT' end")) \
        .withColumn("location", 
            expr("case when rand() < 0.2 then 'Building_A' " +
                 "when rand() < 0.4 then 'Building_B' " +
                 "when rand() < 0.6 then 'Building_C' " +
                 "when rand() < 0.8 then 'Building_D' " +
                 "else 'Building_E' end")) \
        .withColumn("city", 
            expr("case when rand() < 0.2 then 'São Paulo' " +
                 "when rand() < 0.4 then 'Rio de Janeiro' " +
                 "when rand() < 0.6 then 'Belo Horizonte' " +
                 "when rand() < 0.8 then 'Brasília' " +
                 "else 'Curitiba' end")) \
        .withColumn("timestamp", 
            expr("cast(from_unixtime(unix_timestamp('2024-01-01 00:00:00') + cast(rand() * 31536000 as int)) as timestamp)")) \
        .withColumn("value", 
            when(col("sensor_type") == "TEMPERATURE", expr("15.0 + rand() * 20.0"))
            .when(col("sensor_type") == "HUMIDITY", expr("30.0 + rand() * 60.0"))
            .when(col("sensor_type") == "PRESSURE", expr("980.0 + rand() * 50.0"))
            .when(col("sensor_type") == "CO2", expr("400.0 + rand() * 600.0"))
            .otherwise(expr("rand() * 1000.0"))) \
        .withColumn("unit",
            when(col("sensor_type") == "TEMPERATURE", "Celsius")
            .when(col("sensor_type") == "HUMIDITY", "Percent")
            .when(col("sensor_type") == "PRESSURE", "hPa")
            .when(col("sensor_type") == "CO2", "ppm")
            .otherwise("lux")) \
        .withColumn("battery_level", expr("cast(10 + rand() * 90 as int)")) \
        .withColumn("signal_strength", expr("cast(-90 + rand() * 60 as int)")) \
        .withColumn("status", 
            when(col("battery_level") > 20, "ACTIVE")
            .otherwise("LOW_BATTERY")) \
        .drop("id")
    
    elapsed = time.time() - start_time
    
    print(f"✓ Dataset gerado: {df.count():,} registros")
    print(f"✓ Tempo de geração: {elapsed:.2f}s")
    print(f"✓ Schema: {len(df.columns)} colunas")
    print()
    
    return df


# ============================================================================
# ETAPA 2: PERSISTÊNCIA EM MÚLTIPLOS FORMATOS
# ============================================================================

def salvar_em_formatos(df, base_path):
    """
    Salva o dataset em CSV, JSON, Parquet e ORC.
    """
    print("=" * 80)
    print("ETAPA 2: PERSISTÊNCIA EM MÚLTIPLOS FORMATOS")
    print("=" * 80)
    
    resultados = {}
    
    # 1. CSV
    print("Salvando em CSV...")
    start = time.time()
    csv_path = f"{base_path}/csv"
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(csv_path)
    csv_time = time.time() - start
    csv_size = get_directory_size(csv_path)
    resultados['CSV'] = {'time': csv_time, 'size': csv_size, 'path': csv_path}
    print(f"✓ CSV salvo: {csv_size / (1024**2):.2f} MB em {csv_time:.2f}s")
    
    # 2. JSON
    print("Salvando em JSON...")
    start = time.time()
    json_path = f"{base_path}/json"
    df.coalesce(1).write.mode("overwrite").json(json_path)
    json_time = time.time() - start
    json_size = get_directory_size(json_path)
    resultados['JSON'] = {'time': json_time, 'size': json_size, 'path': json_path}
    print(f"✓ JSON salvo: {json_size / (1024**2):.2f} MB em {json_time:.2f}s")
    
    # 3. Parquet (Snappy)
    print("Salvando em Parquet (Snappy)...")
    start = time.time()
    parquet_path = f"{base_path}/parquet"
    df.write.mode("overwrite").option("compression", "snappy").parquet(parquet_path)
    parquet_time = time.time() - start
    parquet_size = get_directory_size(parquet_path)
    resultados['Parquet'] = {'time': parquet_time, 'size': parquet_size, 'path': parquet_path}
    print(f"✓ Parquet salvo: {parquet_size / (1024**2):.2f} MB em {parquet_time:.2f}s")
    
    # 4. ORC (Snappy)
    print("Salvando em ORC (Snappy)...")
    start = time.time()
    orc_path = f"{base_path}/orc"
    df.write.mode("overwrite").option("compression", "snappy").orc(orc_path)
    orc_time = time.time() - start
    orc_size = get_directory_size(orc_path)
    resultados['ORC'] = {'time': orc_time, 'size': orc_size, 'path': orc_path}
    print(f"✓ ORC salvo: {orc_size / (1024**2):.2f} MB em {orc_time:.2f}s")
    
    print()
    return resultados


def get_directory_size(path):
    """Calcula tamanho total de um diretório em bytes."""
    total = 0
    for entry in Path(path).rglob('*'):
        if entry.is_file():
            total += entry.stat().st_size
    return total


# ============================================================================
# ETAPA 3: ANÁLISE DE PERFORMANCE
# ============================================================================

def analisar_performance(spark, formatos_info):
    """
    Analisa performance de leitura e queries para cada formato.
    """
    print("=" * 80)
    print("ETAPA 3: ANÁLISE DE PERFORMANCE")
    print("=" * 80)
    
    resultados = {}
    
    for formato, info in formatos_info.items():
        print(f"\nAnalisando {formato}...")
        path = info['path']
        
        # Leitura completa
        start = time.time()
        if formato == 'CSV':
            df = spark.read.option("header", "true").csv(path)
        elif formato == 'JSON':
            df = spark.read.json(path)
        elif formato == 'Parquet':
            df = spark.read.parquet(path)
        else:  # ORC
            df = spark.read.orc(path)
        
        count = df.count()
        read_time = time.time() - start
        
        # Query com filtro
        start = time.time()
        filtered = df.filter(col("value") > 500).count()
        filter_time = time.time() - start
        
        # Query com seleção de colunas
        start = time.time()
        selected = df.select("sensor_id", "value", "timestamp").count()
        select_time = time.time() - start
        
        # Query com agregação
        start = time.time()
        agg = df.groupBy("city").count().collect()
        agg_time = time.time() - start
        
        resultados[formato] = {
            'read_time': read_time,
            'filter_time': filter_time,
            'select_time': select_time,
            'agg_time': agg_time,
            'size_mb': info['size'] / (1024**2)
        }
        
        print(f"  Leitura completa: {read_time:.2f}s")
        print(f"  Query com filtro: {filter_time:.2f}s")
        print(f"  Seleção de colunas: {select_time:.2f}s")
        print(f"  Agregação: {agg_time:.2f}s")
    
    print()
    return resultados


# ============================================================================
# ETAPA 4: RELATÓRIO FINAL
# ============================================================================

def gerar_relatorio(resultados_performance):
    """
    Gera relatório comparativo em formato texto e JSON.
    """
    print("=" * 80)
    print("RELATÓRIO FINAL - COMPARATIVO DE FORMATOS")
    print("=" * 80)
    print()
    
    # Tabela comparativa de tamanho
    print("TAMANHO EM DISCO:")
    print("-" * 80)
    print(f"{'Formato':<15} {'Tamanho (MB)':<15} {'Redução vs CSV':<20}")
    print("-" * 80)
    
    csv_size = resultados_performance['CSV']['size_mb']
    for formato in ['CSV', 'JSON', 'Parquet', 'ORC']:
        size = resultados_performance[formato]['size_mb']
        reducao = ((csv_size - size) / csv_size) * 100 if formato != 'CSV' else 0
        print(f"{formato:<15} {size:<15.2f} {reducao:>18.1f}%")
    
    print()
    
    # Tabela comparativa de performance
    print("PERFORMANCE DE LEITURA:")
    print("-" * 80)
    print(f"{'Formato':<15} {'Leitura (s)':<15} {'Filtro (s)':<15} {'Agregação (s)':<15}")
    print("-" * 80)
    
    for formato in ['CSV', 'JSON', 'Parquet', 'ORC']:
        r = resultados_performance[formato]
        print(f"{formato:<15} {r['read_time']:<15.2f} {r['filter_time']:<15.2f} {r['agg_time']:<15.2f}")
    
    print()
    
    # Salvar relatório JSON
    report_path = OUTPUT_DIR / "relatorio_comparativo.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(resultados_performance, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Relatório JSON salvo em: {report_path}")
    print()
    
    # Conclusões
    print("CONCLUSÕES:")
    print("-" * 80)
    
    # Melhor formato por tamanho
    melhor_tamanho = min(resultados_performance.items(), 
                         key=lambda x: x[1]['size_mb'])
    print(f"✓ Menor tamanho: {melhor_tamanho[0]} ({melhor_tamanho[1]['size_mb']:.2f} MB)")
    
    # Melhor formato por performance de leitura
    melhor_leitura = min(resultados_performance.items(),
                         key=lambda x: x[1]['read_time'])
    print(f"✓ Leitura mais rápida: {melhor_leitura[0]} ({melhor_leitura[1]['read_time']:.2f}s)")
    
    # Melhor formato por performance de query
    melhor_query = min(resultados_performance.items(),
                       key=lambda x: x[1]['filter_time'])
    print(f"✓ Query mais rápida: {melhor_query[0]} ({melhor_query[1]['filter_time']:.2f}s)")
    
    print()
    print("RECOMENDAÇÃO:")
    print("-" * 80)
    print("Para Data Lakes modernos, recomenda-se o uso de formatos colunares")
    print("(Parquet ou ORC) devido à:")
    print("  • Redução de 70%+ no espaço de armazenamento")
    print("  • Performance 3-4x superior em queries analíticas")
    print("  • Suporte a Predicate e Projection Pushdown")
    print("  • Compressão eficiente com Snappy ou GZIP")
    print()


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """
    Executa o pipeline completo de análise de formatos.
    """
    inicio_total = time.time()
    
    try:
        # 1. Criar Spark Session
        spark = criar_spark_session()
        
        # 2. Gerar dataset
        df = gerar_dataset_iot(spark, NUM_RECORDS)
        
        # 3. Salvar em múltiplos formatos
        formatos_info = salvar_em_formatos(df, str(DATA_DIR))
        
        # 4. Analisar performance
        resultados = analisar_performance(spark, formatos_info)
        
        # 5. Gerar relatório
        gerar_relatorio(resultados)
        
        # Finalizar
        tempo_total = time.time() - inicio_total
        print("=" * 80)
        print(f"EXECUÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"Tempo total: {tempo_total:.2f}s ({tempo_total/60:.1f} minutos)")
        print("=" * 80)
        
        spark.stop()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
