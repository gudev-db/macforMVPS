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

# Função para exibir subseções (modificada)
def exibir_subsecoes(selecao_sidebar, subsecao_selecionada):
    if not subsecao_selecionada:
        if selecao_sidebar == "Macro - Planejamentos Estratégicos":
            st.header("Planejamentos Estratégicos")
            st.text("No nível macro, você pode definir e estruturar os pilares estratégicos fundamentais para o crescimento da sua organização. "
                    "Aqui, você terá a oportunidade de criar planos detalhados para as várias áreas-chave de marketing, comunicação e crescimento.")
            st.subheader("1. Planejamento de Pesquisa e Estratégia")
            st.text("Desenvolva um planejamento tático e de pesquisa robusto que guiará todas as ações estratégicas de marketing da sua empresa. "
                    "Essa seção permite estruturar análises aprofundadas sobre o mercado, concorrência e comportamento do público-alvo.")
            st.subheader("2. Planejamento de Redes e Mídias")
            st.text("Elabore um planejamento detalhado para sua gestão de mídias e redes sociais. Com esse plano, você poderá traçar estratégias criativas "
                    "para atrair, engajar e fidelizar seu público, otimizando os resultados em cada plataforma social.")
            st.subheader("3. Planejamento de CRM")
            st.text("Construa um fluxo de comunicação eficaz com seus leads e clientes. Essa área oferece ferramentas para estruturar estratégias de relacionamento, "
                    "automação de processos e gestão de dados, garantindo um acompanhamento eficaz e personalizado do seu público.")
            st.subheader("4. Investigação de Leads")
            st.text("Aprofunde-se no perfil do seu lead inserindo dados relevantes como informações de LinkedIn e dados de comportamento. "
                    "Aqui, você gera relatórios detalhados que ajudam a entender a persona, suas necessidades e como realizar uma aproximação estratégica para uma conversão mais eficaz.")

        elif selecao_sidebar == "Micro - Conteúdo Específico":
            st.header("Micro - Conteúdo Específico")
            st.text("No nível micro, você tem a chance de criar e otimizar conteúdos prontos para o dia a dia da sua operação de marketing. "
                    "Esse espaço permite um desenvolvimento detalhado e altamente estratégico de conteúdo que pode ser usado em tempo real.")
            st.subheader("1. Cronograma de Temas de Emails")
            st.text("Construa um cronograma estratégico de temas de emails que irão captar a atenção dos seus leads de forma segmentada e personalizada. "
                    "Utilize esse espaço para planejar campanhas de email marketing, criando uma jornada de comunicação eficiente e impactante.")
            st.subheader("2. Redação de Emails")
            st.text("Não comece do zero! Aqui, você pode gerar exemplos de emails com base nas melhores práticas e estratégias de comunicação. "
                    "Crie mensagens persuasivas e adequadas para cada estágio do funil de vendas, garantindo uma comunicação eficaz com seus leads e clientes.")
            st.subheader("3. Brainstorming de Anúncios")
            st.text("Alavanque suas campanhas publicitárias com um brainstorming detalhado para anúncios. Ao inserir informações chave, você irá gerar várias sugestões "
                    "de anúncios criativos e de alto impacto, otimizando suas campanhas para engajar e converter seu público alvo com maior eficiência.")
            st.subheader("4. Geração de Imagens")
            st.text("Dê vida ao seu conteúdo visual! Aqui, você pode gerar ideias de imagens baseadas em uma descrição detalhada do que deseja comunicar. "
                    "Com esse brainstorming visual, você vai poder criar imagens de impacto que complementam suas campanhas e atraem a atenção do público.")
            st.subheader("5. Pesquisa de Tendências")
            st.text("Este espaço oferece a possibilidade de acompanhar as últimas tendências do mercado. Ao inserir um tema estratégico, você terá acesso a "
                    "análises e insights atualizados sobre as tendências mais recentes, ajudando a guiar suas decisões de marketing e garantindo que você sempre esteja à frente.")

        elif selecao_sidebar == "Documentos Salvos":
            st.header("Documentos Salvos")
            st.text("Aqui você pode visualizar, editar e organizar todos os documentos gerados ao longo do processo. "
                    "Essa área é essencial para manter o controle de todas as estratégias e materiais criados, facilitando o acesso e a edição desses conteúdos quando necessário.")


# Verifique se o login foi feito antes de exibir o conteúdo
if login():
    # Sidebar para escolher entre "Plano Estratégico" ou "Brainstorming"
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        ["Macro - Planejamentos Estratégicos", "Micro - Conteúdo Específico", "Documentos Salvos"],
        index=0  # Predefinir como 'Plano Estratégico' ativo
    )

    # Exibir as subseções com explicações dependendo da seleção no sidebar
    exibir_subsecoes(selecao_sidebar)

    # Seção para "Plano Estratégico"
    if selecao_sidebar == "Macro - Planejamentos Estratégicos":
        st.sidebar.subheader("Planejamentos Completos")
        plano_estrategico = st.sidebar.selectbox(
            "Escolha o tipo de plano:",
            [
                "Selecione uma opção",
                "Planejamento de Pesquisa e Estratégia",
                "Planejamento de Redes e Mídias",
                "Planejamento de CRM",
                "Investigação de Leads"
            ]
        )

        if plano_estrategico != "Selecione uma opção":
            if plano_estrategico == "Planejamento de Pesquisa e Estratégia":
                planej_mkt_page()
            elif plano_estrategico == "Planejamento de Redes e Mídias":
                planej_midias_page()
            elif plano_estrategico == "Planejamento de CRM":
                planej_crm_page()
            elif plano_estrategico == "Investigação de Leads":
                osint_report()

    # Seção para "Brainstorming"
    elif selecao_sidebar == "Micro - Conteúdo Específico":
        st.sidebar.subheader("Micro")
        brainstorming_option = st.sidebar.selectbox(
            "Escolha o tipo de conteúdo Micro:",
            [
                "Selecione uma opção",
                "Brainstorming de Temas de Emails",
                "Brainstorming de Emails",
                "Brainstorming de Anúncios",
                "Brainstorming de Imagem",
                "Pesquisa de Tendências",
            ]
        )

        if brainstorming_option != "Selecione uma opção":
            if brainstorming_option == "Temas de Emails":
                gen_temas_emails()
            elif brainstorming_option == "Brainstorming de Emails":
                gen_emails()
            elif brainstorming_option == "Brainstorming de Anúncios":
                planej_campanhas()
            elif brainstorming_option == "Brainstorming de Imagem":
                gen_img()
            elif brainstorming_option == "Pesquisa de Tendências":
                pesquisa()

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
