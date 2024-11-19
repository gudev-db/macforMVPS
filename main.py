import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
import base64
from datetime import datetime
from crewai_tools import FileReadTool, WebsiteSearchTool

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

import os

# Access the keys
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# Função de login
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
        st.title('Criação de Plano Estratégico e Tático de Marketing')

        # Inputs do cliente
        nome_cliente = st.text_input('Nome do Cliente:', key="nome_cliente")
        site_cliente = st.text_input('Site do Cliente:', key="site_cliente")
        ramo_atuacao = st.text_input('Ramo de Atuação:', key="ramo_atuacao")
        intuito_plano = st.text_input('Intuito do Plano Estratégico:', key="intuito_plano")
        publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo")
        concorrentes = st.text_input('Concorrentes:', key="concorrentes")
        site_concorrentes = st.text_input('Site dos Concorrentes:', key="site_concorrentes")

        # Se o relatório já foi gerado, exiba os resultados
        if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
            st.subheader("Relatório Gerado")
            for tarefa in st.session_state.resultados_tarefas:
                st.markdown(f"**Arquivo**: {tarefa['output_file']}")
                st.markdown(tarefa["output"])

            # Botão para limpar o estado
            if st.button("Gerar Novo Relatório"):
                limpar_estado()
                st.experimental_rerun()
        else:
            # Validação de entrada e geração de relatório
            if st.button('Iniciar Planejamento'):
                if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    # Definindo os agentes
                    agentes = [
                    Agent(
                        role="Líder e revisor geral de estratégia",
                        goal=f"Revisar toda a estratégia de {nome_cliente} e garantir alinhamento com os objetivos de marca e o público-alvo '{publico_alvo}'.",
                        backstory=f"Você é Philip Kotler, renomado estrategista de marketing, liderando o planejamento de {nome_cliente} no ramo de {ramo_atuacao}.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Analista PEST",
                        goal=f"Realizar a análise PEST para o cliente {nome_cliente}.",
                        backstory=f"Você é Philip Kotler, liderando a análise PEST para o planejamento estratégico de {nome_cliente}.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador do posicionamento de marca",
                        goal=f"Criar o posicionamento adequado para {nome_cliente}, considerando o público-alvo '{publico_alvo}'.",
                        backstory="Você é Al Ries, responsável por desenvolver o posicionamento de marca.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador do Golden Circle",
                        goal=f"Desenvolver o Golden Circle para {nome_cliente}, considerando o público-alvo '{publico_alvo}'.",
                        backstory="Você é Simon Sinek, desenvolvendo o Golden Circle.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador da Brand Persona",
                        goal=f"Definir a Brand Persona de {nome_cliente}, garantindo consistência na comunicação.",
                        backstory="Você é Marty Neumeier, criando a Brand Persona.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador da Buyer Persona e Público-Alvo",
                        goal=f"Definir a buyer persona e o público-alvo de {nome_cliente}.",
                        backstory="Você é Adele Revella, conduzindo a criação da buyer persona.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador da Matriz SWOT",
                        goal=f"Desenvolver uma análise SWOT para {nome_cliente} considerando os concorrentes '{concorrentes}'.",
                        backstory="Você é Michael Porter, desenvolvendo a análise SWOT.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador do Tom de Voz",
                        goal=f"Definir o tom de voz de {nome_cliente}.",
                        backstory="Você é Ann Handley, desenvolvendo a voz da marca.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    )
                ]

                # Criando tarefas correspondentes aos agentes
                tarefas = [
                    Task(
                        description="Revisar a estratégia geral.",
                        expected_output="Revisão detalhada da estratégia considerando o público-alvo em português.",
                        agent=agentes[0],
                        output_file = 'revisao.md'
                    ),
                    Task(
                        description="Criar o posicionamento de marca.",
                        expected_output="Posicionamento de marca em uma única frase.",
                        agent=agentes[2],
                        output_file = 'posMar.md'
                    ),
                    Task(
                        description="Desenvolver o Golden Circle.",
                        expected_output="Golden Circle completo com 'how', 'why' e 'what' resumidos em uma frase cada.",
                        agent=agentes[3],
                        output_file = 'GC.md'
                    ),
                    Task(
                        description="Criar a Brand Persona.",
                        expected_output="Brand Persona detalhada, alinhada com a marca do cliente.",
                        agent=agentes[4],
                        output_file = 'BP.md'
                    ),
                    Task(
                        description="Definir a Buyer Persona e o Público-Alvo.",
                        expected_output="Descrição detalhada da buyer persona e do público-alvo.",
                        agent=agentes[5],
                        output_file = 'BuyerP.md'
                    ),
                    Task(
                        description="Criar a Matriz SWOT.",
                        expected_output="Análise SWOT completa em formato de tabela.",
                        agent=agentes[6],
                        output_file = 'SWOT.md'
                    ),
                    Task(
                        description="Definir o Tom de Voz.",
                        expected_output="Descrição do tom de voz, incluindo nuvem de palavras e palavras proibidas.",
                        agent=agentes[7],
                        output_file = 'TV.md'
                    ),
                    Task(
                        description="Análise PEST.",
                        expected_output="Análise PEST com pelo menos 5 pontos em cada etapa.",
                        agent=agentes[1],
                        output_file = 'pest.md'
                    )
                ]

                # Processo do Crew
                equipe = Crew(
                    agents=agentes,
                    tasks=tarefas,
                    process=Process.hierarchical,
                    manager_llm=modelo_linguagem,
                    verbose=True,
                    language='português brasileiro'
                )

                # Executa as tarefas do processo
                resultado = equipe.kickoff()


                for tarefa in tarefas:
                    st.markdown(f"**Arquivo**: {tarefa.output_file}")
                    st.markdown(tarefa.output.raw)


    