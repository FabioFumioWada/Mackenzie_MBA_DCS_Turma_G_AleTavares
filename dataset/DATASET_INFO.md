# Informações sobre o Dataset - Tema B

## 📊 Visão Geral

Este diretório contém o dataset pré-gerado utilizado no Tema B para análise comparativa de formatos de armazenamento.

## 📁 Arquivo Principal

**Nome:** `tema_b_sensores_iot.csv`

**Descrição:** Dataset de leituras de sensores IoT de uma rede de monitoramento ambiental.

## 📈 Características do Dataset

### Estatísticas

- **Número de Registros:** 1.000.000 (1 milhão)
- **Número de Colunas:** 10
- **Tamanho em Disco (CSV):** ~87 MB
- **Período dos Dados:** 1 ano (2024-01-01 a 2024-12-31)
- **Encoding:** UTF-8
- **Delimitador:** Vírgula (,)
- **Header:** Sim (primeira linha)

### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `sensor_id` | String | Identificador único do sensor | SENSOR_0001 |
| `sensor_type` | String | Tipo de sensor | TEMPERATURE, HUMIDITY, PRESSURE, CO2, LIGHT |
| `location` | String | Localização física do sensor | Building_A, Building_B, Building_C, Building_D, Building_E |
| `city` | String | Cidade onde o sensor está instalado | São Paulo, Rio de Janeiro, Belo Horizonte, Brasília, Curitiba |
| `timestamp` | Timestamp | Data e hora da leitura | 2024-06-15 14:30:45 |
| `value` | Double | Valor medido pelo sensor | 23.5, 65.2, 1015.3, etc. |
| `unit` | String | Unidade de medida | Celsius, Percent, hPa, ppm, lux |
| `battery_level` | Integer | Nível de bateria do sensor (%) | 10-100 |
| `signal_strength` | Integer | Força do sinal (dBm) | -90 a -30 |
| `status` | String | Status operacional do sensor | ACTIVE, LOW_BATTERY |

## 🔧 Geração do Dataset

### Metodologia

O dataset foi gerado usando um script Python com as seguintes características:

1. **Seed Fixo:** 42 (para reprodutibilidade)
2. **Distribuição Uniforme:** Todos os tipos de sensores, localizações e cidades têm probabilidade igual
3. **Timestamps Aleatórios:** Distribuídos uniformemente ao longo de 2024
4. **Valores Realistas:** Baseados em faixas típicas para cada tipo de sensor

### Distribuição por Tipo de Sensor

| Tipo | Faixa de Valores | Unidade | Distribuição |
|------|------------------|---------|--------------|
| TEMPERATURE | 15.0 - 35.0 | Celsius | ~20% dos registros |
| HUMIDITY | 30.0 - 90.0 | Percent | ~20% dos registros |
| PRESSURE | 980.0 - 1030.0 | hPa | ~20% dos registros |
| CO2 | 400.0 - 1000.0 | ppm | ~20% dos registros |
| LIGHT | 0.0 - 1000.0 | lux | ~20% dos registros |

### Distribuição por Localização

| Localização | Descrição | Distribuição |
|-------------|-----------|--------------|
| Building_A | Prédio A | ~20% dos registros |
| Building_B | Prédio B | ~20% dos registros |
| Building_C | Prédio C | ~20% dos registros |
| Building_D | Prédio D | ~20% dos registros |
| Building_E | Prédio E | ~20% dos registros |

### Distribuição por Cidade

| Cidade | Distribuição |
|--------|--------------|
| São Paulo | ~20% dos registros |
| Rio de Janeiro | ~20% dos registros |
| Belo Horizonte | ~20% dos registros |
| Brasília | ~20% dos registros |
| Curitiba | ~20% dos registros |

## 📝 Exemplo de Registros

```csv
sensor_id,sensor_type,location,city,timestamp,value,unit,battery_level,signal_strength,status
SENSOR_0001,TEMPERATURE,Building_A,Brasília,2024-11-26 01:29:22,32.72,Celsius,100,-53,ACTIVE
SENSOR_0002,HUMIDITY,Building_A,Brasília,2024-07-04 22:15:49,32.31,Percent,72,-60,ACTIVE
SENSOR_0003,HUMIDITY,Building_E,Brasília,2024-05-25 06:30:41,41.49,Percent,37,-39,ACTIVE
SENSOR_0004,PRESSURE,Building_D,Belo Horizonte,2024-06-24 05:32:17,989.76,hPa,29,-53,ACTIVE
SENSOR_0005,LIGHT,Building_B,Curitiba,2024-08-13 19:45:33,856.42,lux,95,-68,ACTIVE
```

