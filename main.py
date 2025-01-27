import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from etapas.mkt import planej_mkt_page
from tools.retrieve import visualizar_planejamentos  # Importando a função visualizar_planejamentos
from tavily import TavilyClient
from etapas.gemini_midias import planej_midias_page
from etapas.gemini_crm import planej_crm_page
from etapas.gemini_campanhas import planej_campanhas
import google.generativeai as genai
from contato.temaEmail import gen_temas_emails
from etapas.image_gen import gen_img

st.set_page_config(
    layout="wide",
    page_title="Macfor AutoDoc",
    page_icon="static/page-icon.png"
)

# Configuração das chaves de API
gemini_api_key = os.getenv("GEM_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")

# Inicializa o cliente Tavily
client = TavilyClient(api_key=t_api_key1)

# Inicializa o modelo LLM com OpenAI
modelo_linguagem = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    frequency_penalty=0.5
)

# Configura o modelo de AI Gemini
genai.configure(api_key=gemini_api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")

# Função de login
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.subheader("Página de Login")

    nome_usuario = st.text_input("Nome de Usuário", type="default")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if nome_usuario == "admin" and senha == "senha123":
            st.session_state.logged_in = True
            st.success("Login bem-sucedido!")
            return True
        else:
            st.error("Usuário ou senha incorretos.")
            return False
    return False


# Função para visualizar os planejamentos (com correções)
def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")
    db = client['arquivos_planejamento']  # Substitua pelo nome do seu banco de dados
    collection = db['auto_doc']

    # Obter todos os IDs dos documentos (presumindo que 'id_planejamento' seja o identificador único)
    planejamentos = collection.find({}, {"_id": 1, "id_planejamento": 1})

    # Se não houver documentos encontrados
    if collection.count_documents({}) == 0:
        st.write("Não há planejamentos registrados.")
        return

    # Lista de 'id_planejamento' para o selectbox
    id_planejamentos = [planejamento['id_planejamento'] for planejamento in planejamentos]

    # Usar session_state para manter a seleção persistente
    if 'selected_id' not in st.session_state:
        st.session_state.selected_id = id_planejamentos[0]  # Inicializa com o primeiro ID

    # Criar um selectbox para o usuário escolher um id_planejamento específico
    selected_id = st.selectbox("Selecione um planejamento:", id_planejamentos, key="id_planejamento")

    # Atualizar a seleção armazenada na session_state
    st.session_state.selected_id = selected_id

    # Buscar o planejamento completo com base no id_planejamento selecionado
    selected_planejamento = collection.find_one({"id_planejamento": st.session_state.selected_id})

    if selected_planejamento:
        # Exibindo o nome do cliente e o tipo de plano
        st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano')}")
        st.subheader(f"Cliente: {selected_planejamento.get('nome_cliente')}")

        # Exibindo as seções do planejamento com subheaders e os dados respectivos
        st.header('1. Etapa de Pesquisa de Mercado')
        st.subheader('1.1 Análise SWOT')
        st.markdown(f"**SWOT:** {selected_planejamento.get('SWOT')}")

        st.subheader('1.2 Análise PEST')
        st.markdown(f"**P:** {selected_planejamento.get('P')}")
        st.markdown(f"**E:** {selected_planejamento.get('E')}")
        st.markdown(f"**S:** {selected_planejamento.get('S')}")
        st.markdown(f"**T:** {selected_planejamento.get('T')}")

        st.subheader('1.3 Tendências de Mercado')
        st.markdown(f"**Tendências:** {selected_planejamento.get('Tendencias')}")

        st.header('2. Etapa Estratégica')
        st.subheader('2.1 Golden Circle')
        st.markdown(f"**GC:** {selected_planejamento.get('GC')}")

        st.subheader('2.2 Posicionamento de Marca')
        st.markdown(f"**Posicionamento de Marca:** {selected_planejamento.get('Posicionamento_Marca')}")

        st.subheader('2.3 Brand Persona')
        st.markdown(f"**Brand Persona:** {selected_planejamento.get('Brand_Persona')}")

        st.subheader('2.4 Buyer Persona')
        st.markdown(f"**Buyer Persona:** {selected_planejamento.get('Buyer_Persona')}")

        st.subheader('2.5 Tom de Voz')
        st.markdown(f"**Tom de Voz:** {selected_planejamento.get('Tom_Voz')}")

        st.header('3. Etapa de Planejamento de Mídias e Redes Sociais')
        st.subheader('3.1 Visual')
        st.markdown(f"**Estruturação do KV:** {selected_planejamento.get('KV')}")
        st.markdown(f"**Plano de Redes Sociais:** {selected_planejamento.get('Plano_Redes')}")

        st.subheader('3.2 Plano para Criativos')
        st.markdown(f"**Criativos:** {selected_planejamento.get('Plano_Criativos')}")

        st.subheader('3.3 Plano de SEO')
        st.markdown(f"**Plano de Palavras Chave:** {selected_planejamento.get('Plano_Palavras_Chave')}")

        st.subheader('3.4 Plano de CRM')
        st.markdown(f"**Estratégia Geral de CRM:** {selected_planejamento.get('Plano_Estrategia_CRM')}")
        st.markdown(f"**Fluxo Geral de CRM:** {selected_planejamento.get('Plano_Fluxo_CRM')}")
        st.markdown(f"**Gestão de Contato com o Cliente - Email:** {selected_planejamento.get('Plano_Contato_Email')}")
        st.markdown(f"**Gestão de Contato com o Cliente - SMS/WhatsApp:** {selected_planejamento.get('Plano_Contato_SMS_WhatsApp')}")
        st.markdown(f"**Gestão de Contato com o Cliente - NPS:** {selected_planejamento.get('Plano_Contato_NPS')}")
        st.markdown(f"**Softwares Recomendados:** {selected_planejamento.get('Recomend_Software')}")
    else:
        st.write("Planejamento não encontrado.")


# Verifique se o login foi feito antes de exibir o conteúdo
if login():
    st.image('static/macLogo.png', width=300)
    st.text(
        "Empoderada por IA, a Macfor conta com um sistema gerador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e gere documentos automáticos para otimizar o tempo de sua equipe. "
        "Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!"
    )

    # Sidebar para escolher entre "Plano Estratégico" ou "Brainstorming"
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        ["Plano Estratégico", "Brainstorming"],
        index=0  # Predefinir como 'Plano Estratégico' ativo
    )

    # Opções para "Plano Estratégico"
    if selecao_sidebar == "Plano Estratégico":
        st.sidebar.subheader("Planos Estratégicos")
        plano_estrategico = st.sidebar.selectbox(
            "Escolha o tipo de plano:",
            [
                "Selecione uma opção",
                "Plano Estratégico e de Pesquisa",
                "Plano Estratégico de Redes e Mídias",
                "Plano de CRM"
            ]
        )

        if plano_estrategico != "Selecione uma opção":
            if plano_estrategico == "Plano Estratégico e de Pesquisa":
                planej_mkt_page()
            elif plano_estrategico == "Plano Estratégico de Redes e Mídias":
                planej_midias_page()
            elif plano_estrategico == "Plano de CRM":
                planej_crm_page()

    # Opções para "Brainstorming"
    elif selecao_sidebar == "Brainstorming":
        st.sidebar.subheader("Brainstorming")
        brainstorming_option = st.sidebar.selectbox(
            "Escolha o tipo de brainstorming:",
            [
                "Selecione uma opção",
                "Brainstorming Conteúdo de Nutrição de Leads",
                "Brainstorming de Anúncios",
                "Brainstorming de Imagem"
            ]
        )

        if brainstorming_option != "Selecione uma opção":
            if brainstorming_option == "Brainstorming Conteúdo de Nutrição de Leads":
                gen_temas_emails()
            elif brainstorming_option == "Brainstorming de Anúncios":
                planej_campanhas()
            elif brainstorming_option == "Brainstorming de Imagem":
                gen_img()

    # Visualizar Documentos Gerados
    st.sidebar.subheader("Documentos Gerados")

    # Criar um formulário para encapsular o selectbox e a chamada da função
    with st.sidebar.form("visualizar_form"):
        # Chama a função para exibir os planejamentos ao clicar no botão
        if st.form_submit_button("Visualizar Documentos Gerados"):
            visualizar_planejamentos()
