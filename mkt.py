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
import SEOtools
from equipe import agentes




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

    # Step 2. Executing a simple search query
    politic = client1.search("Considerando o cliente {nome_cliente} no ramo de atuação {ramo_atuacao}, Como está a situação política no brasil atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital?")
    economic = client1.search("Considerando o cliente {nome_cliente} no ramo de atuação {ramo_atuacao}, Como está a situação econômica no brasil atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital??")
    social = client1.search("Considerando o cliente {nome_cliente} no ramo de atuação {ramo_atuacao}, Como está a situação social no brasil atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital??")
    tec = client1.search("Considerando o cliente {nome_cliente} no ramo de atuação {ramo_atuacao}, Quais as novidades tecnológicas no context brasileiro atualmente em um contexto geral e de forma detalhada para planejamento estratégico de marketing digital??")


    performance_metrics_df = SEOtools.check_website_performance(site_cliente)
    website_all_texts = SEOtools.scrape_all_texts(site_cliente)


  

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

                    

                        # Criando tarefas correspondentes aos agentes
                        tarefas_pesquisa = [
                                
                                Task(
                                    description="Criar a Matriz SWOT.",
                                    expected_output=f'''Considerando o seguinte contexto (texto raspado do site do cliente {nome_cliente}) :{website_all_texts},e a referência da marca:
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
                                    description="Análise PEST.",
                                    expected_output=f'''Análise PEST com pelo menos 10 pontos relevantes em cada etapa em português brasileiro 
                                    considerando     contexto político: {politic}, contexto econômico: {economic}, contexto social: {social}, contexto tecnológico: {tec}.
                                    Quero pelo menos 10 pontos em cada segmento da análise PEST. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing.''',
                                    agent=agentes[1],
                                    output_file = 'pest.md'
                                )
                            
                        ]


                        
                        tarefas_estrategica = [
                                
                                
                                Task(
                                    description="Desenvolver o Golden Circle.",
                                    expected_output=f'''Golden Circle completo com 'how', 'why' e 'what' resumidos 
                                    em uma frase cada em português brasileiro. Considerando o seguinte contexto (texto raspado do site do cliente {nome_cliente}) 
                                    :{website_all_texts}, e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca},''',
                                    agent=agentes[3],
                                    output_file = 'GC.md'
                                ),
                                Task(
                                    description="Criar o posicionamento de marca.",
                                    expected_output=f'''Posicionamento de marca em uma única frase em português brasileiro. 
                                    Considerando o seguinte contexto (texto raspado do site do cliente {nome_cliente}) :{website_all_texts}
                                    , e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca},''',
                                    agent=agentes[2],
                                    output_file = 'posMar.md'
                                ),
                                Task(
                                    description="Criar a Brand Persona.",
                                    expected_output=f'''2 Brand Personas detalhada, alinhada com a marca do {nome_cliente} que é do setor de atuação {ramo_atuacao} em português brasileiro considerando o 
                                    seguinte contexto (texto raspado do site do cliente {nome_cliente}) :{website_all_texts}
                                    , e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
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
                                    Retorne entre 10 a 15 adjetivos que definem o tom com suas respectivas explicações. ex: tom é amigavel, para transparecer uma 
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
                        
                
                    
                        save_to_mongo(tarefas_pesquisa,tarefas_estrategica,tarefas_midia , nome_cliente)





