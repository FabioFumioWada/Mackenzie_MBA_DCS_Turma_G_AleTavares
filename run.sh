#!/bin/bash
################################################################################
# Script de Execução Rápida - Tema B
################################################################################
#
# Este script facilita a execução do projeto em diferentes ambientes.
# Compatível com GitHub Codespaces e Docker local.
#
# Uso:
#   ./run.sh [opção]
#
################################################################################

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detectar ambiente
if [ -d "/workspace" ]; then
    ENVIRONMENT="codespaces"
    WORKSPACE_DIR="/workspace"
    echo -e "${BLUE}⚡ Ambiente: GitHub Codespaces${NC}"
else
    ENVIRONMENT="docker"
    WORKSPACE_DIR="/app"
    echo -e "${BLUE}🐳 Ambiente: Docker local${NC}"
fi

# Funções auxiliares
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está instalado (apenas para ambiente local)
check_docker() {
    if [ "$ENVIRONMENT" = "docker" ]; then
        if ! command -v docker &> /dev/null; then
            print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
            exit 1
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
            exit 1
        fi
    fi
}

# Construir imagem Docker (apenas para ambiente local)
build() {
    if [ "$ENVIRONMENT" = "codespaces" ]; then
        print_warn "Build não necessário no Codespaces (já está pronto)"
        return 0
    fi
    
    print_info "Construindo imagem Docker..."
    docker-compose build
    print_info "Imagem construída com sucesso!"
}

# Iniciar container (apenas para ambiente local)
start() {
    if [ "$ENVIRONMENT" = "codespaces" ]; then
        print_warn "Start não necessário no Codespaces (já está rodando)"
        return 0
    fi
    
    print_info "Iniciando container..."
    docker-compose up -d
    print_info "Container iniciado com sucesso!"
    print_info "Aguardando 5 segundos para o Spark inicializar..."
    sleep 5
}

# Executar análise principal
exec_analysis() {
    print_info "Executando análise de formatos..."
    
    if [ "$ENVIRONMENT" = "codespaces" ]; then
        # No Codespaces, executar diretamente
        python3 ${WORKSPACE_DIR}/scripts/tema_b_otimizacao_docker.py
    else
        # No Docker local, executar via docker-compose
        docker-compose exec spark-tema-b python3 /app/scripts/tema_b_otimizacao_docker.py
    fi
}

# Parar container (apenas para ambiente local)
stop() {
    if [ "$ENVIRONMENT" = "codespaces" ]; then
        print_warn "Stop não aplicável no Codespaces"
        return 0
    fi
    
    print_info "Parando container..."
    docker-compose down
    print_info "Container parado com sucesso!"
}

# Limpar tudo
clean() {
    print_warn "Isso irá remover dados gerados. Continuar? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Limpando ambiente..."
        
        if [ "$ENVIRONMENT" = "docker" ]; then
            docker-compose down -v
            docker rmi tema_b_github_spark-tema-b 2>/dev/null || true
        fi
        
        # Limpar dados gerados (manter dataset original)
        rm -rf ${WORKSPACE_DIR}/data/csv ${WORKSPACE_DIR}/data/json ${WORKSPACE_DIR}/data/parquet ${WORKSPACE_DIR}/data/orc 2>/dev/null || true
        rm -f ${WORKSPACE_DIR}/output/* 2>/dev/null || true
        
        print_info "Ambiente limpo!"
    else
        print_info "Operação cancelada."
    fi
}

# Exibir logs (apenas para ambiente local)
logs() {
    if [ "$ENVIRONMENT" = "codespaces" ]; then
        print_warn "Logs não aplicável no Codespaces (use o terminal)"
        return 0
    fi
    
    docker-compose logs -f spark-tema-b
}

# Abrir shell no container (apenas para ambiente local)
shell() {
    if [ "$ENVIRONMENT" = "codespaces" ]; then
        print_warn "Você já está em um shell no Codespaces!"
        return 0
    fi
    
    print_info "Abrindo shell no container..."
    docker-compose exec spark-tema-b /bin/bash
}

# Executar pipeline completo
full_run() {
    print_info "Executando pipeline completo..."
    
    if [ "$ENVIRONMENT" = "docker" ]; then
        build
        start
    fi
    
    exec_analysis
    
    print_info "Pipeline concluído! Verifique os resultados em ${WORKSPACE_DIR}/output/"
}

# Menu de ajuda
show_help() {
    cat << EOF
Uso: ./run.sh [opção]

Opções:
  exec        Executa a análise principal (recomendado)
  full        Executa pipeline completo
  clean       Remove dados gerados (mantém dataset original)
  help        Exibe esta mensagem de ajuda

${YELLOW}Opções específicas para Docker local:${NC}
  build       Constrói a imagem Docker
  start       Inicia o container
  stop        Para o container
  logs        Exibe logs do container
  shell       Abre shell no container

Exemplos:
  ./run.sh exec           # Executa apenas a análise
  ./run.sh full           # Executa tudo automaticamente
  ./run.sh clean          # Limpa dados gerados

${BLUE}Ambiente detectado: ${ENVIRONMENT}${NC}

EOF
}

# Main
main() {
    check_docker
    
    case "${1:-help}" in
        build)
            build
            ;;
        start)
            start
            ;;
        exec)
            exec_analysis
            ;;
        stop)
            stop
            ;;
        clean)
            clean
            ;;
        logs)
            logs
            ;;
        shell)
            shell
            ;;
        full)
            full_run
            ;;
        help|*)
            show_help
            ;;
    esac
}

main "$@"
