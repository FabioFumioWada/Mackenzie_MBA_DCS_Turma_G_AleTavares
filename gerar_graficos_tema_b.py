#!/usr/bin/env python3
"""
Script para Gerar Gráficos Comparativos - Tema B
Lê o relatório JSON e gera gráficos de comparação de formatos
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Configurar estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Diretórios
BASE_DIR = Path("/workspace") if Path("/workspace").exists() else Path("/app")
OUTPUT_DIR = BASE_DIR / "output"
RELATORIO_PATH = OUTPUT_DIR / "relatorio_comparativo.json"

def carregar_relatorio():
    """Carrega o relatório JSON gerado pela análise"""
    print(f"📂 Carregando relatório: {RELATORIO_PATH}")
    
    if not RELATORIO_PATH.exists():
        print(f"❌ Erro: Relatório não encontrado em {RELATORIO_PATH}")
        print("   Execute primeiro: ./run.sh full")
        sys.exit(1)
    
    with open(RELATORIO_PATH, 'r') as f:
        return json.load(f)

def gerar_grafico_tamanho(dados):
    """Gera gráfico de comparação de tamanho em disco"""
    print("📊 Gerando gráfico de tamanho em disco...")
    
    formatos = list(dados['comparativo_tamanho'].keys())
    tamanhos_mb = [dados['comparativo_tamanho'][f]['tamanho_mb'] for f in formatos]
    
    # Cores para cada formato
    cores = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(formatos, tamanhos_mb, color=cores, alpha=0.8, edgecolor='black')
    
    # Adicionar valores em cima das barras
    for bar, tamanho in zip(bars, tamanhos_mb):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{tamanho:.1f} MB',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Formato de Arquivo', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tamanho em Disco (MB)', fontsize=12, fontweight='bold')
    ax.set_title('Comparação de Tamanho em Disco por Formato\n1 Milhão de Registros de Sensores IoT', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar
    output_path = OUTPUT_DIR / "grafico_tamanho_disco.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {output_path}")
    plt.close()

def gerar_grafico_performance(dados):
    """Gera gráfico de comparação de performance de leitura"""
    print("📊 Gerando gráfico de performance de leitura...")
    
    formatos = list(dados['comparativo_performance'].keys())
    
    # Extrair tempos de leitura
    tempo_leitura = [dados['comparativo_performance'][f]['tempo_leitura_segundos'] for f in formatos]
    tempo_filtro = [dados['comparativo_performance'][f]['tempo_query_filtro_segundos'] for f in formatos]
    tempo_agregacao = [dados['comparativo_performance'][f]['tempo_query_agregacao_segundos'] for f in formatos]
    
    # Configurar gráfico de barras agrupadas
    x = range(len(formatos))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars1 = ax.bar([i - width for i in x], tempo_leitura, width, 
                   label='Leitura Completa', color='#3498db', alpha=0.8, edgecolor='black')
    bars2 = ax.bar([i for i in x], tempo_filtro, width, 
                   label='Query com Filtro', color='#2ecc71', alpha=0.8, edgecolor='black')
    bars3 = ax.bar([i + width for i in x], tempo_agregacao, width, 
                   label='Query com Agregação', color='#f39c12', alpha=0.8, edgecolor='black')
    
    # Adicionar valores em cima das barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}s',
                    ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Formato de Arquivo', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tempo de Execução (segundos)', fontsize=12, fontweight='bold')
    ax.set_title('Comparação de Performance de Leitura e Queries\n1 Milhão de Registros de Sensores IoT', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(formatos)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar
    output_path = OUTPUT_DIR / "grafico_performance_leitura.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {output_path}")
    plt.close()

def gerar_grafico_reducao(dados):
    """Gera gráfico de redução percentual em relação ao CSV"""
    print("📊 Gerando gráfico de redução de tamanho...")
    
    formatos = list(dados['comparativo_tamanho'].keys())
    reducoes = [dados['comparativo_tamanho'][f]['reducao_percentual'] for f in formatos]
    
    # Cores: vermelho para aumento, verde para redução
    cores = ['#e74c3c' if r < 0 else '#2ecc71' for r in reducoes]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(formatos, reducoes, color=cores, alpha=0.8, edgecolor='black')
    
    # Adicionar valores nas barras
    for bar, reducao in zip(bars, reducoes):
        width = bar.get_width()
        label_x = width + (2 if width > 0 else -2)
        ax.text(label_x, bar.get_y() + bar.get_height()/2.,
                f'{reducao:+.1f}%',
                ha='left' if width > 0 else 'right', 
                va='center', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Redução de Tamanho vs CSV (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Formato de Arquivo', fontsize=12, fontweight='bold')
    ax.set_title('Redução de Tamanho em Relação ao CSV\nValores Positivos = Economia de Espaço', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar
    output_path = OUTPUT_DIR / "grafico_reducao_tamanho.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {output_path}")
    plt.close()

def gerar_grafico_speedup(dados):
    """Gera gráfico de speedup em relação ao CSV"""
    print("📊 Gerando gráfico de speedup...")
    
    formatos = list(dados['comparativo_performance'].keys())
    
    # Calcular speedup (quanto mais rápido em relação ao CSV)
    tempo_csv = dados['comparativo_performance']['CSV']['tempo_leitura_segundos']
    speedups = [tempo_csv / dados['comparativo_performance'][f]['tempo_leitura_segundos'] 
                for f in formatos]
    
    # Cores
    cores = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(formatos, speedups, color=cores, alpha=0.8, edgecolor='black')
    
    # Adicionar valores em cima das barras
    for bar, speedup in zip(bars, speedups):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{speedup:.2f}x',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Baseline (CSV)')
    ax.set_xlabel('Formato de Arquivo', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speedup (vezes mais rápido que CSV)', fontsize=12, fontweight='bold')
    ax.set_title('Speedup de Leitura em Relação ao CSV\nValores > 1 = Mais Rápido que CSV', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar
    output_path = OUTPUT_DIR / "grafico_speedup.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {output_path}")
    plt.close()

def main():
    """Função principal"""
    print("=" * 80)
    print("GERAÇÃO DE GRÁFICOS COMPARATIVOS - TEMA B")
    print("=" * 80)
    print()
    
    # Carregar dados
    dados = carregar_relatorio()
    print(f"✅ Relatório carregado com sucesso!")
    print(f"   Data da análise: {dados['metadata']['data_execucao']}")
    print(f"   Total de registros: {dados['metadata']['total_registros']:,}")
    print()
    
    # Criar diretório de saída se não existir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Gerar gráficos
    print("Gerando gráficos...")
    print()
    
    gerar_grafico_tamanho(dados)
    gerar_grafico_performance(dados)
    gerar_grafico_reducao(dados)
    gerar_grafico_speedup(dados)
    
    print()
    print("=" * 80)
    print("✅ TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
    print("=" * 80)
    print()
    print(f"📁 Localização: {OUTPUT_DIR}")
    print()
    print("Arquivos gerados:")
    print("  1. grafico_tamanho_disco.png")
    print("  2. grafico_performance_leitura.png")
    print("  3. grafico_reducao_tamanho.png")
    print("  4. grafico_speedup.png")
    print()
    print("💡 Dica: Você pode baixar os gráficos clicando com o botão direito")
    print("         nos arquivos no explorador do VS Code e selecionando 'Download'")
    print()

if __name__ == "__main__":
    main()
