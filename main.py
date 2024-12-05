__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from crewai_tools import FileReadTool, WebsiteSearchTool, PDFSearchTool, CSVSearchTool
import os
from mkt import planej_mkt_page

# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(layout="wide",
                  page_icon="Screenshot Capture - 2024-11-26 - 20-34-58.png")  # Isso faz o layout ficar mais largo

# Carregando o arquivo CSS para personalizar a fonte
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

from crewai_tools import BaseTool, tool



# Função de login
file_tool = PDFSearchTool()

st.image('Screenshot Capture - 2024-11-26 - 20-28-31.png', width=150)
st.title('Macfor AI Solutions')










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
        
         # Botões para escolher o tipo de documento
        if st.button('Plano Estratégico de Marketing'):
            st.session_state.tipo_documento = 'Plano Estratégico de Marketing'
            st.success('Você escolheu o Plano Estratégico de Marketing!')
        
        

    
        # Exibindo o conteúdo relacionado ao tipo de documento escolhido
        if "tipo_documento" in st.session_state:
            tipo_documento = st.session_state.tipo_documento

          
            if tipo_documento == 'Plano Estratégico de Marketing':

              planej_mkt_page()
              
             

            

            
