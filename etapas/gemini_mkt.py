import streamlit as st
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import uuid
import os
from pymongo import MongoClient
from datetime import datetime
import os
from pymongo import MongoClient
import requests



rapid_key = os.getenv("RAPID_API")



exp_golden = '''

Comunique seu 'porquê' aos seus clientes

Sinek explica que o 'Porquê' é provavelmente a mensagem mais importante que uma organização ou indivíduo pode comunicar, pois é isso que inspira os outros a agir. "Comece pelo Porquê" é a forma de explicar seu propósito, a razão pela qual você existe e se comporta como se comporta. A teoria de Sinek é que comunicar com sucesso a paixão por trás do 'Porquê' é uma maneira de se conectar com o cérebro límbico do ouvinte. Essa é a parte do nosso cérebro que processa sentimentos como confiança e lealdade – além de ser responsável pela tomada de decisões.

Articular com sucesso seu 'Porquê' é uma maneira muito impactante de se comunicar com outras pessoas, definir sua proposta de valor específica e inspirá-las a agir. Sinek argumenta que comunicar o 'Porquê' ativa a parte do cérebro que influencia o comportamento. É por isso que o modelo do Círculo Dourado é considerado uma teoria tão influente de liderança. No nível organizacional, comunicar seu 'Porquê' é a base de uma proposta de valor forte que diferenciará sua marca das demais.

Anthony Villis apresenta um visual útil no blog First Wealth, relacionando os objetivos do Círculo Dourado à resposta psicológica.

Como
Os fatores do 'Como' de uma organização podem incluir seus pontos fortes ou valores que a diferenciam da concorrência. Sinek afirma que a mensagem do 'Como' também pode se comunicar com o cérebro límbico – a parte importante que governa o comportamento e a emoção. No entanto, ele defende que as organizações deveriam melhorar a forma como articulam seu 'Porquê', além do 'Como'.

O que
É relativamente fácil para qualquer líder ou organização articular 'O que' fazem. Isso pode ser expresso pelos produtos que uma empresa vende ou pelos serviços que oferece. Para um indivíduo, seria seu cargo. Sinek argumenta que a comunicação do 'O que' envolve apenas o neocórtex – a parte racional do nosso cérebro. Ele acredita que essa parte do cérebro tem um papel menor na tomada de decisões em comparação ao cérebro límbico, que é alcançado melhor pelo 'Porquê' e pelo 'Como'. Pessoas e organizações bem-sucedidas expressam por que fazem o que fazem, em vez de se concentrarem apenas no que fazem.

'''



# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = "gemini-1.5-flash"  # Usando Gemini






golden_exp = '''
Comunique seu 'porquê' aos seus clientes

Sinek explica que o 'Porquê' é provavelmente a mensagem mais importante que uma organização ou indivíduo pode comunicar, pois é isso que inspira os outros a agir. "Comece pelo Porquê" é a forma de explicar seu propósito, a razão pela qual você existe e se comporta como se comporta. A teoria de Sinek é que comunicar com sucesso a paixão por trás do 'Porquê' é uma maneira de se conectar com o cérebro límbico do ouvinte. Essa é a parte do nosso cérebro que processa sentimentos como confiança e lealdade – além de ser responsável pela tomada de decisões.

Articular com sucesso seu 'Porquê' é uma maneira muito impactante de se comunicar com outras pessoas, definir sua proposta de valor específica e inspirá-las a agir. Sinek argumenta que comunicar o 'Porquê' ativa a parte do cérebro que influencia o comportamento. É por isso que o modelo do Círculo Dourado é considerado uma teoria tão influente de liderança. No nível organizacional, comunicar seu 'Porquê' é a base de uma proposta de valor forte que diferenciará sua marca das demais.

Anthony Villis apresenta um visual útil no blog First Wealth, relacionando os objetivos do Círculo Dourado à resposta psicológica.

Como
Os fatores do 'Como' de uma organização podem incluir seus pontos fortes ou valores que a diferenciam da concorrência. Sinek afirma que a mensagem do 'Como' também pode se comunicar com o cérebro límbico – a parte importante que governa o comportamento e a emoção. No entanto, ele defende que as organizações deveriam melhorar a forma como articulam seu 'Porquê', além do 'Como'.

O que
É relativamente fácil para qualquer líder ou organização articular 'O que' fazem. Isso pode ser expresso pelos produtos que uma empresa vende ou pelos serviços que oferece. Para um indivíduo, seria seu cargo. Sinek argumenta que a comunicação do 'O que' envolve apenas o neocórtex – a parte racional do nosso cérebro. Ele acredita que essa parte do cérebro tem um papel menor na tomada de decisões em comparação ao cérebro límbico, que é alcançado melhor pelo 'Porquê' e pelo 'Como'. Pessoas e organizações bem-sucedidas expressam por que fazem o que fazem, em vez de se concentrarem apenas no que fazem.
'''


