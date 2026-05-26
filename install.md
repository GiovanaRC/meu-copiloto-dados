# 📑 Guia de Implementação e Segurança (Replicação do Ambiente)

Este documento serve como guia passo a passo para replicar a infraestrutura do Copiloto de Dados em ambientes locais ou estações de trabalho corporativas, detalhando os requisitos e as premissas de segurança de dados.

---

## 🔐 Segurança e Conformidade da API (Google Cloud)

Um ponto fundamental para a governança de TI da empresa é o ecossistema de segurança da camada de Inteligência Artificial:

1. **Herança de Segurança da Conta:** O projeto utiliza o SDK oficial do Google (`google-genai`). Consequentemente, a autenticação via `GEMINI_API_KEY` está diretamente vinculada à sua conta Google. Isso significa que a ferramenta **herda automaticamente todos os níveis de segurança, políticas de acesso, auditoria e criptografia** já configurados na sua conta (seja ela pessoal ou uma conta corporativa do Google Workspace).
2. **Trânsito Seguro de Dados (SSL/TLS):** Toda e qualquer comunicação entre a sua máquina local e os servidores do Google para o processamento do LLM é feita de forma estritamente criptografada via HTTPS/TLS.
3. **Privacidade dos Metadados:** Conforme as diretrizes de privacidade de API do Google para desenvolvedores, os metadados estruturais enviados para auxílio na query não são utilizados para treinamento de modelos públicos.

---

## 🛠️ Passo a Passo para Instalação

### 1. Preparação do Ambiente Local
Abra o terminal ou PowerShell na pasta onde deseja reconstruir o projeto e crie o ambiente virtual (VENV) para isolar as bibliotecas:
```bash
python -m venv .venv

Ative o ambiente virtual para que o terminal passe a usar o isolamento:

No Windows (PowerShell): .venv\Scripts\Activate.ps1

No Windows (Prompt CMD): .venv\Scripts\activate.bat

2. Instalação das Dependências
Certifique-se de que o arquivo requirements.txt está na raiz da pasta com o seguinte conteúdo:

Plaintext
streamlit
google-genai
psycopg2-binary
Instale todas as dependências de uma vez executando:

Bash
pip install -r requirements.txt
3. Configuração das Chaves e Credenciais (Cofre Local)
Crie a pasta .streamlit e, dentro dela, o arquivo secrets.toml. Este arquivo funcionará como o seu cofre local de senhas. Substitua pelos acessos da sua conta e do banco da empresa:

Ini, TOML
GEMINI_API_KEY = "SUA_CHAVE_API_VINCULADA_A_SUA_CONTA_GOOGLE"

[postgres]
host = "localhost"
port = 5432
database = "meu_banco_local"
user = "postgres"
password = "sua_senha_local"

[redshift]
host = "seu-cluster-redshift.amazonaws.com"
port = 5439
database = "banco_producao"
user = "seu_usuario_redshift"
password = "sua_senha_redshift"
⚠️ Nota de Segurança: Certifique-se de que o seu arquivo .gitignore possua a linha .streamlit/secrets.toml para que essas informações nunca saiam da sua máquina.

4. Inicialização do Sistema
Com o arquivo app.py devidamente estruturado na pasta, execute o comando abaixo para abrir a interface no navegador:

Bash
streamlit run app.py

---

### 🚀 Como referenciar isso no seu `README.md` principal e subir para o GitHub

Para o seu repositório principal ficar conectado com esse novo manual, abra o seu arquivo **`README.md`** antigo, apague aquela parte do passo a passo que estava nele, e substitua por uma seção elegante assim:

```markdown
## 📑 Guia de Instalação e Replicação

Para entender como replicar este projeto do absoluto zero na sua máquina ou no ambiente corporativo, siga o nosso manual detalhado de instalação, configuração de ambiente virtual e notas sobre conformidade com a API do Google:

👉 **[Clique aqui para acessar o Guia de Implementação (INSTALL.md)](./INSTALL.md)**