## 🎯 Uso no Projeto

### Propósito

Este dataset é utilizado para:

1. **Comparação de Formatos:** Converter para CSV, JSON, Parquet e ORC
2. **Análise de Tamanho:** Medir espaço em disco de cada formato
3. **Análise de Performance:** Medir tempo de leitura e queries
4. **Demonstração de Otimizações:** Predicate Pushdown, Projection Pushdown

### Fluxo de Processamento

```
tema_b_sensores_iot.csv (87 MB)
    │
    ├─> Conversão para JSON (~120 MB)
    ├─> Conversão para Parquet (~25 MB, Snappy)
    └─> Conversão para ORC (~22 MB, Snappy)
```

## 🔄 Regeneração do Dataset

Se você precisar regenerar o dataset com as mesmas características:

```python
import csv
import random
from datetime import datetime, timedelta

# Configurar seed para reprodutibilidade
SEED = 42
random.seed(SEED)

# Parâmetros
NUM_RECORDS = 1_000_000
START_DATE = datetime(2024, 1, 1)

# Listas de valores
sensor_types = ["TEMPERATURE", "HUMIDITY", "PRESSURE", "CO2", "LIGHT"]
locations = ["Building_A", "Building_B", "Building_C", "Building_D", "Building_E"]
cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Curitiba"]

# Gerar dataset
with open("tema_b_sensores_iot.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Header
    writer.writerow([
        "sensor_id", "sensor_type", "location", "city", "timestamp",
        "value", "unit", "battery_level", "signal_strength", "status"
    ])
    
    # Registros
    for i in range(1, NUM_RECORDS + 1):
        sensor_id = f"SENSOR_{i % 1000:04d}"
        sensor_type = random.choice(sensor_types)
        location = random.choice(locations)
        city = random.choice(cities)
        
        # Timestamp aleatório
        seconds_offset = random.randint(0, 365 * 24 * 60 * 60)
        timestamp = (START_DATE + timedelta(seconds=seconds_offset)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Valor baseado no tipo de sensor
        if sensor_type == "TEMPERATURE":
            value = round(random.uniform(15.0, 35.0), 2)
            unit = "Celsius"
        elif sensor_type == "HUMIDITY":
            value = round(random.uniform(30.0, 90.0), 2)
            unit = "Percent"
        elif sensor_type == "PRESSURE":
            value = round(random.uniform(980.0, 1030.0), 2)
            unit = "hPa"
        elif sensor_type == "CO2":
            value = round(random.uniform(400.0, 1000.0), 2)
            unit = "ppm"
        else:  # LIGHT
            value = round(random.uniform(0.0, 1000.0), 2)
            unit = "lux"
        
        battery_level = random.randint(10, 100)
        signal_strength = random.randint(-90, -30)
        status = "ACTIVE" if battery_level > 20 else "LOW_BATTERY"
        
        writer.writerow([
            sensor_id, sensor_type, location, city, timestamp,
            value, unit, battery_level, signal_strength, status
        ])
```

## 📊 Estatísticas Detalhadas

### Distribuição de Status

- **ACTIVE:** ~80% dos registros (battery_level > 20)
- **LOW_BATTERY:** ~20% dos registros (battery_level ≤ 20)

### Número de Sensores Únicos

- **Total de IDs únicos:** 1.000 (SENSOR_0000 a SENSOR_0999)
- **Leituras por sensor:** ~1.000 em média

### Intervalo de Timestamps

- **Início:** 2024-01-01 00:00:00
- **Fim:** 2024-12-31 23:59:59
- **Distribuição:** Uniforme ao longo do ano

## ⚠️ Observações Importantes

1. **Dados Sintéticos:** Este dataset foi gerado artificialmente para fins educacionais
2. **Não Usar em Produção:** Os dados não refletem leituras reais de sensores
3. **Reprodutibilidade:** O seed fixo garante que o mesmo dataset seja gerado sempre
4. **Tamanho:** O arquivo CSV tem ~87 MB, adequado para demonstrações

## 📚 Referências

- Script de geração: `/home/ubuntu/gerar_datasets.py`
- Documentação do projeto: `../README.md`
- Resultados esperados: `../RESULTADOS_ESPERADOS.md`

---

**Última Atualização:** Novembro 2025  
**Versão do Dataset:** 1.0