# Conexão com MongoDB
client2 = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client2['arquivos_planejamento']
collection = db['auto_doc']
banco = client2["arquivos_planejamento"]
db_clientes = banco["clientes"]  # info clientes

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

# Função para salvar no MongoDB
def save_to_mongo_MKT(SWOT_output,PEST_output, concorrencias_output, golden_output,posicionamento_output,brand_persona_output,buyer_persona_output,tom_output, nome_cliente):    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano Estratégico' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano Estratégico',
        "Etapa_1_Pesquisa_Mercado": {
            "Análise_SWOT": SWOT_output,
            "Análise_PEST": PEST_output,
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
    st.subheader('Planejamento de Pesquisa e Estratégia')
    st.text('''Aqui é gerado o planejamento de Pesquisa e Estratégia. Geramos análise SWOT, análise PEST, análise de tendências de mercado,
            análise de concorrências, Golden Circle, Posicionamento de marca, Brand Persona, Buyer Pesona e Tom de Voz''')
    


    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")
   
    # Exibir os campos preenchidos com os dados do cliente
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente")
    ramo_atuacao = st.text_input('Ramo de Atuação:', key="ramo_atuacao")
    
    # Intuito do Plano Estratégico
    intuito_plano = st.text_input('Intuito do Planejamento estratégico: Utilize esse campo para explicitar quais são as espectativas do cliente no desenvolvimento desse planejamento. Exemplo: Gerar mais leads, aumentar vendas, aumentar reconhecimento em alguma região estratégica, etc', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre. O que você deseja alcançar com esse plano?")
    
    # Público-Alvo
    publico_alvo = st.text_input('Público alvo: Utilize esse campo para definir qual é o perfil do público alvo que deve ser atingido por esse planejamento estratégico. Seja idade, região, gênero, área de atuação. Aproveite para ser o quão detalhado for necessário.', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda. Defina o perfil das pessoas que você quer atingir.")
    
    # Concorrentes
    concorrentes = st.text_input('Concorrentes: Utilize esse campo para definir quais são os concorrentes do cliente.', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C. Liste os concorrentes que você considera mais relevantes no seu mercado.")
    
    # Sites dos Concorrentes
    site_concorrentes = st.text_input('Site dos concorrentes: Utilize esse campo para colocar os sites dos concorrentes. A forma como decidir dividí-los não importa. Ex (, ou ; ou .)', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br. Insira os sites dos seus concorrentes para compararmos.")
    
    
    # Objetivos de Marca
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]
    
    objetivos_de_marca = st.selectbox('Quais são os objetivos da sua marca?', objetivos_opcoes, key="objetivos_marca")
    
    # Referência da Marca
    referencia_da_marca = st.text_area('Referência de marca: Utilize esse campo para escrever um texto que define o cliente quanto ao seu ramo de atuação, objetivos e personalidade.', key="referencia_da_marca", placeholder="Conte um pouco mais sobre sua marca, o que ela representa, seus valores e diferenciais no mercado.")

    sucesso = st.text_input('O que é sucesso para a marca?:', key="sucesso", help='Redija aqui um texto que define o que a marca considera como sucesso. O que ela precisa alcançar para considerar que atingiu os seus objetivos?')

    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)

        # Set parameters for the search
    days = 90
    max_results = 15


  
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
                    with st.spinner('Gerando o planejamento...'):

                        model_id = "gemini-2.0-flash"

                        google_search_tool = Tool(
                            google_search = GoogleSearch()
                        )
                        
                        # Agente de pesquisa política
                        pls = client.models.generate_content(
                            model=model_id,
                            contents="Faça uma pesquisa sobre notícias políticas recentes sobre o Brasil",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )
                        
                        # Agente de pesquisa econômica do Brasil
                        dados_econ_brasil = client.models.generate_content(
                            model=model_id,
                            contents="Faça uma pesquisa sobre dados econômicos recentes sobre o Brasil",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )
                        
                        # Agente de notícias sobre concorrentes
                        novids_conc = client.models.generate_content(
                            model=model_id,
                            contents=f"Faça uma pesquisa sobre as notícias mais recentes sobre os concorrentes: {concorrentes}",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )

                        # Agente de pesquisa Social
                        tend_social_duck = client.models.generate_content(
                            model=model_id,
                            contents="Pesquise sobre novidades no âmbito social brasileiro",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )
                        
                        # Agente de pesquisa tecnológica
                        tec = client.models.generate_content(
                            model=model_id,
                            contents=f'''Pesquise novidades tecnológicas no ramo de atuação: {ramo_atuacao}''',
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )





                       





                      

                        # Agente desenvolvedor de análise SWOT

                        prompt_SWOT = f'''Assumindo um especialista em administração de marketing, extraia todo o conhecimento existente sobre marketing em um nível extremamente aprofundado.
                        
                        Para o cliente {nome_cliente}, Considerando o seguinte contexto a referência da marca:
                                    {referencia_da_marca}, para o cliente no ramo de atuação {ramo_atuacao}. E considerando o que a marca considera como sucesso em ({sucesso}) e os objetivos de marca ({objetivos_de_marca}):
                                    realize a Análise SWOT completa em português brasileiro. 
                                    Elabore 10 pontos em cada segmento da análise SWOT. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing. 
                                    Cada ponto deve ser pelo menos 3 frases detalhadas, profundas e não genéricas. 
                                    Você está aqui para trazer conhecimento estratégico. organize os pontos em bullets
                                    pra ficarem organizados dentro de cada segmento da tabela.'''

                        
                        pre_SWOT_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_SWOT]).text

                        SWOT_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                  ###SISTEMA###
                                  Você é um redator humano especialista em redijir planejamentos estratégicos, você
                                  irá receber como entrada etapas do planejamento estratégico e seu papel é aproximar
                                  essa entrada de uma saída de um especialista humano. Seu papel é tornar a entrada
                                  melhor e menos genérica. Apenas reescreva a entrada. Não fale o que você mudou. Apenas 
                                  reescreva o que você recebu de entrada e a torne melhor. Não seja genérico. Não seja vago. Seja prático.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###

                            Reescreva a seguinte análise SWOT menos genérica e mais relevante:{pre_SWOT_output}''']).text
                        
                        # Avaliador SWOT
                        SWOT_guides = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                  ###SISTEMA###
                                  Você é um expert em analisar análises SWOT e apontar como elas podem melhorar. Você não inventa informações e se trouxer números, traz o link da fonte.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###

                            Considerando o output de análise SWOT, proponha melhoras para que ele fique menos genérico
                                  e melhor reidijido  Você deve encontrar falhas na redação e ver como ela pode
                                  se tornar menos amadora:{SWOT_output}''']).text
                        
                        SWOT_final = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                   ###SISTEMA###
                                  Você é um redator humano especialista em redijir planejamentos estratégicos, você
                                  irá receber como entrada etapas do planejamento estratégico e seu papel é aproximar
                                  essa entrada de uma saída de um especialista humano. Seu papel é tornar a entrada
                                  melhor e menos genérica. Apenas reescreva a entrada. Não fale o que você mudou. Apenas 
                                  reescreva o que você recebu de entrada e a torne melhor. Mantenha o formato de uma análise SWOT. Não traga percentuais ou métricas na análise.
                                  Essas são as melhorias propostas: {SWOT_guides}
                                  
                                  ###FIM DAS DIRETRIZES DE SISTEMA###

                            Considerando os guias de melhorias e o output prévio da análise SWOT :{SWOT_output}, reescreva a análise SWOT melhorada.''']).text
                        
                        




                        prompt_concorrencias = f'''Assumindo o papel um especialista em administração de marketing, extraia todo o conhecimento existente sobre marketing em um nível extremamente aprofundado., -
                                    
                                    
                                    - considerando o que a marca considera como sucesso em ({sucesso}) e os objetivos de marca ({objetivos_de_marca})
                                    -Considerando {concorrentes} como a concorrência direta de {nome_cliente}, redija sobre as notícias sobre o concorrente explicitadas em {novids_conc} e como o
                                    cliente {nome_cliente} pode superar isso. Aprofundando em um nível bem detalhado, com parágrafos para cada ponto extremamente bem
                                    explicado. Não seja superficial. Seja detalhista, comunicativo, aprofundado, especialista. Tenha um olhar sob a ótica de marketing, que é o foco de nossa empresa.
                                    Veja como {nome_cliente} pode se destacar em contraponto ao(s) concorrente(s) sob uma ótica estratégica de marketing. Traga impacto nas suas análises. Você é um especialista e está aqui para liderar nossos processos.
                                    -  Se não houver nenhuma informação sobre a concorrência (se nenhum concorrente for listado), mantenha esse campo em branco. Você não deve inventar informações.

