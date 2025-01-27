__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import os
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from etapas.mkt import planej_mkt_page
from tools.retrieve import visualizar_planejamentos
from tavily import TavilyClient
from etapas.gemini_midias import planej_midias_page
from etapas.gemini_crm import planej_crm_page
from etapas.gemini_campanhas import planej_campanhas
import google.generativeai as genai
from contato.temaEmail import gen_temas_emails
from etapas.image_gen import gen_img

st.set_page_config(
    layout="wide",
    page_title="Macfor AutoDoc",
    page_icon="static/page-icon.png"
)

gemini_api_key = os.getenv("GEM_API_KEY")

# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")

client = TavilyClient(api_key=t_api_key1)

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

genai.configure(api_key=gemini_api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")


def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


from crewai_tools import BaseTool, tool

# Adiciona a logo na sidebar
st.sidebar.image('static/macLogo.png', width=200)

# Login
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.subheader("Página de Login")

    # Entradas de nome de usuário e senha
    nome_usuario = st.text_input("Nome de Usuário", type="default")
    senha = st.text_input("Senha", type="password")

    # Validação de login
    if st.button("Entrar"):
        if nome_usuario == "admin" and senha == "senha123":  # Troque pelas credenciais reais
            st.session_state.logged_in = True
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Usuário ou senha incorretos.")
            return False
    return False

# Verifique se o login foi feito antes de exibir o conteúdo do aplicativo
if login():
    # Mensagem inicial
    st.image('static/macLogo.png', width=300)
    st.text(
        "Empoderada por IA, a Macfor conta com um sistema gerador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e gere documentos automáticos para otimizar o tempo de sua equipe. "
        "Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!"
    )

    # Sidebar: Selecione qual seção (Plano ou Brainstorming)
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        ["Plano Estratégico", "Brainstorming"],
        key="selecao_sidebar",
        index=0  # Predefinir como 'Plano Estratégico' ativo
    )

    if selecao_sidebar == "Plano Estratégico":
        # Sidebar: Opções de Plano Estratégico
        st.sidebar.subheader("Planos Estratégicos")
        plano_estrategico = st.sidebar.selectbox(
            "Escolha o tipo de plano:",
            [
                "Selecione uma opção",
                "Plano Estratégico e de Pesquisa",
                "Plano Estratégico de Redes e Mídias",
                "Plano de CRM"
            ],
            key="plano_estrategico"
        )

        if plano_estrategico != "Selecione uma opção":
            if plano_estrategico == "Plano Estratégico e de Pesquisa":
                planej_mkt_page()
            elif plano_estrategico == "Plano Estratégico de Redes e Mídias":
                planej_midias_page()
            elif plano_estrategico == "Plano de CRM":
                planej_crm_page()

    elif selecao_sidebar == "Brainstorming":
        # Sidebar: Opções de Brainstorming
        st.sidebar.subheader("Brainstorming")
        brainstorming_option = st.sidebar.selectbox(
            "Escolha o tipo de brainstorming:",
            [
                "Selecione uma opção",
                "Brainstorming Conteúdo de Nutrição de Leads",
                "Brainstorming de Anúncios",
                "Brainstorming de Imagem"
            ],
            key="brainstorming_option"
        )

        if brainstorming_option != "Selecione uma opção":
            if brainstorming_option == "Brainstorming Conteúdo de Nutrição de Leads":
                gen_temas_emails()
            elif brainstorming_option == "Brainstorming de Anúncios":
                planej_campanhas()
            elif brainstorming_option == "Brainstorming de Imagem":
                gen_img()

    # Sidebar: Botão para visualizar documentos gerados
    st.sidebar.subheader("Documentos Gerados")
    if st.sidebar.button("Visualizar Documentos Gerados"):
        visualizar_planejamentos()
