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
import SEO-tools
import equipe




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
       
        

        "Plano_Redes": tarefas_midia[0].output.raw,
        "Plano_Criativos": tarefas_midia[1].output.raw,
        "Plano_Saude_Site": tarefas_midia[2].output.raw,
        "Plano_Palavras_Chave": tarefas_midia[3].output.raw,
        "Plano_CRM": tarefas_midia[4].output.raw,
        "Plano_Design": tarefas_midia[5].output.raw,
        "Estrategia_Conteudo": tarefas_midia[6].output.raw,
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


def planej_midias_page():
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


    performance_metrics_df = SEO-tools.check_website_performance(site_cliente)
    website_all_texts = SEO-tools.scrape_all_texts(site_cliente)


  

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
                    with st.spinner('Gerando o planejamento de SEO...'):




                       
                        tarefas_midia = [

                             # Redes Sociais
                                Task(
                                    description='''Definição de estratégia de abordagem de cada rede social''',
                                    expected_output=f'''Em portugês brasileiro, primeiro, definir em linhas gerais a abordagem de cada rede social 
                                    (instagram, facebook, youtube, linkedin, whatsapp) para as campanhas de marketing digital para 
                                    {nome_cliente}. Quero soluções originais, personalizadas e pulo do gato
                                    considerando seu ramo de atuação específico: {ramo_atuacao}, 
                                    o intuito do planejamento estratégico conforme detalhado em: {intuito_plano} e o publico alvo: 
                                    {publico_alvo},e a referência da marca:
                                    {referencia_da_marca},. 

                                    Em seguida, detalhar considerando o intuito do planejamento estratégico conforme detalhado em: {intuito_plano} e o publico alvo: 
                                    {publico_alvo}:

                                    
                                    Em facebook e instagram, definir o que deve ser feito em:
                                    - reels e stories
                                    - estático e carrossel
                                    - conteúdo localizado

                                    Em linkedin, definir o que deve ser feito em:
                                    - Conteúdos educativos e informativos
                                    - Depoimentos de sucesso
                                    - Eventos e comemorações
                                    - Tom de voz 
                                    - CTA’s  fortes (defina-as em grande detalhe. seja original, traga soluções pulo do gato para o caso específico de atuação. você é um especialista em redes sociais e cta's.) (pelo menos 5 sugestões, com motivo do porque seriam interessantes)

                                    Em whatsapp, definir o que deve ser feito em:
                                    - Canal 
                                    - Lista de transmissão 
                                    - Análises regulares 

                                    Em Youtube, definir o que deve ser feito em termos de:
                                    - shorts 
                                    - conteúdos de especialistas
                                    - vídeos 
                                    - análises regulares 

                                    Em geral, também definir do's e don't's                                                          
                                    ''',
                                    agent=agentes[13],
                                    output_file = 'redes.md'
                                ),

                            # Criativos
                                Task(
                                    description='''Criativos da campanha de marketing digital''',
                                    expected_output=f'''Em portugês brasileiro, Criar 10 Criativos (título, descrição e tipo de imagem sugerida) para as campanhas de marketing digital para 
                                    {nome_cliente} Quero soluções originais, personalizadas e pulo do gato
                                    considerando seu ramo de atuação: {ramo_atuacao}, o intuito do planejamento estratégico conforme detalhado em: {intuito_plano} e o publico alvo: 
                                    {publico_alvo},e a referência da marca:
                                    {referencia_da_marca},.''',
                                    agent=agentes[10],
                                    output_file = 'Criativos.md'
                                ),

                            #SEO
                            #Saude Site
                            
                                Task(
                                    description="Desenvolver relatório de performance do site do planejamento estratégico.",
                                    expected_output=f''' Em portugês brasileiro, Um relatório minuciosamente detalhado sobre a saúde do site para {nome_cliente}
                                    que contém as etapas:
                                    
                                    -Um relatório para TODAS as páginas em {performance_metrics_df} sobre a performance do site do dito cliente: {site_cliente}
                                    que detalha todas as métricas observadas página por página, conforme explicitado em: ({performance_metrics_df})
                                    , Tal relatório deve conter insights, análises e a apresentação dos dados brutos no seguinte formato para cada página:

                                    -URL
                                    -Status Code
                                    -Load Time (s)
                                    -Content Length (KB)
                                    -Title
                                    -Meta Description
                                    -H1 Tags'
                                    -Word Count
                                    -Robots Meta
                                    -Canonical Tag
                                    -10 sugestões de melhora bem detalhadas. embasadas em expertise de SEO. pelo menos um parágrafo para cada sugestão de melhora para cada página.
                                    
                                
                                    -Você é claro e detalhista, analítico e se comunica de forma excelente.''',
                                    agent=agentes[9],
                                    output_file = 'performance.md'
                                ),

                            #Palavras Chave
                            
                            Task(
                                    description="Desenvolver relatório de performance do site do planejamento estratégico.",
                                    expected_output=f''' Em portugês brasileiro, Um relatório minuciosamente detalhado sobre sugestões de palavras chave para {nome_cliente}
                                    considerando seu ramo de atuação {ramo_atuacao}, o público alvo {publico_alvo}
                                    
                                    

                                    - Insights de palavras chave relevantes para {nome_cliente}, assim como mais valiosos insights
                                    sobre SEO que devem estar contidos em diretrizes de um especialista que estudou minuciosamente todos os detalhes sobre o cliente e sabe o que
                                    deve ser feito para fazer com que o cliente cresça. Você é um especialista em SEO.
                                    Você é claro e detalhista, criativo e se comunica de forma excelente.''',
                                    agent=agentes[9],
                                    output_file = 'keywords.md'
                                ),

                            

                            #CRM
                                Task(
                                    description="Criar a estratégia de CRM.",
                                    expected_output=f'''

                                    Gere um documento no formato abaixo adaptado para as necessidades({intuito_plano}) de {nome_cliente}
                                    
                                    Relatório de CRM para {nome_cliente}

                                        Objetivo: Desenvolver uma abordagem centrada no cliente, com foco em segmentação e compreensão profunda das necessidades, comportamentos e expectativas de diferentes grupos de clientes. A seguir, apresento um planejamento estratégico detalhado para atingir esse objetivo, considerando o ramo de atuação: {ramo_atuacao}, o intuito do plano: {intuito_plano}, o público-alvo: {publico_alvo} e a referência da marca: {referencia_da_marca}.
                                        
                                        1. Segmentação e Compreensão do Cliente
                                        Análise de dados dos clientes:
                                        Segmentação dos clientes por características demográficas, comportamentais e psicográficas.
                                        Mapeamento das necessidades, expectativas e pontos de dor de cada grupo de clientes.
                                        Objetivo: Obter uma compreensão clara dos diferentes perfis de clientes para personalizar as estratégias.
                                        2. Coleta e Análise de Dados Relevantes
                                        Fontes de dados a serem coletadas:
                                        Histórico de compras (frequência, valores, produtos adquiridos).
                                        Comportamento digital (interações no site, redes sociais, cliques, tempo de navegação).
                                        Feedback de clientes (pesquisas de satisfação, Net Promoter Score - NPS).
                                        Objetivo: Obter uma visão 360º do cliente para basear as ações de marketing e relacionamento.
                                        3. Desenvolvimento de Estratégias de Comunicação Personalizadas
                                        Canais a serem utilizados:
                                        E-mail marketing, mensagens SMS, redes sociais, notificações push.
                                        Mensagens personalizadas:
                                        Criação de campanhas direcionadas para cada segmento (promoções, novos produtos, eventos especiais).
                                        Personalização da comunicação com base em dados de compras e comportamento.
                                        Objetivo: Maximizar a relevância e eficácia das mensagens enviadas, com base nas preferências do cliente.
                                        4. Implementação de Ferramentas de Automação de Marketing
                                        Ferramentas recomendadas:
                                        Automação de e-mail (ex: envio de e-mails para abandono de carrinho).
                                        CRM para centralização de dados de clientes, histórico e interações.
                                        Objetivo: Automatizar a comunicação e personalizar a experiência de forma escalável.
                                        5. Programas de Fidelidade e Engajamento
                                        Desenvolvimento de programas de fidelidade:
                                        Oferecer recompensas, pontos ou benefícios exclusivos para clientes frequentes.
                                        Ações de engajamento:
                                        Manter o cliente envolvido com a marca através de conteúdos exclusivos, eventos, ofertas especiais.
                                        Objetivo: Aumentar a lealdade e a retenção dos clientes.
                                        6. Otimização do Atendimento ao Cliente
                                        Canais de atendimento:
                                        Atendimento via chat, e-mail, WhatsApp, redes sociais.
                                        Treinamento das equipes:
                                        Capacitação da equipe de atendimento para oferecer um serviço personalizado e rápido.
                                        Objetivo: Garantir uma excelente experiência para o cliente, resolvendo suas dúvidas e problemas de maneira eficiente.
                                        7. Promoção da Retenção e Maximização do Valor do Cliente
                                        Estratégias de retenção:
                                        Programas de fidelização, follow-ups pós-compra, promoções personalizadas.
                                        Ações para reengajar clientes inativos.
                                        Maximização do valor do cliente (CLV):
                                        Estratégias para aumentar o ticket médio e a frequência de compras (ex: upselling, cross-selling).
                                        Objetivo: Maximizar o Lifetime Value (LTV) do cliente, promovendo sua permanência e aumentando suas compras ao longo do tempo.
                                        8. Integração entre Equipes de Marketing, Vendas e Atendimento
                                        Coordenação das equipes:
                                        Compartilhamento de dados e informações entre marketing, vendas e atendimento.
                                        Utilização de um CRM centralizado para manter todos os departamentos alinhados.
                                        Objetivo: Criar uma abordagem consistente e eficaz em todas as interações com o cliente, garantindo uma comunicação sem falhas.
                                        9. Soluções Personalizadas para {nome_cliente}
                                        Considerações específicas:
                                        Ajustar as estratégias para o ramo de atuação: {ramo_atuacao}, com foco em personalizar a experiência de acordo com as necessidades do público-alvo de {publico_alvo}.
                                        Adaptar as campanhas de CRM com base na referência da marca: {referencia_da_marca}.
                                        Objetivo: Criar soluções originais e eficazes que atendam às necessidades e expectativas de {nome_cliente}, alinhadas com sua identidade de marca.
                                                                            
                                    
                                    
                                    ''',
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
                                    {nome_cliente}. Quero soluções originais, personalizadas e pulo do gato
                                    considerando seu ramo de atuação: {ramo_atuacao}, o intuito do planejamento estratégico conforme detalhado em: {intuito_plano} e o publico alvo: 
                                    {publico_alvo} ,e a referência da marca:
                                    {referencia_da_marca}. Suas guias serão práticas, claras, não genéricas. Você deve fornecer praticamente o que deve ser feito em termos de marca e design. Não
                                    seja vago e não seja raso.''',
                                    agent=agentes[12],
                                    output_file = 'Marca_Design.md'
                                ),

                                Task(
                                description=f'''Sendo o mais detalhista possível e com a profundidade de um especialista em marketing digital, 
                                Levando em conta a análise PEST, Tom de Voz, Buyer Persona, Brando Persona, Público alvo, posicionamento de marca, 
                                    análise SWOT e golden circle gerados, Criar as editorias de conteúdo da marca considerando a identidade, os objetivos 
                                    da marca e o público-alvo.''',
                                expected_output=f'''Em portugês brasileiro, Editorias de conteúdo detalhadas e alinhadas com os objetivos da marca ({intuito_plano}) ,e a referência da marca:
                                    {referencia_da_marca},. 
                                Classificamos as editorias em 
                5 pilares, que foram revistos e sugeridos para posicionar a marca, engajar, relacionar e gerar identificação com o público.

                        Os 5 Pilares:
                        - Institucional
                        - Inspiração
                        - Educação
                        - Produtos/Serviços
                        - Relacionamento
                        
                        Para cada um dos 5 pilares, definir:
                        - objetivo
                        - conteúdo
                        - canal'''
                        ,
                                agent=agentes[8],
                                output_file='estrategia_editoriais.md'
                            )
                            ]

                        # Processo do Crew

                        equipe_midia = Crew(
                            agents=equipe.agentes,
                            tasks=tarefas_midia,
                            process=Process.hierarchical,
                            manager_llm=modelo_linguagem,
                            language='português brasileiro'
                        )


                        # Executa as tarefas do processo
                        resultado_midia = equipe_midia.kickoff()

                        #Printando Tarefas

                        st.header('3. Etapa de Planejamento de Mídias')
                        st.subheader('3.1 Plano para Redes')
                        st.markdown(tarefas_midia[0].output.raw)
                        st.subheader('3.2 Plano para Criativos')
                        st.markdown(tarefas_midia[1].output.raw)
                        st.subheader('3.3 SEO')
                        st.subheader('3.3.1 Análise de Saúde do Site')
                        st.markdown(tarefas_midia[2].output.raw)
                        st.subheader('3.3.2 Sugestões de palavras chave')
                        st.markdown(tarefas_midia[3].output.raw)
                        st.subheader('3.4 Plano de CRM')
                        st.markdown(tarefas_midia[4].output.raw)
                        st.subheader('3.5 Plano de Design/Marca')
                        st.markdown(tarefas_midia[5].output.raw)
                        st.subheader('3.6 Estratégia de Conteúdo')
                        st.markdown(tarefas_midia[6].output.raw)

                        

                        save_to_mongo(tarefas_pesquisa,tarefas_estrategica,tarefas_midia , nome_cliente)