'''

                        concorrencias_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_concorrencias]).text

                       


                        prompt_PEST = f'''Assumindo um especialista em administração de marketing.
                                    - considerando o que a marca considera como sucesso em ({sucesso}) e os objetivos de marca ({objetivos_de_marca})

                        Análise PEST com pelo menos 10 pontos relevantes em cada etapa em português brasileiro 
                                    considerando:   contexto político: {pls}, dados econômicos
                                    relevantes: ({dados_econ_brasil}), contexto social:
                                    ({tend_social_duck}), contexto tecnológico: ({tec}).
                                    Quero pelo menos 10 pontos em cada segmento da análise PEST. Pontos relevantes que irão alavancar insights poderosos no planejamento de marketing.'''
                        

                        pre_PEST_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_PEST]).text

                        PEST_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                            ###SISTEMA###
                                  Você é um redator humano especialista em redijir planejamentos estratégicos, você
                                  irá receber como entrada etapas do planejamento estratégico e seu papel é aproximar
                                  essa entrada de uma saída de um especialista humano. Seu papel é tornar a entrada
                                  melhor e menos genérica. Apenas reescreva a entrada. Não fale o que você mudou. Apenas 
                                  reescreva o que você recebu de entrada e a torne melhor.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###
                        
                        
                                  Reescreva a seguinte análise PEST menos genérica, melhor redijida: {pre_PEST_output}''']).text


                         # Avaliador PEST
                        PEST_guides = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                  ###SISTEMA###
                                  Você é um expert em analisar análises PEST e apontar como elas podem melhorar. Você deve encontrar falhas na redação e ver como ela pode
                                  se tornar menos amadora. Você não inventa informações e se trouxer números, traz o link da fonte.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###

                            Considerando o output de análise PEST, proponha melhoras para que ele fique menos genérico
                                  e melhor reidijido :{PEST_output}''']).text
                        
                        PEST_final = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                   ###SISTEMA###
                                  Você é um redator humano especialista em redijir planejamentos estratégicos, você
                                  irá receber como entrada etapas do planejamento estratégico e seu papel é aproximar
                                  essa entrada de uma saída de um especialista humano. Seu papel é tornar a entrada
                                  melhor e menos genérica. Apenas reescreva a entrada. Não fale o que você mudou. Apenas 
                                  reescreva o que você recebu de entrada e a torne melhor. Mantenha o formato de uma análise PEST. Não traga percentuais ou métricas na análise.
                                  Essas são as melhorias propostas: {PEST_guides}
                                  
                                  ###FIM DAS DIRETRIZES DE SISTEMA###
                                  Você nunca deve mudar a sigla Análise PEST.

                            Considerando os guias de melhorias e o output prévio da análise PEST :{PEST_output}, reescreva a análise PEST melhorada.''']).text
                        

                        prompt_golden = f'''

                        eis uma explicação sobre o que é golden circle: ({exp_golden});

                        
                        - não seja genérico
                        - traga impacto com seu output
                        - você é um especialista em administração de marketing; Você tem todo o conhecimento possível comparavel à Simon Sinek
                        - Você está aqui para fazer a diferença
                        - considerando o que a marca considera como sucesso em ({sucesso}) e os objetivos de marca ({objetivos_de_marca})
                        - seja único. una o que torna o cliente {nome_cliente} de diferente em relação ao resto.

                        Como um especialista em administração de marketing, gere um Golden Circle completo com 'how', 'why' e 'what' resumidos 
                                    em uma frase cada. Considerando e sintetizando de forma perspicaz o seguinte contexto 
                                     e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca}, a análise SWOT ({SWOT_output}).'''
                      

                        pre_golden_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_golden]).text

                        golden_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                        ###SISTEMA###
                                  Você é um redator humano especialista em redijir planejamentos estratégicos, você
                                  irá receber como entrada etapas do planejamento estratégico e seu papel é aproximar
                                  essa entrada de uma saída de um especialista humano. Seu papel é tornar a entrada
                                  melhor e menos genérica. Apenas reescreva a entrada. Não fale o que você mudou. Apenas 
                                  reescreva o que você recebu de entrada e a torne melhor.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###
                        
                                  Reescreva o seguinte Golden Circle menos genérico, melhor redijido, com mais impacto (MANTENHA UMA ÚNICA FRASE PARA O HOW, WHAT e WHY): {pre_golden_output}''']).text

                        prompt_posicionamento = f'''
                            
                                    - levando em conta a análise SWOT: ({SWOT_output}) e o golden circle: ({golden_output}) e considerando que a marca considera como sucesso: {sucesso}.
                                    - considerando os objetivos de marca ({objetivos_de_marca})
                                    - traga impacto, originalidade, sagacidade com seu retorno

                                    Gerar 1 Posicionamento de marca para o cliente {nome_cliente} do ramo de atuação {ramo_atuacao} Com um slogan com essas inspirações (que não
                                    devem ser copiadas, mas sim, usadas como referência na construção de um novo e original slogan) Seja original,
                                    esperto com as palavras na construção do slogan. Correlacione-as e crie impacto com a construção do seu slogan
                                    original. Tire ideias pulo do gato:

                                    Exemplos de bons slogans (não copie-os, apenas aprenda com eles o que é um bom slogan):
                                    
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

                                    
                                    - O posicionamento de marca deve ter impacto, um tcham. Não seja genérico.
                                    - Me traga a lógica de como o posicionamento foi pensado. Me explique porque ele é como é. Justifique. Use base
                                    de conhecimento de marketing digital para justificá-lo.
                                    
                                    '''
                  

                        pre_posicionamento_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_posicionamento]).text

                        posicionamento_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                        ###SISTEMA###
                                  Você é um redator humano especialista em redijir posicionamentos de marcas únicos e inétidos. De uma forma que relacionem
                                  a atividade fim da empresa e seus objetivos, assim como sua identidade. Você está aqui para reescrever um posicionamento de 
                                  marca de forma que ele fique simplesmente melhor, mais único, menos genérico, mais representativo, mais impactante.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###
                                  
                                  Reescreva o seguinte posicionamento de marca menos genérico, de melhor qualidade, com mais impacto: {pre_posicionamento_output}]).text
                                Você precisa fazer com que o posicionamento de marca torne a empresa {nome_cliente} de fato 'dono' do posicionamento.''']

                         # Avaliador de Posicionamento
                        posicionamento_guides = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                  ###SISTEMA###
                                  Você é um expert em analisar posicionamento de marca e apontar como elas podem melhorar. Você não inventa informações e se trouxer números, traz o link da fonte.
                                  ###FIM DAS DIRETRIZES DE SISTEMA###

                            Considerando o output de posicionamento de marca, proponha melhoras para que ele fique menos genérico
                                  e melhor reidijido:{posicionamento_output}''']).text
                        
                        posicionamento_final = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''
                                   ###SISTEMA###
                                  Você é um redator humano especialista em redijir planejamentos estratégicos, você
                                  irá receber como entrada etapas do planejamento estratégico e seu papel é aproximar
                                  essa entrada de uma saída de um especialista humano. Seu papel é tornar a entrada
                                  melhor e menos genérica. Apenas reescreva a entrada. Não fale o que você mudou. Apenas 
                                  reescreva o que você recebu de entrada e a torne melhor. Mantenha o formato de um posicionamento de marca.
                                  Essas são as melhorias propostas: {posicionamento_guides}
                                  
                                  ###FIM DAS DIRETRIZES DE SISTEMA###

                            Considerando os guias de melhorias e o output prévio da análise PEST :{posicionamento_output}, reescreva a análise PEST melhorada.''']).text
                        

                        prompt_brand_persona = f'''2 Brand Personas detalhada, alinhada com a marca do {nome_cliente} que é do setor de atuação {ramo_atuacao} em português brasileiro considerando o 
                                    seguinte contexto. Lembre que a brand persona é uma persona representativa da marca e da forma como ela se apresenta para o cliente.
                                    
                                    o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca},. 

                                    Essa persona deve representar a MARCA do cliente {nome_cliente}. É uma persona que incorpora a empresa em si. seus valores, forma de ser, ramo de atuação. Como a empresa se apresenta para o cliente.
                                    
                                    - Defina seu nome (deve ser o nome de uma pessoa normal como fernando pessoa, maria crivellari, etc)
                                    -Defina seu gênero, faixa de idade, qual a sua bagagem, defina sua personalidade. 
                                    -Defina suas características: possui filhos? É amigável? quais seus objetivos? qual seu repertório? O que gosta de fazer?
                                    -Comunicação: Como se expressa? Qual o seu tom? Qual o seu linguajar?

                                    -apresente demonstração de escuta ativa ou dados primários que justifiquem as escolhas estratégicas. Traga dores que não sejam superficiais. aprofunde no “por que” das personas.
                                    
                                    Crie exemplos práticos de aplicação das personas também. Como essa persona interage? Que decisões toma? Como é a comunicação dela? Que tipos de post ela faria? Como ela escreve?'''
                  

                        pre_brand_persona_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_brand_persona]).text

                        brand_persona_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''Considere a seguinte Brand Persona, faça com que ela realmente represente a marca, aproxime-a de uma persona que representa a marca {nome_cliente}, ela não deve ser um buyer persona, ela deve ser um brand persona, aproxime-a do conceito de BRAND PERSONA: {pre_brand_persona_output}.                                     -apresente demonstração de escuta ativa ou dados primários que justifiquem as escolhas estratégicas. Traga dores que não sejam superficiais. aprofunde no “por que” das personas.
