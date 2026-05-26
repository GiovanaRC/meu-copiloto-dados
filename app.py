import os
import psycopg2
import streamlit as st
from google import genai

# ==========================================
# 1. CONFIGURAÇÃO DA CHAVE E CLIENTE GEMINI
# ==========================================
if "gemini_client" not in st.session_state:
    MINHA_API_KEY = st.secrets["GEMINI_API_KEY"]
    st.session_state.gemini_client = genai.Client(api_key=MINHA_API_KEY)

# ==========================================
# 2. FUNÇÃO ADAPTATIVA DE SCHEMA (POSTGRES / REDSHIFT)
# ==========================================
def obtener_schema_banco(schema_alvo, ambiente):
    # Se o usuário não digitou nada ainda, evita rodar a query à toa
    if not schema_alvo:
        return "Aguardando você digitar o nome do schema na barra lateral...", False
        
    try:
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],    
            user=st.secrets["DB_USER"],        
            password=st.secrets["DB_PASSWORD"], 
            port=st.secrets["DB_PORT"]
        )
        cursor = conn.cursor()
        
        # Redshift (Camada 3 / Spectrum / External Tables)
        if ambiente == "Empresa (Redshift)":
            query_schema = f"""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = '{schema_alvo}'
                
                UNION ALL
                
                SELECT tablename AS table_name, columnname AS column_name, external_type AS data_type
                FROM svv_external_columns
                WHERE schemaname = '{schema_alvo}';
            """
        else:
            # Postgres local (Casa)
            query_schema = f"""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = '{schema_alvo}';
            """
        
        cursor.execute(query_schema)
        colunas = cursor.fetchall()
        
        if not colunas:
            return f"Nenhuma tabela encontrada no schema '{schema_alvo}'. Verifique se digitou o nome corretamente.", False
            
        schema_texto = f"Estrutura do Banco de Dados (Schema: {schema_alvo}):\n"
        for tabela, coluna, tipo in colunas:
            schema_texto += f"Tabela: {tabela} | Coluna: {coluna} ({tipo})\n"
            
        cursor.close()
        conn.close()
        return schema_texto, True
        
    except Exception as e:
        return f"Erro ao conectar no banco de dados: {e}", False

# ==========================================
# 3. INTERFACE E BARRA LATERAL (AGORA LIVRE)
# ==========================================
st.set_page_config(page_title="Copiloto de Dados Dinâmico", layout="wide")
st.title("🤖 Copiloto de Dados Avançado")

st.sidebar.header("⚙️ Configurações de Contexto")

# Escolha do Ambiente (Casa x Empresa)
ambiente_atual = st.sidebar.radio(
    "Onde você está rodando o app agora?",
    options=["Casa (Postgres)", "Empresa (Redshift)"]
)

# 🎯 O PULO DO GATO: Campo livre para você digitar o schema na hora!
schema_selecionado = st.sidebar.text_input(
    "Digite o nome do schema/setor alvo:",
    value="industrial"  # Deixa 'industrial' como sugestão inicial padrão
).strip()

# Executa a busca baseada no texto que você digitou na tela
mapa_do_banco, conexao_ok = obtener_schema_banco(schema_selecionado, ambiente_atual)

# Monitora se você mudou o texto ou o ambiente para limpar o chat antigo
if "schema_atual" not in st.session_state:
    st.session_state.schema_atual = schema_selecionado
if "ambiente_atual" not in st.session_state:
    st.session_state.ambiente_atual = ambiente_atual

if st.session_state.schema_atual != schema_selecionado or st.session_state.ambiente_atual != ambiente_atual:
    st.session_state.schema_atual = schema_selecionado
    st.session_state.ambiente_atual = ambiente_atual
    st.session_state.mensagens = []
    if "gemini_chat" in st.session_state: del st.session_state.gemini_chat
    st.rerun()

# Inicializa as memórias do Streamlit
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "gemini_chat" not in st.session_state:
    prompt_sistema = f"""
    Você é um Analista de Dados Sênior e Engenheiro de Analytics extremamente crítico, técnico e pragmático.
    O seu objetivo NÃO é apenas agradar o usuário, mas garantir a precisão dos dados, performance das queries e consistência lógica.
    
    O usuário direcionou o escopo estritamente para o schema: '{schema_selecionado}'.
    Aqui estão as tabelas e colunas reais desse local para você trabalhar:
    {mapa_do_banco}
    
    Diretrizes de Comportamento e Personalidade:
    1. CETICISMO PROFISSIONAL: Se o usuário apontar uma suposta inconsistência ou erro na sua query, NÃO peça desculpas imediatamente e NÃO mude o código sem antes reanalisar. Verifique se o usuário tem razão técnica. Se ele estiver correto, explique o erro e corrija. Se ele estiver equivocado, defenda seu ponto logicamente usando o mapa do banco fornecido.
    2. PERFORMANCE E BOAS PRÁTICAS: Ao criar queries para o Redshift, priorize performance (evite subqueries desnecessárias, prefira CTEs estruturadas, alerte sobre JOINs perigosos que possam duplicar dados).
    3. DESAFIE CONSTRUTIVAMENTE: Se o usuário pedir uma métrica complexa em DAX ou SQL que pareça ambígua, questione ou sugira a abordagem ideal antes de simplesmente cuspir um código qualquer.
    4. FOCO ABSOLUTO: Não use ou invente nenhuma tabela ou coluna que não esteja explicitamente no mapa do banco enviado. Se o usuário pedir algo inviável com os dados atuais, avise-o diretamente.
    
    Sempre retorne o código formatado de maneira limpa e explique sua linha de raciocínio de forma direta, como um par sênior conversando com outro.
    """
    st.session_state.gemini_chat = st.session_state.gemini_client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": prompt_sistema}
    )

# Status na barra lateral
if conexao_ok:
    st.sidebar.success(f"🟢 Focado no Schema: {schema_selecionado}")
    with st.sidebar.expander("Ver tabelas mapeadas"):
        st.text(mapa_do_banco)
else:
    st.sidebar.error("🔴 Banco Desconectado")
    st.sidebar.caption(mapa_do_banco)

if st.sidebar.button("Limpar Histórico Manual"):
    st.session_state.mensagens = []
    if "gemini_chat" in st.session_state: del st.session_state.gemini_chat
    if "gemini_client" in st.session_state: del st.session_state.gemini_client
    st.rerun()

# ==========================================
# 4. EXIBIÇÃO E FLUXO DO CHAT
# ==========================================
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]): st.markdown(msg["text"])

if pergunta := st.chat_input("Peça uma query, um DAX ou mande uma alteração..."):
    with st.chat_message("user"): st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "text": pergunta})
    
    with st.chat_message("assistant"):
        with st.spinner("Analisando metadados..."):
            try:
                response = st.session_state.gemini_chat.send_message(pergunta)
                st.markdown(response.text)
                st.session_state.mensagens.append({"role": "assistant", "text": response.text})
            except Exception as e:
                st.error(f"Erro ao processar: {e}")