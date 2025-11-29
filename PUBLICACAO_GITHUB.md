# Guia de Publicação no GitHub

Este documento fornece instruções passo a passo para publicar o Tema B no GitHub e disponibilizá-lo para execução no GitHub Codespaces.

## 📋 Pré-requisitos

- Conta no GitHub (gratuita)
- Git instalado localmente (opcional, pode usar interface web)
- Projeto completo baixado/descompactado

## 🚀 Método 1: Publicação via Interface Web (Mais Fácil)

### Passo 1: Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha:
   - **Repository name:** `tema-b-otimizacao-armazenamento`
   - **Description:** `Projeto Final - Tema B: Otimização de Armazenamento com PySpark`
   - **Visibility:** Public (para usar Codespaces gratuito)
   - **NÃO** marque "Initialize with README" (já temos um)
5. Clique em **"Create repository"**

### Passo 2: Preparar Arquivos Localmente

1. Descompacte o projeto em uma pasta local
2. Abra um terminal nessa pasta

### Passo 3: Inicializar Git e Fazer Upload

```bash
# Navegar até o diretório do projeto
cd tema_b_github

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "Initial commit: Tema B - Otimização de Armazenamento"

# Adicionar remote (substitua SEU_USUARIO pelo seu username)
git remote add origin https://github.com/SEU_USUARIO/tema-b-otimizacao-armazenamento.git

# Fazer push
git branch -M main
git push -u origin main
```

**Nota:** Você será solicitado a fazer login no GitHub. Use suas credenciais ou um Personal Access Token.

---

## 🔧 Método 2: Upload via GitHub Desktop (Mais Visual)

### Passo 1: Instalar GitHub Desktop

1. Baixe em: [desktop.github.com](https://desktop.github.com)
2. Instale e faça login com sua conta GitHub

### Passo 2: Criar Repositório

1. No GitHub Desktop, clique em **"File" → "New repository"**
2. Preencha:
   - **Name:** `tema-b-otimizacao-armazenamento`
   - **Local path:** Selecione a pasta do projeto
3. Clique em **"Create repository"**

### Passo 3: Publicar

1. Clique em **"Publish repository"**
2. Marque **"Public"** se quiser usar Codespaces gratuito
3. Clique em **"Publish repository"**

---

## 📦 Método 3: Upload via Interface Web (Sem Git)

### Passo 1: Criar Repositório Vazio

1. Siga o Passo 1 do Método 1
2. Após criar, você verá uma página vazia

### Passo 2: Upload de Arquivos

1. Clique em **"uploading an existing file"**
2. Arraste todos os arquivos e pastas do projeto
3. Escreva uma mensagem de commit: `Initial commit`
4. Clique em **"Commit changes"**

**Nota:** Este método pode ter limitações para muitos arquivos. Prefira Método 1 ou 2.

---

## ✅ Verificar Publicação

Após publicar, verifique se os seguintes arquivos estão visíveis no repositório:

- ✓ `README.md`
- ✓ `Dockerfile`
- ✓ `docker-compose.yml`
- ✓ `.devcontainer/devcontainer.json`
- ✓ `scripts/tema_b_otimizacao_docker.py`
- ✓ `INSTRUCOES.md`
- ✓ `RESULTADOS_ESPERADOS.md`

---

## 🌐 Configurar GitHub Codespaces

### Passo 1: Habilitar Codespaces

1. Vá até o repositório no GitHub
2. Clique em **"Settings"** (engrenagem)
3. No menu lateral, clique em **"Codespaces"**
4. Certifique-se de que Codespaces está habilitado

### Passo 2: Testar Codespace

1. Vá para a página principal do repositório
2. Clique no botão verde **"Code"**
3. Selecione a aba **"Codespaces"**
4. Clique em **"Create codespace on main"**
5. Aguarde a criação (2-5 minutos)

### Passo 3: Executar Teste

No terminal do Codespace:

```bash
# Verificar ambiente
python3 --version
java -version
ls -la /opt/spark

# Executar análise
./run.sh full
```

Se tudo funcionar corretamente, o Codespace está pronto! ✅

---

## 📝 Adicionar Badge ao README (Opcional)

Adicione um badge ao `README.md` para facilitar o acesso ao Codespace:

```markdown
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SEU_USUARIO/tema-b-otimizacao-armazenamento)
```

Substitua `SEU_USUARIO` pelo seu username do GitHub.

---

## 🔒 Configurações de Privacidade

### Repositório Público

**Vantagens:**
- Codespaces gratuito (60 horas/mês)
- Pode ser incluído no portfólio
- Facilita compartilhamento com avaliadores

**Desvantagens:**
- Código visível para todos

### Repositório Privado

**Vantagens:**
- Código privado
- Controle de acesso

**Desvantagens:**
- Codespaces pago (após limite gratuito)
- Precisa adicionar colaboradores manualmente

**Recomendação:** Use público para o projeto acadêmico.

---

## 👥 Compartilhar com Avaliador

### Opção 1: Link Direto

Envie o link do repositório:
```
https://github.com/SEU_USUARIO/tema-b-otimizacao-armazenamento
```

### Opção 2: Link para Codespace

Envie o link direto para criar Codespace:
```
https://codespaces.new/SEU_USUARIO/tema-b-otimizacao-armazenamento
```

### Opção 3: Adicionar como Colaborador

1. Vá em **Settings → Collaborators**
2. Clique em **"Add people"**
3. Digite o username do avaliador
4. Selecione permissão **"Read"** (apenas visualização)

---

## 🐛 Troubleshooting

### Erro: "Permission denied"

**Solução:**
```bash
# Configurar Git com suas credenciais
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Usar Personal Access Token ao invés de senha
# Gere em: https://github.com/settings/tokens
```

### Erro: "Repository already exists"

**Solução:**
- Escolha outro nome para o repositório
- Ou delete o repositório existente e recrie

### Codespace não Inicia

**Solução:**
- Verifique se `.devcontainer/devcontainer.json` existe
- Verifique se `docker-compose.yml` está correto
- Veja os logs de build do Codespace

### Upload Muito Lento

**Solução:**
- Remova arquivos grandes desnecessários
- Use `.gitignore` para excluir `data/` e `output/`
- Faça upload via Git (mais eficiente que interface web)

---

## 📚 Recursos Adicionais

- [Documentação GitHub Codespaces](https://docs.github.com/en/codespaces)
- [Guia de Git Básico](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Desktop](https://desktop.github.com)
- [Markdown Guide](https://www.markdownguide.org)

---

## ✨ Dicas Finais

1. **Teste Localmente Primeiro:** Execute `./run.sh full` localmente antes de publicar
2. **README Atraente:** O README.md é a primeira impressão. Mantenha-o claro e bem formatado
3. **Documentação Completa:** Inclua INSTRUCOES.md e RESULTADOS_ESPERADOS.md
4. **Commits Descritivos:** Use mensagens de commit claras
5. **Tags de Versão:** Crie uma tag `v1.0` para marcar a versão final:
   ```bash
   git tag -a v1.0 -m "Versão final do Projeto"
   git push origin v1.0
   ```

---

**Boa sorte com a publicação! 🚀**
