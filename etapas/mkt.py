__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from crewai_tools import tool
import os
from tavily import TavilyClient
from pymongo import MongoClient



# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")

# Configure the Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

client = TavilyClient(api_key=t_api_key1)



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
collection = db['auto_doc'] #docs gerados

banco = client["arquivos_planejamento"]
db_clientes = banco["clientes"]  #info clientes

import uuid

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

def save_to_mongo(tarefas_pesquisa,tarefas_estrategica, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepare the document to be inserted into MongoDB
    task_outputs = {
        "id_planejamento":'Plano Estratégico e de Planejamento' +'_'+ nome_cliente + '_' + id_planejamento,  # Use o ID gerado como chave
        "nome_cliente": nome_cliente,  # Adiciona o nome do cliente ao payload
        "tipo_plano": 'Plano Estratégico e de Planejamento',
        "SWOT": tarefas_pesquisa[0].output.raw,
        "PEST": tarefas_pesquisa[2].output.raw,
        "Tendencias": tarefas_pesquisa[1].output.raw,

        
        "GC": tarefas_estrategica[0].output.raw,
        "Posicionamento_Marca": tarefas_estrategica[1].output.raw,
        "Brand_Persona": tarefas_estrategica[2].output.raw,
        "Buyer_Persona": tarefas_estrategica[3].output.raw,
        "Tom_Voz": tarefas_estrategica[4].output.raw,
     
    }

    # Insert the document into MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")






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
    # Buscar todos os clientes do banco de dados
    clientes = list(db_clientes.find({}, {
        "_id": 0, 
        "nome": 1, 
        "site": 1, 
        "ramo": 1, 
        "concorrentes": 1, 
        "intuito": 1, 
        "publicoAlvo": 1, 
        "referenciaMarca": 1, 
        "siteConcorrentes": 1
    }))

    # Criar uma lista para o selectbox
    opcoes_clientes = [cliente["nome"] for cliente in clientes]

    # Selectbox para escolher o cliente
    nome_cliente = st.selectbox('Selecione o Cliente:', opcoes_clientes, key="nome_cliente")

    # Obter as informações do cliente selecionado
    cliente_info = next((cliente for cliente in clientes if cliente["nome"] == nome_cliente), None)

    # Preencher os campos automaticamente com as informações do cliente
    if cliente_info:
        site_cliente = cliente_info.get("site", "")
        ramo_atuacao = cliente_info.get("ramo", "")
        concorrentes = cliente_info.get("concorrentes", "")
        site_concorrentes = cliente_info.get("siteConcorrentes", "")
        intuito_plano = cliente_info.get("intuito", "")
        publico_alvo = cliente_info.get("publicoAlvo", "")
        referencia_da_marca = cliente_info.get("referenciaMarca", "")
    else:
        site_cliente = ""
        ramo_atuacao = ""
        concorrentes = ""
        site_concorrentes = ""
        intuito_plano = ""
        publico_alvo = ""
        referencia_da_marca = ""

    # Exibir os campos preenchidos com os dados do cliente
    st.text_input('Site do Cliente:', value=site_cliente, key="site_cliente")
    st.text_input('Ramo de Atuação:', value=ramo_atuacao, key="ramo_atuacao")
    st.text_input('Concorrentes:', value=concorrentes, key="concorrentes")
    st.text_input('Site dos Concorrentes:', value=site_concorrentes, key="site_concorrentes")
    st.text_input('Intuito do Plano Estratégico:', value=intuito_plano, key="intuito_plano")
    st.text_input('Público-Alvo:', value=publico_alvo, key="publico_alvo")
    st.text_area(
        'Referência da Marca:', 
        value=referencia_da_marca, 
        key="referencia_da_marca", 
        height=200  
    )


    # Criando o selectbox com as opções definidas
    objetivos_de_marca = st.selectbox(
        'Selecione os objetivos de marca',
        objetivos_opcoes,
        key="objetivos_marca"
    )
   

    # Tendências
    tendencias = st.text_input('Quais tendências gostaria que o agente pesquisasse?',placeholder="Ex: IA, otimização de CRM, ...")


  
    


    st.subheader("(Opcional) Suba os Arquivos Estratégicos (PDF) (Único ou múltiplos)")
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)

    # Set parameters for the search
    days = 90
    max_results = 15
    
    politic = client1.search(
        f'''Como está a situação política no brasil atualmente em um contexto geral e de forma detalhada para planejamento 
        estratégico de marketing digital no contexto do ramo de atuação: {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )
    
    economic = client1.search(
        f'''Como está a situação econômica no brasil atualmente em um contexto geral e de forma detalhada para 
        planejamento estratégico de marketing digital no contexto do ramo de atuação: {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )
    
    social = client1.search(
        f'''Como está a situação social no brasil atualmente em um contexto geral e de forma detalhada para planejamento
        estratégico de marketing digital no contexto do ramo de atuação: {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )
    
    tec = client1.search(
        f'''Quais as novidades tecnológicas no context brasileiro atualmente em um contexto geral e de forma detalhada para
        planejamento estratégico de marketing digital no contexto do ramo de atuação: {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )
    
    tend_novids = client1.search(
        f'''Quais as recentes tendências de mercado para {tendencias}?''',
        days=days, 
        max_results=max_results
    )
    
    tend_ramo = client1.search(
        f'''Quais as recentes tendências de mercado para o ramo de atuação do cliente explicitado em: {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )



  

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


                        agentes = [
                            Agent(
                                role="Líder e revisor geral de estratégia",
                                goal=f'''Aprenda sobre revisão geral de estratégia em {pest_files}. Revisar toda a estratégia de {nome_cliente} e garantir 
                                alinhamento com os {objetivos_de_marca}, o público-alvo {publico_alvo} e as {referencia_da_marca}.''',
                                backstory=f'''Você é Philip Kotler, renomado estrategista de marketing, usando todo o seu conhecimento 
                                avançado em administração de marketing como nos documentos de {pest_files}, liderando o planejamento de {nome_cliente} no 
                                ramo de {ramo_atuacao} em português brasileiro.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Analista PEST",
                                goal=f'''Aprenda sobre análise PEST em {pest_files}. Realizar a análise PEST para o cliente {nome_cliente} em português brasileiro.''',
                                backstory=f'''Você é Philip Kotler, liderando a análise PEST para o planejamento estratégico de {nome_cliente} em português brasileiro. 
                                Levando em conta as informações coletadas em {politic}, {economic}, {social} e {tec} realize a análise PEST, essas informações são o que a sua 
                                análise PEST deve se basear em. Você está realizando essa análise PEST para o cliente {nome_cliente} que é do setor de atuação {ramo_atuacao}.
                                O intuito do planejamento estratégico está explicitado em {intuito_plano}. Você possui uma vasta experiência em desenvolver análises PEST relevantes,
                                perspicazes e detalhadas. Você sabe exatamente como extrair informações relevantes para o crescimento de seus clientes.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Analista SWOT",
                                goal=f'''Aprenda sobre análise SWOT e crie a análise para {nome_cliente}, com base nos dados de mercado disponíveis.''',
                                backstory='''Você é um analista de marketing focado em realizar uma análise SWOT completa com dados extraídos de fontes diversas, como documentos PDF e CSV.''',
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
                                goal=f'''Analisar a estratégia de preços para {nome_cliente}, utilizando dados de mercado e concorrência.''',
                                backstory=f'''Você é um consultor de pricing experiente e ajudará {nome_cliente} a entender as melhores práticas
                                de precificação com base na análise de mercado e concorrência.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Analista de Segmentação de Mercado",
                                goal=f'''Segmentar o mercado para {nome_cliente} com base nos dados de concorrentes e no perfil do público-alvo.''',
                                backstory=f'''Você é um analista de mercado com a missão de segmentar o público de {nome_cliente} e gerar insights acionáveis
                                para o planejamento de marketing.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Criador de Persona",
                                goal=f'''Desenvolver personas para o {nome_cliente} com base nos dados de público-alvo e concorrência.''',
                                backstory=f'''Você é um especialista em marketing digital, com o objetivo de criar personas detalhadas para 
                                {nome_cliente}, que ajudem a direcionar a comunicação de marketing.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Estratégia de Mídia Social",
                                goal=f'''Desenvolver uma estratégia de mídia social para {nome_cliente} com base nas análises de mercado e público-alvo.''',
                                backstory=f'''Você é um especialista em mídia social, com foco em ajudar marcas a maximizar sua presença nas
                                plataformas de mídia social com base em dados do mercado.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em Inbound Marketing",
                                goal=f'''Desenvolver uma estratégia de inbound marketing para {nome_cliente}, com foco em atrair e converter leads.''',
                                backstory=f'''Você é um especialista em inbound marketing, utilizando as melhores práticas 
                                para atrair e engajar clientes em potencial para {nome_cliente}.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em SEO",
                                goal=f'''Melhorar o SEO de {nome_cliente}''',
                                backstory=f'''Você é um especialista em SEO, com o objetivo de melhorar a visibilidade do site de {nome_cliente} 
                                nos motores de busca, com base na análise do conteúdo existente e da concorrência.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em Criativos",
                                goal=f'''Desenvolver criativos da campanha de {nome_cliente}, com base no {ramo_atuacao}, {intuito_plano} e {publico_alvo}.''',
                                backstory=f'''Você é um especialista em Criativos de marketing digital, você é original, detalhista, 
                                minucioso, criativo, com uma vasta experiência de mercado lidando com uma gama de empresas que atingiram sucesso por conta do seu 
                                extenso repertório profissional, com o objetivo de trazer o máximo de atenção às campanhas do cliente. 
                                Tornando-as relevantes e fazendo com que o cliente atinja seus objetivos.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            
                            Agent(
                                role="Especialista em CRM",
                                goal=f'''Desenvolver estratégias de CRM para o cliente: {nome_cliente}.''',
                                backstory=f'''Você é um especialista em CRM. você é original, detalhista, minucioso, 
                                criativo, com uma vasta experiência de mercado lidando com uma gama de empresas que atingiram sucesso por conta do seu extenso 
                                repertório profissional, Você sabe estabelecer relações durarouras com clientes e sabe tudo que há de se
                                saber para detalhar planos de como firmar e continuar relacionamentos estratégicos com clientes.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            
                            Agent(
                                role="Especialista em Marca/Design",
                                goal=f'''Desenvolver ideias de Marca/Design do cliente: {nome_cliente}.''',
                                backstory=f'''Você é um especialista em Marca/Design, você é original, detalhista, minucioso, criativo, 
                                com uma vasta experiência de mercado lidando com uma gama de empresas que atingiram sucesso por conta do seu extenso repertório profissional, 
                                com o objetivo de melhorar a visibilidade de {nome_cliente} trazendo a sua marca
                                de uma forma coerente e chamativa.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),

                            Agent(
                                role="Especialista em SEO",
                                goal=f'''Melhorar o SEO de {nome_cliente}, com base na análise do site e na concorrência.''',
                                backstory=f'''Você é um especialista em SEO, você é analítico, detalhista, minucioso, criativo, 
                                com uma vasta experiência de mercado lidando com uma gama de empresas que atingiram sucesso por conta do seu extenso repertório 
                                profissional, com o objetivo de melhorar a visibilidade do site de {nome_cliente} nos motores de busca, com base na análise do
                                conteúdo existente e da concorrência.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Especialista em Redes Sociais",
                                goal=f'''Estabelecer o plano de atuação em redes sociais de {nome_cliente} no planejamento estratégico, com base na análise do site e na concorrência.''',
                                backstory=f'''Você é um especialista em marketing em redes sociais, 
                                você é original, detalhista, minucioso, criativo, com uma vasta experiência de mercado lidando com uma gama de 
                                empresas que atingiram sucesso por conta do seu extenso repertório profissional, com o objetivo de melhorar a visibilidade nas campanhas 
                                {nome_cliente}, com base na análise do conteúdo existente e da concorrência.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                            Agent(
                                role="Analista de Tendências",
                                goal=f'''Analista de tendências de mercado em prol do cliente: {nome_cliente} para o  planejamento estratégico.''',
                                backstory=f'''Você é um especialista em marketing e análise de tendências no ramo de atuação {ramo_atuacao}, 
                                você é original, detalhista, minucioso, criativo, com uma vasta experiência de mercado lidando com uma gama de 
                                empresas que atingiram sucesso por conta do seu extenso repertório profissional, com o objetivo de encontrar aspectos chaves no mercado
                                para o melhor aproveitamento de marketing.''',
                                allow_delegation=False,
                                llm=modelo_linguagem,
                                tools=[]
                            ),
                        ]

                    

                        # Criando tarefas correspondentes aos agentes
                        tarefas_pesquisa = [
                                
                                Task(
                                    description="Criar a Matriz SWOT.",
                                    expected_output=f'''Considerando o seguinte contexto a referência da marca:
                                    {referencia_da_marca},
                                    realize a Análise SWOT completa em formato de tabela em português brasileiro. 
                                    Quero pelo menos 10 pontos em cada segmento da análise SWOT. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing. 
                                    Cada ponto deve ser pelo menos 3 frases detalhadas, profundas e não genéricas. 
                                    Você estáa aqui para trazer conhecimento estratégico. organize os pontos em bullets
                                    pra ficarem organizados dentro de cada segmento da tabela.''',
                                    agent=agentes[6],
                                    output_file = 'SWOT.md'
                                ),
                                Task(
                                    description="Pesquisa de tendências.",
                                    expected_output=f'''em português brasileiro, Relatório extremamente detalhado de Análise de tendências consideranto as respostas da pesquisa obtidas em tendências de novidades: ({tend_novids}) e 
                                    tendências de ramo de atuação do cliente: ({tend_ramo}).
                                    
                                    Realize um relatório detalhado e formal de todas as tendências e como isso pode ser usado no planejamento estratégico.''',
                                    agent=agentes[15],
                                    output_file = 'tendencia.md'
                                ),
                                Task(
                                    description="Análise PEST.",
                                    expected_output=f'''Análise PEST com pelo menos 10 pontos relevantes em cada etapa em português brasileiro 
                                    considerando     contexto político: {politic}, contexto econômico: {economic}, contexto social: {social}, contexto tecnológico: {tec}.
                                    Quero pelo menos 10 pontos em cada segmento da análise PEST. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing.''',
                                    agent=agentes[1],
                                    output_file = 'pest.md'
                                ),
                            
                            
                        ]


                        
                        tarefas_estrategica = [
                                
                                
                                Task(
                                    description="Desenvolver o Golden Circle.",
                                    expected_output=f'''Golden Circle completo com 'how', 'why' e 'what' resumidos 
                                    em uma frase cada em português brasileiro. Considerando o seguinte contexto 
                                     e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca},''',
                                    agent=agentes[3],
                                    output_file = 'GC.md'
                                ),
                                Task(
                                    description="Criar o posicionamento de marca.",
                                    expected_output=f'''Em português brasileiro,. 
                            
                                    
                                    5 Posicionamentos de marca para o cliente {nome_cliente} do ramo de atuação {ramo_atuacao} Com um slogan com essa inspiração:
                                    
                                    "Pense diferente."
                                    "Abra a felicidade."
                                    "Just do it."
                                    "Acelere a transição do mundo para energia sustentável."
                                    "Amo muito tudo isso."
                                    "Red Bull te dá asas."
                                    "Compre tudo o que você ama."
                                    "Porque você vale muito."
                                    "Viva a vida ao máximo."
                                    "O melhor ou nada."
                                    "Organizar as informações do mundo e torná-las acessíveis e úteis."
                                    "A máquina de condução definitiva."
                                    "Onde os sonhos se tornam realidade."
                                    "Impossible is nothing."
                                    "Abra a boa cerveja."
                                    "Para um dia a dia melhor em casa."
                                    "Be moved."
                                    "Go further."
                                    "Inspire o mundo, crie o futuro."
                                    "Vamos juntos para o futuro.",

                                    e Uma frase detalhada.

                                    
                                    
                                    ''',
                                    agent=agentes[2],
                                    output_file = 'posMar.md'
                                ),
                                Task(
                                    description="Criar a Brand Persona.",
                                    expected_output=f'''2 Brand Personas detalhada, alinhada com a marca do {nome_cliente} que é do setor de atuação {ramo_atuacao} em português brasileiro considerando o 
                                    seguinte contexto 
                                    
                                    o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca},. 
                                    
                                    - Defina seu nome (deve ser o nome de uma pessoa normal como fernando pessoa, maria crivellari, etc)
                                    -Defina seu gênero, faixa de idade, qual a sua bagagem, defina sua personalidade. 
                                    -Defina suas características: possui filhos? É amigável? quais seus objetivos? qual seu repertório? O que gosta de fazer?
                                    -Comunicação: Como se expressa? Qual o seu tom? Qual o seu linguajar?''',
                                    agent=agentes[4],
                                    output_file = 'BP.md'
                                ),
                                Task(
                                    description="Definir a Buyer Persona e o Público-Alvo.",
                                    expected_output=f'''Descrição detalhada da buyer persona considerando o público-alvo: {publico_alvo} e o 
                                    objetivo do plano estratégico como descrito em {intuito_plano} com os seguintes atributos enunciados: 
                                    nome fictício, idade, gênero, classe social, objetivos,  vontades, Emoções negativas (o que lhe traz anseio, aflinge, etc), Emoções positivas,
                                    quais são suas dores, quais são suas objeções, quais são seus resultados dos sonhos,
                                    suas metas e objetivos e qual o seu canal favorito (entre facebook, instagram, whatsapp, youtube ou linkedin), em português brasileiro. 
                                    Crie oito buyer personas.''', 
                                    agent=agentes[5],
                                    output_file = 'BuyerP.md'
                                ),
                                Task(
                                    description="Definir o Tom de Voz.",
                                    expected_output=f'''Descrição do tom de voz, incluindo nuvem de palavras e palavras proibidas. 
                                    Retorne 10 adjetivos que definem o tom com suas respectivas explicações. ex: tom é amigavel, para transparecer uma 
                                    relação de confiança com frases de exemplo de aplicação do tom em português brasileiro.''',
                                    agent=agentes[7],
                                    output_file = 'TV.md'
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


                        # Executa as tarefas do processo
                        resultado_pesquisa = equipe_pesquisa.kickoff()

                        # Executa as tarefas do processo
                        resultado_estrategica = equipe_estrategica.kickoff()

                       
                        #Printando Tarefas

                        st.header('1. Etapa de Pesquisa de Mercado')
                        st.subheader('1.1 Análise SWOT')
                        st.markdown(tarefas_pesquisa[0].output.raw)
                        st.subheader('1.2 Análise PEST')
                        st.markdown(tarefas_pesquisa[2].output.raw)
                        st.subheader('1.3 Análise de tendências')
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
                        
                
                    
                        save_to_mongo(tarefas_pesquisa,tarefas_estrategica , nome_cliente)






