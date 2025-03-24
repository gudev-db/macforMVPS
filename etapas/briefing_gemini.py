import streamlit as st
from google import genai
import os
from datetime import datetime
import os
import requests


def briefing():

    oq_brief = '''É O DOCUMENTO QUE
    CONSOLIDA TODA INFORMAÇÃO
    RELEVANTE E NECESSÁRIA
    PARA A EXECUÇÃO DO
    TRABALHO.
    
    serve como guia, inspiração e também como destrave para
    o processo estratégico e criativo.
    
    
    ANTES DE INICIAR QUALQUER TRABALHO DE
    COMUNICAÇÃO/ESTRATÉGIA É IMPORTANTE
    QUE O PLANEJADOR TENHA O BRIEFING
    CORRETO PARA CONSEGUIR CONSTRUIR A
    MELHOR SOLUÇÃO PARA O OBJETIVO.
    
    
    UM BOM BRIEFING DEVE SER
    
    CLARO
    CONCISO
    LINEAR
    INSPIRADOR
    
    As informações precisam estar detalhadas
    de forma precisa, com uma narrativa que
    seja de fácil entendimento e que fique
    evidente qual é o problema a ser
    resolvido.
    
    DESAFIOS PARA A
    CONSTRUÇÃO DE UM BRIEFING
    POTENTE:
    
    INFORMAÇÕES QUE SÃO REALMENTE RELEVANTES.
    
    NÃO ABORDAR OBJETIVOS E
    INFORMAÇÕES SECUNDÁRIAS QUE NÃO
    SEJAM RELEVANTE
    
    PARA O TRABALHO. MUITAS VEZES MENOS É MAIS.
    
    # ORGANIZAÇÃO DA INFORMAÇÃO
    # ASSERTIVIDADE
    
    # DIRECIONAMENTO CLARO
    
    INFORMAÇÕES QUE
    SÃO
    FUNDAMENTAIS:
    
    Contexto
    
    Objetivo do projeto
    Target (Público-alvo)
    Mercado / Concorrência
    Budget (orçamento)
    Prazo
    
    Pontos de atenção
    
    2023
    
    MIAMI AD SCHOOL
    
    BRIEFING & INSIGHT
    
    BRIEFING & INSIGHT
    
    MIAMI AD SCHOOL
    
    2023
    
    INFORMAÇÕES QUE
    SÃO
    FUNDAMENTAIS:
    
    _CONTEXTO
    
    Por que esse trabalho vai ser desenvolvido?
    
    Um panorama geral sobre o que está acontecendo
    e uma breve introdução do que vai ser explorado.
    
    ex: “nos últimos anos a categoria se tornou extremamente
    competitiva e com isso a imagem da marca vem perdendo
    força como referência em inovação"
    
    2023
    
    MIAMI AD SCHOOL
    
    BRIEFING & INSIGHT
    
    BRIEFING & INSIGHT
    
    MIAMI AD SCHOOL
    
    2023
    
    INFORMAÇÕES QUE
    SÃO
    FUNDAMENTAIS:
    
    _OBJETIVO DO PROJETO
    
    Qual é o principal desafio a ser resolvido?
    
    Lançamento de produto
    Fortalecimento de imagem
    Posicionamento de marca
    Reposicionamento de marca
    Campanha institucional
    Campanha de aquisição
    Rejuvenescimento de marca
    Jornada do consumidor
    
    2023
    
    MIAMI AD SCHOOL
    
    BRIEFING & INSIGHT
    
    BRIEFING & INSIGHT
    
    MIAMI AD SCHOOL
    
    2023
    
    INFORMAÇÕES QUE
    SÃO
    FUNDAMENTAIS:
    
    _TARGET (PÚBLICO-ALVO)
    
    Com quem iremos nos conectar?
    
    _Faixa etária
    
    _Classe social
    
    _Localização
    
    _Hábitos de consumo
    
    _Descrição atitudinal - muito importante
    
    2023
    
    MIAMI AD SCHOOL
    
    BRIEFING & INSIGHT
    
    BRIEFING & INSIGHT
    
    MIAMI AD SCHOOL
    
    2023
    
    INFORMAÇÕES QUE
    SÃO
    FUNDAMENTAIS:
    
    2023
    
    MIAMI AD SCHOOL
    
    BRIEFING & INSIGHT
    
    _MERCADO / CONCORRÊNCIA
    
    Em que mar navegamos? Existe algum ponto de atenção?
    
    últimos movimentos de comunicação, posicionamento, iniciativas de marca e comunicação
    
    _Cenário atual
    
    _Fortalezas
    
    _Fraquezas
    
    _Principais movimentos
    
    _Concorrentes diretos
    
    BRIEFING & INSIGHT
    
    MIAMI AD SCHOOL
    
    2023
    
    INFORMAÇÕES QUE
    SÃO
    FUNDAMENTAIS:
    
    _BUDGET (ORÇAMENTO) E PRAZO
    
    Qual é o nosso universo de execução?
    
    _PONTOS DE ATENÇÃO
    
    Existe alguma dica que vale ser ressaltada que
    ajudará no projeto?
    
    '''
    
    
    
    
    # Configuração do Gemini API
    gemini_api_key = os.getenv("GEM_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    

    
    # Função para limpar o estado do Streamlit
    def limpar_estado():
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
  # Interface do Streamlit
st.set_page_config(layout="wide", page_title="Gerador de Briefing Macfor")
st.title("📋 Gerador de Briefing por Setor - Macfor Marketing Digital")
st.sidebar.header("Configurações")

# Seletor de setor e data
col1, col2 = st.sidebar.columns(2)
with col1:
    setor_selecionado = st.selectbox("Escolha o setor:", setores)
with col2:
    data_briefing = st.date_input("Data do briefing:", datetime.today())

# Informações básicas
st.header("1. Informações Básicas")
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nome_cliente = st.text_input("Nome do Cliente*:", key="cliente")
        projeto_peca = st.text_input("Nome do Projeto/Peça*:", key="projeto")
        responsavel = st.text_input("Responsável no Cliente:", key="responsavel")
        
    with col2:
        contato = st.text_input("Contato do Cliente:", key="contato")
        verba = st.text_input("Verba Disponível (R$):", key="verba")
        periodo = st.text_input("Período de Execução:", key="periodo")

    cenario = st.text_area("Cenário Atual/Contexto*:", height=100, key="cenario")
    objetivos = st.text_area("Objetivos Principais*:", height=100, key="objetivos")
    publico = st.text_area("Público-Alvo*:", height=100, key="publico")

# Seção específica por setor
st.header(f"2. Informações Específicas - {setor_selecionado}")
with st.container(border=True):
    if setor_selecionado == "Social Media":
        redes = st.multiselect(
            "Redes Sociais:",
            ["Instagram", "Facebook", "LinkedIn", "TikTok", "Twitter", "YouTube", "Outros"],
            key="redes"
        )
        outros_redes = st.text_input("Outras redes:", key="outros_redes")
        estrategia = st.text_area("Estratégia de Conteúdo:", height=100, key="estrategia_social")
        tom_voz = st.text_input("Tom de Voz:", key="tom_voz_social")
        metricas = st.text_input("Métricas de Sucesso:", key="metricas_social")
        
    elif setor_selecionado == "CRM":
        ferramentas = st.selectbox(
            "Ferramenta de CRM:",
            ["RD Station", "HubSpot", "Salesforce", "Outros"],
            key="ferramentas_crm"
        )
        outros_ferramentas = st.text_input("Outra ferramenta:", key="outros_ferramentas_crm")
        tamanho_base = st.text_input("Tamanho da Base:", key="tamanho_base")
        segmentacao = st.text_area("Segmentação do Público:", height=100, key="segmentacao")
        fluxo_comunicacao = st.text_area("Fluxo de Comunicação:", height=100, key="fluxo_crm")
        
    elif setor_selecionado == "Mídia":
        canais = st.multiselect(
            "Canais de Mídia:",
            ["Google Ads", "Meta Ads", "LinkedIn Ads", "TikTok Ads", "Display", "Outros"],
            key="canais_midia"
        )
        outros_canais = st.text_input("Outros canais:", key="outros_canais_midia")
        formatos = st.multiselect(
            "Formatos de Anúncio:",
            ["Imagem", "Vídeo", "Carrossel", "Stories", "Lead Ads", "Outros"],
            key="formatos_midia"
        )
        mecanismo = st.text_area("Mecanismo Promocional:", height=100, key="mecanismo")
        kpis = st.text_input("KPIs Principais:", key="kpis_midia")
        
    elif setor_selecionado == "Tech":
        tipo_projeto = st.selectbox(
            "Tipo de Projeto:",
            ["Landing Page", "Site Institucional", "E-commerce", "Aplicativo", "Outros"],
            key="tipo_projeto_tech"
        )
        outros_tipo = st.text_input("Outro tipo:", key="outros_tipo_tech")
        tecnologias = st.text_area("Tecnologias Utilizadas:", height=100, key="tecnologias")
        integracoes = st.text_area("Integrações Necessárias:", height=100, key="integracoes")
        requisitos = st.text_area("Requisitos Técnicos:", height=100, key="requisitos_tech")
        
    elif setor_selecionado == "Analytics":
        ferramentas_analytics = st.multiselect(
            "Ferramentas de Analytics:",
            ["Google Analytics", "Meta Analytics", "Google Data Studio", "Power BI", "Outros"],
            key="ferramentas_analytics"
        )
        outros_ferramentas_analytics = st.text_input("Outras ferramentas:", key="outros_ferramentas_analytics")
        kpis = st.text_area("KPIs para Monitoramento:", height=100, key="kpis_analytics")
        dashboards = st.text_area("Necessidades de Dashboard:", height=100, key="dashboards")
        
    elif setor_selecionado == "Design":
        tipo_arte = st.selectbox(
            "Tipo de Arte:",
            ["Post Social", "Banner", "Landing Page", "E-mail Marketing", "Outros"],
            key="tipo_arte"
        )
        outros_tipo_arte = st.text_input("Outro tipo:", key="outros_tipo_arte")
        referencias = st.text_area("Referências Visuais:", height=100, key="referencias")
        restricoes = st.text_area("Restrições de Design:", height=100, key="restricoes")
        elementos = st.text_area("Elementos Obrigatórios:", height=100, key="elementos_design")
        
    elif setor_selecionado == "Redação":
        tipo_conteudo = st.selectbox(
            "Tipo de Conteúdo:",
            ["Post Blog", "E-mail", "Anúncio", "Roteiro", "Outros"],
            key="tipo_conteudo"
        )
        outros_tipo_conteudo = st.text_input("Outro tipo:", key="outros_tipo_conteudo")
        tom_voz = st.text_area("Tom de Voz:", height=100, key="tom_voz_redacao")
        palavras_chave = st.text_area("Palavras-chave:", height=100, key="palavras_chave_redacao")
        ctas = st.text_area("CTAs Obrigatórios:", height=100, key="ctas")
        
    elif setor_selecionado == "SEO":
        estrategia_seo = st.selectbox(
            "Estratégia de SEO:",
            ["On-Page", "Off-Page", "Técnico", "Local", "Conteúdo"],
            key="estrategia_seo"
        )
        palavras_chave = st.text_area("Palavras-chave Prioritárias:", height=100, key="palavras_chave_seo")
        concorrentes = st.text_area("Concorrentes de Referência:", height=100, key="concorrentes_seo")
        metricas = st.text_area("Métricas de Performance:", height=100, key="metricas_seo")
        
    elif setor_selecionado == "Planejamento":
        fase_funil = st.selectbox(
            "Fase do Funil:",
            ["Topo", "Meio", "Fundo", "Retenção"],
            key="fase_funil"
        )
        cronograma = st.text_area("Cronograma Detalhado:", height=100, key="cronograma")
        desafios = st.text_area("Desafios Esperados:", height=100, key="desafios")
        metricas = st.text_area("Métricas de Sucesso:", height=100, key="metricas_planejamento")

# Seção de materiais de referência
st.header("3. Materiais de Referência")
with st.container(border=True):
    referencias = st.text_area("Links ou Referências Úteis:", height=100, key="referencias_geral")
    observacoes = st.text_area("Observações Adicionais:", height=100, key="observacoes")

# Botão de geração
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("✨ Gerar Briefing Completo", use_container_width=True):
        # Validação dos campos obrigatórios
        campos_obrigatorios = {
            "Nome do Cliente": nome_cliente,
            "Projeto/Peça": projeto_peca,
            "Cenário Atual": cenario,
            "Objetivos": objetivos,
            "Público-Alvo": publico
        }
        
        faltantes = [k for k, v in campos_obrigatorios.items() if not v]
        
        if faltantes:
            st.error(f"🚨 Campos obrigatórios faltando: {', '.join(faltantes)}")
        else:
            with st.spinner("🔍 Gerando briefing profissional..."):
                try:
                    # Construção do prompt estruturado
                    prompt = f"""
                    Gere um briefing profissional para {setor_selecionado} seguindo rigorosamente este formato:

                    # BRIEFING {setor_selecionado.upper()} - {nome_cliente.upper()}
                    *Data: {data_briefing.strftime('%d/%m/%Y')}*

                    ## 1. INFORMAÇÕES BÁSICAS
                    - **Cliente:** {nome_cliente}
                    - **Projeto/Peça:** {projeto_peca}
                    - **Responsável no Cliente:** {responsavel if responsavel else 'Não informado'}
                    - **Contato:** {contato if contato else 'Não informado'}
                    - **Período de Execução:** {periodo if periodo else 'Não definido'}
                    - **Verba Disponível:** {verba if verba else 'Não informada'}

                    ### Contexto
                    {cenario}

                    ### Objetivos
                    {objetivos}

                    ### Público-Alvo
                    {publico}

                    ## 2. INFORMAÇÕES ESPECÍFICAS - {setor_selecionado.upper()}
                    """
                    
                    # Adiciona conteúdo específico por setor
                    if setor_selecionado == "Social Media":
                        redes_lista = redes + ([outros_redes] if outros_redes else [])
                        prompt += f"""
                        - **Redes Sociais:** {', '.join(redes_lista) if redes_lista else 'Não definidas'}
                        - **Estratégia de Conteúdo:** {estrategia if estrategia else 'Não definida'}
                        - **Tom de Voz:** {tom_voz if tom_voz else 'Não definido'}
                        - **Métricas de Sucesso:** {metricas if metricas else 'Não definidas'}
                        """
                    
                    elif setor_selecionado == "CRM":
                        ferramenta = outros_ferramentas if ferramentas == "Outros" else ferramentas
                        prompt += f"""
                        - **Ferramenta de CRM:** {ferramenta if ferramenta else 'Não definida'}
                        - **Tamanho da Base:** {tamanho_base if tamanho_base else 'Não informado'}
                        - **Segmentação do Público:** {segmentacao if segmentacao else 'Não definida'}
                        - **Fluxo de Comunicação:** {fluxo_comunicacao if fluxo_comunicacao else 'Não definido'}
                        """
                    
                    # [...] (continuar para outros setores seguindo o mesmo padrão)
                    
                    prompt += f"""
                    ## 3. MATERIAIS DE REFERÊNCIA
                    {referencias if referencias else 'Nenhuma referência fornecida'}

                    ## 4. OBSERVAÇÕES
                    {observacoes if observacoes else 'Nenhuma observação adicional'}

                    ## 5. DIRETRIZES MACFOR
                    {OQ_BRIEF}

                    FORMATO FINAL:
                    - Linguagem profissional
                    - Seções claramente demarcadas
                    - Destaque para informações críticas
                    - Listas com marcadores quando aplicável
                    - Sem informações inventadas
                    """
                    
                    # Chamada à API do Gemini
                    response = client.generate_content(
                        model="gemini-1.5-pro-latest",
                        contents=[{"parts": [{"text": prompt}]}],
                        generation_config={
                            "temperature": 0.3,
                            "top_p": 0.95,
                            "max_output_tokens": 8192
                        }
                    )
                    
                    briefing_gerado = response.text
                    
                    # Exibição do resultado
                    st.success("✅ Briefing gerado com sucesso!")
                    st.subheader(f"Briefing {setor_selecionado} - {nome_cliente}")
                    st.markdown(briefing_gerado)
                    
                    # Opção para download
                    st.download_button(
                        label="📥 Download do Briefing",
                        data=briefing_gerado,
                        file_name=f"Briefing_{setor_selecionado}_{nome_cliente}_{data_briefing.strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Erro ao gerar briefing: {str(e)}")

# Botão para limpar o formulário
with st.sidebar:
    if st.button("🧹 Limpar Formulário", use_container_width=True):
        limpar_estado()
        st.rerun()

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 Macfor Marketing Digital")
