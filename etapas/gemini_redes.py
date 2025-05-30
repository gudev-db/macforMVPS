import streamlit as st
from google import genai
import uuid
import os
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from pymongo import MongoClient

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Conexão com MongoDB
client1 = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client1['arquivos_planejamento']
collection = db['auto_doc']
banco = client1["arquivos_planejamento"]
db_clientes = banco["clientes"]  # info clientes

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

# Função para salvar no MongoDB
def save_to_mongo_midias(kv_output, redesplanej_output, redesplanej_output_crono, redes_output_meta, redes_output_link, redes_output_wpp, redes_output_yt, criativos_output, palavras_chave_output, estrategia_conteudo_output, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano de Mídias' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de Mídias',
        "KV": kv_output,
        "Plano_redes_macro": redesplanej_output,
        "Cronograma_redes": redesplanej_output_crono,
        "Plano_Redes_Meta": redes_output_meta if 'meta' in st.session_state.selected_networks else None,
        "Plano_Redes_Link": redes_output_link if 'linkedin' in st.session_state.selected_networks else None,
        "Plano_Redes_Wpp": redes_output_wpp if 'whatsapp' in st.session_state.selected_networks else None,
        "Plano_Redes_Yt": redes_output_yt if 'youtube' in st.session_state.selected_networks else None,
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
def planej_redes_page():
    st.subheader('Planejamento de Mídias e Redes')
    st.text('''Aqui geramos plano para criativos, plano de Key Visual, Plano de atuação segmentado por canal (ex: Linkedin, Facebook, Instagram...),
            brainstorming de criativos a serem utilizados, estratégia de conteúdo e sugestões de palavras chave.''')

    # Initialize session state for selected networks if not already set
    if 'selected_networks' not in st.session_state:
        st.session_state.selected_networks = ['meta', 'linkedin', 'whatsapp', 'youtube']  # Default: todas selecionadas

    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")
    site_cliente = st.text_input('Site do Cliente:', help="Digite o site do cliente.")
    ramo_atuacao = st.text_input('Ramo de atuação do cliente:', help="Digite o site do cliente.")

    # Intuito do Plano Estratégico
    intuito_plano = st.text_input('Intuito do Planejamento estratégico:', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre.", help="""
    **Qual o objetivo principal deste planejamento?**
    
    Seja específico sobre as expectativas do cliente. 
    
    Exemplos:
        * Gerar mais leads qualificados.
        * Aumentar as vendas online.
        * Fortalecer o reconhecimento da marca em uma região específica.
    """)

    # Público-Alvo
    publico_alvo = st.text_input('Público alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda.", help="""
    **Quem você quer atingir com essa estratégia?**
    
    Descreva detalhadamente o perfil do seu público-alvo:
    
    * Idade
    * Gênero
    * Localização
    * Interesses
    * Comportamentos
    * etc.
    """)

    # Concorrentes
    concorrentes = st.text_input('Concorrentes:', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C. Liste os concorrentes que você considera mais relevantes no seu mercado.", help="""
    **Quem são seus principais concorrentes?**
    
    Liste as empresas que competem diretamente com o seu cliente.
    """)

    # Sites dos Concorrentes
    site_concorrentes = st.text_input('Site dos concorrentes:', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br.", help="""
    **Quais são os sites dos seus concorrentes?**
    
    Insira os links para os sites dos concorrentes, separados por vírgula, ponto e vírgula ou ponto.
    """)

    # Tendências de Interesse
    tendaux = st.text_input('Tendências de mercado estratégicas:', key="tendaux", placeholder="Ex: IA, novos fluxos de marketing, etc.", help="""
    **Quais tendências de mercado são relevantes para o seu cliente?**
    
    Liste as tendências que podem influenciar a estratégia, como novas tecnologias, mudanças no comportamento do consumidor, etc.
    """)

    # Objetivos de Marca
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]

    objetivos_de_marca = st.selectbox('Quais são os objetivos da sua marca?', objetivos_opcoes, key="objetivos_marca", help="""
    **O que a marca busca alcançar?**
    
    Selecione os objetivos que melhor se encaixam com a estratégia do cliente.
    """)

    # Referência da Marca
    referencia_da_marca = st.text_area('Referência de marca:', key="referencia_da_marca", placeholder="Conte um pouco mais sobre sua marca, o que ela representa, seus valores e diferenciais no mercado.", height=200, help="""
    **Como você descreveria a marca do cliente?**
    
    Forneça informações sobre a identidade da marca, seus valores, sua proposta única de valor e como ela se diferencia no mercado.
    """)

    budget = st.text_input('Orçamento de Anúncios:', key="budget", placeholder="Valor em reais", help="""
    **Quanto o cliente está disposto a investir em anúncios?**
    
    Informe o orçamento disponível para as campanhas de mídia.
    """)

    start_date = st.date_input("Data de Início do período de contratação de serviços:", key="start_date", help="""
    **Quando a estratégia deve começar a ser implementada?**
    """)
    end_date = st.date_input("Data do Fim do período de contratação de serviços::", key="end_date", help="""
    **Quando a estratégia deve ser finalizada?**
    """)

    # Seção para seleção de redes sociais
    st.subheader("Selecione as Redes Sociais para Incluir no Plano")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        meta = st.checkbox("Meta (Instagram/Facebook)", value='meta' in st.session_state.selected_networks)
    with col2:
        linkedin = st.checkbox("LinkedIn", value='linkedin' in st.session_state.selected_networks)
    with col3:
        whatsapp = st.checkbox("WhatsApp", value='whatsapp' in st.session_state.selected_networks)
    with col4:
        youtube = st.checkbox("YouTube", value='youtube' in st.session_state.selected_networks)
    
    # Atualiza as redes selecionadas na sessão
    st.session_state.selected_networks = []
    if meta:
        st.session_state.selected_networks.append('meta')
    if linkedin:
        st.session_state.selected_networks.append('linkedin')
    if whatsapp:
        st.session_state.selected_networks.append('whatsapp')
    if youtube:
        st.session_state.selected_networks.append('youtube')

    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True, help="""
    **Você possui algum material de referência sobre o mercado do cliente?**
    
    Envie arquivos PDF que possam auxiliar na análise do mercado e na criação da estratégia.
    """)

    if st.button('Iniciar Planejamento'):
        if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
            st.error("Por favor, preencha todas as informações do cliente.")
        elif not st.session_state.selected_networks:
            st.error("Por favor, selecione pelo menos uma rede social para o planejamento.")
        else:
            with st.spinner('Gerando o planejamento de mídias...'):
                model_id = "gemini-2.0-flash"
                google_search_tool = Tool(google_search = GoogleSearch())
                
                # Agente de pesquisa de concorrentes
                concorrentes_out = client.models.generate_content(
                    model=model_id,
                    contents=f"Faça uma pesquisa sobre a empresa {concorrentes}",
                    config=GenerateContentConfig(
                        tools=[google_search_tool],
                        response_modalities=["TEXT"],
                    )
                )

                tendencias_out = client.models.generate_content(
                    model=model_id,
                    contents=f"Faça uma pesquisa sobre a empresa {tendaux}",
                    config=GenerateContentConfig(
                        tools=[google_search_tool],
                        response_modalities=["TEXT"],
                    )
                )

                # Geração do Key Visual
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
                kv_output = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_kv]).text
                
                prompt_kv_aval = f"""
                Você é um especialista em garantir a qualidade de Key Visual. Considerando os guias de se fazer um bom key visual.
                
                ##Definição de Key Visual##
                O Key Visual deve ser a representação visual central para campanhas de marketing, refletindo a identidade da marca e ressoando com o público-alvo. Ele deve ser aplicável em diferentes materiais de comunicação, como anúncios, redes sociais, e embalagens.
                
                A definição do Key Visual deve ser detalhada da seguinte forma:
                
                1. **Imagem Conceito:** Defina a imagem que encapsula os valores e o propósito da marca. Justifique a escolha com base em elementos visuais comumente utilizados no ramo de atuação {ramo_atuacao} e como isso se conecta ao público-alvo {publico_alvo}. Explique por que essa imagem foi escolhida, incluindo referências culturais, psicológicas e comportamentais.
                Imagine que você irá contratar um designer para desenvolver essa imagem. Detalhe-a em como ela deve ser feita em um nível extremamente detalhados. Serão guidelines extremamente
                delhadados, precisos e justificados que o designer irá receber para desenvolver a imagem conceito. Não seja vago. Dia exatamente quais são os elementos visuais em extremo
                detalhe e justificados.
                
                2. **Tipografia:** Escolha uma fonte tipográfica que complemente a imagem conceito. Detalhe a escolha e a forma como a tipografia reflete a identidade da marca, levando em conta a legibilidade e a conexão emocional com o público. Explique as escolhas de estilo, espessura e espaçamento.
                
                3. **Cores:** Selecione uma paleta de cores específica para o Key Visual. Justifique as escolhas com base em psicologia das cores e tendências do mercado no ramo de atuação {ramo_atuacao}. Detalhe como essas cores evocam emoções e criam uma identidade visual forte e coesa.
                
                4. **Elementos Gráficos:** Defina quais elementos gráficos, como formas, ícones ou texturas, são fundamentais para compor o Key Visual. Justifique a escolha desses elementos em relação à consistência da identidade visual e à relevância para o público-alvo.
                
                ##Fim de definição de key visual##

                Aponte todas as formas que o key visual seguinte pode melhorar. Assim como ele pode ser mais original e ser algo que um especialista em mídias iria gerar. A imagem deve ser coesa e não muito poluída. Você deve atingir seu objetivo com menos é mais.

                ##Key visual a ser melhorado##
                ({kv_output})
                ## Fim do key visual##
                """
                
                kv_output_final = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[f'''Considerando a avaliação do Key Visual
                            
                            ###Avaliação Key Visual###
                            {prompt_kv_aval}
                            ###Fim da avaliação do Key visual###

                            Com base na avaliação, reescreva o Key Visual Seguinte de uma forma que atenda a avaliação. Não me diga o que você mudou, apenas escreva o novo Key Visual.

                            ##Key Visual a ser avaliado##
                            {kv_output}
                            ##Fim do Key Visual a ser avaliado###
                            
                            ''']).text
                
                # Geração do plano geral de redes
                prompt_redesplanej = f"""
                Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                - O ramo de atuação: {ramo_atuacao}.
                - O intuito estratégico do plano: {intuito_plano}.
                - O público-alvo: {publico_alvo}.
                - A referência da marca: {referencia_da_marca}.
                - data de inicio {start_date}
                - data fim {end_date}
                - orçamento para plataformas de anúncios: {budget} reais

                
                - Extraia todo o seu conhecimento possível sobre marketing digital, estratégicas de campanhas. Não seja vago. Nâo me dê diretrizes, me de ações concretas. Não me ensina sobre marketing, me diga exatamente o que fazer e por que.
                """
                redesplanej_output = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_redesplanej]).text
                
                # Geração do cronograma
                prompt_redesplanej_crono = f"""
                Com base na estratégia de redes definida abaixo
                ##START ESTRATEGIA DE REDES##
                {redesplanej_output}
                ##END ESTRATEGIA DE REDES##

                
                
                - Em formato de tabela, cronograma COMPLETO e considerando datas comemorativas, divida a estratégia de acordo com cada rede social (Instagram, Facebook, LinkedIn, WhatsApp, YouTube) no que se refere a alocação do orçamento para os anúncios: {budget} reais (alocação
                devida e detalhadamente justificada) definindo tambem
                tipos de campanhas a serem realizadas (ex: pesquisa, display, video, app, pmax) de acordo com a plataforma e porque. Quebre o investimento, tipo de campanha e estratégia
                por plataforma e periodo (dentro de {start_date} e {end_date}). Detalhe o quanto cada campanha deve gastar, por qual pedíodo, por qual plataforma, qual é o tipo de campanha,
                justificando sempre o porque de cada atributo.
                """
                redesplanej_output_crono = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_redesplanej_crono]).text
                
                # Geração dos planos específicos por rede social (somente para as selecionadas)
                redes_output_meta = None
                redes_output_link = None
                redes_output_wpp = None
                redes_output_yt = None
                
                if 'meta' in st.session_state.selected_networks:
                    prompt_redes_meta = f"""
                    Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                    - O ramo de atuação: {ramo_atuacao}.
                    - O intuito estratégico do plano: {intuito_plano}.
                    - O público-alvo: {publico_alvo}.
                    - A referência da marca: {referencia_da_marca}.
                    - notícias sobre tendência escolhida: {tendencias_out}
                    - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                    - O Key Visual : {kv_output_final}
                    - Objetivos de marca: {objetivos_de_marca}
                    
                    Otimize sua estratégia para Instagram e Facebook. Considerando suas forças e limitações como rede                        
                    **Instagram & Facebook:**
                       - 5 ideias de Reels e Stories: Explique como essas ideias capturam a atenção e engajam o público.
                       - 5 ideias de posts estáticos e carrosséis: Descreva como esses formatos ajudam a aumentar a conscientização da marca.
                       - 5 ideias de conteúdo localizado: Aproxime a marca do público local, considerando preferências culturais e comportamentais.
                    """
                    redes_output_meta = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_redes_meta]).text
                
                if 'linkedin' in st.session_state.selected_networks:
                    prompt_redes_link = f"""
                    Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                    - O ramo de atuação: {ramo_atuacao}.
                    - O intuito estratégico do plano: {intuito_plano}.
                    - O público-alvo: {publico_alvo}.
                    - A referência da marca: {referencia_da_marca}.
                    - notícias sobre tendência escolhida: {tendencias_out}
                    - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                    - O Key Visual : {kv_output_final}
                    - Objetivos de marca: {objetivos_de_marca}
                    
                    Otimize a estratégia para Linkedin. Considerando suas forças e limitações como rede                        
                    
                     **LinkedIn:**
                       - 5 ideias de conteúdos educativos e informativos: Envolva o público com informações valiosas e especializadas.
                       - 5 ideias de depoimentos de sucesso: Utilize histórias reais para gerar confiança e credibilidade.
                       - 5 ideias de eventos e comemorações: Relacione a marca com momentos importantes para o público.
                       - Defina o tom de voz para LinkedIn.
                       - 5 sugestões de CTAs: Proponha ações com objetivos claros e atraentes.
                    """
                    redes_output_link = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_redes_link]).text
                
                if 'whatsapp' in st.session_state.selected_networks:
                    prompt_redes_wpp = f"""
                    Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                    - O ramo de atuação: {ramo_atuacao}.
                    - O intuito estratégico do plano: {intuito_plano}.
                    - O público-alvo: {publico_alvo}.
                    - A referência da marca: {referencia_da_marca}.
                    - notícias sobre tendência escolhida: {tendencias_out}
                    - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                    - O Key Visual : {kv_output_final}
                    - Objetivos de marca: {objetivos_de_marca}
                    
                    Otimize a estratégia para whatsapp. Considerando suas forças e limitações
                    
                     **WhatsApp:**
                       - 5 ideias de canais: Estratégias de comunicação direta e personalizada.
                       - 5 ideias de listas de transmissão: Engajamento com grupos segmentados.
                       - 5 ideias de análises regulares: Como medir o impacto da comunicação e melhorar o engajamento.
                    """
                    redes_output_wpp = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_redes_wpp]).text
                
                if 'youtube' in st.session_state.selected_networks:
                    prompt_redes_yt = f"""
                    Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                    - O ramo de atuação: {ramo_atuacao}.
                    - O intuito estratégico do plano: {intuito_plano}.
                    - O público-alvo: {publico_alvo}.
                    - A referência da marca: {referencia_da_marca}.
                    - notícias sobre tendência escolhida: {tendencias_out}
                    - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                    - O Key Visual : {kv_output_final}
                    - Objetivos de marca: {objetivos_de_marca}
                    
                    otimize a estratégia para o Youtube. Considerando suas forças e limitações como rede social

                     **YouTube:**
                       - 5 ideias de Shorts: Estratégias curtas e impactantes.
                       - 5 ideias de conteúdos com especialistas: Produza conteúdos com autoridade no tema.
                       - 5 ideias de vídeos: Defina o tipo de vídeos que atraem e educam o público.
                       - 5 ideias de análises regulares: Como fazer revisões de performance para otimizar a estratégia.
                    
                    Além disso, inclua sugestões sobre o que evitar em cada plataforma, para não prejudicar a imagem da marca.
                    """
                    redes_output_yt = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_redes_yt]).text
                
                # Geração de criativos
                prompt_criativos = f"""
                Gere ideias de criativos para a marca {nome_cliente}, considerando:
                - Key Visual: {kv_output_final}
                - Público-alvo: {publico_alvo}
                - Objetivos de marca: {objetivos_de_marca}
                - Intuito do plano: {intuito_plano}
                
                Forneça:
                1. 5 ideias de posts para Instagram/Facebook
                2. 5 ideias de stories
                3. 5 ideias de banners/anúncios
                4. 5 ideias de conteúdo para LinkedIn
                5. 5 ideias de vídeos para YouTube
                
                Cada ideia deve incluir:
                - Título/conceito
                - Descrição detalhada do visual
                - Texto/copy sugerido
                - Chamada para ação
                """
                criativos_output = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_criativos]).text
                
                # Geração de palavras-chave
                prompt_palavras_chave = f"""
                Sugira uma lista de palavras-chave relevantes para a marca {nome_cliente}, considerando:
                - Ramo de atuação: {ramo_atuacao}
                - Público-alvo: {publico_alvo}
                - Concorrentes: {concorrentes}
                - Tendências: {tendaux}
                
                Forneça:
                1. 20 palavras-chave principais (alto volume de busca)
                2. 20 palavras-chave de cauda longa (mais específicas)
                3. 10 palavras-chave negativas (para excluir em campanhas)
                4. Análise de concorrência para cada palavra-chave principal
                """
                palavras_chave_output = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_palavras_chave]).text
                
                # Estratégia de conteúdo
                prompt_estrategia_conteudo = f"""
                Desenvolva uma estratégia de conteúdo detalhada para {nome_cliente}, incluindo:
                - Calendário editorial mensal (temas, formatos, frequência)
                - Distribuição por plataforma
                - Métricas de sucesso
                - Processo de criação e aprovação
                - Estratégia de repurposing de conteúdo
                - Análise de desempenho e otimização
                
                Considere:
                - Público-alvo: {publico_alvo}
                - Objetivos: {objetivos_de_marca}
                - Key Visual: {kv_output_final}
                - Orçamento: {budget}
                - Período: {start_date} a {end_date}
                """
                estrategia_conteudo_output = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt_estrategia_conteudo]).text
                
                # Exibe os resultados na interface
                st.header('Plano de Redes Sociais e Mídias')
                st.subheader('1. Plano de Key Visual')
                st.markdown(kv_output_final)
                st.subheader('2. Plano Geral de Redes')
                st.markdown(redesplanej_output)
                st.subheader('2.1 Cronograma de Redes')
                st.markdown(redesplanej_output_crono)
                
                if 'meta' in st.session_state.selected_networks:
                    st.subheader('2.2 Meta (Instagram e Facebook)')
                    st.markdown(redes_output_meta)
                
                if 'linkedin' in st.session_state.selected_networks:
                    st.subheader('2.3 LinkedIn')
                    st.markdown(redes_output_link)
                
                if 'whatsapp' in st.session_state.selected_networks:
                    st.subheader('2.4 WhatsApp')
                    st.markdown(redes_output_wpp)
                
                if 'youtube' in st.session_state.selected_networks:
                    st.subheader('2.5 YouTube')
                    st.markdown(redes_output_yt)
                
                st.subheader('3. Brainstorming de Criativos')
                st.markdown(criativos_output)
                
                st.subheader('4. Palavras-Chave para SEO/Ads')
                st.markdown(palavras_chave_output)
                
                st.subheader('5. Estratégia de Conteúdo')
                st.markdown(estrategia_conteudo_output)
                
                # Botão para salvar no MongoDB
                if st.button('Salvar Planejamento no Banco de Dados'):
                    save_to_mongo_midias(
                        kv_output_final,
                        redesplanej_output,
                        redesplanej_output_crono,
                        redes_output_meta,
                        redes_output_link,
                        redes_output_wpp,
                        redes_output_yt,
                        criativos_output,
                        palavras_chave_output,
                        estrategia_conteudo_output,
                        nome_cliente
                    )

