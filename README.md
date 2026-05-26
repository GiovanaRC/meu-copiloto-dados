# 🤖 Copiloto de Dados Avançado (Multischema & Redshift Spectrum)

Este é um assistente de inteligência artificial de nível corporativo desenvolvido em **Python** com **Streamlit** e integrado à API do **Google Gemini**. A ferramenta foi projetada para atuar como um parceiro técnico e cético de alta performance, auxiliando na criação, refinação e auditoria de queries complexas em SQL (PostgreSQL/Redshift) e fórmulas DAX.

---

## 🔒 Premissas de Segurança, Escopo e Governança (Uso Corporativo)

Para garantir a total conformidade com as políticas de Segurança da Informação (SI) da empresa, o projeto foi estruturado sob os seguintes pilares:

* **Escopo Estritamente Individual e Interno:** Esta ferramenta foi desenhada para **uso local e individual**. A aplicação roda exclusivamente na máquina local do analista (ambiente de desenvolvimento ou workstation interna). Não há publicação, deploy em servidores externos abertos ou compartilhamento de acessos, mitigando riscos de exposição de rede.
* **Segurança Padrão Ouro (Zero Trust para Credenciais):** Toda a infraestrutura de chaves de API e credenciais de acesso a bancos de dados é centralizada e criptografada localmente via `st.secrets` (armazenada no arquivo `.streamlit/secrets.toml`). **Este arquivo está explicitamente incluso no `.gitignore`**, o que impede que qualquer senha ou endpoint corporativo seja exposto no código-fonte ou enviado ao repositório público do GitHub.
* **Consumo de Metadados Isolado:** A ferramenta **não faz varredura de dados sensíveis ou registros de clientes**. Ela lê estritamente o *schema* (nomes de tabelas, colunas e tipos de dados). A IA trabalha apenas com a estrutura lógica do banco para ajudar na sintaxe, garantindo a privacidade das informações armazenadas.

---

## 🚀 Diferenciais Técnicos

* **Arquitetura Híbrida e Adaptativa:** Permite alternar dinamicamente através da interface entre o ambiente local de testes e validações (**PostgreSQL**) e o ambiente de nuvem corporativa (**Amazon Redshift**).
* **Superpoder de Leitura em Camada 3 (Redshift Spectrum):** Supera a limitação tradicional de LLMs ao ler tabelas externas em Data Lakes (S3). A aplicação realiza uma query unificada utilizando a tabela de sistema `svv_external_columns` do Redshift, mapeando perfeitamente os metadados de estruturas externas.
* **Controle Absoluto de Perímetro:** O analista delimita o escopo de atuação da IA digitando o schema exato que deseja focar na barra lateral. Isso zera alucinações do modelo e otimiza o consumo de tokens.
* **Prompt Engineering de Ceticismo Profissional:** Programado sob uma diretriz de senioridade técnica. O copiloto debate performance (CTEs, JOINs perigosos) e valida feedbacks logicamente antes de propor alterações.

---

## 📁 Estrutura do Projeto

```text
meu-copiloto-dados/
├── .streamlit/
│   └── secrets.toml     # Cofre de credenciais local e individual (Ignorado pelo Git)
├── .gitignore           # Política estrita de exclusão de arquivos confidenciais
├── app.py               # Core do sistema, interface e queries de metadados
└── requirements.txt     # Dependências (Streamlit, Gemini SDK, Psycopg2)
