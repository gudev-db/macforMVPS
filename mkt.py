__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from crewai_tools import tool
from crewai_tools import FileReadTool, WebsiteSearchTool, PDFSearchTool, CSVSearchTool
import os
import PyPDF2


# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

def extrair_texto_pdf(pdf_files):
    textos_extraidos = []
    for pdf_file in pdf_files:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        texto = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto += page.extract_text()
        textos_extraidos.append(texto)
    return textos_extraidos

def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

from crewai_tools import BaseTool, tool
# Definindo a lista de opções para o selectbox
objetivos_opcoes = [
    'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
    'Entregar potenciais consumidores para a área comercial',
    'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
    'Fidelizar e reter um público fiel já convertido',
    'Garantir que o público esteja engajado com os canais ou ações da marca'
]


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
    referencia_da_marca = st.text_input('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', key="referencias_marca", placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.")
    
    st.subheader("Suba os Arquivos Estratégicos (PDF) (Único ou múltiplos)")
    pest_files1 = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)
    pest_files = extrair_texto_pdf(pest_files1)

    @tool("CSVSearchTool")
    def csv_search_tool(market_files: list, search_term: str) -> str:
        """
        Tool for searching for a term in multiple uploaded CSV files.
        - market_files: A list of paths to the uploaded CSV files.
        - search_term: The term to search for within the CSV files.
        
        Returns a string with search results or a message indicating no results.
        """
        try:
            found_text = []

            for csv_file in market_files:
                with open(csv_file, newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    
                    for row_num, row in enumerate(reader):
                        row_text = ' '.join(row)
                        
                        if search_term.lower() in row_text.lower():
                            found_text.append(f"File: {csv_file} - Row {row_num + 1}: {row_text[:200]}...")  # Preview de 200 caracteres
                        
            if found_text:
                return "\n".join(found_text)
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
        try:
            document = pest_files
            found_text = []

            for file in pest_files:
                for page_num in range(document.page_count):
                    page = document.load_page(page_num)
                    text = page.get_text()
                    
                    if search_term.lower() in text.lower():
                        found_text.append(f"Page {page_num + 1}: {text[:200]}...")  # Preview of the first 200 characters
                
                if found_text:
                    return "\n".join(found_text)
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
                    with st.spinner('Gerando o planejamento...'):

                    # Definindo os agentes
                        agentes = [
                            Agent(
                                role="Líder e revisor geral de estratégia",
                                goal=f"Aprenda sobre revisão geral de estratégia em {pest_files}. Revisar toda a estratégia de {nome_cliente} e garantir alinhamento com os {objetivos_de_marca}, o público-alvo {publico_alvo} e as {referencia_da_marca}.",
                                backstory=f"Você é Philip Kotler, renomado estrategista de marketing, usando todo o seu conhecimento avançado em administração de marketing como nos documentos de {pest_files}, liderando o planejamento de {nome_cliente} no ramo de {ramo_atuacao} em português brasileiro.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Analista PEST",
                                goal=f"Aprenda sobre análise PEST em {pest_files}. Realizar a análise PEST para o cliente {nome_cliente} em português brasileiro.",
                                backstory=f"Você é Philip Kotler, liderando a análise PEST para o planejamento estratégico de {nome_cliente} em português brasileiro. Extraia informações sobre atualidades de {pest_files} para realizar a análise PEST. Extraia informações de {market_files} para ter mais repertório também. Os arquivos em {pest_files} e {market_files} devem ter um efeito direto em sua análise aprenda sobre marketing com eles. Use suas ferramentas para analisá-los.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Analista SWOT",
                                goal=f"Aprenda sobre análise SWOT e crie a análise para {nome_cliente}, com base nos dados de mercado disponíveis.",
                                backstory="Você é um analista de marketing focado em realizar uma análise SWOT completa com dados extraídos de fontes diversas, como documentos PDF e CSV.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Especialista em Matriz BCG",
                                goal=f"Desenvolver a Matriz BCG para o {nome_cliente}, com base nas informações do mercado e concorrência disponíveis.",
                                backstory="Você é um especialista em estratégia de negócios e está ajudando a construir a Matriz BCG com base nos dados de mercado disponíveis, incluindo concorrentes.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Consultor de Pricing",
                                goal=f"Analisar a estratégia de preços para {nome_cliente}, utilizando dados de mercado e concorrência.",
                                backstory="Você é um consultor de pricing experiente e ajudará {nome_cliente} a entender as melhores práticas de precificação com base na análise de mercado e concorrência.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Analista de Segmentação de Mercado",
                                goal=f"Segmentar o mercado para {nome_cliente} com base nos dados de concorrentes e no perfil do público-alvo.",
                                backstory="Você é um analista de mercado com a missão de segmentar o público de {nome_cliente} e gerar insights acionáveis para o planejamento de marketing.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Criador de Persona",
                                goal=f"Desenvolver personas para o {nome_cliente} com base nos dados de público-alvo e concorrência.",
                                backstory="Você é um especialista em marketing digital, com o objetivo de criar personas detalhadas para {nome_cliente}, que ajudem a direcionar a comunicação de marketing.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Estratégia de Mídia Social",
                                goal=f"Desenvolver uma estratégia de mídia social para {nome_cliente} com base nas análises de mercado e público-alvo.",
                                backstory="Você é um especialista em mídia social, com foco em ajudar marcas a maximizar sua presença nas plataformas de mídia social com base em dados do mercado.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Especialista em Inbound Marketing",
                                goal=f"Em portugês brasileiro, Desenvolver uma estratégia de inbound marketing para {nome_cliente}, com foco em atrair e converter leads.",
                                backstory="Você é um especialista em inbound marketing, utilizando as melhores práticas para atrair e engajar clientes em potencial para {nome_cliente}.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
                            Agent(
                                role="Especialista em SEO",
                                goal=f"Em portugês brasileiro, Melhorar o SEO de {nome_cliente}, com base na análise do site e na concorrência.",
                                backstory="Você é um especialista em SEO, com o objetivo de melhorar a visibilidade do site de {nome_cliente} nos motores de busca, com base na análise do conteúdo existente e da concorrência.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[PDFSearchTool(), CSVSearchTool()]
                            ),
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
                                    expected_output="Em portugês brasileiro, Revisão detalhada de cada uma das tarefas realizadas pelos agentes levando em conta os princípios de marketing para entender se há ponto de melhoria para objermos uma estratégia assertiva de acordo com os {objetivos  de marca} do {cliente} considerando o público-alvo em português brasileiro.",
                                    agent=agentes[0],
                                    output_file = 'revisao.md'),

                                Task(
                                description="Em portugês brasileiro, Sendo o mais detalhista possível e com a profundidade de um especialista em marketing digital, Levando em conta a análise PEST, Tom de Voz, Buyer Persona, Brando Persona, Público alvo, posicionamento de marca, análise SWOT e golden circle gerados, Criar as editorias de conteúdo da marca considerando a identidade, os objetivos da marca e o público-alvo.",
                                expected_output="Em portugês brasileiro, Editorias de conteúdo detalhadas e alinhadas com os objetivos da marca.",
                                agent=agentes[8],
                                output_file='estrategia_conteudo.md'
                            ),
                            Task(
                                description="Plano de SEO Em portugês brasileiro.",
                                expected_output="Em portugês brasileiro, Sendo o mais detalhista possível e com a profundidade de um especialista em marketing digital, Levando em conta a análise PEST, Tom de Voz, Buyer Persona, Brando Persona, Público alvo, posicionamento de marca, análise SWOT e golden circle gerados, faça o Plano de SEO para melhorar a visibilidade do site de {nome_cliente}.",
                                agent=agentes[9],
                                output_file='seo.md'
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

                        for tarefa in tarefas:
                            st.markdown(tarefa.output.raw)
                        st.success("Planejamento gerado com sucesso!")
