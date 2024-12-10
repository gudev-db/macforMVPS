import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

# Função para limpar o estado do session_state
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de criativos de posts
def criativos_posts_page():
    nome_cliente = st.text_input('Nome do Cliente:', key="nome_cliente", placeholder="Ex: Empresa X")
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente", placeholder="Ex: www.empresa-x.com.br")
    
    # Selectbox para escolher o veículo da campanha (Google ou Meta)
    veiculo_campanha = st.selectbox("Selecione o veículo da campanha", ['Google', 'Meta'], key="veiculo_campanha")
    
    # Selectbox para escolher o tipo de campanha
    tipo_campanha = st.selectbox("Selecione o tipo de campanha", ['Search', 'Display'], key="tipo_campanha")
    
    # Input de texto para objetivo da campanha
    objetivo_campanha = st.text_input('Objetivo da Campanha:', key="objetivo_campanha", placeholder="Ex: Aumentar conversões")
    
    # Input de texto para público-alvo
    publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos interessados em moda")

    # Definindo o objetivo da marca com base no selectbox
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]
    objetivo_de_marca = st.selectbox(
        'Selecione os objetivos de marca',
        objetivos_opcoes,
        key="objetivo_de_marca"
    )
    
    # Botão para gerar os criativos
    if st.button('Gerar Criativos'):
        if not nome_cliente or not site_cliente or not objetivo_campanha or not publico_alvo:
            st.write("Por favor, preencha todas as informações do cliente.")
        else:
            # Criando os agentes responsáveis por gerar os criativos
            agentes = [
                Agent(
                    role="Gerador de Títulos",
                    goal=f"Gerar 10 títulos criativos para a campanha do cliente {nome_cliente} no veículo {veiculo_campanha}. Objetivo: {objetivo_campanha}. Público-alvo: {publico_alvo}.",
                    backstory=f"Você é um especialista em marketing digital e vai criar títulos criativos para a campanha de {nome_cliente} no veículo {veiculo_campanha} com o objetivo de {objetivo_campanha}.",
                    allow_delegation=False,
                    llm=modelo_linguagem,
                ),
                Agent(
                    role="Gerador de Descrições",
                    goal=f"Gerar 10 descrições criativas para a campanha do cliente {nome_cliente} no veículo {veiculo_campanha}. Objetivo: {objetivo_campanha}. Público-alvo: {publico_alvo}.",
                    backstory=f"Você é um especialista em copywriting e vai criar descrições criativas para a campanha de {nome_cliente} no veículo {veiculo_campanha} com o objetivo de {objetivo_campanha}.",
                    allow_delegation=False,
                    llm=modelo_linguagem,
                ),
                Agent(
                    role="Gerador de Texto de Link",
                    goal=f"Gerar 10 textos criativos para o link do site do cliente {nome_cliente} no veículo {veiculo_campanha}. Objetivo: {objetivo_campanha}.",
                    backstory=f"Você é um especialista em marketing digital e vai criar textos criativos para os links da campanha de {nome_cliente} no veículo {veiculo_campanha}.",
                    allow_delegation=False,
                    llm=modelo_linguagem,
                ),
                Agent(
                    role="Gerador de Extensões de Frase",
                    goal=f"Gerar 10 extensões de frases criativas para a campanha de {nome_cliente} no veículo {veiculo_campanha}. Objetivo: {objetivo_campanha}. Público-alvo: {publico_alvo}.",
                    backstory=f"Você é um especialista em copywriting e vai criar extensões de frases criativas para a campanha de {nome_cliente} no veículo {veiculo_campanha}.",
                    allow_delegation=False,
                    llm=modelo_linguagem,
                ),
            ]
            
            # Criando tarefas para gerar os outputs
            tarefas = [
                Task(
                    description="Gerar 10 títulos criativos para a campanha",
                    expected_output="10 títulos criativos para a campanha em português brasileiro.",
                    agent=agentes[0],
                    output_file='titulos.md'
                ),
                Task(
                    description="Gerar 10 descrições criativas para a campanha",
                    expected_output="10 descrições criativas para a campanha em português brasileiro.",
                    agent=agentes[1],
                    output_file='descricoes.md'
                ),
                Task(
                    description="Gerar 10 textos criativos para o link do site",
                    expected_output="10 textos criativos para o link do site da campanha em português brasileiro.",
                    agent=agentes[2],
                    output_file='texto_link.md'
                ),
                Task(
                    description="Gerar 10 extensões de frases criativas para a campanha",
                    expected_output="10 extensões de frases criativas para a campanha em português brasileiro.",
                    agent=agentes[3],
                    output_file='extensoes.md'
                ),
            ]
            
            # Criando o processo Crew com os agentes e tarefas
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
                st.markdown(f"**Arquivo**: {tarefa.output_file}")
                st.markdown(tarefa.output.raw)
                
            st.success("Criativos gerados com sucesso!")
