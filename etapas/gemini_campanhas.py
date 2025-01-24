import streamlit as st
import google.generativeai as genai
import uuid
import os
from pymongo import MongoClient

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
def save_to_mongo_ads(ads_output, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano de Mídias' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de Anúncios',
        "ads": ads_output,
       
    }

    # Insere o documento no MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def planej_campanhas():
    st.subheader('Brainstorming de Anúncios')
    st.text('Aqui geramos brainstorming para campanhas.')

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
    intuito_plano = st.text_input('Intuito da campanha:', key="intuito_plano", placeholder="Ex: Gerar mais atendimentos, captar leads, etc")
    publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda")
    
    tipo_anuncio = [
        'Search',
        'Display',
        'Shopping',
        'App',
        'Vídeo'
    ]

    plats = [
      'Meta Ads',
      'Google Ads',
      'Linkedin Ads'
    ]

    # Use chaves únicas para os elementos
    tipo = st.selectbox('Selecione o tipo de campanha', tipo_anuncio, key="tipo_anuncio")
    platform = st.selectbox('Selecione a plataforma de anúncios', plats, key="plataforma_anuncios")
    referencia_da_marca = st.text_area('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', 
                                       key="referencias_marca", 
                                       placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.", 
                                       height=200)
    
    budget = st.text_input('Orçamento para o anúncio:', key="budget", placeholder="Valor em reais")
    start_date = st.date_input("Data de Início:", key="start_date")
    end_date = st.date_input("Data de Fim:", key="end_date")

    if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
        st.subheader("Anúncio gerado")
        for tarefa in st.session_state.resultados_tarefas:
            st.markdown(f"**Arquivo**: {tarefa['output_file']}")
            st.markdown(tarefa["output"])
        
        if st.button("Gerar Novo Anúncio"):
            limpar_estado()
            st.experimental_rerun()
    else:
        if st.button('Iniciar Planejamento'):
            if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
                st.write("Por favor, preencha todas as informações do cliente.")
            else:
                with st.spinner('Brainstorming...'):
                    prompt_ads = f"""
                    Desenvolva um anúncio {nome_cliente}, levando em consideração e otimizando a criação da campanha para os seguintes pontos:
                    - O ramo de atuação da empresa: {ramo_atuacao}.
                    - O intuito estratégico do plano de marketing: {intuito_plano}.
                    - O público-alvo: {publico_alvo}.
                    - A referência da marca: {referencia_da_marca}.
                    - Tipo de anúncio: {tipo}
                    - Orçamento: {budget} reais
                    - Data de início: {start_date}
                    - Data fim: {end_date}
                    - Plataforma: {platform}
                  
                        
                        
                        
                    - Para cada um dos anúncios, desenvolva, sendo original, com solução pulo do gato, sem ser genérico (seja preciso. Diga exatamente o que deve ser feito):

                        **Motivação**: Reduja um texto extenso justificando sua linha de pensamento para a concepção do anúncio, o porque ele será eficaz e como você está
                        otimizando as suas escolhas para o caso específico do cliente. Use esse espaço como uma oportunidade de ensinar conceitos de marketing digital, dado que
                        você é um especialista com conhecimento extremamente aprofundado. Você é comunicativo, criativo, único, perspicaz. Você é original. Você é um especialista.
                        
                        1. **Imagem ou vídeo:** Defina a imagem que encapsula os valores e o propósito da marca. Justifique a escolha com base em elementos visuais comumente utilizados no ramo de atuação {ramo_atuacao} e como isso se conecta ao público-alvo {publico_alvo}. Explique por que essa imagem foi escolhida, incluindo referências culturais, psicológicas e comportamentais.
                        Imagine que você irá contratar um designer para desenvolver essa imagem. Detalhe-a em como ela deve ser feita em um nível extremamente detalhados. Serão guidelines extremamente
                        delhadados, precisos e justificados que o designer irá receber para desenvolver a imagem conceito. Não seja vago. Dia exatamente quais são os elementos visuais em extremo
                        detalhe e justificados.
                        
                        2. **Tipografia:** Escolha uma fonte tipográfica que complemente a imagem. Detalhe a escolha e a forma como a tipografia reflete a identidade da marca, levando em conta a legibilidade e a conexão emocional com o público. Explique as escolhas de estilo, espessura e espaçamento.
                        
                        3. **Cores:** Selecione uma paleta de cores específica para o Key Visual. Justifique as escolhas com base em psicologia das cores e tendências do mercado no ramo de atuação {ramo_atuacao}. Detalhe como essas cores evocam emoções e criam uma identidade visual forte e coesa.
                        
                        4. **Elementos Gráficos:** Defina quais elementos gráficos, como formas, ícones ou texturas, são fundamentais para compor o Key Visual. Justifique a escolha desses elementos em relação à consistência da identidade visual e à relevância para o público-alvo.
                        5. **Descrição:** Texto associado ao anúncio.
                        6. **Cronograma:** Cronograma orçamentário de anúncios.

                        """
                    ads_output = modelo_linguagem.generate_content(prompt_ads).text

                     


                        # Exibe os resultados na interface
                    st.header('Brainstorming de Anúncios')
                    st.markdown(ads_output)
                  

                        # Salva o planejamento no MongoDB
                    save_to_mongo_ads(ads_output, nome_cliente)
