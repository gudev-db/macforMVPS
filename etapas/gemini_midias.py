import streamlit as st
import google.generativeai as genai
import uuid
import os
from pymongo import MongoClient
import google.generativeai as genai

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

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
def save_to_mongo_midias(kv_output,redes_output,redesplanej_output,criativos_output,palavras_chave_output,estrategia_conteudo_output, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano de Mídias' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de Mídias',
        "KV": kv_output,
        "Plano_redes_macro":redesplanej_output,
        "Plano_Redes": redes_output,
        "Plano_Criativos": criativos_output,
        "Plano_Palavras_Chave": palavras_chave_output,
        "Estrategia_Conteudo": estrategia_conteudo_output,
    }

    # Insere o documento no MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def planej_midias_page():
    st.subheader('Planejamento de Mídias e Redes')
    st.text('''Aqui geramos plano para criativos, plano de Key Visual, Plano de atuação segmentado por canal (ex: Linkedin, Facebook, Instagram...),
            brainstorming de criativos a serem utilizados, estratégia de conteúdo e sugestões de palavras chave.''')




    # Buscar todos os clientes do banco de dados
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    opcoes_clientes = [cliente["nome"] for cliente in clientes]

    # Selectbox para escolher o cliente
    nome_cliente = st.text_input('Nome do cliente')

    # Obter as informações do cliente selecionado
    cliente_info = next((cliente for cliente in clientes if cliente["nome"] == nome_cliente), None)
    site_cliente = cliente_info["site"] if cliente_info else ""
    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""

    # Exibir os campos preenchidos com os dados do cliente
    st.text_input('Site do Cliente:', value=site_cliente, key="site_cliente")
    st.text_input('Ramo de Atuação:', value=ramo_atuacao, key="ramo_atuacao")
        # Intuito do Plano Estratégico
    intuito_plano = st.text_input('Intuito do Planejamento estratégico: Utilize esse campo para explicitar quais são as espectativas do cliente no desenvolvimento desse planejamento. Exemplo: Gerar mais leads, aumentar vendas, aumentar reconhecimento em alguma região estratégica, etc', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre.")
    
    # Público-Alvo
    publico_alvo = st.text_input('Público alvo: Utilize esse campo para definir qual é o perfil do público alvo que deve ser atingido por esse planejamento estratégico. Seja idade, região, gênero, área de atuação. Aproveite para ser o quão detalhado for necessário.', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda.")
    
    # Concorrentes
    concorrentes = st.text_input('Concorrentes: Utilize esse campo para definir quais são os concorrentes do cliente.', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C. Liste os concorrentes que você considera mais relevantes no seu mercado.")
    
    # Sites dos Concorrentes
    site_concorrentes = st.text_input('Site dos concorrentes: Utilize esse campo para colocar os sites dos concorrentes. A forma como decidir dividí-los não importa. Ex (, ou ; ou .)', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br.")
    
    # Tendências de Interesse
    tendaux = st.text_input('Tendências de mercado estratégicas: Utilize esse campo para definir quais tendências de mercado você gostaria que os agentes de IA pesquisassem sobre de uma forma que o retorno tenha impacto no planejamento estratégico.', key="tendaux", placeholder="Ex: IA, novos fluxos de marketing, etc.")
    
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
    referencia_da_marca = st.text_area('Referência de marca: Utilize esse campo para escrever um texto que define o cliente quanto ao seu ramo de atuação, objetivos e personalidade.', key="referencia_da_marca", placeholder="Conte um pouco mais sobre sua marca, o que ela representa, seus valores e diferenciais no mercado.", height = 200)

    budget = st.text_input('Orçamento de Anúncios: Utilize esse campo para explicitar o orçamento disponível para o desenvolvimento dos anúncios a serem gerados.', key="budget", placeholder="Valor em reais")

    start_date = st.date_input("Data de Início do período de contratação de serviços:", key="start_date")
    end_date = st.date_input("Data do Fim do período de contratação de serviços::", key="end_date")

    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)

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

                        prompt_kv = f"""
                        Defina o Key Visual para a marca {nome_cliente}, levando em consideração os seguintes pontos:

                        - O ramo de atuação da empresa: {ramo_atuacao}.
                        - O intuito estratégico do plano de marketing: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        
                        O Key Visual deve ser a representação visual central para campanhas de marketing, refletindo a identidade da marca e ressoando com o público-alvo. Ele deve ser aplicável em diferentes materiais de comunicação, como anúncios, redes sociais, e embalagens.
                        
                        A definição do Key Visual deve ser detalhada da seguinte forma:
                        
                        1. **Imagem Conceito:** Defina a imagem que encapsula os valores e o propósito da marca. Justifique a escolha com base em elementos visuais comumente utilizados no ramo de atuação {ramo_atuacao} e como isso se conecta ao público-alvo {publico_alvo}. Explique por que essa imagem foi escolhida, incluindo referências culturais, psicológicas e comportamentais.
                        Imagine que você irá contratar um designer para desenvolver essa imagem. Detalhe-a em como ela deve ser feita em um nível extremamente detalhados. Serão guidelines extremamente
                        delhadados, precisos e justificados que o designer irá receber para desenvolver a imagem conceito. Não seja vago. Dia exatamente quais são os elementos visuais em extremo
                        detalhe e justificados.
                        
                        2. **Tipografia:** Escolha uma fonte tipográfica que complemente a imagem conceito. Detalhe a escolha e a forma como a tipografia reflete a identidade da marca, levando em conta a legibilidade e a conexão emocional com o público. Explique as escolhas de estilo, espessura e espaçamento.
                        
                        3. **Cores:** Selecione uma paleta de cores específica para o Key Visual. Justifique as escolhas com base em psicologia das cores e tendências do mercado no ramo de atuação {ramo_atuacao}. Detalhe como essas cores evocam emoções e criam uma identidade visual forte e coesa.
                        
                        4. **Elementos Gráficos:** Defina quais elementos gráficos, como formas, ícones ou texturas, são fundamentais para compor o Key Visual. Justifique a escolha desses elementos em relação à consistência da identidade visual e à relevância para o público-alvo.

                        """
                        kv_output = modelo_linguagem.generate_content(prompt_kv).text

                        prompt_redesplanej = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - data de inicio {start_date}
                        - data fim {end_date}
                        - orçamento para plataformas de anúncios: {budget} reais
                        
                        - Extraia todo o seu conhecimento possível sobre marketing digital, estratégicas de campanhas:
                        
                        - Em formato de tabela, cronograma e considerando datas comemorativas, divida a estratégia de acordo com cada rede social (Instagram, Facebook, LinkedIn, WhatsApp, YouTube) no que se refere a alocação do orçamento para os anúncios: {budget} reais (alocação
                        devida e detalhadamente justificada) definindo tambem
                        tipos de campanhas a serem realizadas (ex: pesquisa, display, video, app, pmax) de acordo com a plataforma e porque. Quebre o investimento, tipo de campanha e estratégia
                        por plataforma e periodo (dentro de {start_date} e {end_date}). Detalhe o quanto cada campanha deve gastar, por qual pedíodo, por qual plataforma, qual é o tipo de campanha,
                        justificando sempre o porque de cada atributo. Primeiro justifique a alocação de recursos temporalmente e depois por plataforma. Quantidade a ser gasta em cada etapa temporal
                        por que? Quantidade a ser gasta em cada plataforma porque? Redija textos justificando o porque que cada fase recebe mais ou menos recursos,
                        o porque que cada plataforma recebe mais ou menos recursos. 
                     
                        
                        não resuma ou pule etapas. quero o cronograma completo.
                        


                        """
                        redesplanej_output = modelo_linguagem.generate_content(prompt_redesplanej).text

                        prompt_redes = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        
                        Divida a estratégia de acordo com cada rede social (Instagram, Facebook, LinkedIn, WhatsApp, YouTube), oferecendo ideias criativas e diferenciadas para cada plataforma. Para cada uma delas, defina o tom de voz e estratégias específicas de conteúdo.
                        
                        1. **Instagram & Facebook:**
                           - 5 ideias de Reels e Stories: Explique como essas ideias capturam a atenção e engajam o público.
                           - 5 ideias de posts estáticos e carrosséis: Descreva como esses formatos ajudam a aumentar a conscientização da marca.
                           - 5 ideias de conteúdo localizado: Aproxime a marca do público local, considerando preferências culturais e comportamentais.
                        
                        2. **LinkedIn:**
                           - 5 ideias de conteúdos educativos e informativos: Envolva o público com informações valiosas e especializadas.
                           - 5 ideias de depoimentos de sucesso: Utilize histórias reais para gerar confiança e credibilidade.
                           - 5 ideias de eventos e comemorações: Relacione a marca com momentos importantes para o público.
                           - Defina o tom de voz para LinkedIn.
                           - 5 sugestões de CTAs: Proponha ações com objetivos claros e atraentes.
                        
                        3. **WhatsApp:**
                           - 5 ideias de canais: Estratégias de comunicação direta e personalizada.
                           - 5 ideias de listas de transmissão: Engajamento com grupos segmentados.
                           - 5 ideias de análises regulares: Como medir o impacto da comunicação e melhorar o engajamento.
                        
                        4. **YouTube:**
                           - 5 ideias de Shorts: Estratégias curtas e impactantes.
                           - 5 ideias de conteúdos com especialistas: Produza conteúdos com autoridade no tema.
                           - 5 ideias de vídeos: Defina o tipo de vídeos que atraem e educam o público.
                           - 5 ideias de análises regulares: Como fazer revisões de performance para otimizar a estratégia.
                        
                        Além disso, inclua sugestões sobre o que evitar em cada plataforma, para não prejudicar a imagem da marca.

                        """
                        
                        redes_output = modelo_linguagem.generate_content(prompt_redes).text

                        prompt_criativos = f"""
                        Crie 10 criativos para as campanhas de marketing digital em um nível bem detalhado, aprodundado,
                        oriundos da concepção de um especialista em nível acadêmico sobre marketing digital, que referencia e justifica todas
                        as suas escolhas. Para {nome_cliente}, considerando os seguintes pontos:

                        - Ramo de atuação: {ramo_atuacao}.
                        - Intuito estratégico do plano: {intuito_plano}.
                        - Público-alvo: {publico_alvo}.
                        - Referência da marca: {referencia_da_marca}.
                        
                        Cada criativo deve incluir:
                        
                        1. **Título**: Seja criativo, objetivo e alinhado com a proposta de valor da marca.
                        2. **Descrição**: Corpo de texto do anúncio.
                        3. **Tipo de Imagem ou Vídeo Sugerido**: Indique qual estilo de imagem ou elemento visual deve ser usado (foto, ilustração, gráfico, etc.) e explique por que esse tipo de imagem é o mais eficaz para o público e o ramo de atuação.
                        Detalhe-a em como ela deve ser feita em um nível extremamente detalhados. Serão guidelines extremamente
                        delhadados, precisos e justificados que o designer irá receber para desenvolver a imagem conceito. Não seja vago. Dia exatamente quais são os elementos visuais em extremo
                        detalhe e justificados.

                        
                        Seja original e proponha ideias que possam ser executadas com um alto impacto.

                        """
                        criativos_output = modelo_linguagem.generate_content(prompt_criativos).text


                        #SEO e Site


                        prompt_palavras_chave = f"""
                        Desenvolva um relatório detalhado de sugestões de palavras-chave para SEO para {nome_cliente}, levando em conta:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O público-alvo: {publico_alvo}.
                        - O comportamento de busca online do público-alvo.
                        
                        No relatório, inclua:
                        
                        1. **Palavras-chave principais**: Liste as palavras-chave mais relevantes, com base em volume de busca e relevância para o cliente.
                        2. **Palavras-chave secundárias**: Inclua termos relacionados que podem gerar tráfego complementar.
                        3. **Tendências e variações de busca**: Analise variações de palavras-chave que podem ajudar a aumentar a visibilidade.
                        4. **Sugestões de conteúdo otimizado**: Ofereça sugestões de tipos de conteúdo que possam ser usados para melhorar o SEO, como artigos, blogs ou vídeos.
                        5. **Estratégias de otimização on-page e off-page**: Forneça dicas de como melhorar a presença online de {nome_cliente} a partir dessas palavras-chave.
                        
                        Seja claro e detalhado, com uma explicação de como cada palavra-chave pode gerar resultados tangíveis para a marca.

                        """
                        palavras_chave_output = modelo_linguagem.generate_content(prompt_palavras_chave).text

                        prompt_estrategia_conteudo = f"""
                       Crie uma estratégia de conteúdo detalhada para {nome_cliente}, considerando:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        
                        A estratégia deve ser dividida em 5 pilares de conteúdo, com explicações detalhadas sobre como cada um contribuirá para os objetivos da marca:
                        
                        1. **Institucional**:
                           - Objetivo: Posicionar a marca e gerar credibilidade.
                           - Conteúdo: Defina o tipo de conteúdo (ex: história da empresa, missão, visão).
                           - Canal: Sugira as plataformas onde esse conteúdo deve ser veiculado.
                        
                        2. **Inspiração**:
                           - Objetivo: Criar uma conexão emocional com o público.
                           - Conteúdo: Defina histórias e temas inspiradores.
                           - Canal: Sugira plataformas adequadas para esse tipo de conteúdo.
                        
                        3. **Educação**:
                           - Objetivo: Educar o público sobre produtos, serviços ou tendências do mercado.
                           - Conteúdo: Ofereça temas educativos relevantes para o público-alvo.
                           - Canal: Defina as plataformas mais eficazes para esse tipo de conteúdo.
                        
                        4. **Produtos/Serviços**:
                           - Objetivo: Gerar leads e promover vendas.
                           - Conteúdo: Detalhe como destacar os produtos ou serviços de maneira atrativa.
                           - Canal: Quais canais serão mais eficazes para conversões?
                        
                        5. **Relacionamento**:
                           - Objetivo: Criar e manter um relacionamento de longo prazo com o público.
                           - Conteúdo: Defina conteúdo interativo ou de engajamento.
                           - Canal: Sugira canais onde o engajamento direto com o público seja mais efetivo.
                        
                        Inclua também sugestões de formatos, como blogs, vídeos, webinars, posts interativos, etc.

                        """
                        estrategia_conteudo_output = modelo_linguagem.generate_content(prompt_estrategia_conteudo).text

                        tarefas_midia = [
                            {"output": kv_output},
                            {"output": redes_output},
                            {"output": criativos_output},
                            {"output": palavras_chave_output},
                            {"output": estrategia_conteudo_output},
                        ]

                        # Exibe os resultados na interface
                        st.header('Plano de Redes Sociais e Mídias')
                        st.subheader('1. Plano de Key Visual')
                        st.markdown(kv_output)
                        st.subheader('2. Plano para Redes')
                        st.markdown(redesplanej_output)
                        st.markdown(redes_output)                   
                        st.subheader('3. Plano para Criativos')
                        st.markdown(criativos_output)
                        st.subheader('4. Estratégia de Conteúdo')
                        st.markdown(estrategia_conteudo_output)
                        st.subheader('5. SEO - Palavras Chave')
                        st.markdown(palavras_chave_output)


                        # Salva o planejamento no MongoDB
                        save_to_mongo_midias(kv_output,redes_output,redesplanej_output,criativos_output,palavras_chave_output,estrategia_conteudo_output, nome_cliente)
