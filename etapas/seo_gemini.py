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
def seo_page():
    st.subheader('Planejamento de SEO')
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

                        

                        prompt_palavras_chave = f"""
                        Desenvolva um relatório detalhado de sugestões de palavras-chave para SEO para {nome_cliente}, levando em conta:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O público-alvo: {publico_alvo}.
                        - Os Objetivos de Marca: {objetivos_de_marca}
                        - A referência de marca: {referencia_da_marca}
                        - Os concorrentes: {concorrentes}
                        - O comportamento de busca online do público-alvo.
                        
                        No relatório, inclua:
                        
                        **Palavras-chave principais**: Liste as palavras-chave mais relevantes, com base em volume de busca e relevância para o cliente.
                       
                        Seja claro e detalhado, com uma explicação de como cada palavra-chave pode gerar resultados tangíveis para a marca.

                        """

                        seop_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_palavras_chave]).text

                        prompt_palavras_chave = f"""
                        Desenvolva um relatório detalhado de sugestões de palavras-chave para SEO para {nome_cliente}, levando em conta:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O público-alvo: {publico_alvo}.
                        - O comportamento de busca online do público-alvo.
                        - Os Objetivos de Marca: {objetivos_de_marca}
                        - A referência de marca: {referencia_da_marca}
                        - Os concorrentes: {concorrentes}
                        
                        No relatório, inclua:
                        
                         **Palavras-chave secundárias**: Inclua termos relacionados que podem gerar tráfego complementar.
                       
                        Seja claro e detalhado, com uma explicação de como cada palavra-chave pode gerar resultados tangíveis para a marca.

                        """

                        seos_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_palavras_chave]).text

                        prompt_palavras_chave = f"""
                        Desenvolva um relatório detalhado de sugestões de palavras-chave para SEO para {nome_cliente}, levando em conta:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O público-alvo: {publico_alvo}.
                        - O comportamento de busca online do público-alvo.
                        - Os Objetivos de Marca: {objetivos_de_marca}
                        - A referência de marca: {referencia_da_marca}
                        - Os concorrentes: {concorrentes}
                        
                        No relatório, inclua:
                        
                         **Tendências e variações de busca**: Analise variações de palavras-chave que podem ajudar a aumentar a visibilidade.
                        
                        Seja claro e detalhado, com uma explicação de como cada palavra-chave pode gerar resultados tangíveis para a marca.

                        """

                        teds_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_palavras_chave]).text

                        prompt_palavras_chave = f"""
                        Desenvolva um relatório detalhado de sugestões de palavras-chave para SEO para {nome_cliente}, levando em conta:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O público-alvo: {publico_alvo}.
                        - O comportamento de busca online do público-alvo.
                        - Os Objetivos de Marca: {objetivos_de_marca}
                        - A referência de marca: {referencia_da_marca}
                        - Os concorrentes: {concorrentes}
                        
                        No relatório, inclua:
                        
                         **Sugestões de conteúdo otimizado**: Ofereça sugestões de tipos de conteúdo que possam ser usados para melhorar o SEO, como artigos, blogs ou vídeos.
                        
                        Seja claro e detalhado, com uma explicação de como cada palavra-chave pode gerar resultados tangíveis para a marca.

                        """

                        sugest_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_palavras_chave]).text

                        prompt_palavras_chave = f"""
                        Desenvolva um relatório detalhado de sugestões de palavras-chave para SEO para {nome_cliente}, levando em conta:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O público-alvo: {publico_alvo}.
                        - O comportamento de busca online do público-alvo.
                        - Os Objetivos de Marca: {objetivos_de_marca}
                        - A referência de marca: {referencia_da_marca}
                        - Os concorrentes: {concorrentes}
                        
                        No relatório, inclua:
                        
                         **Estratégias de otimização on-page e off-page**: Forneça dicas de como melhorar a presença online de {nome_cliente} a partir dessas palavras-chave.
                        
                        Seja claro e detalhado, com uma explicação de como cada palavra-chave pode gerar resultados tangíveis para a marca.

                        """

                        estr_output = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[prompt_palavras_chave]).text
                        

                        # Exibe os resultados na interface
                        st.header('Plano de SEO')
                        st.subheader('1. Palavras-chave principais')
                        st.markdown(seop_output)
                        st.subheader('2. Palavras-chave secundárias')
                        st.markdown(seos_output)
                        st.subheader('3. Tendências e variações de buscas')
                        st.markdown(teds_output)
                        st.subheader('4. Sugestões de conteúdo otimizado')
                        st.markdown(sugest_output) 
                        st.subheader('5. *Estratégias de otimização on-page e off-page')  
                        st.markdown(estr_output)   
                       
                        



                       


                       