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
    temperature=0.3,
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
        "id_planejamento": nome_cliente + '_' + id_planejamento,  # Use o ID gerado como chave
        "nome_cliente": nome_cliente,  # Adiciona o nome do cliente ao payload
        
        "Plano_Estrategia_CRM": tarefas_crm[0].output.raw,
        "Plano_Analise_Dados_CRM": tarefas_crm[1].output.raw,
        "Plano_Gestao_Leads_CRM": tarefas_crm[2].output.raw,
        "Plano_Gestao_Relacionamento_CRM": tarefas_crm[3].output.raw,
        "Plano_Analise_Performance_CRM": tarefas_crm[4].output.raw,
        "Plano_Automacao_CRM": tarefas_crm[5].output.raw,
        "Plano_Consultoria_SLA_CRM": tarefas_crm[6].output.raw,
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
    st.subheader('Planejamento de Mídias')

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
                    with st.spinner('Gerando o planejamento de mídias...'):

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
        Relatório de Estratégia de CRM para {nome_cliente}

        Objetivo: Desenvolver uma estratégia de CRM centrada no cliente, focada em segmentação e personalização da experiência para {nome_cliente}, 
        considerando os seguintes parâmetros:
        
        1. Ramo de atuação: {ramo_atuacao}
        2. Intuito do plano estratégico: {intuito_plano}
        3. Público-alvo: {publico_alvo}
        4. Canais disponíveis: {canais_disponiveis}
        5. Metas a serem alcançadas: {metas_crm}
        
        Estratégia:
        - A segmentação de clientes será realizada com base nas características demográficas, comportamentais e psicográficas.
        - Análise do comportamento do cliente em canais digitais, interações em redes sociais, compras anteriores, entre outros.
        - Estratégias de comunicação personalizadas, utilizando canais como e-mail marketing, SMS, WhatsApp e redes sociais.
        
        Objetivo: Criar um alinhamento estratégico entre as equipes de marketing, vendas e atendimento para garantir a execução das metas e alcançar o 
        sucesso no relacionamento com os clientes.
        ''',
        agent=agentes_crm[0],  # Agente de Estratégia Geral de CRM
        output_file='estrategia_crm.md'
    ),
    
    # Task de Análise de Dados CRM
    Task(
        description="Analisar a base de dados de clientes e segmentá-los para estratégias de CRM.",
        expected_output=f'''
        Relatório de Análise de Dados CRM para {nome_cliente}

        Objetivo: Realizar uma análise detalhada da base de dados de clientes de {nome_cliente}, segmentando-os com base nos dados demográficos, 
        comportamentais e psicográficos, de acordo com os parâmetros:

        1. Tamanho da base: {tamanho_base}
        2. Público-alvo: {publico_alvo}
        3. Canais de comunicação disponíveis: {canais_disponiveis}
        
        Análise:
        - Identificação dos segmentos de clientes com maior potencial de conversão.
        - Padrões de comportamento e interações nos canais de comunicação.
        - Comportamento de compra e fidelidade à marca.
        
        Objetivo: Identificar os perfis mais rentáveis e desenvolver campanhas personalizadas para cada grupo, melhorando as taxas de conversão.
        ''',
        agent=agentes_crm[1],  # Agente de Análise de Dados CRM
        output_file='analise_dados_crm.md'
    ),
    
    # Task de Gestão de Leads e Fluxos CRM
    Task(
        description="Desenvolver e implementar fluxos de CRM para nutrição de leads.",
        expected_output=f'''
        Relatório de Gestão de Leads e Fluxos CRM para {nome_cliente}

        Objetivo: Criar fluxos de nutrição de leads para aumentar a conversão e melhorar a jornada do cliente. Considerando os seguintes aspectos:

        1. Objetivos de CRM: {objetivo_crm}
        2. Metas a serem alcançadas: {metas_crm}
        3. Público-alvo: {publico_alvo}
        4. Canais disponíveis: {canais_disponiveis}

        Estratégia de Fluxos:
        - Desenvolvimento de campanhas de e-mail marketing, SMS e redes sociais com base no comportamento do cliente.
        - Fluxos de automação para nutrição de leads, incluindo e-mails personalizados, ofertas e promoções.
        - Análise do estágio do funil para adaptar os fluxos e garantir conversão eficiente.

        Objetivo: Melhorar a jornada do cliente e aumentar a conversão de leads qualificados, utilizando automação de marketing e personalização.
        ''',
        agent=agentes_crm[2],  # Agente de Gestão de Leads e Fluxos CRM
        output_file='gestao_leads_fluxos_crm.md'
    ),
    
    # Task de Gestão de Relacionamento com Clientes
    Task(
        description="Desenvolver e implementar estratégias de gestão de relacionamento com clientes.",
        expected_output=f'''
        Relatório de Gestão de Relacionamento com Clientes para {nome_cliente}

        Objetivo: Criar e implementar estratégias focadas na fidelização e retenção de clientes, considerando as seguintes informações:

        1. Público-alvo: {publico_alvo}
        2. Canais de comunicação disponíveis: {canais_disponiveis}
        3. Metas a serem alcançadas: {metas_crm}
        
        Estratégia:
        - Criação de programas de fidelidade para clientes frequentes.
        - Ações de engajamento contínuo, como conteúdos exclusivos e promoções personalizadas.
        - Implementação de comunicação omnicanal, oferecendo uma experiência consistente em todos os canais.

        Objetivo: Aumentar a lealdade dos clientes e maximizar o Lifetime Value (LTV), melhorando a retenção e o engajamento ao longo do tempo.
        ''',
        agent=agentes_crm[3],  # Agente de Gestão de Relacionamento com Clientes
        output_file='gestao_relacionamento_crm.md'
    ),
    
    # Task de Análise de Performance de CRM
    Task(
        description="Monitorar e analisar a performance das ações de CRM.",
        expected_output=f'''
        Relatório de Análise de Performance de CRM para {nome_cliente}

        Objetivo: Avaliar a eficácia das estratégias de CRM e ajustar conforme necessário. Para isso, será analisada a seguinte performance:

        1. Metas de CRM: {metas_crm}
        2. Canais de comunicação: {canais_disponiveis}
        3. Feedback dos clientes: (ex: NPS, pesquisas de satisfação)

        Indicadores de Performance:
        - Taxa de conversão de leads.
        - Retenção de clientes e aumento do LTV.
        - Satisfação do cliente e impacto nas campanhas de fidelização.

        Objetivo: Ajustar as campanhas e fluxos de CRM para melhorar a performance com base em dados de interação, conversão e satisfação do cliente.
        ''',
        agent=agentes_crm[4],  # Agente de Análise de Performance de CRM
        output_file='analise_performance_crm.md'
    ),
    
    # Task de Automação de CRM
    Task(
        description="Desenvolver automações de CRM para personalização e escalabilidade.",
        expected_output=f'''
        Relatório de Automação de CRM para {nome_cliente}

        Objetivo: Implementar ferramentas de automação para personalizar a experiência do cliente e escalabilidade das ações. Considerando os seguintes dados:

        1. Canais de comunicação disponíveis: {canais_disponiveis}
        2. Público-alvo: {publico_alvo}
        3. Metas de CRM: {metas_crm}

        Automação:
        - Automação de e-mails para abandono de carrinho e promoções personalizadas.
        - Integração de ferramentas de CRM para centralizar dados e otimizar a comunicação com clientes.
        - Utilização de notificações push, SMS e e-mail marketing automatizados.

        Objetivo: Otimizar a gestão de leads e melhorar a comunicação com o cliente de forma escalável, sem perder a personalização.
        ''',
        agent=agentes_crm[5],  # Agente de Automação de CRM
        output_file='automacao_crm.md'
    ),
    
    # Task de Consultoria de SLA CRM
    Task(
        description="Analisar e ajustar o SLA entre marketing e vendas.",
        expected_output=f'''
        Relatório de SLA CRM para {nome_cliente}

        Objetivo: Analisar o SLA entre as equipes de marketing e vendas, garantindo a efetividade do processo de geração de leads. Para isso, considera-se:

        1. Metas de CRM: {metas_crm}
        2. Público-alvo: {publico_alvo}
        3. Canais de comunicação: {canais_disponiveis}

        Estratégia de SLA:
        - Definição de prazos e expectativas para cada etapa do processo de conversão de leads.
        - Alinhamento entre marketing e vendas sobre os critérios de qualificação de leads e feedback contínuo.

        Objetivo: Garantir um fluxo de trabalho eficiente entre marketing e vendas, para maximizar a conversão de leads qualificados.
        ''',
        agent=agentes_crm[6],  # Agente de Consultoria de SLA CRM
        output_file='sla_crm.md'
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
                        st.subheader('2. Análise de Dados CRM')
                        st.markdown(tarefas_crm[1].output.raw)
                        st.subheader('3. Gestão de Leads e Fluxos CRM')
                        st.markdown(tarefas_crm[2].output.raw)
                        st.subheader('4. Gestão de Relacionamento com Clientes')
                        st.markdown(tarefas_crm[3].output.raw)
                        st.subheader('5. Análise de Performance de CRM')
                        st.markdown(tarefas_crm[4].output.raw)
                        st.subheader('6. Automação de CRM')
                        st.markdown(tarefas_crm[5].output.raw)
                        st.subheader('7. Consultoria de SLA CRM')
                        st.markdown(tarefas_crm[6].output.raw)


                        

                        save_to_mongo_crm(tarefas_crm , nome_cliente)



