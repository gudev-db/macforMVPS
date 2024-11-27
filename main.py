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

# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(layout="wide",
                  page_icon="Screenshot Capture - 2024-11-26 - 20-34-58.png")  # Isso faz o layout ficar mais largo

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

col1, col2 = st.columns([1, 6])  # O primeiro valor (1) define a largura da imagem e o segundo valor (6) define a largura do texto

with col1:
    st.image('Screenshot Capture - 2024-11-26 - 20-28-31.png', width=150)  # Logo da empresa

with col2:
    st.title('AI Solutions')  # Título

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
# Definindo as opções para o SelectBox
objetivos_opcoes = [
    'Aumentar vendas',
    'Melhorar reconhecimento de marca',
    'Expandir mercado',
    'Aumentar engajamento nas redes sociais',
    'Lançar novo produto',
    'Melhorar a experiência do cliente',
    'Aumentar tráfego para o site',
    'Fortalecer a lealdade do cliente',
    'Melhorar a presença online',
    'Ser líder no mercado online'
]
# Verifique se o login foi feito antes de exibir o conteúdo do aplicativo
if login():
    # Interface do Streamlit
        
         # Botões para escolher o tipo de documento
        if st.button('Plano Estratégico de Marketing'):
            st.session_state.tipo_documento = 'Plano Estratégico de Marketing'
            st.success('Você escolheu o Plano Estratégico de Marketing!')
        
        if st.button('Planejamento de Cronograma de Projetos'):
            st.session_state.tipo_documento = 'Planejamento de Cronograma de Projetos'
            st.success('Você escolheu o Planejamento de Cronograma de Projetos!')
        
        if st.button('Orçamento de Projetos'):
            st.session_state.tipo_documento = 'Orçamento de Projetos'
            st.success('Você escolheu o Orçamento de Projetos!')

    
        # Exibindo o conteúdo relacionado ao tipo de documento escolhido
        if "tipo_documento" in st.session_state:
            tipo_documento = st.session_state.tipo_documento
            if tipo_documento == 'Plano Estratégico de Marketing':
              nome_cliente = st.text_input('Nome do Cliente:', key="nome_cliente", placeholder="Ex: Empresa X")
              site_cliente = st.text_input('Site do Cliente:', key="site_cliente", placeholder="Ex: www.empresa-x.com.br")
              ramo_atuacao = st.text_input('Ramo de Atuação:', key="ramo_atuacao", placeholder="Ex: E-commerce de Moda")
              intuito_plano = st.text_input('Intuito do Plano Estratégico:', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre")
              publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda")
              concorrentes = st.text_input('Concorrentes:', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C")
              site_concorrentes = st.text_input('Site dos Concorrentes:', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br")
      
      
      # Criando o selectbox com as opções definidas
              objetivos_de_marca = st.selectbox(
          'Selecione os objetivos de marca',
          objetivos_opcoes,
          key="objetivos_marca"
      )
              referencia_da_marca = st.text_input('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', key = "referencias_marca", placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.")
              
              st.subheader("Suba os Arquivos Estratégicos (PDF)")
              st.text('Suba arquivos PDF para acrescentar à base de conhecimento da equipe de agentes')
              pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)
              st.subheader("Suba os Arquivos Estratégicos (CSV)")
              st.text('Suba arquivos CSV para acrescentar à base de conhecimento da equipe de agentes')
              market_files = st.file_uploader("Escolha arquivos csv para análise de mercado", type=["csv"], accept_multiple_files=True)
      
      
      
              import csv
      
              @tool("CSVSearchTool")
              def csv_search_tool(market_files: list, search_term: str) -> str:
                  """
                  Tool for searching for a term in multiple uploaded CSV files.
                  - market_files: A list of paths to the uploaded CSV files.
                  - search_term: The term to search for within the CSV files.
                  
                  Returns a string with search results or a message indicating no results.
                  """
                  try:
                      # Inicializa uma lista para armazenar os resultados encontrados
                      found_text = []
              
                      # Loop através de cada arquivo CSV em market_files
                      for csv_file in market_files:
                          with open(csv_file, newline='', encoding='utf-8') as file:
                              reader = csv.reader(file)
                              
                              # Loop através de cada linha no CSV
                              for row_num, row in enumerate(reader):
                                  # Junta todas as células da linha em uma string única para busca
                                  row_text = ' '.join(row)
                                  
                                  if search_term.lower() in row_text.lower():  # Busca insensível a maiúsculas/minúsculas
                                      found_text.append(f"File: {csv_file} - Row {row_num + 1}: {row_text[:200]}...")  # Preview de 200 caracteres
                      
                      if found_text:
                          return "\n".join(found_text)  # Retorna todas as linhas correspondentes
                      else:
                          return f"No occurrences of '{search_term}' found in the documents."
                  
                  except Exception as e:
                      return f"An error occurred while processing the CSV files: {str(e)}"
      
              @tool("PDFSearchTool")
              def pdf_search_tool(pdf_file: str, search_term: str) -> str:
                  """
                  Tool for searching for a term in an uploaded PDF document.
                  - pdf_file: The path to the uploaded PDF file.
                  - search_term: The term to search for within the PDF.
                  
                  Returns a string with search results or a message indicating no results.
                  """
                  # Open the uploaded PDF
                  try:
                      document = pest_files  # Open the PDF file
                      
                      found_text = []
              
                      for file in pest_files:
                      
                          # Loop through each page of the PDF
                          for page_num in range(document.page_count):
                              page = document.load_page(page_num)  # Load each page
                              text = page.get_text()  # Extract text from the page
                              
                              # If the search term is found on the page, add it to the results
                              if search_term.lower() in text.lower():
                                  found_text.append(f"Page {page_num + 1}: {text[:200]}...")  # Preview of the first 200 characters
                          
                          if found_text:
                              return "\n".join(found_text)  # Return all matching pages
                          else:
                              return f"No occurrences of '{search_term}' found in the document."
                  
                  except Exception as e:
                      return f"An error occurred while processing the PDF: {str(e)}"
                          
                      
                      
      
              if pest_files is not None:
            
      
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
                                  goal=f"Revisar toda a estratégia de {nome_cliente} e garantir alinhamento com os {objetivos_de_marca}, o público-alvo {publico_alvo} e as {referencia_da_marca}.",
                                  backstory=f"Você é Philip Kotler, renomado estrategista de marketing, usando todo o seu conhecimento avançado em administração de marketing como nos documentos de {pest_files}, liderando o planejamento de {nome_cliente} no ramo de {ramo_atuacao} em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem
                              ),
                              Agent(
                                  role="Analista PEST",
                                  goal=f"Realizar a análise PEST para o cliente {nome_cliente} em português brasileiro.",
                                  backstory=f"Você é Philip Kotler, liderando a análise PEST para o planejamento estratégico de {nome_cliente} em português brasileiro. Extraia informações sobre atualidades de {pest_files} para realizar a análise PEST. Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool()]
                              ),
                              Agent(
                                  role="Criador do posicionamento de marca",
                                  goal=f"Criar o posicionamento de marca adequado para {nome_cliente}, considerando o público-alvo {publico_alvo}, o {objetivos_de_marca} a análise SWOT, e o Golden Circle e a referencia de marca: {referencia_da_marca} em português brasileiro.  Extraia informações sobre de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  backstory="Você é Al Ries, responsável por desenvolver o posicionamento de marca em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador do Golden Circle",
                                  goal=f"Desenvolver o Golden Circle para {nome_cliente}, considerando o público-alvo '{publico_alvo}', SWOT, {objetivos_de_marca} e a referencia de marca: {referencia_da_marca} em português brasileiro. Extraia informações de {market_files} para ter mais repertório também.", 
                                  backstory="Você é Simon Sinek, desenvolvendo o Golden Circle em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador da Brand Persona",
                                  goal=f"Definir a Brand Persona com nome real (como bruna, fernanda, etc) de {nome_cliente}, garantindo consistência na comunicação e levando em conta o objetivo de marca: {objetivos_de_marca} e a referencia de marca: {referencia_da_marca} em português brasileiro.  Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  backstory="Você é Marty Neumeier, criando a Brand Persona em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem
                              ),
                              Agent(
                                  role="Criador da Buyer Persona e Público-Alvo",
                                  goal=f"Definir a buyer persona com nome real (como bruna, fernanda, etc) e o público-alvo de {nome_cliente} levando em conta o objetivo de marca: {objetivos_de_marca} e a referencia de marca: {referencia_da_marca}, os {concorrentes} o posicionamento de marca e o golden circle em português brasileiro.  Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  backstory="Você é Adele Revella, conduzindo a criação da buyer persona em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem
                              ),
                              Agent(
                                  role="Criador da Matriz SWOT",
                                  goal=f"Desenvolver uma análise SWOT para {nome_cliente} considerando os concorrentes '{concorrentes}, o objetivo de marca: {objetivos_de_marca} e a referencia de marca: {referencia_da_marca} em português brasileiro. Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.", 
                                  backstory="Você é Michael Porter, desenvolvendo a análise SWOT em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador do Tom de Voz",
                                  goal=f"Definir o tom de voz de {nome_cliente} em português brasileiro.",
                                  backstory="Você é Ann Handley, desenvolvendo a voz da marca o objetivo de marca: {objetivo de marca} e a referencia de marca: {referencia_de_marca} o posicionamento, brand persona e golden circle em português brasileiro. Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              )
                          ]
          
                          # Criando tarefas correspondentes aos agentes
                          tarefas = [
                              
                              Task(
                                  description="Criar a Matriz SWOT.",
                                  expected_output="Análise SWOT completa em formato de tabela em português brasileiro.",
                                  agent=agentes[6],
                                  output_file = 'SWOT.md'
                              ),
                              Task(
                                  description="Desenvolver o Golden Circle.",
                                  expected_output="Golden Circle completo com 'how', 'why' e 'what' resumidos em uma frase cada em português brasileiro.",
                                  agent=agentes[3],
                                  output_file = 'GC.md'
                              ),
                              Task(
                                  description="Criar o posicionamento de marca.",
                                  expected_output="Posicionamento de marca em uma única frase em português brasileiro.",
                                  agent=agentes[2],
                                  output_file = 'posMar.md'
                              ),
                              Task(
                                  description="Criar a Brand Persona.",
                                  expected_output=f"Brand Persona detalhada, alinhada com a marca do {nome_cliente} em português brasileiro.",
                                  agent=agentes[4],
                                  output_file = 'BP.md'
                              ),
                              Task(
                                  description="Definir a Buyer Persona e o Público-Alvo.",
                                  expected_output="Descrição detalhada da buyer persona e do público-alvo com os seguintes atributos enunciados: nome fictício, idade, gênero, classe social, objetivos, dores, vontades em português brasileiro.", 
                                  agent=agentes[5],
                                  output_file = 'BuyerP.md'
                              ),
                              Task(
                                  description="Definir o Tom de Voz.",
                                  expected_output="Descrição do tom de voz, na {pessoa}, incluindo nuvem de palavras e palavras proibidas. Retorne entre 3 a 5 adjetivos que definem o tom com suas respectivas explicações. ex: 'tom é amigavel, para transparecer uma relação de confiança' com frases de exemplo de aplicação do tom em português brasileiro.",
                                  agent=agentes[7],
                                  output_file = 'TV.md'
                              ),
                              Task(
                                  description="Análise PEST.",
                                  expected_output=f"Análise PEST com pelo menos 5 pontos em cada etapa em português brasileiro.",
                                  agent=agentes[1],
                                  output_file = 'pest.md'
                              ),
                              Task(
                                  description="Revisar a estratégia geral.",
                                  expected_output="Revisão detalhada de cada uma das tarefas realizadas pelos agentes levando em conta os princípios de marketing para entender se há ponto de melhoria para objermos uma estratégia assertiva de acordo com os {objetivos  de marca} do {cliente} considerando o público-alvo em português brasileiro.",
                                  agent=agentes[0],
                                  output_file = 'revisao.md')
                          ]
          
                          # Processo do Crew
                          equipe = Crew(
                              agents=agentes,
                              tasks=tarefas,
                              process=Process.hierarchical,
                              manager_llm=modelo_linguagem,
                              # verbose=True,
                              language='português brasileiro'
                          )
          
                          # Executa as tarefas do processo
                          resultado = equipe.kickoff()
          
          
                          for tarefa in tarefas:
                              st.markdown(f"**Arquivo**: {tarefa.output_file}")
                              st.markdown(tarefa.output.raw)

            elif tipo_documento == 'Planejamento de Cronograma de Projetos':
                st.subheader("Gerando o Planejamento de Cronograma de Projetos...")
                # Aqui você pode colocar o código para gerar o planejamento do cronograma de projetos.
                st.text('Preencha os campos abaixo para criar o cronograma de projetos.')
                # Inputs para o cronograma de projetos (exemplo)
                nome_projeto = st.text_input('Nome do Projeto:', key="nome_projeto", placeholder="Ex: Projeto X")
                data_inicio = st.date_input('Data de Início:', key="data_inicio")
                data_fim = st.date_input('Data de Fim:', key="data_fim")
                # Código para gerar o cronograma...

            elif tipo_documento == 'Orçamento de Projetos':
                st.subheader("Gerando o Orçamento de Projetos...")
                # Aqui você pode colocar o código para gerar o orçamento de projetos.
                st.text('Preencha os campos abaixo para criar o orçamento de projetos.')
                # Inputs para o orçamento de projetos (exemplo)
                nome_projeto = st.text_input('Nome do Projeto:', key="nome_projeto_orcamento", placeholder="Ex: Projeto X")
                orcamento_estimado = st.number_input('Orçamento Estimado:', key="orcamento_estimado", min_value=0, step=1000)
                # Código para gerar o orçamento...
