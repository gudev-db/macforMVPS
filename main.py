__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from etapas.gemini_mkt import planej_mkt_page
from tools.retrieve import visualizar_planejamentos  # Importando a função visualizar_planejamentos
from tavily import TavilyClient
from etapas.gemini_midias import planej_midias_page
from etapas.gemini_crm import planej_crm_page
from etapas.gemini_campanhas import planej_campanhas
import google.generativeai as genai
from contato.temaEmail import gen_temas_emails
from etapas.image_gen import gen_img
from etapas.lead_osint import osint_report
from contato.Email import gen_emails
from contato.noticias import pesquisa

st.set_page_config(
    layout="wide",
    page_title="Macfor AutoDoc",
    page_icon="static/page-icon.png"
)

st.image('static/macLogo.png', width=300)
st.text(
        "Empoderada por IA, a Macfor conta com um sistema gerador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e gere documentos automáticos para otimizar o tempo de sua equipe. "
        "Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!"
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

# Função para exibir as subseções com explicação
def exibir_subsecoes(selecao_sidebar):
    if selecao_sidebar == "Macro - Planejamentos Estratégicos":
        st.header("Planejamentos Estratégicos")
        st.subheader("Escolha uma subseção para iniciar:")
        
        subsecoes = {
            "Planejamento de Pesquisa e Estratégia": "Esta seção ajuda a criar e organizar estratégias de pesquisa para entender o mercado e os concorrentes.",
            "Planejamento de Redes e Mídias": "Aqui você pode planejar ações e campanhas nas redes sociais, escolhendo as melhores mídias para o seu negócio.",
            "Planejamento de CRM": "Esta seção é voltada para o planejamento de ações de CRM (Gestão de Relacionamento com Clientes), visando melhorar o relacionamento com os clientes.",
            "Investigação de Leads": "Use essa opção para investigar possíveis leads e gerar informações detalhadas sobre eles."
        }

        for subsecao, descricao in subsecoes.items():
            if st.button(subsecao):
                st.markdown(f"### {subsecao}")
                st.write(descricao)
                if subsecao == "Planejamento de Pesquisa e Estratégia":
                    planej_mkt_page()
                elif subsecao == "Planejamento de Redes e Mídias":
                    planej_midias_page()
                elif subsecao == "Planejamento de CRM":
                    planej_crm_page()
                elif subsecao == "Investigação de Leads":
                    osint_report()

    elif selecao_sidebar == "Micro - Conteúdo Específico":
        st.header("Conteúdo Específico")
        st.subheader("Escolha uma subseção para iniciar:")
        
        subsecoes = {
            "Brainstorming de Temas de Emails": "Aqui você pode gerar ideias criativas para temas de emails, otimizando sua campanha de email marketing.",
            "Brainstorming de Anúncios": "Use essa opção para gerar ideias de anúncios para suas campanhas de marketing.",
            "Brainstorming de Imagem": "Esta opção permite que você crie ideias para imagens que podem ser usadas em anúncios ou publicações.",
            "Brainstorming de Emails": "Aqui você pode gerar ideias completas de emails, incluindo conteúdo e estrutura para campanhas.",
            "Pesquisa de Tendências": "Pesquise as tendências mais atuais para sua área, ajudando a manter suas campanhas de marketing atualizadas."
        }

        for subsecao, descricao in subsecoes.items():
            if st.button(subsecao):
                st.markdown(f"### {subsecao}")
                st.write(descricao)
                if subsecao == "Brainstorming de Temas de Emails":
                    gen_temas_emails()
                elif subsecao == "Brainstorming de Emails":
                    gen_emails()
                elif subsecao == "Brainstorming de Anúncios":
                    planej_campanhas()
                elif subsecao == "Brainstorming de Imagem":
                    gen_img()
                elif subsecao == "Pesquisa de Tendências":
                    pesquisa()

if login():
    # Sidebar para escolher entre "Plano Estratégico" ou "Brainstorming"
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        ["Macro - Planejamentos Estratégicos", "Micro - Conteúdo Específico", "Documentos Salvos"],
        index=0  # Predefinir como 'Plano Estratégico' ativo
    )

    # Exibir as subseções com explicações dependendo da seleção no sidebar
    exibir_subsecoes(selecao_sidebar)

    # Seção para "Documentos Salvos"
    elif selecao_sidebar == "Documentos Salvos":
        st.sidebar.subheader("Visualizar Documentos Salvos")

        # Obter a lista de documentos salvos
        documentos_salvos = visualizar_planejamentos()  # Deve retornar [{"id": 1, "conteudo": "Texto 1"}, ...]

        if documentos_salvos:
            # Criar um selectbox para selecionar o documento pelo ID
            doc_ids_salvos = [doc["id"] for doc in documentos_salvos]
            doc_selecionado_id_salvo = st.sidebar.selectbox(
                "Selecione o documento salvo pelo ID:",
                ["Selecione um ID"] + doc_ids_salvos,
                index=0
            )

            # Exibir o conteúdo do documento selecionado
            if doc_selecionado_id_salvo != "Selecione um ID":
                documento_selecionado_salvo = next(doc for doc in documentos_salvos if doc["id"] == doc_selecionado_id_salvo)
                st.markdown("## Documento Salvo Selecionado")
                st.text_area("Conteúdo do Documento", documento_selecionado_salvo["conteudo"], height=300)
        else:
            st.info("Nenhum documento salvo disponível no momento.")
