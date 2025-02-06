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


guias_mote = '''

Guia completo para criar um mote de campanha eficaz

Você já se perguntou como algumas campanhas publicitárias conseguem capturar a atenção do público e se tornar um sucesso instantâneo? A resposta está, muitas vezes, no poder de um mote de campanha eficaz.
Um mote de campanha é uma frase ou slogan curto e memorável que representa a essência da mensagem que uma empresa ou organização deseja transmitir ao público. É a oportunidade de criar uma conexão emocional com os consumidores e despertar interesse em relação ao produto ou serviço oferecido.
Para criar um mote de campanha eficaz, é importante levar em consideração alguns elementos-chave:
Clareza: O mote deve transmitir a mensagem de forma direta e compreensível. Evite termos complexos ou ambíguos que possam confundir o público-alvo.
Emoção: Um bom mote deve despertar emoções no público, seja alegria, curiosidade, surpresa ou qualquer outro sentimento que crie uma conexão emocional com a marca.
Originalidade: É importante criar um mote que seja único e diferenciado dos concorrentes. Isso ajudará a marca a se destacar e a ser lembrada pelos consumidores.
Relevância: O mote deve estar alinhado com os valores e propósitos da marca, além de ser relevante para o público-alvo. Conhecer bem o mercado e o perfil dos consumidores é essencial para criar um mote que ressoe com eles.
Memorabilidade: Um bom mote deve ser fácil de lembrar. Pense em frases curtas, simples e impactantes que fiquem na mente das pessoas por um longo tempo.
É importante ressaltar que a criação de um mote de campanha eficaz requer habilidades de marketing e comunicação. Embora este guia forneça dicas valiosas, ele não substitui a assessoria jurídica especializada. É recomendável que as empresas consultem profissionais qualificados para garantir que o mote esteja em conformidade com as leis e regulamentações vigentes.
Ao criar um mote de campanha, é fundamental realizar pesquisas de mercado, analisar a concorrência e testar diferentes opções com o público-alvo. Aperfeiçoar o mote com base no feedback recebido é uma prática recomendada para garantir sua eficácia.
Em resumo, um mote de campanha eficaz é uma poderosa ferramenta de comunicação que pode impulsionar o sucesso de uma campanha publicitária. Seguir os princípios de clareza, emoção, originalidade, relevância e memorabilidade ajudará a criar um mote que se destaque e conecte com o público-alvo. Lembre-se sempre de buscar a orientação adequada para garantir conformidade legal.

'''

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

    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")
    site_cliente = st.text_input('Site do Cliente:', help="Digite o site do cliente.")

    ramo_atuacao = st.text_input('Ramo de atuação do cliente:', help="Digite o site do cliente.")
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
    platform = st.selectbox('Selecione a plataforma de anúncios', plats, key="plataforma_anuncios")
    referencia_da_marca = st.text_area('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', 
                                       key="referencias_marca", 
                                       placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.", 
                                       height=200)
    
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
            if 1 ==1:
                with st.spinner('Brainstorming...'):
                    prompt_ads = f"""
                    Desenvolva um anúncio {nome_cliente}, levando em consideração e otimizando a criação da campanha para os seguintes pontos:
                    - O ramo de atuação da empresa: {ramo_atuacao}.
                    - O intuito estratégico do plano de marketing: {intuito_plano}.
                    - O público-alvo: {publico_alvo}.
                    - A referência da marca: {referencia_da_marca}.
                    - Tipo de anúncio: dado os tipos de anúncio em {tipo_anuncio}, escolha o(s) que faz(em) mais sentido para que o cliente atinja seus objetivos.
                    - Data de início: {start_date}
                    - Data fim: {end_date}
                    - Plataforma: {platform}
                  
                        
                        
                        
                    - Para cada um dos anúncios, desenvolva, sendo original, com solução pulo do gato, sem ser genérico (seja preciso. Diga exatamente o que deve ser feito):

                        **Motivação**: Reduja um texto extenso justificando sua linha de pensamento para a concepção do anúncio, o porque ele será eficaz e como você está
                        otimizando as suas escolhas para o caso específico do cliente. Use esse espaço como uma oportunidade de ensinar conceitos de marketing digital, dado que
                        você é um especialista com conhecimento extremamente aprofundado. Você é comunicativo, criativo, único, perspicaz. Você é original. Você é um especialista.
                        

                        1. **Mote de Campanha:** dado o guia para se criar um bom mote de campanha: {guias_mote}. Crie 5 motes de campanha

                        2. **Imagem ou vídeo:** Defina a imagem que encapsula os valores e o propósito da marca. Justifique a escolha com base em elementos visuais comumente utilizados no ramo de atuação {ramo_atuacao} e como isso se conecta ao público-alvo {publico_alvo}. Explique por que essa imagem foi escolhida, incluindo referências culturais, psicológicas e comportamentais.
                        Imagine que você irá contratar um designer para desenvolver essa imagem. Detalhe-a em como ela deve ser feita em um nível extremamente detalhados. Serão guidelines extremamente
                        delhadados, precisos e justificados que o designer irá receber para desenvolver a imagem conceito. Não seja vago. Dia exatamente quais são os elementos visuais em extremo
                        detalhe e justificados.
                        
                        3. **Tipografia:** Escolha uma fonte tipográfica que complemente a imagem. Detalhe a escolha e a forma como a tipografia reflete a identidade da marca, levando em conta a legibilidade e a conexão emocional com o público. Explique as escolhas de estilo, espessura e espaçamento.
                        
                        4. **Cores:** Selecione uma paleta de cores específica para o Key Visual. Justifique as escolhas com base em psicologia das cores e tendências do mercado no ramo de atuação {ramo_atuacao}. Detalhe como essas cores evocam emoções e criam uma identidade visual forte e coesa.
                        
                        5. **Elementos Gráficos:** Defina quais elementos gráficos, como formas, ícones ou texturas, são fundamentais para compor o Key Visual. Justifique a escolha desses elementos em relação à consistência da identidade visual e à relevância para o público-alvo.
                        6. **Descrição:** Texto associado ao anúncio.
                        7. **Cronograma:** Cronograma de anúncios em formato de fluxograma. Seja estratégico com o fluxo de uma forma que otimize os resultados. Você é um especialista bem analítico em marketing digital.

                        """
                    ads_output = modelo_linguagem.generate_content(prompt_ads).text

                     


                        # Exibe os resultados na interface
                    st.header('Brainstorming de Anúncios')
                    st.markdown(ads_output)
                  

                        # Salva o planejamento no MongoDB
                    save_to_mongo_ads(ads_output, nome_cliente)
