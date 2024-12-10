__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from mkt import planej_mkt_page
from creative import criativos_posts_page
from crewai_tools import FileReadTool, WebsiteSearchTool, PDFSearchTool, CSVSearchTool
import os
from tavily import TavilyClient

st.set_page_config(layout="wide",page_title="Macfor AutoDoc",
                  page_icon="Screenshot Capture - 2024-11-26 - 20-34-58.png")  # Isso faz o layout ficar mais largo

# Carregando o arquivo CSS para personalizar a fonte
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
client = TavilyClient(api_key='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')


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

st.image('macLogo.png', width=1500)
#st.title('Macfor AI Solutions')





def criativos_posts_page():
    # Coleta as informações do cliente e da campanha
    nome_cliente = st.text_input('Nome do Cliente:', key="nome_cliente", placeholder="Ex: Empresa X")
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente", placeholder="Ex: www.empresa-x.com.br")
    
    # Coleta as informações adicionais de concorrentes
    concorrentes = st.text_input('Concorrentes:', key="concorrentes", placeholder="Ex: Empresa Y, Empresa Z")
    site_concorrentes = st.text_input('Sites dos Concorrentes:', key="site_concorrentes", placeholder="Ex: www.empresa-y.com.br, www.empresa-z.com.br")
    
    # Coleta o intuito da campanha e o ramo de atuação
    intuito_campanha = st.text_input('Intuito da Campanha:', key="intuito_campanha", placeholder="Ex: Aumentar a conscientização sobre o produto")
    ramo_atuacao = st.text_input('Ramo de Atuação do Cliente:', key="ramo_atuacao", placeholder="Ex: Moda, Tecnologia, Saúde")
    
    # Selectbox para o veículo de campanha (Google ou Meta)
    veiculo_campanha = st.selectbox("Escolha o Veículo de Campanha", ['Google', 'Meta','Linkedin','Tiktok'], key="veiculo_campanha")
    
    # Selectbox para o tipo de campanha
    tipo_campanha = st.selectbox(
    "Escolha o Tipo de Campanha", 
    ['Search', 'Display', 'Shopping', 'Vídeo', 'App'], 
    key="tipo_campanha"
)
    
    publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda")

    # Botão para iniciar o processo de criação dos criativos
    if st.button("Gerar Criativos de Posts"):
        if not nome_cliente or not objetivo_campanha or not publico_alvo:
            st.write("Por favor, preencha todas as informações do cliente e da campanha.")
        else:
            with st.spinner('Gerando criativos de posts...'):
                # Definir os agentes e tarefas
                agentes = [
                    Agent(
                        role="Criador de Títulos de Post",
                        goal=f"Gerar 10 títulos criativos de posts para {nome_cliente}, focados em {objetivo_campanha} e público-alvo {publico_alvo} para o veículo {veiculo_campanha}.",
                        backstory=f"Você é um especialista que fala português brasileiro em marketing digital, especializado em criar títulos de post criativos para campanhas no Google ou Meta. O cliente é {nome_cliente}, o ramo de atuação é {ramo_atuacao}, o intuito da campanha é {intuito_campanha}, e o objetivo é {objetivo_campanha}. Concorrentes: {concorrentes}.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador de Descrições de Post",
                        goal=f"Gerar 10 descrições criativas para os posts de {nome_cliente} com o objetivo de {objetivo_campanha} e para o público {publico_alvo}.",
                        backstory=f"Você é um especialista que fala português brasileiro em criar descrições criativas para posts de campanhas no Google ou Meta. O cliente é {nome_cliente}, o ramo de atuação é {ramo_atuacao}, o intuito da campanha é {intuito_campanha}, e o objetivo é {objetivo_campanha}. Concorrentes: {concorrentes}.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador de Texto para Site Link",
                        goal=f"Gerar 10 exemplos de texto para links de site para a campanha de {nome_cliente} com objetivo de {objetivo_campanha}.",
                        backstory=f"Você é um especialista que fala português brasileiro em marketing digital, criando textos otimizados para links em campanhas de Google ou Meta. O cliente é {nome_cliente}, o ramo de atuação é {ramo_atuacao}, o intuito da campanha é {intuito_campanha}, e o objetivo é {objetivo_campanha}. Concorrentes: {concorrentes}.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador de Extensões de Frase de Destaque",
                        goal=f"Gerar 10 extensões de frase de destaque para a campanha de {nome_cliente}, focada em {objetivo_campanha}.",
                        backstory=f"Você é um especialista que fala português brasileiro em criar extensões de frase de destaque para campanhas publicitárias no Google ou Meta. O cliente é {nome_cliente}, o ramo de atuação é {ramo_atuacao}, o intuito da campanha é {intuito_campanha}, e o objetivo é {objetivo_campanha}. Concorrentes: {concorrentes}.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    )
                ]

                tarefas = [
                    Task(
                        description="Gerar 10 títulos criativos para os posts.",
                        expected_output="10 exemplos de títulos criativos de posts em português brasileiro.",
                        agent=agentes[0],
                        output_file='titulos.md'
                    ),
                    Task(
                        description="Gerar 10 descrições criativas para os posts.",
                        expected_output="10 exemplos de descrições criativas de posts em português brasileiro.",
                        agent=agentes[1],
                        output_file='descricao.md'
                    ),
                    Task(
                        description="Gerar 10 exemplos de texto para links do site.",
                        expected_output="10 exemplos de texto para links de site em português brasileiro.",
                        agent=agentes[2],
                        output_file='texto_site.md'
                    ),
                    Task(
                        description="Gerar 10 extensões de frase de destaque.",
                        expected_output="10 exemplos de extensões de frase de destaque em português brasileiro.",
                        agent=agentes[3],
                        output_file='extensoes_frase.md'
                    )
                ]

                  # Processo do Crew
                equipe = Crew(
                    agents=agentes,
                    tasks=tarefas,
                    process=Process.hierarchical,
                    manager_llm=modelo_linguagem,
                    language='português brasileiro'
                )

                # Executa as tarefas do processo
                resultado = equipe.kickoff()

                # Exibe os resultados
                for tarefa in tarefas:
                    st.markdown(tarefa.output.raw)

                st.success("Criativos gerados com sucesso!")




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
        
        if st.button('Ideias de Criativos'):
            st.session_state.tipo_documento = 'Ideias de Criativos'
            st.success('Você escolheu Ideias de Criativos!')
        
        

    
        # Exibindo o conteúdo relacionado ao tipo de documento escolhido
        if "tipo_documento" in st.session_state:
            tipo_documento = st.session_state.tipo_documento

          
            if tipo_documento == 'Plano Estratégico de Marketing':

              planej_mkt_page()

            if tipo_documento == 'Ideias de Criativos':

              criativos_posts_page()
              
             

            

            
