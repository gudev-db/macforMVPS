import streamlit as st
import google import genai
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
    
    # Setores disponíveis
    setores = ["Social Media", "CRM", "Mídia", "Tech", "Analytics", "Design", "Redação", "SEO", "Planejamento"]
    
    # Interface do Streamlit
    st.title("Gerador de Briefing por Setor")
    st.sidebar.header("Configurações")
    setor_selecionado = st.sidebar.selectbox("Escolha o setor:", setores)
    
    st.subheader(f"Briefing para {setor_selecionado}")
    
    # Campos gerais do briefing
    nome_cliente = st.text_input("Nome do Cliente:")
    projeto_peca = st.text_input("Qual é o projeto ou peça?:")
    cenario = st.text_area("Qual o cenário atual do cliente?:")
    objetivos = st.text_area("Quais são os objetivos do cliente ao contratar a agência?:")
    publico = st.text_area("Qual é o público-alvo?:")
    periodo = st.text_input("Qual será o período de atuação?:")
    verba = st.text_input("Qual a verba disponível?:")
    
    # Campos específicos por setor
    if setor_selecionado == "Social Media":
        redes = st.text_area("Quais redes sociais serão usadas?:")
        estrategia = st.text_area("Qual a estratégia de conteúdo para esse projeto?:")
    elif setor_selecionado == "CRM":
        ferramentas = st.text_area("Quais ferramentas de CRM serão utilizadas?:")
        fluxo_comunicacao = st.text_area("Como será o fluxo de comunicação com os clientes?:")
    elif setor_selecionado == "Mídia":
        canais = st.text_area("Quais canais de mídia serão utilizados?:")
        formatos = st.text_area("Quais formatos de anúncio serão usados?:")
    elif setor_selecionado == "Tech":
        tecnologia = st.text_area("Quais tecnologias serão usadas no projeto?:")
        integracoes = st.text_area("Há necessidade de integração com outras plataformas?:")
    elif setor_selecionado == "Analytics":
        kpis = st.text_area("Quais KPIs serão monitorados?:")
        ferramentas_analytics = st.text_area("Quais ferramentas de análise serão usadas?:")
    elif setor_selecionado == "Design":
        referencias = st.text_area("Quais referências visuais devem ser consideradas?:")
        restricoes = st.text_area("Há alguma restrição no design ou branding a seguir?:")
    elif setor_selecionado == "Redação":
        tom_voz = st.text_area("Qual o tom de voz a ser usado?:")
        palavras_chave = st.text_area("Quais palavras-chave são essenciais no texto?:")
    elif setor_selecionado == "SEO":
        estrategia_seo = st.text_area("Qual a estratégia de SEO para esse projeto?:")
        palavras_chave = st.text_area("Quais palavras-chave devem ser priorizadas?:")
    elif setor_selecionado == "Planejamento":
        cronograma = st.text_area("Qual o cronograma previsto para o projeto?:")
        desafios = st.text_area("Quais desafios podem impactar o planejamento?:")
    
    # Geração do briefing
    if st.button("Gerar Briefing"):
        if not nome_cliente or not projeto_peca or not cenario or not objetivos:
            st.warning("Por favor, preencha os campos obrigatórios.")
        else:
            with st.spinner("Gerando o documento de briefing..."):
                prompt = f"""
                Você é um especialista em {setor_selecionado} que trabalha para a Macfor Marketing Digital. Com base nas informações fornecidas, gere um briefing estruturado e formal.
    
                Consideranto as diretrizes de um bom briefing para a Macfor Marketing Digital: {oq_brief};

                Não acrescente informações, apenas sintetize os inputs do usuário em um formato de documento de briefing;

                Crie uma subseção para cada entrada do usuário
    
                Considerando as informações do cliente:
                
                Cliente: {nome_cliente}
                Projeto: {projeto_peca}
                Cenário: {cenario}
                Objetivos: {objetivos}
                Público-alvo: {publico}
                Período: {periodo}
                Verba: {verba}

                
                """
                
                if setor_selecionado == "Social Media":
                    prompt += f"\nRedes Sociais: {redes}\nEstratégia: {estrategia}"
                elif setor_selecionado == "CRM":
                    prompt += f"\nFerramentas: {ferramentas}\nFluxo de Comunicação: {fluxo_comunicacao}"
                elif setor_selecionado == "Mídia":
                    prompt += f"\nCanais: {canais}\nFormatos: {formatos}"
                elif setor_selecionado == "Tech":
                    prompt += f"\nTecnologias: {tecnologia}\nIntegrações: {integracoes}"
                elif setor_selecionado == "Analytics":
                    prompt += f"\nKPIs: {kpis}\nFerramentas de Analytics: {ferramentas_analytics}"
                elif setor_selecionado == "Design":
                    prompt += f"\nReferências Visuais: {referencias}\nRestrições: {restricoes}"
                elif setor_selecionado == "Redação":
                    prompt += f"\nTom de Voz: {tom_voz}\nPalavras-chave: {palavras_chave}"
                elif setor_selecionado == "SEO":
                    prompt += f"\nEstratégia de SEO: {estrategia_seo}\nPalavras-chave: {palavras_chave}"
                elif setor_selecionado == "Planejamento":
                    prompt += f"\nCronograma: {cronograma}\nDesafios: {desafios}"
                
                briefing_gerado = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt]).text

                
                st.subheader("Briefing Gerado")
                st.markdown(briefing_gerado)
