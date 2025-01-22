import streamlit as st
import google.generativeai as genai
import uuid
import os
from pymongo import MongoClient
from datetime import datetime
import os
from tavily import TavilyClient
from pymongo import MongoClient
import requests

# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")



# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini
client1 = TavilyClient(api_key='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')


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
def save_to_mongo_MKT(SWOT_output,PEST_output,tendencias_output, concorrencias_output, golden_output,posicionamento_output,brand_persona_output,buyer_persona_output,tom_output, nome_cliente):    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano Estratégico' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano Estratégico',
        "Etapa_1_Pesquisa_Mercado": {
            "Análise_SWOT": SWOT_output,
            "Análise_PEST": PEST_output,
            "Análise_Tendências": tendencias_output,
            "Análise_Concorrência": concorrencias_output,
        },
        "Etapa_2_Estrategica": {
            "Golden_Circle": golden_output,
            "Posicionamento_Marca": posicionamento_output,
            "Brand_Persona": brand_persona_output,
            "Buyer_Persona": buyer_persona_output,
            "Tom_de_Voz": tom_output,
        }
    }


    # Insere o documento no MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def planej_mkt_page():
    st.subheader('Planejamento de Mídias e Redes')
    st.text('Aqui geramos plano para criativos, análise de saúde do site, sugestões de palavras chave, plano de CRM, plano de Design/Marca e estratégia de conteúdo.')

    # Buscar todos os clientes do banco de dados
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    opcoes_clientes = [cliente["nome"] for cliente in clientes]

    # Selectbox para escolher o cliente
    nome_cliente = st.selectbox('Selecione o Cliente:', opcoes_clientes, key="nome_cliente")

    # Obter as informações do cliente selecionado
    cliente_info = next((cliente for cliente in clientes if cliente["nome"] == nome_cliente), None)
    site_cliente = cliente_info["site"] if cliente_info else ""
    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""

    # Exibir os campos preenchidos com os dados do cliente
    st.text_input('Site do Cliente:', value=site_cliente, key="site_cliente")
    st.text_input('Ramo de Atuação:', value=ramo_atuacao, key="ramo_atuacao")
    intuito_plano = st.text_input('Intuito do Plano Estratégico:', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre")
    publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda")
    concorrentes = st.text_input('Concorrentes:', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C")
    site_concorrentes = st.text_input('Site dos Concorrentes:', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br")
    tendaux = st.text_input('Tendências de interesse:', key="tendaux", placeholder="Ex: IA, novos fluxos de marketing, etc")

    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]

    objetivos_de_marca = st.selectbox('Selecione os objetivos de marca', objetivos_opcoes, key="objetivos_marca")
    referencia_da_marca = st.text_area('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', key="referencias_marca", placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.", height=200)

    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)

        # Set parameters for the search
    days = 90
    max_results = 15

    import requests

    #DUCK DUCK GO SEARCH de tendências

    url = "https://duckduckgo8.p.rapidapi.com/"
    
    querystring = {"q":f"tendencias em {tendaux}"}
    
    headers = {
    	"x-rapidapi-key": rapid_key,
    	"x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    tend_novids2 = response.text


  #DUCK DUCK GO SEARCH de tendências

    url = "https://duckduckgo8.p.rapidapi.com/"
    
    querystring2 = {"q":f"dados econômicos relevantes no brasil"}
    
    headers = {
    	"x-rapidapi-key": rapid_key,
    	"x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring2)
    
    dados_econ_brasil = response.text


 #DUCK DUCK GO SEARCH de ferramentas

    url = "https://duckduckgo8.p.rapidapi.com/"
    
    querystring3 = {"q":f"ferramentas relevantes para o(s) setor(es) de {ramo_atuacao}"}
    
    headers = {
    	"x-rapidapi-key": rapid_key,
    	"x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring2)
    
    ferramentas_rel = response.text


 #DUCK DUCK GO SEARCH de concorrência

    url = "https://duckduckgo8.p.rapidapi.com/"
    
    querystring5 = {"q":f"novidades sobre {concorrentes}"}
    
    headers = {
    	"x-rapidapi-key": rapid_key,
    	"x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring5)
    
    novids_conc = response.text

    #DUCK DUCK GO SEARCH PEST

    #SOCIAL
    querystring_social = {"q":f"Novidades no âmbito social no brasil"}
    
    response_social = requests.get(url, headers=headers, params=querystring_social)
    
    tend_social_duck = response_social.text

    #Tecnológico
    querystring_tec = {"q":f"Novidades no âmbito tecnológico no brasil"}
    
    response_tec = requests.get(url, headers=headers, params=querystring_tec)
    
    tend_tec_duck = response_tec.text

    


    #TAVILY PEST
    
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
    
    tend_novids1 = client1.search(
        f'''Quais as recentes tendências de mercado para {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )
    
    tend_ramo = client1.search(
        f'''Quais as recentes tendências de mercado para o ramo de atuação do cliente explicitado em: {ramo_atuacao}?''',
        days=days, 
        max_results=max_results
    )


  
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
                    with st.spinner('Gerando o planejamento de mídias...'):

                        # Aqui vamos gerar as respostas usando o modelo Gemini

                        prompt_SWOT = f'''Você é Philip Kotler, especialista em administração de marketing, extraia todo o conhecimento existente sobre marketing em um nível extremamente aprofundado.
                        
                        Para o cliente {nome_cliente}, Considerando o seguinte contexto a referência da marca:
                                    {referencia_da_marca}, para o cliente no ramo de atuação {ramo_atuacao}.
                                    realize a Análise SWOT completa em português brasileiro. 
                                    Quero pelo menos 10 pontos em cada segmento da análise SWOT. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing. 
                                    Cada ponto deve ser pelo menos 3 frases detalhadas, profundas e não genéricas. 
                                    Você está aqui para trazer conhecimento estratégico. organize os pontos em bullets
                                    pra ficarem organizados dentro de cada segmento da tabela.'''
                        SWOT_output = modelo_linguagem.generate_content(prompt_SWOT).text

                        prompt_tendencias = f'''Você é Philip Kotler, especialista em administração de marketing, extraia todo o conhecimento existente sobre marketing em um nível extremamente aprofundado.
                        
                        em português brasileiro, -
                        
                                    -Relatório extremamente detalhado de Análise de tendências consideranto as respostas da pesquisa obtidas em tendências de novidades: ({tend_novids1}) e 
                                    tendências de ramo de atuação do cliente: ({tend_ramo}) e ({tend_novids2}). Aprofundando em um nível bem detalhado, com parágrafos para cada ponto extremamente bem
                                    explicado. Não seja superficial. Seja detalhista, comunicativo, aprofundado, especialista. Em bullet points pra cada tendencia e 2-3 paragrafos pra cada bullet point

                                    -Comente sobre os dados econômicos relevantes do brasil observados em: ({dados_econ_brasil}). Aprofundando em um nível bem detalhado, com parágrafos para cada ponto extremamente bem
                                    explicado. Não seja superficial. Seja detalhista, comunicativo, aprofundado, especialista.

                                    -Comente sobre as ferramentas relevantes no setor de atuação do cliente explicitadas em ({ferramentas_rel}). Aprofundando em um nível bem detalhado, com parágrafos para cada ponto extremamente bem
                                    explicado. Não seja superficial. Seja detalhista, comunicativo, aprofundado, especialista.

                                    
                                    -Realize um relatório detalhado e formal de todas as tendências e como isso pode ser usado no planejamento estratégico.

'''
                        tendencias_output = modelo_linguagem.generate_content(prompt_tendencias).text


                        prompt_concorrencias = f'''Você é Philip Kotler, especialista em administração de marketing, extraia todo o conhecimento existente sobre marketing em um nível extremamente aprofundado.
                        
                        em português brasileiro, -
                        
                                    

                                    -Considerando {concorrentes} como a concorrência direta de {nome_cliente}, redija sobre as notícias sobre o concorrente explicitadas em {novids_conc} e como o
                                    cliente {nome_cliente} pode superar isso. Aprofundando em um nível bem detalhado, com parágrafos para cada ponto extremamente bem
                                    explicado. Não seja superficial. Seja detalhista, comunicativo, aprofundado, especialista.
                                    

'''
                        concorrencias_output = modelo_linguagem.generate_content(prompt_concorrencias).text

                        prompt_PEST = f'''Você é Philip Kotler, especialista em administração de marketing.
                        
                        Análise PEST com pelo menos 10 pontos relevantes em cada etapa em português brasileiro 
                                    considerando o retorno da pesquisa de tendências em: ({tend_novids2}),    contexto político: {politic}, contexto econômico: {economic} e dados econômicos
                                    relevantes: ({dados_econ_brasil}), contexto social: ({social})
                                    e ({tend_social_duck}), contexto tecnológico: ({tec}) e ({tend_tec_duck}). Leve em conta as tendencias em ({tendencias_output}).
                                    Quero pelo menos 10 pontos em cada segmento da análise PEST. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing.'''
                        
                        PEST_output = modelo_linguagem.generate_content(prompt_PEST).text

                        prompt_golden = f'''Golden Circle completo com 'how', 'why' e 'what' resumidos 
                                    em uma frase cada em português brasileiro. Considerando o seguinte contexto 
                                     e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca}, a análise SWOT ({SWOT_output}).'''
                      
                        golden_output = modelo_linguagem.generate_content(prompt_golden).text

                        prompt_posicionamento = f'''Em português brasileiro,. 
                            
                                    levando em conta a análise SWOT: ({SWOT_output}) e o golden circle: ({golden_output}).
                                    
                                    Gerar 5 Posicionamentos de marca para o cliente {nome_cliente} do ramo de atuação {ramo_atuacao} Com um slogan com essa inspiração:
                                    
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

                                    
                                    
                                    '''
                  
                        posicionamento_output = modelo_linguagem.generate_content(prompt_posicionamento).text


                        prompt_brand_persona = f'''2 Brand Personas detalhada, alinhada com a marca do {nome_cliente} que é do setor de atuação {ramo_atuacao} em português brasileiro considerando o 
                                    seguinte contexto 
                                    
                                    o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca},. 
                                    
                                    - Defina seu nome (deve ser o nome de uma pessoa normal como fernando pessoa, maria crivellari, etc)
                                    -Defina seu gênero, faixa de idade, qual a sua bagagem, defina sua personalidade. 
                                    -Defina suas características: possui filhos? É amigável? quais seus objetivos? qual seu repertório? O que gosta de fazer?
                                    -Comunicação: Como se expressa? Qual o seu tom? Qual o seu linguajar?'''
                  
                        brand_persona_output = modelo_linguagem.generate_content(prompt_brand_persona).text

                        prompt_buyer_persona = f'''Descrição detalhada da buyer persona considerando o público-alvo: {publico_alvo} e o 
                                    objetivo do plano estratégico como descrito em {intuito_plano} com os seguintes atributos enunciados: 
                                    nome fictício, idade, gênero, classe social, objetivos,  vontades, Emoções negativas (o que lhe traz anseio, aflinge, etc), Emoções positivas,
                                    quais são suas dores, quais são suas objeções, quais são seus resultados dos sonhos,
                                    suas metas e objetivos e qual o seu canal favorito (entre facebook, instagram, whatsapp, youtube ou linkedin), em português brasileiro. 
                                    Crie oito buyer personas.'''
                  
                        buyer_persona_output = modelo_linguagem.generate_content(prompt_buyer_persona).text


                        prompt_tom = f'''Descrição do tom de voz, incluindo nuvem de palavras e palavras proibidas. Levando em conta o ramo de atuação: ({ramo_atuacao}), o brand persona: ({brand_persona_output})
                        e o buyer persona: ({buyer_persona_output}).
                                    Retorne 10 adjetivos que definem o tom com suas respectivas explicações. ex: tom é amigavel, para transparecer uma 
                                    relação de confiança com frases de exemplo de aplicação do tom em português brasileiro.'''
                  
                        tom_output = modelo_linguagem.generate_content(prompt_tom).text

                        #Printando Tarefas

                        st.header('1. Etapa de Pesquisa de Mercado')
                        st.subheader('1.1 Análise SWOT')
                        st.markdown(SWOT_output)
                        st.subheader('1.2 Análise PEST')
                        st.markdown(PEST_output)
                        st.subheader('1.3 Análise de tendências')
                        st.markdown(tendencias_output)
                        st.subheader('1.4 Análise de concorrências')
                        st.markdown(concorrencias_output)

                        
                

                        st.header('2. Etapa de Estratégica')
                        st.subheader('2.1 Golden Circle')
                        st.markdown(golden_output)
                        st.subheader('2.2 Posicionamento de Marca')
                        st.markdown(posicionamento_output)
                        st.subheader('2.3 Brand Persona')
                        st.markdown(brand_persona_output)
                        st.subheader('2.4 Buyer Persona')
                        st.markdown(buyer_persona_output)
                        st.subheader('2.5 Tom de Voz')
                        st.markdown(tom_output)

                        # Salva o planejamento no MongoDB
                        save_to_mongo_MKT(SWOT_output,PEST_output,tendencias_output, concorrencias_output, golden_output,posicionamento_output,brand_persona_output,buyer_persona_output,tom_output, nome_cliente)
