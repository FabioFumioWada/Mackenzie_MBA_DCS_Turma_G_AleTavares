#!/bin/bash
################################################################################
# Script de Execução Rápida - Tema B
################################################################################
#
# Este script facilita a execução do projeto em diferentes ambientes.
#
# Uso:
#   ./run.sh [opção]
#
# Opções:
#   build   - Constrói a imagem Docker
#   start   - Inicia o container
#   exec    - Executa a análise principal
#   stop    - Para o container
#   clean   - Remove containers e volumes
#   logs    - Exibe logs do container
#   shell   - Abre shell no container
#
################################################################################

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
}

# Construir imagem Docker
build() {
    print_info "Construindo imagem Docker..."
    docker-compose build
    print_info "Imagem construída com sucesso!"
}

# Iniciar container
start() {
    print_info "Iniciando container..."
    docker-compose up -d
    print_info "Container iniciado com sucesso!"
    print_info "Aguardando 5 segundos para o Spark inicializar..."
    sleep 5
}

# Executar análise principal
exec_analysis() {
    print_info "Executando análise de formatos..."
    docker-compose exec spark-tema-b python3 /app/scripts/tema_b_otimizacao_docker.py
}

# Parar container
stop() {
    print_info "Parando container..."
    docker-compose down
    print_info "Container parado com sucesso!"
}

# Limpar tudo
clean() {
    print_warn "Isso irá remover containers, volumes e imagens. Continuar? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Limpando ambiente..."
        docker-compose down -v
        docker rmi tema_b_github_spark-tema-b 2>/dev/null || true
        rm -rf data/* output/* 2>/dev/null || true
        print_info "Ambiente limpo!"
    else
        print_info "Operação cancelada."
    fi
}

# Exibir logs
logs() {
    docker-compose logs -f spark-tema-b
}

# Abrir shell no container
shell() {
    print_info "Abrindo shell no container..."
    docker-compose exec spark-tema-b /bin/bash
}

# Executar pipeline completo
full_run() {
    print_info "Executando pipeline completo..."
    build
    start
    exec_analysis
    print_info "Pipeline concluído! Verifique os resultados em output/"
}

# Menu de ajuda
show_help() {
    cat << EOF
Uso: ./run.sh [opção]

Opções:
  build       Constrói a imagem Docker
  start       Inicia o container
  exec        Executa a análise principal
  stop        Para o container
  clean       Remove containers, volumes e imagens
  logs        Exibe logs do container
  shell       Abre shell no container
  full        Executa pipeline completo (build + start + exec)
  help        Exibe esta mensagem de ajuda

Exemplos:
  ./run.sh build          # Apenas constrói a imagem
  ./run.sh full           # Executa tudo automaticamente
  ./run.sh shell          # Abre shell para exploração manual

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
