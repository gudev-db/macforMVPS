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


client = TavilyClient(api_key=t_api_key1)

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.225,
    frequency_penalty=0.5
)

client1 = TavilyClient(api_key='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')

# Connect to MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']  # Replace with your database name
collection = db['auto_doc'] 

banco = client["arquivos_planejamento"]
db_clientes = banco["clientes"]  #info clientes


import uuid

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

def save_to_mongo_crm(tarefas_crm, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepare the document to be inserted into MongoDB
    task_outputs = {
        "id_planejamento": nome_cliente + '_' + 'CRM' + '_' + id_planejamento,  # Use o ID gerado como chave
        "nome_cliente": nome_cliente,  # Adiciona o nome do cliente ao payload
        "tipo_planejamento": 'CRM',
        "Plano_Estrategia_CRM": tarefas_crm[0].output.raw,
        "Plano_Fluxo_CRM": tarefas_crm[1].output.raw,
        "Plano_Contato_Email": tarefas_crm[2].output.raw,
        "Plano_Contato_SMS_WhatsApp": tarefas_crm[3].output.raw,
        "Plano_Contato_NPS": tarefas_crm[4].output.raw,
        "Recomend_Software": tarefas_crm[5].output.raw
    }

    # Insert the document into MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento de CRM gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")









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


def planej_crm_page():
    st.subheader('Planejamento de CRM')

    st.text('Aqui geramos plano para criativos, análise de saúde do site, sugestões de palavras chave, plano de CRM, plano de Design/Marca e estratégia de conteúdo.')
    
    # Buscar todos os clientes do banco de dados
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))

    # Criar uma lista para o selectbox
    opcoes_clientes = [cliente["nome"] for cliente in clientes]

    # Selectbox para escolher o cliente
    nome_cliente = st.selectbox('Selecione o Cliente:', opcoes_clientes, key="nome_cliente")

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

    descricao_negocio = st.text_area(
        'Descrição do negócio:',
        key="descricao_negocio",
        placeholder="Ex: Empresa especializada em produtos eletrônicos."
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
                    with st.spinner('Gerando o planejamento de CRM...'):

                        agentes_crm = [
    Agent(
        role="Estratégia Geral de CRM",
        goal=f'''Desenvolver e executar a estratégia geral de CRM para {nome_cliente}, levando em consideração o ramo de atuação ({ramo_atuacao}), 
        os objetivos de marca ({objetivos_de_marca}), o público-alvo ({publico_alvo}), o tom de voz ({tom_voz}), os canais de comunicação disponíveis 
        ({canais_disponiveis}), e as metas a serem alcançadas ({metas_crm}). A estratégia deve estar alinhada com os valores e diferenciais da marca 
        ({referencia_da_marca}) e o perfil da empresa ({perfil_empresa}).''',
        backstory=f'''Você é um especialista em CRM com ampla experiência em desenvolver e executar estratégias de CRM para empresas como {nome_cliente}, 
        que atuam no ramo de {ramo_atuacao}. Com base nas informações coletadas, como os objetivos de marca ({objetivos_de_marca}), público-alvo 
        ({publico_alvo}), tom de voz ({tom_voz}) e canais de comunicação ({canais_disponiveis}), você criará uma estratégia de CRM personalizada, 
        que alinha todas as iniciativas com os valores e diferenciais de {nome_cliente}. Além disso, é importante garantir que as metas de CRM 
        ({metas_crm}) sejam atingidas, otimizando os fluxos e campanhas de comunicação de acordo com o perfil da empresa ({perfil_empresa}).''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    ),
    Agent(
        role="Análise de Dados CRM",
        goal=f'''Analisar os dados de clientes de {nome_cliente}, segmentando-os com base nos dados coletados de público-alvo ({publico_alvo}), 
        metas de CRM ({metas_crm}), canais de comunicação ({canais_disponiveis}) e a base de clientes disponível ({tamanho_base}). 
        Identificar padrões de comportamento para otimizar os fluxos de comunicação e campanhas de marketing. A análise deve considerar as 
        segmentações e o perfil da empresa ({perfil_empresa}).''',
        backstory=f'''Você é um analista de dados especializado em CRM. Sua missão é segmentar a base de dados de clientes de {nome_cliente}, 
        utilizando os dados coletados, como o perfil do público-alvo ({publico_alvo}), canais de comunicação disponíveis ({canais_disponiveis}), 
        tamanho da base de dados ({tamanho_base}), e as metas de CRM ({metas_crm}). Você usará essas informações para identificar padrões 
        e otimizar os fluxos de comunicação e as campanhas de marketing de maneira eficaz, alinhando todas as ações com o perfil da empresa ({perfil_empresa}).''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    ),
    Agent(
        role="Gestão de Leads e Fluxos CRM",
        goal=f'''Desenvolver e implementar fluxos de CRM para {nome_cliente}, com foco em nutrição de leads e melhoria da jornada do cliente. 
        Utilizando canais de comunicação disponíveis ({canais_disponiveis}), com base nos objetivos de CRM ({objetivo_crm}) e metas ({metas_crm}). 
        Criar fluxos personalizados e campanhas direcionadas para o público-alvo ({publico_alvo}) e conforme o perfil da empresa ({perfil_empresa}).''',
        backstory=f'''Você é um especialista em CRM com foco na criação e otimização de fluxos de nutrição de leads para {nome_cliente}. 
        Considerando os canais de comunicação disponíveis ({canais_disponiveis}), os objetivos de CRM ({objetivo_crm}), metas a serem alcançadas ({metas_crm}), 
        e o perfil do público-alvo ({publico_alvo}), sua missão é desenvolver fluxos de CRM e campanhas de nutrição de leads que aumentem a conversão 
        e melhorem o engajamento do público-alvo. Todos os fluxos devem estar alinhados com o perfil da empresa ({perfil_empresa}).''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    ),
    Agent(
        role="Gestão de Relacionamento com Clientes",
        goal=f'''Desenvolver e implementar estratégias de gestão de relacionamento com clientes para {nome_cliente}, com foco em fidelização e 
        retenção, utilizando dados de público-alvo ({publico_alvo}), canais de comunicação ({canais_disponiveis}), e metas de CRM ({metas_crm}). 
        Criar campanhas personalizadas para melhorar o engajamento ao longo da jornada do cliente, ajustadas ao perfil da empresa ({perfil_empresa}).''',
        backstory=f'''Você é um especialista em CRM com foco em gestão de relacionamento com clientes (CRM). Sua missão é desenvolver 
        estratégias personalizadas de fidelização e retenção para {nome_cliente}, utilizando os dados do público-alvo ({publico_alvo}), canais 
        de comunicação ({canais_disponiveis}) e as metas de CRM ({metas_crm}). Ao longo da jornada do cliente, você criará campanhas 
        personalizadas, alinhadas com o perfil da empresa ({perfil_empresa}), visando aumentar a satisfação e a longevidade dos clientes.''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    ),
    Agent(
        role="Análise de Performance de CRM",
        goal=f'''Analisar a performance das estratégias de CRM implementadas para {nome_cliente}, ajustando conforme necessário com base em 
        métricas de sucesso, taxas de conversão e feedback dos clientes. Verificar a aderência dos resultados com as metas de CRM ({metas_crm}) 
        e ajustar os fluxos e campanhas conforme as necessidades do público-alvo ({publico_alvo}) e o perfil da empresa ({perfil_empresa}).''',
        backstory=f'''Você é um especialista em análise de performance de CRM. Sua missão é avaliar e monitorar os resultados das estratégias de CRM 
        implementadas para {nome_cliente}. Você utilizará métricas de sucesso, taxas de conversão e feedback dos clientes para ajustar as 
        campanhas de CRM e garantir que as metas de CRM ({metas_crm}) sejam atingidas. A análise deve estar alinhada com os dados de público-alvo 
        ({publico_alvo}) e o perfil da empresa ({perfil_empresa}).''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    ),
    Agent(
        role="Especialista em Automação de CRM",
        goal=f'''Desenvolver e implementar automações de CRM para {nome_cliente}, com foco em otimizar o gerenciamento de leads e a comunicação 
        com clientes em diferentes estágios da jornada de compra. As automações devem ser baseadas nos canais de comunicação disponíveis 
        ({canais_disponiveis}) e ajustadas ao perfil do público-alvo ({publico_alvo}). Assegurar que todos os fluxos automatizados atendam 
        às metas de CRM ({metas_crm}).''',
        backstory=f'''Você é um especialista em automação de CRM. Sua missão é otimizar o gerenciamento de leads e a comunicação com clientes 
        em {nome_cliente}, usando os canais de comunicação disponíveis ({canais_disponiveis}) e garantindo que os fluxos de CRM sejam automatizados 
        para aumentar a eficiência, melhorar a personalização e alcançar as metas de CRM ({metas_crm}). As automações devem ser criadas com base 
        nas necessidades do público-alvo ({publico_alvo}) e adaptadas ao perfil da empresa ({perfil_empresa}).''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    ),
    Agent(
        role="Consultor de SLA CRM",
        goal=f'''Analisar o SLA (Service Level Agreement) entre marketing e vendas para {nome_cliente}, garantindo que as expectativas 
        de tempo e qualidade na geração de leads sejam cumpridas, utilizando o CRM para ajustar os fluxos e otimizar a colaboração entre as 
        equipes. Verificar como as metas de CRM ({metas_crm}) e os canais de comunicação ({canais_disponiveis}) podem impactar essa colaboração.''',
        backstory=f'''Você é um consultor de CRM especializado em gerenciar a relação entre marketing e vendas. Sua missão é garantir que o SLA 
        (Service Level Agreement) entre essas equipes seja cumprido, melhorando o alinhamento e a colaboração para gerar leads de qualidade. 
        Você utilizará os dados de metas de CRM ({metas_crm}), canais de comunicação ({canais_disponiveis}), e a segmentação do público-alvo 
        ({publico_alvo}) para otimizar os fluxos e melhorar a comunicação e colaboração entre marketing e vendas.''',
        allow_delegation=False,
        llm=modelo_linguagem,
        tools=[]
    )
]





                       
                        tarefas_crm = [
    # Task de Estratégia Geral de CRM
    Task(
        description="Criar a estratégia geral de CRM para o cliente.",
        expected_output=f'''
        **Estratégia Geral de CRM para {nome_cliente}**

        Informações Gerais do Cliente:

        O nome do cliente é {nome_cliente}, e seu site oficial pode ser acessado em {site_cliente}. A empresa está inserida no ramo de {ramo_atuacao} e o intuito principal deste plano estratégico é {intuito_plano}. O público-alvo da empresa são {publico_alvo}, e seus principais concorrentes incluem {concorrentes}, cujos sites são {site_concorrentes}.
        Objetivos da Marca:
        
        O objetivo de marca selecionado para {nome_cliente} é {objetivos_de_marca}. A marca se destaca por {referencia_da_marca}.
        Informações sobre o CRM:
        
        {nome_cliente} possui uma ferramenta de CRM? {possui_ferramenta_crm}.
        A maturidade em CRM da empresa é {maturidade_crm}.
        O principal objetivo ao utilizar o CRM é {objetivo_crm}.
        Os canais de comunicação disponíveis para CRM são {canais_disponiveis}.
        O perfil da empresa é {perfil_empresa}.
        As metas que a empresa busca alcançar com o CRM são {metas_crm}.
        A descrição do negócio é: {descricao_negocio}.
        O tamanho da base de dados de clientes é {tamanho_base}.
        O tom de voz desejado para a comunicação é {tom_voz}.
        Os fluxos e e-mails que a empresa deseja trabalhar são: {fluxos_ou_emails}.
        Existe algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads? {sla_entre_marketing_vendas}.

     

        **Ações e Segmentação**:
        - **Segmentação de Clientes**: Definição de segmentação de clientes com base em: 
        **Público-alvo**: {publico_alvo}, **Canais disponíveis**: {canais_disponiveis},
        **Metas de CRM**: {metas_crm} e **Intuito do plano estratégico**: {intuito_plano}


        ''',
        agent=agentes_crm[0],
        output_file='estrategia_crm.md'
    ),

    # Task de Fluxo de CRM
    Task(
        description="Fluxo de CRM.",
        expected_output=f''' Em português brasileiro,

        Informações Gerais do Cliente:

        O nome do cliente é {nome_cliente}, e seu site oficial pode ser acessado em {site_cliente}. A empresa está inserida no ramo de {ramo_atuacao} e o intuito principal deste plano estratégico é {intuito_plano}. O público-alvo da empresa são {publico_alvo}, e seus principais concorrentes incluem {concorrentes}, cujos sites são {site_concorrentes}.
        Objetivos da Marca:
        
        O objetivo de marca selecionado para {nome_cliente} é {objetivos_de_marca}. A marca se destaca por {referencia_da_marca}.
        Informações sobre o CRM:
        
        {nome_cliente} possui uma ferramenta de CRM? {possui_ferramenta_crm}.
        A maturidade em CRM da empresa é {maturidade_crm}.
        O principal objetivo ao utilizar o CRM é {objetivo_crm}.
        Os canais de comunicação disponíveis para CRM são {canais_disponiveis}.
        O perfil da empresa é {perfil_empresa}.
        As metas que a empresa busca alcançar com o CRM são {metas_crm}.
        A descrição do negócio é: {descricao_negocio}.
        O tamanho da base de dados de clientes é {tamanho_base}.
        O tom de voz desejado para a comunicação é {tom_voz}.
        Os fluxos e e-mails que a empresa deseja trabalhar são: {fluxos_ou_emails}.
        Existe algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads? {sla_entre_marketing_vendas}.

        - Proposta de fluxo de CRM que melhor atenda as necessidades do cliente e se melhor encaixe com suas características de negócio. Cada etapa extremamente detalhada com exatamente
        o que deve ser feito e porque. O Fluxo deve deliear o passo a passo da interação com os leads desde o primeiro até o último contato de forma bem detalhada e justificada. Detalhando o 
        canal de contato, tempo de duração de cada etapa, tom a ser utilizado, ação personalizada para o case específico do cliente {nome_cliente} para cada segmento de seu setor de atuação:
        {ramo_atuacao}.
        ''',
        agent=agentes_crm[2],
        output_file='estrategia_fluxo_crm.md'
    ),
                            
    # Task de Estratégia de contato com o cliente SMS Whatsapp
    Task(
        description="estratégia de contato com o cliente por mensagem.",
        expected_output=f'''
        Informações Gerais do Cliente:

        O nome do cliente é {nome_cliente}, e seu site oficial pode ser acessado em {site_cliente}. A empresa está inserida no ramo de {ramo_atuacao} e o intuito principal deste plano estratégico é {intuito_plano}. O público-alvo da empresa são {publico_alvo}, e seus principais concorrentes incluem {concorrentes}, cujos sites são {site_concorrentes}.
        Objetivos da Marca:
        
        O objetivo de marca selecionado para {nome_cliente} é {objetivos_de_marca}. A marca se destaca por {referencia_da_marca}.
        Informações sobre o CRM:
        
        {nome_cliente} possui uma ferramenta de CRM? {possui_ferramenta_crm}.
        A maturidade em CRM da empresa é {maturidade_crm}.
        O principal objetivo ao utilizar o CRM é {objetivo_crm}.
        Os canais de comunicação disponíveis para CRM são {canais_disponiveis}.
        O perfil da empresa é {perfil_empresa}.
        As metas que a empresa busca alcançar com o CRM são {metas_crm}.
        A descrição do negócio é: {descricao_negocio}.
        O tamanho da base de dados de clientes é {tamanho_base}.
        O tom de voz desejado para a comunicação é {tom_voz}.
        Os fluxos e e-mails que a empresa deseja trabalhar são: {fluxos_ou_emails}.
        Existe algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads? {sla_entre_marketing_vendas}.

        - Ideias de **SMS e WhatsApp**: 10 mensagens devidamente redigidas a serem enviados para marketing direto com o consumidor.
        ''',
        agent=agentes_crm[2],
        output_file='estrategia_sms_crm.md'
    ),

                            
    # Task de Estratégia de contato com o cliente email
    Task(
        description="estratégia de contato com o cliente po email.",
        expected_output=f'''
        Informações Gerais do Cliente:

        O nome do cliente é {nome_cliente}, e seu site oficial pode ser acessado em {site_cliente}. A empresa está inserida no ramo de {ramo_atuacao} e o intuito principal deste plano estratégico é {intuito_plano}. O público-alvo da empresa são {publico_alvo}, e seus principais concorrentes incluem {concorrentes}, cujos sites são {site_concorrentes}.
        Objetivos da Marca:
        
        O objetivo de marca selecionado para {nome_cliente} é {objetivos_de_marca}. A marca se destaca por {referencia_da_marca}.
        Informações sobre o CRM:
        
        {nome_cliente} possui uma ferramenta de CRM? {possui_ferramenta_crm}.
        A maturidade em CRM da empresa é {maturidade_crm}.
        O principal objetivo ao utilizar o CRM é {objetivo_crm}.
        Os canais de comunicação disponíveis para CRM são {canais_disponiveis}.
        O perfil da empresa é {perfil_empresa}.
        As metas que a empresa busca alcançar com o CRM são {metas_crm}.
        A descrição do negócio é: {descricao_negocio}.
        O tamanho da base de dados de clientes é {tamanho_base}.
        O tom de voz desejado para a comunicação é {tom_voz}.
        Os fluxos e e-mails que a empresa deseja trabalhar são: {fluxos_ou_emails}.
        Existe algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads? {sla_entre_marketing_vendas}.

        - Ideias de **Email**: 10 emails devidamente redigidos a serem enviados para marketing direto com o consumidor.
        ''',
        agent=agentes_crm[2],
        output_file='estrategia_email_crm.md'
    ),

     # Task de Estratégia de contato com o cliente NPS
    Task(
        description="estratégia de contato NPS com o cliente.",
        expected_output=f'''
        

        -Questionário de NPS score que se adeque para o cliente {nome_cliente} e seu ramo de atuação {ramo_atuacao}.
        ''',
        agent=agentes_crm[2],
        output_file='estrategia_nps_crm.md'
    ),
                            
   

    # Task de Análise de Performance de CRM
    Task(
        description="Monitorar e analisar a performance das ações de CRM.",
        expected_output=f'''
        **Análise de Performance de CRM para {nome_cliente}**

        Informações Gerais do Cliente:

        O nome do cliente é {nome_cliente}, e seu site oficial pode ser acessado em {site_cliente}. A empresa está inserida no ramo de {ramo_atuacao} e o intuito principal deste plano estratégico é {intuito_plano}. O público-alvo da empresa são {publico_alvo}, e seus principais concorrentes incluem {concorrentes}, cujos sites são {site_concorrentes}.
        Objetivos da Marca:
        
        O objetivo de marca selecionado para {nome_cliente} é {objetivos_de_marca}. A marca se destaca por {referencia_da_marca}.
        Informações sobre o CRM:
        
        {nome_cliente} possui uma ferramenta de CRM? {possui_ferramenta_crm}.
        A maturidade em CRM da empresa é {maturidade_crm}.
        O principal objetivo ao utilizar o CRM é {objetivo_crm}.
        Os canais de comunicação disponíveis para CRM são {canais_disponiveis}.
        O perfil da empresa é {perfil_empresa}.
        As metas que a empresa busca alcançar com o CRM são {metas_crm}.
        A descrição do negócio é: {descricao_negocio}.
        O tamanho da base de dados de clientes é {tamanho_base}.
        O tom de voz desejado para a comunicação é {tom_voz}.
        Os fluxos e e-mails que a empresa deseja trabalhar são: {fluxos_ou_emails}.
        Existe algum SLA (Service Level Agreement) combinado entre marketing e vendas para geração de leads? {sla_entre_marketing_vendas}.

        **Objetivo:** com base na pesquisa feita em crm_tools: ({crm_tools}), citar 5 sugestões de softwares de CRM para uso que sejam o melhor encaixe para as necessidades do cliente. com um parágrafo explicando o porquê.
        ''',
        agent=agentes_crm[4],
        output_file='software_crm.md'
    )
]


                        # Processo do Crew

                        equipe_crm = Crew(
                            agents=agentes_crm,
                            tasks=tarefas_crm,
                            process=Process.hierarchical,
                            manager_llm=modelo_linguagem,
                            language='português brasileiro'
                        )


                        # Executa as tarefas do processo
                        resultado_crm = equipe_crm.kickoff()

                        # Printando Tarefas de CRM

                        st.header('Planejamento de CRM')
                        st.subheader('1. Estratégia Geral de CRM')
                        st.markdown(tarefas_crm[0].output.raw)
                        st.subheader('1.1 Fluxo Geral de CRM')
                        st.markdown(tarefas_crm[1].output.raw)
                        st.subheader('2. Gestão de contato com o cliente - SMS/Whatsapp')
                        st.markdown(tarefas_crm[2].output.raw)
                        st.subheader('3. Gestão de contato com o cliente - Email')
                        st.markdown(tarefas_crm[3].output.raw)
                        st.subheader('4. Gestão de contato com o cliente - NPS')
                        st.markdown(tarefas_crm[4].output.raw)


                        st.subheader('5. Software de CRM')
                        st.markdown(tarefas_crm[5].output.raw)



                        

                        save_to_mongo_crm(tarefas_crm , nome_cliente)



