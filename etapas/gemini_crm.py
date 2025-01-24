import streamlit as st
import google.generativeai as genai
import uuid
from pymongo import MongoClient
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from datetime import datetime
import os
from tavily import TavilyClient
from pymongo import MongoClient
import requests

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")



client = TavilyClient(api_key=t_api_key1)

client1 = TavilyClient(api_key='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')

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini

# Conexão com MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']
collection = db['auto_doc']
banco = client["arquivos_planejamento"]
db_clientes = banco["clientes"]  # info clientes

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

# Função para salvar no MongoDB
def save_to_mongo_CRM(fluxo_output, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano de CRM' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de CRM',
        "Fluxo": fluxo_output,

    }

    # Insere o documento no MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de CRM
def planej_crm_page():
    st.subheader('Planejamento de CRM')

    st.text('Aqui geramos plano para criativos, análise de saúde do site, sugestões de palavras chave, plano de CRM, plano de Design/Marca e estratégia de conteúdo.')
    
    # Buscar todos os clientes do banco de dados
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))

    # Criar uma lista para o selectbox
    opcoes_clientes = [cliente["nome"] for cliente in clientes]

    # Selectbox para escolher o cliente
    nome_cliente = st.text_input('Nome do cliente')

    # Obter as informações do cliente selecionado
    cliente_info = next((cliente for cliente in clientes if cliente["nome"] == nome_cliente), None)

    # Preencher os campos automaticamente com as informações do cliente
    if cliente_info:
        site_cliente = cliente_info["site"]
        ramo_atuacao = cliente_info["ramo"]
    else:
        site_cliente = ""
        ramo_atuacao = ""

    # Exibir os campos preenchidos com os dados do cliente
    st.text_input('Site do Cliente:', value=site_cliente, key="site_cliente")
    st.text_input('Ramo de Atuação:', value=ramo_atuacao, key="ramo_atuacao")
    intuito_plano = st.text_input('Intuito do Plano Estratégico:', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre")
    publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda")
    concorrentes = st.text_input('Concorrentes:', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C")
    site_concorrentes = st.text_input('Site dos Concorrentes:', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br")

    
    objetivos_opcoes = [
    'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
    'Entregar potenciais consumidores para a área comercial',
    'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
    'Fidelizar e reter um público fiel já convertido',
    'Garantir que o público esteja engajado com os canais ou ações da marca'
]
    # Objetivos de marca
    objetivos_de_marca = st.selectbox(
        'Selecione os objetivos de marca',
        objetivos_opcoes,  # Substitua 'objetivos_opcoes' com a lista de opções de objetivos que você deseja
        key="objetivos_marca"
    )



    referencia_da_marca = st.text_area(
        'O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?',
        key="referencias_marca",
        placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.",
        height=200  # Ajuste a altura conforme necessário
    )

    # Perguntas relacionadas ao serviço de CRM
    possui_ferramenta_crm = st.selectbox(
        'A empresa possui ferramenta de CRM?',
        ['Sim', 'Não'],
        key="possui_ferramenta_crm"
    )

    maturidade_crm = st.selectbox(
        'Qual é o nível de maturidade em CRM (histórico)?',
        ['Iniciante', 'Intermediário', 'Avançado'],
        key="maturidade_crm"
    )

    objetivo_crm = st.text_input(
        'Qual o objetivo ao utilizar o CRM?',
        key="objetivo_crm",
        placeholder="Ex: Melhorar a gestão de leads, otimizar relacionamento com clientes"
    )

    canais_disponiveis = st.text_input(
        'Quais canais de comunicação estão disponíveis?',
        key="canais_disponiveis",
        placeholder="Ex: E-mail, WhatsApp, Redes sociais"
    )

    perfil_empresa = st.selectbox(
        'Qual é o perfil da empresa?',
        ['B2B', 'B2C'],
        key="perfil_empresa"
    )

    metas_crm = st.text_input(
        'Quais metas a serem alcançadas com o CRM?',
        key="metas_crm",
        placeholder="Ex: Aumentar a taxa de conversão em 20%"
    )



    tamanho_base = st.selectbox(
        'Qual o tamanho da base de dados de clientes?',
        ['Pequena', 'Média', 'Grande'],
        key="tamanho_base"
    )


    tom_voz = st.text_area(
        'Qual o tom de voz desejado para a comunicação?',
        
        key="tom_voz",
         placeholder="Ex: Formal, informal, outro..."
    )

    fluxos_ou_emails = st.text_area(
        'Quais fluxos e/ou e-mails deseja trabalhar?',
        key="fluxos_ou_emails",
        placeholder="Ex: E-mail de boas-vindas, fluxos de nutrição de leads"
    )

    sla_entre_marketing_vendas = st.selectbox(
        'Há algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads?',
        ['Sim', 'Não'],
        key="sla_entre_marketing_vendas"
    )

    pest_files = 1

    crm_tools = client1.search("Quais são as 10 melhores ferramentas de CRM e por quê?")

    #DUCK DUCK GO SEARCH de tendências de CRM

    url = "https://duckduckgo8.p.rapidapi.com/"
    
    querystring = {"q":f"Quais são as tendências de CRM mais atuais?"}
    
    headers = {
    	"x-rapidapi-key": rapid_key,
    	"x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    tend_crm = response.text




    if pest_files is not None:
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
            if st.button('Iniciar Planejamento'):
                if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    with st.spinner('Gerando o fluxo de CRM...'):

                        # Aqui vamos gerar as respostas usando o modelo Gemini

                        prompt_fluxo = f''' Em português brasileiro,
                
                        Informações Gerais do Cliente:
                
                        O nome do cliente é {nome_cliente}, e seu site oficial pode ser acessado em {site_cliente}. A empresa está inserida no ramo de {ramo_atuacao} e o intuito principal deste plano estratégico é {intuito_plano}. O público-alvo da empresa são {publico_alvo}, e seus principais concorrentes incluem {concorrentes}, cujos sites são {site_concorrentes}.
                        Objetivos da Marca:
                        
                        O objetivo de marca selecionado para {nome_cliente} é {objetivos_de_marca}. A marca se destaca por {referencia_da_marca}.
                        Informações sobre o CRM:
                        
                        -{nome_cliente} possui uma ferramenta de CRM? {possui_ferramenta_crm}.
                        -A maturidade em CRM da empresa é {maturidade_crm}.
                        -O principal objetivo ao utilizar o CRM é {objetivo_crm}.
                        -Os canais de comunicação disponíveis para CRM são {canais_disponiveis}.
                        -O perfil da empresa é {perfil_empresa}.
                        -As metas que a empresa busca alcançar com o CRM são {metas_crm}.
                        -O tamanho da base de dados de clientes é {tamanho_base}.
                        -O tom de voz desejado para a comunicação é {tom_voz}.
                        -Os fluxos e e-mails que a empresa deseja trabalhar são: {fluxos_ou_emails}.
                        -Existe algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads? {sla_entre_marketing_vendas}.
                
                        - Proposta de fluxo de CRM de um especialista com embasamento extremamente aprofundado, detalhado e acadêmico do porque de cada etapa com um cronomgrama 
                        extremamente eficaz e detalhado de nutrição de leads que melhor atenda as necessidades do cliente e se melhor encaixe com suas características de negócio. Cada etapa extremamente detalhada com exatamente
                        o que deve ser feito e porque. O Fluxo deve deliear o passo a passo da interação com os leads desde o primeiro até o último contato de forma bem detalhada e justificada. Detalhando o 
                        canal de contato, tempo de duração de cada etapa, tom a ser utilizado, ação personalizada para o case específico do cliente {nome_cliente} para cada segmento de seu setor de atuação:
                        {ramo_atuacao}. Leve em consideração como isso seria aplicado levando em conta as ferramentas de CRM mais atuais explicitadas em: ({crm_tools}), assim como
                        a pesquisa de tendências de CRM explicitada em: ({tend_crm}).

                        defina uma tabela com as colunas: Etapa	Duração	Ações Principais
                        '''
                        fluxo_output = modelo_linguagem.generate_content(prompt_fluxo).text



                        prompt_emails = f''' 

                        Considerando o plano detalhado em ({fluxo_output}).

                        - Redija os emails de contato
                        - Rejida os formulários
                        - Redija as mensagens.
                        
                        '''
                        emails_output = modelo_linguagem.generate_content(prompt_emails).text




                      

                        # Exibe os resultados na interface
                        st.header('Plano de Fluxo de CRM')
                        st.subheader('Fluxo')
                        st.markdown(fluxo_output)
                        st.subheader('Emails')
                        st.markdown(emails_output)

                        

                        # Salva o planejamento no MongoDB
                        save_to_mongo_CRM(fluxo_output, nome_cliente)
