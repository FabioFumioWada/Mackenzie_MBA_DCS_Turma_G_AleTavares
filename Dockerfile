# Dockerfile para Tema B - Otimização de Armazenamento com PySpark
# Base: Python 3.11 com Java 17 (compatível com Spark 3.5.0)

FROM python:3.11-slim

# Metadados
LABEL maintainer="MBA Engenharia de Dados"
LABEL description="Ambiente PySpark para análise de formatos de armazenamento"
LABEL version="2.0"

# Variáveis de ambiente
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYTHONUNBUFFERED=1
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Instalar dependências do sistema
# Nota: Java 17 é usado porque Java 11 não está disponível no Debian Trixie
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    wget \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Baixar e instalar Apache Spark 3.5.0
RUN wget -q https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz \
    && tar -xzf spark-3.5.0-bin-hadoop3.tgz \
    && mv spark-3.5.0-bin-hadoop3 /opt/spark \
    && rm spark-3.5.0-bin-hadoop3.tgz

# Instalar bibliotecas Python
RUN pip install --no-cache-dir \
    pyspark==3.5.0 \
    pandas==2.1.3 \
    numpy==1.26.2 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    jupyter==1.0.0 \
    notebook==7.0.6

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Criar diretórios necessários
RUN mkdir -p /app/data /app/output /app/scripts /app/notebooks

# Expor portas
EXPOSE 8888 4040 8080

# Comando padrão
CMD ["/bin/bash"]
