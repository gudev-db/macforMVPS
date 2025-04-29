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
def save_to_mongo_midias(kv_output,redesplanej_output,redesplanej_output_meta,redesplanej_output_link,redesplanej_output_wpp,redesplanej_output_yt,criativos_output,palavras_chave_output,estrategia_conteudo_output, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano de Mídias' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de Mídias',
        "KV": kv_output,
        "Plano_redes_macro":redesplanej_output,
        "Plano_Redes_Meta": redesplanej_output_meta,
        "Plano_Redes_Link": redesplanej_output_link,
        "Plano_Redes_Wpp": redesplanej_output_wpp,
        "Plano_Redes_Yt": redesplanej_output_yt,
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

    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True, help="""
    **Você possui algum material de referência sobre o mercado do cliente?**
    
    Envie arquivos PDF que possam auxiliar na análise do mercado e na criação da estratégia.
    """)

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

                        

                        model_id = "gemini-2.0-flash"

                        google_search_tool = Tool(
                            google_search = GoogleSearch()
                        )
                        
                        # Agente de pesquisa de concorrentes
                        concorrentes_out = client.models.generate_content(
                            model=model_id,
                            contents="Faça uma pesquisa sobre a empresa {concorrentes}",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )

                        tendencias_out = client.models.generate_content(
                            model=model_id,
                            contents="Faça uma pesquisa sobre a empresa {tendaux}",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )

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

                        kv_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_kv]).text

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

                        redesplanej_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_redesplanej]).text

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

                        


                        redesplanej_output_crono = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_redesplanej_crono]).text

                        

                        prompt_redes_meta = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        Otimize sua estratégia para Instagram e Facebook. Considerando suas forças e limitações como rede                        
                        **Instagram & Facebook:**
                           - 5 ideias de Reels e Stories: Explique como essas ideias capturam a atenção e engajam o público.
                           - 5 ideias de posts estáticos e carrosséis: Descreva como esses formatos ajudam a aumentar a conscientização da marca.
                           - 5 ideias de conteúdo localizado: Aproxime a marca do público local, considerando preferências culturais e comportamentais.
                        
                        
                        """

                        prompt_redes_link = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        Otimize a estratégia para Linkedin. Considerando suas forças e limitações como rede                        
                        
                         **LinkedIn:**
                           - 5 ideias de conteúdos educativos e informativos: Envolva o público com informações valiosas e especializadas.
                           - 5 ideias de depoimentos de sucesso: Utilize histórias reais para gerar confiança e credibilidade.
                           - 5 ideias de eventos e comemorações: Relacione a marca com momentos importantes para o público.
                           - Defina o tom de voz para LinkedIn.
                           - 5 sugestões de CTAs: Proponha ações com objetivos claros e atraentes.
                        
                        
                        """

                        prompt_redes_wpp = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        Otimize a estratégia para whatsapp. Considerando suas forças e limitações
                        
                         **WhatsApp:**
                           - 5 ideias de canais: Estratégias de comunicação direta e personalizada.
                           - 5 ideias de listas de transmissão: Engajamento com grupos segmentados.
                           - 5 ideias de análises regulares: Como medir o impacto da comunicação e melhorar o engajamento.
                        
                        
                        """

                        prompt_redes_yt = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        otimize a estratégia para o Youtube. Considerando suas forças e limitações como rede social

                         **YouTube:**
                           - 5 ideias de Shorts: Estratégias curtas e impactantes.
                           - 5 ideias de conteúdos com especialistas: Produza conteúdos com autoridade no tema.
                           - 5 ideias de vídeos: Defina o tipo de vídeos que atraem e educam o público.
                           - 5 ideias de análises regulares: Como fazer revisões de performance para otimizar a estratégia.
                        
                        Além disso, inclua sugestões sobre o que evitar em cada plataforma, para não prejudicar a imagem da marca.

                        """
                        

                        redes_output_meta = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_redes_meta]).text

                        redes_output_link = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_redes_link]).text

                        redes_output_wpp = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_redes_wpp]).text

                        redes_output_yt = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_redes_yt]).text

                        


                        


                        

                        #Etapa estratégia de conteúdo - Pilar institucional

                        prompt_estrategia_conteudo_inst = f"""
                       Crie uma estratégia de conteúdo detalhada para {nome_cliente}, considerando:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        Crie o pilar institucional do conteúdo

                         **Institucional**:
                           - Objetivo: Posicionar a marca e gerar credibilidade.
                           - Conteúdo: Defina o tipo de conteúdo (ex: história da empresa, missão, visão).
                           - Canal: Sugira as plataformas onde esse conteúdo deve ser veiculado.
                        


                        """

                        estrategia_conteudo_output_inst1 = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_inst]).text

                        #Refinação da etapa institucional
                        prompt_estrategia_conteudo_inst_guias = f"""
                        Você é um especialista no pilar de institucional em estratégia de conteúdo


                       Dada a seguinte estratégia de conteúdo de Produtos e Serviços
                       ## {estrategia_conteudo_output_inst1} ##

                       Faça uma avaliação sobre o que a torna genérica demais e como ela pode melhorar.

                        """

                        estrategia_conteudo_output_inst_guias = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_inst_guias]).text

                        estrategia_conteudo_output_inst = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[f'''Dado os guias de melhorias
                                  ##{estrategia_conteudo_output_inst_guias}##
                                  Reescreva o pilar institucional de estratégia de conteúdo a seguir.

                                  ##{estrategia_conteudo_output_inst1}##

                                  Apenas escreva uma nova estratégia de conteudo - pilar institucional. Não aponte o que você mudou
                                   ''']).text



                        #Etapa pilar inspiração
                        prompt_estrategia_conteudo_insp = f"""
                       Crie uma estratégia de conteúdo detalhada para {nome_cliente}, considerando:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        Crie o pilar Inspiração da estratégia de conteúdo                        

                        
                        **Inspiração**:
                           - Objetivo: Criar uma conexão emocional com o público.
                           - Conteúdo: Defina histórias e temas inspiradores.
                           - Canal: Sugira plataformas adequadas para esse tipo de conteúdo.

                        """

                        estrategia_conteudo_output_insp1 = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_insp]).text

                        #Refinação da etapa de inspiração
                        prompt_estrategia_conteudo_insp_guias = f"""
                        Você é um especialista no pilar de educação em estratégia de conteúdo


                       Dada a seguinte estratégia de conteúdo de Produtos e Serviços
                       ## {estrategia_conteudo_output_insp1} ##

                       Faça uma avaliação sobre o que a torna genérica demais e como ela pode melhorar.

                        """

                        estrategia_conteudo_output_insp_guias = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_insp_guias]).text

                        estrategia_conteudo_output_insp = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[f'''Dado os guias de melhorias
                                  ##{estrategia_conteudo_output_insp_guias}##
                                  Reescreva o pilar de inspiração de estratégia de conteúdo a seguir.

                                  ##{estrategia_conteudo_output_insp1}##

                                  Apenas escreva uma nova estratégia de conteudo - pilar inspiração. Não aponte o que você mudou
                                   ''']).text

                        #Etapa de estratégia de geração de conteúdo - pilar educação
                        prompt_estrategia_conteudo_edu = f"""
                       Crie uma estratégia de conteúdo detalhada para {nome_cliente}, considerando:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        
                        Crie o pilar Educação do conteúdo                        

                        
                        **Educação**:
                           - Objetivo: Educar o público sobre produtos, serviços ou tendências do mercado.
                           - Conteúdo: Ofereça temas educativos relevantes para o público-alvo.
                           - Canal: Defina as plataformas mais eficazes para esse tipo de conteúdo.
                        


                        """

                        estrategia_conteudo_output_edu1 = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_edu]).text


                        #Refinamento de estratégia de educação

                        prompt_estrategia_conteudo_edu_guias = f"""
                        Você é um especialista no pilar de educação em estratégia de conteúdo


                       Dada a seguinte estratégia de conteúdo de Produtos e Serviços
                       ## {estrategia_conteudo_output_edu1} ##

                       Faça uma avaliação sobre o que a torna genérica demais e como ela pode melhorar.

                        """

                        estrategia_conteudo_output_edu_guias = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_edu_guias]).text

                        estrategia_conteudo_output_edu = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[f'''Dado os guias de melhorias
                                  ##{estrategia_conteudo_output_edu_guias}##
                                  Reescreva o pilar de educação do pilar de estratégia de conteúdo a seguir.

                                  ##{estrategia_conteudo_output_edu1}##

                                  Apenas escreva uma nova estratégia de conteudo - pilar educação. Não aponte o que você mudou
                                   ''']).text

                        #Etapa de estratégia de produtos e serviços
                        prompt_estrategia_conteudo_prod1 = f"""
                       Crie uma estratégia de conteúdo detalhada para {nome_cliente}, considerando:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        

                        Crie o pilar produtos/serviços da estratégia de conteúdo
                        **Produtos/Serviços**:
                           - Objetivo: Gerar leads e promover vendas.
                           - Conteúdo: Detalhe como destacar os produtos ou serviços de maneira atrativa.
                           - Canal: Quais canais serão mais eficazes para conversões?
                        

                        """

                        

                        estrategia_conteudo_output_prod1 = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_prod1]).text

                        # Refinamento de Estratégia de Produtos e Serviços
                        prompt_estrategia_conteudo_prod_guias = f"""
                        Você é um especialista no pilar de produtos e serviços em estratégia de conteúdo


                       Dada a seguinte estratégia de conteúdo de Produtos e Serviços
                       ## {estrategia_conteudo_output_prod1} ##

                       Faça uma avaliação sobre o que a torna genérica demais e como ela pode melhorar.

                        """

                        estrategia_conteudo_output_prod_guias = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_prod_guias]).text

                        estrategia_conteudo_output_prod = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[f'''Dado os guias de melhorias
                                  ##{estrategia_conteudo_output_prod_guias}##
                                  Reescreva o pilar de relacionamento do pilar de estratégia de conteúdo a seguir.

                                  ##{estrategia_conteudo_output_prod1}##

                                  Apenas escreva uma nova estratégia de conteudo - pilar relacionamento. Não aponte o que você mudou
                                   ''']).text


                        # Estratégia de Relacionamento
                        prompt_estrategia_conteudo_rel1 = f"""
                       Crie uma estratégia de conteúdo detalhada para {nome_cliente}, considerando:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        - notícias sobre tendência escolhida: {tendencias_out}
                        - notícias sobre concorrente que precisamos superar: {concorrentes_out}
                        

                        Crie o pilar de relacionamento da estratégia de conteúdo
                         **Relacionamento**:
                           - Objetivo: Criar e manter um relacionamento de longo prazo com o público.
                           - Conteúdo: Defina conteúdo interativo ou de engajamento.
                           - Canal: Sugira canais onde o engajamento direto com o público seja mais efetivo.
                        
                        Inclua também sugestões de formatos, como blogs, vídeos, webinars, posts interativos, etc.

                        """

                        estrategia_conteudo_output_rel1 = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_rel1]).text

                        # Refinamento de Estratégia de Relacionamento
                        prompt_estrategia_conteudo_rel_guias = f"""
                        Você é um especialista no pilar de relacionamento em estratégia de conteúdo


                       Dada a seguinte estratégia de conteúdo de Relacionamento
                       ## {estrategia_conteudo_output_rel1} ##

                       Faça uma avaliação sobre o que a torna genérica demais e como ela pode melhorar.

                        """

                        estrategia_conteudo_output_rel_guias = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_estrategia_conteudo_rel_guias]).text

                        estrategia_conteudo_output_rel = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[f'''Dado os guias de melhorias
                                  ##{estrategia_conteudo_output_rel_guias}##
                                  Reescreva o pilar de relacionamento do pilar de estratégia de conteúdo a seguir.

                                  ##{estrategia_conteudo_output_rel1}##

                                  Apenas escreva uma nova estratégia de conteudo - pilar relacionamento. Não aponte o que você mudou
                                   ''']).text

                        

                        # Exibe os resultados na interface
                        st.header('Plano de Redes Sociais e Mídias')
                        st.subheader('1. Plano de Key Visual')
                        st.markdown(kv_output_final)
                        st.subheader('2. Plano Geral de Redes')
                        st.markdown(redesplanej_output)
                        st.subheader('2.1 Cronograma de Redes')
                        st.markdown(redesplanej_output_crono)
                        st.subheader('2.2 Meta (Instagram e Facebook)')
                        st.markdown(redes_output_meta) 
                        st.subheader('2.3 Linkedin')  
                        st.markdown(redes_output_link)   
                        st.subheader('2.4 Whatsapp')
                        st.markdown(redes_output_wpp)   
                        st.subheader('2.5 Youtube')
                        st.markdown(redes_output_yt)                   
                        st.subheader('3. Estratégia de Conteúdo')
                        st.subheader('3.1 Estratégia de Conteúdo - Institucional')
                        st.markdown(estrategia_conteudo_output_inst)
                        st.subheader('3.2 Estratégia de Conteúdo - Inspiração')
                        st.markdown(estrategia_conteudo_output_insp)
                        st.subheader('3.3 Estratégia de Conteúdo - Educação')
                        st.markdown(estrategia_conteudo_output_edu)
                        st.subheader('3.4 Estratégia de Conteúdo - Produtos/Serviços')
                        st.markdown(estrategia_conteudo_output_prod)
                        st.subheader('3.5 Estratégia de Conteúdo - Relação com o cliente')
                        st.markdown(estrategia_conteudo_output_rel)
                        
                        



                       


                       