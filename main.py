import __import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from etapas.gemini_mkt import planej_mkt_page
from tools.retrieve import visualizar_planejamentos  # Importando a função visualizar_planejamentos
from tavily import TavilyClient
from etapas.gemini_midias import planej_midias_page
from etapas.gemini_crm import planej_crm_page
from etapas.gemini_campanhas import planej_campanhas
import google.generativeai as genai
from contato.temaEmail import gen_temas_emails
from etapas.image_gen import gen_img
from etapas.lead_osint import osint_report

# Exibe a logo na sidebar antes do login
st.sidebar.image('static/macLogo.png', width=200)

# Configuração das chaves de API
gemini_api_key = os.getenv("GEM_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")

# Inicializa o cliente Tavily
client = TavilyClient(api_key=t_api_key1)

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

# Configura o modelo de AI Gemini
genai.configure(api_key=gemini_api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")

# Função de login
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.subheader("Página de Login")

    nome_usuario = st.text_input("Nome de Usuário", type="default")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if nome_usuario == "admin" and senha == "senha123":
            st.session_state.logged_in = True
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Usuário ou senha incorretos.")
            return False
    return False

# Verifique se o login foi feito antes de exibir o conteúdo
if login():
    # Exibe a logo novamente após o login com tamanho maior
    st.image('static/macLogo.png', width=300)
    st.text(
        "Empoderada por IA, a Macfor conta com um sistema gerador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e gere documentos automáticos para otimizar o tempo de sua equipe. "
        "Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!"
    )

    # Sidebar para escolher entre "Plano Estratégico" ou "Brainstorming"
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        ["Planejamentos Estratégicos", "Brainstorming", "Documentos Salvos"],
        index=0  # Predefinir como 'Plano Estratégico' ativo
    )

    # Opções para "Plano Estratégico"
    if selecao_sidebar == "Planejamentos Estratégicos":
        st.sidebar.subheader("Planejamentos Estratégicos")
        plano_estrategico = st.sidebar.selectbox(
            "Escolha o tipo de plano:",
            [
                "Selecione uma opção",
                "Planejamento de Pesquisa e Estratégia",
                "Planejamento de Redes e Mídias",
                "Planejamento de CRM",
                "Investigação de Leads"
            ]
        )

        if plano_estrategico != "Selecione uma opção":
            if plano_estrategico == "Planejamento de Pesquisa e Estratégia":
                planej_mkt_page()
            elif plano_estrategico == "Planejamento de Redes e Mídias":
                planej_midias_page()
            elif plano_estrategico == "Planejamento de CRM":
                planej_crm_page()
            elif plano_estrategico == "Investigação de Leads":
                osint_report()

    # Opções para "Brainstorming"
    elif selecao_sidebar == "Brainstorming":
        st.sidebar.subheader("Brainstorming")
        brainstorming_option = st.sidebar.selectbox(
            "Escolha o tipo de brainstorming:",
            [
                "Selecione uma opção",
                "Brainstorming Conteúdo de Nutrição de Leads",
                "Brainstorming de Anúncios",
                "Brainstorming de Imagem"
            ]
        )

        if brainstorming_option != "Selecione uma opção":
            if brainstorming_option == "Brainstorming Conteúdo de Nutrição de Leads":
                gen_temas_emails()
            elif brainstorming_option == "Brainstorming de Anúncios":
                planej_campanhas()
            elif brainstorming_option == "Brainstorming de Imagem":
                gen_img()

    # Seção para "Documentos Salvos"
    elif selecao_sidebar == "Documentos Salvos":
        st.sidebar.subheader("Visualizar Documentos Salvos")

        # Obter a lista de documentos salvos
        documentos_salvos = visualizar_planejamentos()  # Deve retornar [{"id": 1, "conteudo": "Texto 1"}, ...]

        if documentos_salvos:
            # Criar um selectbox para selecionar o documento pelo ID
            doc_ids_salvos = [doc["id"] for doc in documentos_salvos]
            doc_selecionado_id_salvo = st.sidebar.selectbox(
                "Selecione o documento salvo pelo ID:",
                ["Selecione um ID"] + doc_ids_salvos,
                index=0
            )

            # Exibir o conteúdo do documento selecionado
            if doc_selecionado_id_salvo != "Selecione um ID":
                documento_selecionado_salvo = next(doc for doc in documentos_salvos if doc["id"] == doc_selecionado_id_salvo)
                st.markdown("## Documento Salvo Selecionado")
                st.text_area("Conteúdo do Documento", documento_selecionado_salvo["conteudo"], height=300)
        else:
            st.info("Nenhum documento salvo disponível no momento.")
