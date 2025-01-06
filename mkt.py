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
from tavily import TavilyClient
from pymongo import MongoClient



# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

client1 = TavilyClient(api_key='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')

# Connect to MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']  # Replace with your database name
collection = db['auto_doc'] 

import uuid

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

def save_to_mongo(tarefas_pesquisa,tarefas_estrategica,tarefas_midia, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepare the document to be inserted into MongoDB
    task_outputs = {
        "id_planejamento": nome_cliente + '_' + id_planejamento,  # Use o ID gerado como chave
        "nome_cliente": nome_cliente,  # Adiciona o nome do cliente ao payload
        "SWOT": tarefas_pesquisa[0].output.raw,
        "PEST": tarefas_pesquisa[1].output.raw,

        
        "GC": tarefas_estrategica[0].output.raw,
        "Posicionamento_Marca": tarefas_estrategica[1].output.raw,
        "Brand_Persona": tarefas_estrategica[2].output.raw,
        "Buyer_Persona": tarefas_estrategica[3].output.raw,
        "Tom_Voz": tarefas_estrategica[4].output.raw,
        

        
        "Plano_Criativos": tarefas_midia[0].output.raw,
        "Plano_SEO": tarefas_midia[1].output.raw,
        "Plano_CRM": tarefas_midia[2].output.raw,
        "Plano_Design": tarefas_midia[3].output.raw,
        "Estrategia_Conteudo": tarefas_midia[4].output.raw,
    }

    # Insert the document into MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")



# Step 2. Executing a simple search query
politic = client1.search("Como está a situação política no brasil atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital?")
economic = client1.search("Como está a situação econômica no brasil atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital??")
social = client1.search("Como está a situação social no brasil atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital??")
tec = client1.search("Quais as novidades tecnológicas no context brasileiro atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital??")


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
    referencia_da_marca = st.text_area(
    'O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?',
    key="referencias_marca",
    placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.",
    height=200  # Adjust the height in pixels as needed
)    
    st.subheader("(Opcional) Suba os Arquivos Estratégicos (PDF) (Único ou múltiplos)")
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)
   

  

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
                                tools=[]
                            ),
                            Agent(
                                role="Analista PEST",
                                goal=f"Aprenda sobre análise PEST em {pest_files}. Realizar a análise PEST para o cliente {nome_cliente} em português brasileiro.",
                                backstory=f"Você é Philip Kotler, liderando a análise PEST para o planejamento estratégico de {nome_cliente} em português brasileiro. Levando em conta as informações coletadas em {politic}, {economic}, {social} e {tec} realize a análise PEST, essas informações são o que a sua análise PEST deve se basear em.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Analista SWOT",
                                goal=f"Aprenda sobre análise SWOT e crie a análise para {nome_cliente}, com base nos dados de mercado disponíveis.",
                                backstory="Você é um analista de marketing focado em realizar uma análise SWOT completa com dados extraídos de fontes diversas, como documentos PDF e CSV.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em Matriz BCG",
                                goal=f"Desenvolver a Matriz BCG para o {nome_cliente}, com base nas informações do mercado e concorrência disponíveis.",
                                backstory="Você é um especialista em estratégia de negócios e está ajudando a construir a Matriz BCG com base nos dados de mercado disponíveis, incluindo concorrentes.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Consultor de Pricing",
                                goal=f"Analisar a estratégia de preços para {nome_cliente}, utilizando dados de mercado e concorrência.",
                                backstory=f"Você é um consultor de pricing experiente e ajudará {nome_cliente} a entender as melhores práticas de precificação com base na análise de mercado e concorrência.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Analista de Segmentação de Mercado",
                                goal=f"Segmentar o mercado para {nome_cliente} com base nos dados de concorrentes e no perfil do público-alvo.",
                                backstory=f"Você é um analista de mercado com a missão de segmentar o público de {nome_cliente} e gerar insights acionáveis para o planejamento de marketing.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Criador de Persona",
                                goal=f"Desenvolver personas para o {nome_cliente} com base nos dados de público-alvo e concorrência.",
                                backstory=f"Você é um especialista em marketing digital, com o objetivo de criar personas detalhadas para {nome_cliente}, que ajudem a direcionar a comunicação de marketing.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Estratégia de Mídia Social",
                                goal=f"Desenvolver uma estratégia de mídia social para {nome_cliente} com base nas análises de mercado e público-alvo.",
                                backstory=f"Você é um especialista em mídia social, com foco em ajudar marcas a maximizar sua presença nas plataformas de mídia social com base em dados do mercado.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em Inbound Marketing",
                                goal=f"Desenvolver uma estratégia de inbound marketing para {nome_cliente}, com foco em atrair e converter leads.",
                                backstory=f"Você é um especialista em inbound marketing, utilizando as melhores práticas para atrair e engajar clientes em potencial para {nome_cliente}.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em SEO",
                                goal=f"Melhorar o SEO de {nome_cliente}, com base na análise do site e na concorrência.",
                                backstory=f"Você é um especialista em SEO, com o objetivo de melhorar a visibilidade do site de {nome_cliente} nos motores de busca, com base na análise do conteúdo existente e da concorrência.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em Criativos",
                                goal=f"Desenvolver criativos da campanha de {nome_cliente}, com base no {ramo_atuacao}, {intuito_plano} e {publico_alvo}, aprendendo bastante sobre a marca em sua referencia de marca, conforme detalhada em {referencia_da_marca}.",
                                backstory=f'''Você é um especialista em Criativos de marketing digital, com o objetivo de trazer o máximo de atenção às campanhas do cliente. 
                                Tornando-as relevantes e fazendo com que o cliente atinja seus objetivos.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            
                            Agent(
                                role="Especialista em CRM",
                                goal=f"Desenvolver estratégias de CRM para o cliente: {nome_cliente}.",
                                backstory=f'''Você é um especialista em CRM. Você sabe estabelecer relações durarouras com clientes e sabe tudo que há de se
                                saber para detalhar planos de como firmar e continuar relacionamentos estratégicos com clientes.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            
                            Agent(
                                role="Especialista em Marca/Design",
                                goal=f"Desenvolver ideias de Marca/Design do cliente: {nome_cliente}.",
                                backstory=f'''Você é um especialista em Marca/Design, com o objetivo de melhorar a visibilidade de {nome_cliente} trazendo a sua marca
                                de uma forma coerente e chamativa.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),

                            Agent(
                                role="Especialista em SEO",
                                goal=f"Melhorar o SEO de {nome_cliente}, com base na análise do site e na concorrência.",
                                backstory=f"Você é um especialista em SEO, com o objetivo de melhorar a visibilidade do site de {nome_cliente} nos motores de busca, com base na análise do conteúdo existente e da concorrência.",
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                        ]

                        # Criando tarefas correspondentes aos agentes
                        tarefas_pesquisa = [
                                
                                Task(
                                    description="Criar a Matriz SWOT.",
                                    expected_output="Análise SWOT completa em formato de tabela em português brasileiro.",
                                    agent=agentes[6],
                                    output_file = 'SWOT.md'
                                ),
                                Task(
                                    description="Análise PEST.",
                                    expected_output=f"Análise PEST com pelo menos 5 pontos em cada etapa em português brasileiro.",
                                    agent=agentes[1],
                                    output_file = 'pest.md'
                                )
                            
                        ]


                        
                        tarefas_estrategica = [
                                
                                
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
                                )
                            ]


                        #falta definir agentes de mídia
                       
                        tarefas_midia = [

                            # Criativos
                                Task(
                                    description='''Criativos da campanha de marketing digital''',
                                    expected_output='''Em portugês brasileiro, Criar 10 Criativos,usando originalidade (título, descrição e tipo de imagem sugerida) para as campanhas de marketing digital para 
                                    {nome_do_cliente} considerando seu {ramo_atuacao}, o intuito do planejamento estratégico conforme detalhado em {intuito_plano} e o publico alvo 
                                    {publico_alvo}.''',
                                    agent=agentes[10],
                                    output_file = 'Criativos.md'
                                ),

                            #SEO
                                Task(
                                    description="Desenvolver o plano de SEO do planejamento estratégico.",
                                    expected_output=f'''Em portugês brasileiro, Plano detalhado que visa melhorar a posição de um site nos resultados dos motores de busca. 
                                    Fazendo uso extensivo de conhecimentos de marketing digital. Para {nome_cliente} considerando seu {ramo_atuacao}, o 
                                    intuito do planejamento estratégico conforme detalhado em {intuito_plano} e o publico algo {publico_alvo}.''',
                                    agent=agentes[9],
                                    output_file = 'SEO.md'
                                ),

                            #CRM
                                Task(
                                    description="Criar a estratégia de CRM.",
                                    expected_output=f'''Em portugês brasileiro, Uma abordagem centrada no cliente, visando segmentar e compreender profundamente as necessidades, comportamentos e expectativas 
                                    de diferentes grupos de clientes. Isso envolve a coleta e análise de dados relevantes, o desenvolvimento de estratégias de comunicação personalizadas, a 
                                    implementação de ferramentas de automação de marketing e o estabelecimento de programas de fidelidade e engajamento. 
                                    Além disso, é essencial otimizar o atendimento ao cliente, promover a retenção e maximizar o valor do cliente ao longo do 
                                    tempo, garantindo a integração de informações entre as equipes de marketing, vendas e atendimento para uma abordagem consistente e eficaz 
                                    para {nome_cliente} considerando seu {ramo_atuacao}, o intuito do planejamento estratégico conforme detalhado em {intuito_plano} e o 
                                    publico algo {publico_alvo}.''',
                                    agent=agentes[11],
                                    output_file = 'CRM.md'
                                ),

                            #Marca/Design
                                Task(
                                    description="Criar a estratégia de marca e design.",
                                    expected_output=f'''Em portugês brasileiro, Gerar guias para identidade visual e posicionamento claros e coerentes, alinhados com os valores, missão e visão da empresa. 
                                    Isso envolve a criação de um logotipo, paleta de cores, tipografia e outros elementos gráficos que transmitam a personalidade da marca, além de 
                                    definir uma voz e 
                                    tom consistentes na comunicação. A estratégia também deve garantir que a experiência do cliente seja reforçada por meio do design, criando uma 
                                    identidade que seja 
                                    facilmente reconhecível e que se conecte emocionalmente com o público-alvo. 
                                    Além disso, é importante monitorar e ajustar continuamente a percepção da marca no mercado para manter sua relevância e diferenciá-la da concorrência para 
                                    {nome_cliente} considerando seu {ramo_atuacao}, o intuito do planejamento estratégico conforme detalhado em {intuito_plano} e o publico alvo 
                                    {publico_alvo}.''',
                                    agent=agentes[12],
                                    output_file = 'Marca_Design.md'
                                ),

                                Task(
                                description='''
                                Sendo o mais detalhista possível e com a profundidade de um especialista em marketing digital, Levando em conta a análise PEST,
                                Tom de Voz, Buyer Persona, Brando Persona, Público alvo, posicionamento de marca, análise SWOT e golden circle gerados,
                                Criar as editorias de conteúdo da marca considerando a identidade, os objetivos da marca e o público-alvo.",
                                expected_output="Em portugês brasileiro, Editorias de conteúdo detalhadas e alinhadas com os objetivos da marca.''',
                                agent=agentes[8],
                                output_file='estrategia_conteudo.md'
                            )
                            ]

                        # Processo do Crew
                        equipe_pesquisa = Crew(
                            agents=agentes,
                            tasks=tarefas_pesquisa,
                            process=Process.hierarchical,
                            manager_llm=modelo_linguagem,
                            language='português brasileiro'
                        )

                        equipe_estrategica = Crew(
                            agents=agentes,
                            tasks=tarefas_estrategica,
                            process=Process.hierarchical,
                            manager_llm=modelo_linguagem,
                            language='português brasileiro'
                        )

                        equipe_midia = Crew(
                            agents=agentes,
                            tasks=tarefas_midia,
                            process=Process.hierarchical,
                            manager_llm=modelo_linguagem,
                            language='português brasileiro'
                        )

                        # Executa as tarefas do processo
                        resultado_pesquisa = equipe_pesquisa.kickoff()

                        # Executa as tarefas do processo
                        resultado_estrategica = equipe_estrategica.kickoff()

                        # Executa as tarefas do processo
                        resultado_midia = equipe_midia.kickoff()

                        #Printando Tarefas

                        st.header('1. Etapa de Pesquisa de Mercado')
                        st.subheader('1.1 Análise SWOT')
                        st.markdown(tarefas_pesquisa[0].output.raw)
                        st.subheader('1.2 Análise PEST')
                        st.markdown(tarefas_pesquisa[1].output.raw)
                

                        st.header('2. Etapa de Estratégica')
                        st.subheader('2.1 Golden Circle')
                        st.markdown(tarefas_estrategica[0].output.raw)
                        st.subheader('2.2 Posicionamento de Marca')
                        st.markdown(tarefas_estrategica[1].output.raw)
                        st.subheader('2.3 Brand Persona')
                        st.markdown(tarefas_estrategica[2].output.raw)
                        st.subheader('2.4 Buyer Persona')
                        st.markdown(tarefas_estrategica[3].output.raw)
                        st.subheader('2.5 Tom de Voz')
                        st.markdown(tarefas_estrategica[4].output.raw)
                        
                
                        st.header('3. Etapa de Planejamento de Mídias')
                        st.subheader('3.1 Plano para Criativos')
                        st.markdown(tarefas_midia[0].output.raw)
                        st.subheader('3.2 Plano de SEO')
                        st.markdown(tarefas_midia[1].output.raw)
                        st.subheader('3.3 Plano de CRM')
                        st.markdown(tarefas_midia[2].output.raw)
                        st.subheader('3.4 Plano de Design/Marca')
                        st.markdown(tarefas_midia[3].output.raw)
                        st.subheader('3.5 Estratégia de Conteúdo')
                        st.markdown(tarefas_midia[4].output.raw)

                        

                        save_to_mongo(tarefas_pesquisa,tarefas_estrategica,tarefas_midia , nome_cliente)



