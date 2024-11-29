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

def planej_mkt_page():
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
                                  goal=f"Aprenda sobre revisão geral de estratégia em {pest_files}. Revisar toda a estratégia de {nome_cliente} e garantir alinhamento com os {objetivos_de_marca}, o público-alvo {publico_alvo} e as {referencia_da_marca}.",
                                  backstory=f"Você é Philip Kotler, renomado estrategista de marketing, usando todo o seu conhecimento avançado em administração de marketing como nos documentos de {pest_files}, liderando o planejamento de {nome_cliente} no ramo de {ramo_atuacao} em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Analista PEST",
                                  goal=f"Aprenda sobre análise PEST em {pest_files}. Realizar a análise PEST para o cliente {nome_cliente} em português brasileiro.",
                                  backstory=f"Você é Philip Kotler, liderando a análise PEST para o planejamento estratégico de {nome_cliente} em português brasileiro. Extraia informações sobre atualidades de {pest_files} para realizar a análise PEST. Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador do posicionamento de marca",
                                  goal=f"Aprenda sobre posicionamento de marca em {pest_files}. Criar o posicionamento de marca adequado para {nome_cliente}, considerando o público-alvo {publico_alvo}, o {objetivos_de_marca} a análise SWOT, e o Golden Circle e a referencia de marca: {referencia_da_marca} em português brasileiro.  Extraia informações sobre de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  backstory="Você é Al Ries, responsável por desenvolver o posicionamento de marca em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador do Golden Circle",
                                  goal=f"Aprenda sobre golden circle em {pest_files}. Desenvolver o Golden Circle para {nome_cliente}, considerando o público-alvo '{publico_alvo}', SWOT, {objetivos_de_marca} e a referencia de marca: {referencia_da_marca} em português brasileiro. Extraia informações de {market_files} para ter mais repertório também.", 
                                  backstory="Você é Simon Sinek, desenvolvendo o Golden Circle em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador da Brand Persona",
                                  goal=f"Aprenda sobre brand persona em {pest_files}. Definir a Brand Persona com nome real (como bruna, fernanda, etc) de {nome_cliente}, garantindo consistência na comunicação e levando em conta o objetivo de marca: {objetivos_de_marca} e a referencia de marca: {referencia_da_marca} em português brasileiro.  Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  backstory="Você é Marty Neumeier, criando a Brand Persona em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador da Buyer Persona e Público-Alvo",
                                  goal=f"Aprenda sobre buyer persona em {pest_files}. Definir a buyer persona com nome real (como bruna, fernanda, etc) e o público-alvo de {nome_cliente} levando em conta o objetivo de marca: {objetivos_de_marca} e a referencia de marca: {referencia_da_marca}, os {concorrentes} o posicionamento de marca e o golden circle em português brasileiro.  Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                  backstory="Você é Adele Revella, conduzindo a criação da buyer persona em português brasileiro.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem,
                                  tools = [PDFSearchTool(),CSVSearchTool()]
                              ),
                              Agent(
                                  role="Criador da Matriz SWOT",
                                  goal=f"Aprenda sobre matriz SWOT em {pest_files}. Desenvolver uma análise SWOT para {nome_cliente} considerando os concorrentes '{concorrentes}, o objetivo de marca: {objetivos_de_marca} e a referencia de marca: {referencia_da_marca} em português brasileiro. Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.", 
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
                              ),

                                Agent(
                                  role="Criador das editorias de conteúdo da marca",
                                  goal="Criar as editorias de conteúdo para a marca, considerando quem ela é, os objetivos da marca e onde ela quer chegar.",
                                  backstory="Você é Joe Pulizzi, especializado em criar estratégias de conteúdo de marcas, considerando o alinhamento com os objetivos da marca e o público-alvo.",
                                  allow_delegation=False,
                                  llm=modelo_linguagem
                              ),

                                Agent(
                                role="Criador dos canais onde a marca estará",
                                goal="Definir os canais estratégicos onde a marca deve estar presente para atingir seus objetivos de marketing, alinhando-os com o objetivo da marca e onde ela quer chegar.",
                                backstory="Você é Seth Godin, especialista em marketing e comunicação, responsável por definir os canais ideais para que a marca se conecte com seu público e alcance seus objetivos.",
                                allow_delegation=False,
                                llm=modelo_linguagem
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
                                  output_file = 'revisao.md'),

                               Task(
                              description="Criar as editorias de conteúdo da marca considerando a identidade, os objetivos da marca e o público-alvo.",
                              expected_output="Editorias de conteúdo detalhadas e alinhadas com os objetivos da marca.",
                              agent=agentes[8],
                              output_file='estrategia_conteudo.md'
                          ),

                            Task(
                              description="Criar uma estratégia de canais, considerando os objetivos de marketing da marca e onde ela quer chegar.",
                              expected_output="Definição dos canais estratégicos (online e offline) que a marca deve utilizar para alcançar seu público-alvo e objetivos de marketing.",
                              agent=agentes[9],
                              output_file='estrategia_canais.md'
                          )
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
