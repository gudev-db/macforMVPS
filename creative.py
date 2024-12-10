import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from crewai_tools import tool
import random

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.5, 
    frequency_penalty=0.5
)

# Função para limpar o estado
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função para criar a página de planejamento criativo de posts
def criativos_posts_page():
    # Coleta as informações do cliente e da campanha
    nome_cliente = st.text_input('Nome do Cliente:', key="nome_cliente", placeholder="Ex: Empresa X")
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente", placeholder="Ex: www.empresa-x.com.br")
    
    # Selectbox para o veículo de campanha (Google ou Meta)
    veiculo_campanha = st.selectbox("Escolha o Veículo de Campanha", ['Google', 'Meta','Linkedin','Tiktok'], key="veiculo_campanha")
    
    # Selectbox para o tipo de campanha
    tipo_campanha = st.selectbox(
    "Escolha o Tipo de Campanha", 
    ['Search', 'Display', 'Shopping', 'Vídeo', 'App'], 
    key="tipo_campanha"
)
    
    objetivo_campanha = st.text_input('Objetivo da Campanha:', key="objetivo_campanha", placeholder="Ex: Aumentar tráfego no site")
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
                        backstory="Você é um especialista que fala português brasileiro em marketing digital, especializado em criar títulos de post criativos para campanhas no Google ou Meta.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador de Descrições de Post",
                        goal=f"Gerar 10 descrições criativas para os posts de {nome_cliente} com o objetivo de {objetivo_campanha} e para o público {publico_alvo}.",
                        backstory="Você é um especialista que fala português brasileiro em criar descrições criativas para posts de campanhas no Google ou Meta.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador de Texto para Site Link",
                        goal=f"Gerar 10 exemplos de texto para links de site para a campanha de {nome_cliente} com objetivo de {objetivo_campanha}.",
                        backstory="Você é um especialista que fala português brasileiro em marketing digital, criando textos otimizados para links em campanhas de Google ou Meta.",
                        allow_delegation=False,
                        llm=modelo_linguagem
                    ),
                    Agent(
                        role="Criador de Extensões de Frase de Destaque",
                        goal=f"Gerar 10 extensões de frase de destaque para a campanha de {nome_cliente}, focada em {objetivo_campanha}.",
                        backstory="Você é um especialista que fala português brasileiro em criar extensões de frase de destaque para campanhas publicitárias no Google ou Meta.",
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