''']).text

                        brand_persona_talk = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f''' Com base no brand pesona: {brand_persona_output}, redija exemplos de fala para ela''']).text

                        prompt_buyer_persona = f'''
                                    - considerando o que a marca considera como sucesso em ({sucesso}) e os objetivos de marca ({objetivos_de_marca})
                        
                        Descrição detalhada de 2 buyer personas considerando o público-alvo: {publico_alvo} e o 
                                    objetivo do plano estratégico como descrito em {intuito_plano} com os seguintes atributos enunciados: 
                                    nome fictício, idade, gênero, classe social, objetivos,  vontades, Emoções negativas (o que lhe traz anseio, aflinge, etc), Emoções positivas,
                                    quais são suas dores, quais são suas objeções, quais são seus resultados dos sonhos,
                                    suas metas e objetivos e qual o seu canal favorito (entre facebook, instagram, whatsapp, youtube ou linkedin), em português brasileiro. 
                                     -apresente demonstração de escuta ativa ou dados primários que justifiquem as escolhas estratégicas. Traga dores que não sejam superficiais. aprofunde no “por que” das personas.

                                    Crie exemplos práticos de aplicação das personas também. Como essa persona interage? Que decisões toma? Como é a comunicação dela? Que tipos de post ela faria? Como ela escreve?
                                    '''
                  

                        buyer_persona_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_buyer_persona]).text

                        buyer_persona_talk = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f''' Com base no buyer pesona: {buyer_persona_output}, redija exemplos de fala para ela. ''']).text


                        prompt_tom = f'''Descrição do tom de voz, incluindo nuvem de palavras e palavras proibidas. Levando em conta o ramo de atuação: ({ramo_atuacao}), o brand persona: ({brand_persona_output})
                        e o buyer persona: ({buyer_persona_output}).
                                    Retorne 5 adjetivos que definem o tom com suas respectivas explicações. ex: tom é amigavel, para transparecer uma 
                                    relação de confiança com frases de exemplo de aplicação do tom em português brasileiro.
                                    
                                    
                                    Crie exemplos práticos do tom de voz proposto. Você está aqui para substituir o trabalho dos redatores.
                                    
                                    Me diga também contra exemplos do tom de voz; Me mostre como ele não deve se comunicar.
                                    
                                    - Não seja genérico. Traga impacto no seu retorno. Você está aqui para direcionar o trabalho da equipe.'''
                  

                        tom_output = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt_tom]).text

                        #Printando Tarefas

                        st.header('1. Etapa de Pesquisa de Mercado')
                       
                        st.subheader('1.1 Análise SWOT - Avaliada')
                        st.markdown(SWOT_final)
                        
                        st.subheader('1.2 Análise PEST - Avaliada')
                        st.markdown(PEST_final)
                        st.subheader('1.3 Análise de concorrências')
                        st.markdown(concorrencias_output)

                        
                

                        st.header('2. Etapa de Estratégica')
                        st.subheader('2.1 Golden Circle')
                        st.markdown(golden_output)
                        st.subheader('2.2 Posicionamento de Marca')
                        st.markdown(posicionamento_final)
                        st.subheader('2.3 Brand Persona')
                        st.markdown(brand_persona_output)
                        st.markdown(brand_persona_talk)
                        st.subheader('2.4 Buyer Persona')
                        st.markdown(buyer_persona_output)
                        st.markdown(buyer_persona_talk)
                        st.subheader('2.5 Tom de Voz')
                        st.markdown(tom_output)
              
                        # Salva o planejamento no MongoDB
                        save_to_mongo_MKT(SWOT_final,PEST_final,concorrencias_output, golden_output,posicionamento_final,brand_persona_output,buyer_persona_output,tom_output, nome_cliente)
