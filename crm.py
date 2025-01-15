__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from crewai_tools import tool
#from crewai_tools import FileReadTool, WebsiteSearchTool, PDFSearchTool, CSVSearchTool
import os
from tavily import TavilyClient
from pymongo import MongoClient
import SEOtools
#from equipe import agentes




# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.125,
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

def save_to_mongo_crm(tarefas_crm, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepare the document to be inserted into MongoDB
    task_outputs = {
        "id_planejamento": nome_cliente + '_' + 'CRM' + '_' + id_planejamento,  # Use o ID gerado como chave
        "nome_cliente": nome_cliente,  # Adiciona o nome do cliente ao payload
        "tipo_planejamento": 'CRM',
        "Plano_Estrategia_CRM": tarefas_crm[0].output.raw,
        "Plano_Contato_Email": tarefas_crm[1].output.raw,
        "Plano_Contato_SMS_WhatsApp": tarefas_crm[2].output.raw,
        "Plano_Contato_NPS": tarefas_crm[3].output.raw,
        "Plano_Analise_Dados_CRM": tarefas_crm[4].output.raw,
        "Plano_Automacao_CRM": tarefas_crm[5].output.raw,
        "Recomend_Software": tarefas_crm[6].output.raw
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
    
    # Informações gerais do cliente
    nome_cliente = st.text_input('Nome do Cliente:', key="nome_cliente", placeholder="Ex: Empresa X")
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente", placeholder="Ex: www.empresa-x.com.br")
    ramo_atuacao = st.text_input('Ramo de Atuação:', key="ramo_atuacao", placeholder="Ex: E-commerce de Moda")
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

                        import yaml
                        from crm_agents import Agent  
                        
                        # Step 1: Load the YAML file
                        with open('crm_agents.yaml', 'r', encoding='utf-8') as file:
                            agents_data = yaml.safe_load(file)
                        
                        # Step 2: Create a function to convert YAML data to Agent objects
                        def create_agents_from_yaml(agents_data):
                            agents = []
                            for agent_data in agents_data['agentes_crm']:
                                agent = Agent(
                                    role=agent_data['role'],
                                    goal=agent_data['goal'],
                                    backstory=agent_data['backstory'],
                                    allow_delegation=agent_data['allow_delegation'],
                                    llm=agent_data['llm'],  # Make sure this points to your LLM model or class
                                    tools=agent_data['tools']
                                )
                                agents.append(agent)
                            return agents
                        
                        # Step 3: Create the agents from YAML data
                        agentes_crm = create_agents_from_yaml(agents_data)





                       
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

    # Task de Estratégia de contato com o cliente Email
    Task(
        description="estratégia de contato com o cliente.",
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

        - Ideias de **E-mail Marketing**: 10 emails devidamente redigidos com campos de 1: Assunto; 2: Saudações, 3: Corpo Principal (dois parágrafos chamativos, personalizados e não genéricos), 4: CTA.
        ''',
        agent=agentes_crm[2],
        output_file='estrategia_email_crm.md'
    ),
                            
    # Task de Estratégia de contato com o cliente SMS Whatsapp
    Task(
        description="estratégia de contato com o cliente.",
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

     # Task de Estratégia de contato com o cliente NPS
    Task(
        description="estratégia de contato NPS com o cliente.",
        expected_output=f'''
        

        -Questionário de NPS score que se adeque para o cliente {nome_cliente} e seu ramo de atuação {ramo_atuacao}.
        ''',
        agent=agentes_crm[2],
        output_file='estrategia_nps_crm.md'
    ),
                            
    
    # Fluxo CRM
    Task(
        description="Delineamento de propostas de fluxo de CRM.",
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

        **Objetivo:** Delineamento de propostas de fluxo de CRM..


        **Plano de Ação**:
        - delinear aprodundada e detalhadamente o fluxo de CRM.
        ''',
        agent=agentes_crm[1],
        output_file='fluxo_crm.md'
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

        **Objetivo:** Avaliar a eficácia das campanhas de CRM e ajustar conforme necessário.

        **Indicadores a Monitorar**:
        - **Taxa de Conversão de Leads**: Acompanhar a taxa de conversão de cada fluxo de nutrição e campanha de abandono de carrinho.
        - **Retenção de Clientes**: Monitorar a retenção mensal de clientes que participam do programa de fidelidade.
        - **Satisfação do Cliente**: Analisar o Net Promoter Score (NPS) e os resultados de pesquisas de satisfação.

        **Ações de Ajuste**:
        - Ajustar campanhas de e-mail marketing com base na taxa de abertura e cliques.
        - Refinar os fluxos de nutrição de leads para melhorar a taxa de conversão, com foco no envio de conteúdo relevante.

        **Plano de Ação**:
        - Gerar relatórios semanais de desempenho.
        - Ajustar campanhas com base em métricas de sucesso e feedback dos clientes.
        ''',
        agent=agentes_crm[4],
        output_file='analise_performance_crm.md'
    )

,    # Task de Análise de Performance de CRM
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
                        st.subheader('2. Gestão de contato com o cliente - Email')
                        st.markdown(tarefas_crm[1].output.raw)
                        st.subheader('3. Gestão de contato com o cliente - SMS/Whatsapp')
                        st.markdown(tarefas_crm[2].output.raw)
                        st.subheader('4. Gestão de contato com o cliente - NPS')
                        st.markdown(tarefas_crm[3].output.raw)

                        st.subheader('5. Delineamento de fluxo de CRM')
                        st.markdown(tarefas_crm[4].output.raw)

                        st.subheader('6. Automação de CRM')
                        st.markdown(tarefas_crm[5].output.raw)

                        st.subheader('7. Software de CRM')
                        st.markdown(tarefas_crm[6].output.raw)



                        

                        save_to_mongo_crm(tarefas_crm , nome_cliente)



