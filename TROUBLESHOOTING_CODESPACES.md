# Troubleshooting - GitHub Codespaces

Este documento ajuda a resolver problemas comuns ao usar o projeto no GitHub Codespaces.

## ❌ Erro: "O workspace não existe"

### Causa
Este erro ocorre quando o GitHub Codespaces não consegue encontrar o workspace configurado no `devcontainer.json`.

### Solução ✅

O projeto foi atualizado com uma configuração simplificada que resolve este problema. Siga os passos:

#### 1. Deletar Codespace Existente (se houver)

1. Vá para [github.com/codespaces](https://github.com/codespaces)
2. Encontre o Codespace problemático
3. Clique nos três pontos (...) → **Delete**

#### 2. Criar Novo Codespace

1. Vá para o repositório no GitHub
2. Clique em **Code** → **Codespaces** → **Create codespace on main**
3. Aguarde 2-5 minutos para a criação

#### 3. Verificar Ambiente

Após a criação, execute no terminal:

```bash
# Verificar diretório de trabalho
pwd
# Esperado: /workspace

# Verificar Python
python3 --version
# Esperado: Python 3.11.x

# Verificar Spark
ls -la /opt/spark
# Esperado: Diretório com arquivos do Spark

# Verificar dataset
ls -lh /workspace/data/tema_b_sensores_iot.csv
# Esperado: ~87 MB
```

#### 4. Executar Análise

```bash
./run.sh full
```

---

## 🐛 Outros Problemas Comuns

### Problema: "Permission denied" ao executar run.sh

**Solução:**
```bash
chmod +x run.sh
./run.sh full
```

### Problema: Dataset não encontrado

**Solução:**
```bash
# Verificar se dataset existe
ls -lh /workspace/data/

# Se não existir, o script irá gerar automaticamente
python3 /workspace/scripts/tema_b_otimizacao_docker.py
```

### Problema: Spark não inicia

**Solução:**
```bash
# Verificar se Spark está instalado
echo $SPARK_HOME
# Esperado: /opt/spark

# Verificar Java
java -version
# Esperado: OpenJDK 11

# Reiniciar Codespace
# GitHub → Codespaces → Restart
```

### Problema: Memória insuficiente

**Sintomas:**
- Processo morto (Killed)
- Out of Memory errors

**Solução:**
1. Vá para Settings do Codespace
2. Aumente a máquina para **4-core** ou **8-core**
3. Recrie o Codespace

### Problema: Execução muito lenta

**Causas possíveis:**
- Máquina pequena (2-core)
- Rede lenta
- Muitos processos rodando

**Soluções:**
```bash
# 1. Verificar recursos
free -h
df -h

# 2. Usar máquina maior
# GitHub → Codespaces → Change machine type → 4-core

# 3. Limpar cache
./run.sh clean
```

---

## 📋 Checklist de Verificação

Antes de reportar um problema, verifique:

- [ ] Codespace foi criado com sucesso (sem erros)
- [ ] Python 3.11 está disponível (`python3 --version`)
- [ ] Spark está instalado (`ls /opt/spark`)
- [ ] Dataset existe (`ls /workspace/data/tema_b_sensores_iot.csv`)
- [ ] Diretório de trabalho é `/workspace` (`pwd`)
- [ ] Script tem permissão de execução (`ls -l run.sh`)

---

## 🔄 Resetar Ambiente Completamente

Se nada funcionar, resete tudo:

```bash
# 1. Limpar dados gerados
./run.sh clean

# 2. Deletar Codespace
# GitHub → Codespaces → Delete

# 3. Criar novo Codespace
# GitHub → Code → Codespaces → Create codespace on main

# 4. Testar novamente
./run.sh full
```

---

## 📊 Logs e Debugging

### Ver logs detalhados

```bash
# Executar com verbose
python3 -u /workspace/scripts/tema_b_otimizacao_docker.py 2>&1 | tee execution.log
```

### Verificar variáveis de ambiente

```bash
env | grep -E "(SPARK|PYTHON|PATH)"
```

### Testar Spark manualmente

```bash
# Abrir PySpark shell
pyspark

# No shell Python:
>>> spark.version
>>> spark.sparkContext.getConf().getAll()
>>> exit()
```

---

## 🆘 Suporte

Se o problema persistir:

1. **Verifique a documentação:**
   - `README.md`
   - `INSTRUCOES.md`

2. **Revise os requisitos:**
   - Conta GitHub ativa
   - Codespaces habilitado
   - Repositório público (para uso gratuito)

3. **Informações úteis para reportar:**
   - Output de `python3 --version`
   - Output de `ls -la /workspace`
   - Mensagem de erro completa
   - Screenshots do problema

---

## ✅ Configuração Correta

Quando tudo estiver funcionando, você verá:

```bash
$ ./run.sh full

⚡ Ambiente: GitHub Codespaces
[INFO] Executando pipeline completo...
[INFO] Executando análise de formatos...
================================================================================
TEMA B - OTIMIZAÇÃO DE ARMAZENAMENTO E CONSULTA v2.0
================================================================================
Diretório base: /workspace
Diretório de dados: /workspace/data
Diretório de saída: /workspace/output
Dataset pré-gerado: Sim

Iniciando Spark Session...
✓ Spark 3.5.0 iniciado com sucesso
✓ Adaptive Query Execution: Habilitado

================================================================================
ETAPA 1: OBTENÇÃO DO DATASET
================================================================================
Dataset pré-gerado encontrado: /workspace/data/tema_b_sensores_iot.csv
Carregando dataset...
✓ Dataset carregado: 1,000,000 registros
✓ Tempo de carregamento: 10.5s
...
```

---

**Última atualização:** Novembro 2025  
**Versão:** 2.0
