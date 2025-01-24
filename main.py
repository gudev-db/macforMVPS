__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from etapas.mkt import planej_mkt_page
from tools.retrieve import visualizar_planejamentos
import os
from tavily import TavilyClient
from etapas.gemini_midias import planej_midias_page
from etapas.gemini_crm import planej_crm_page
from etapas.gemini_campanhas import planej_campanhas
import google.generativeai as genai
from contato.temaEmail import gen_temas_emails



st.set_page_config(layout="wide",page_title="Macfor AutoDoc",
                  page_icon="static/page-icon.png")  




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


st.image('static/macLogo.png', width=300)
#st.title('Macfor AI Solutions')


st.text('Empoderada por IA, a Macfor conta com um sistema gerador de documentos automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo e gere documentos automáticos e otimizar o tempo de sua equipe. Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!')


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
        if nome_usuario == "admin" and senha == "senha123":  # Aqui você pode trocar pelas credenciais reais
            st.session_state.logged_in = True
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Usuário ou senha incorretos.")
            return False
    return False

# Verifique se o login foi feito antes de exibir o conteúdo do aplicativo
if login():
    # Interface do Streamlit

    # Sidebar com selectbox para escolher o tipo de documento
    menu_options = [
        "Selecione uma opção",  # Valor inicial padrão
        "Plano Estratégico e de Pesquisa",
        "Plano Estratégico de Redes e Mídias",
        "Plano de CRM",
        "Visualizar documentos gerados",
        "Conteúdo de Nutrição de Leads",
        "Brainstorming de Anúncios"
    ]

    # Guardando a escolha do usuário na session state
    tipo_documento = st.sidebar.selectbox(
        "Escolha o que deseja fazer:",
        menu_options,
        key="menu_options"  # Chave única para armazenar no session_state
    )

    if tipo_documento != "Selecione uma opção":  # Ignorar a opção padrão
        st.session_state.tipo_documento = tipo_documento
        st.sidebar.success(f"Você escolheu: {tipo_documento}!")

    # Exibindo o conteúdo relacionado ao tipo de documento escolhido
    if "tipo_documento" in st.session_state:
        tipo_documento = st.session_state.tipo_documento

        if tipo_documento == "Plano Estratégico e de Pesquisa":
            planej_mkt_page()

        elif tipo_documento == "Plano Estratégico de Redes e Mídias":
            planej_midias_page()

        elif tipo_documento == "Plano de CRM":
            planej_crm_page()

        elif tipo_documento == "Visualizar documentos gerados":
            visualizar_planejamentos()
        
        elif tipo_documento == "Conteúdo de Nutrição de Leads":
            gen_temas_emails()

        elif tipo_documento == "Brainstorming de Anúncios":
            planej_campanhas()




            
