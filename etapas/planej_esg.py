import streamlit as st
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import uuid
import os
from pymongo import MongoClient
from datetime import datetime

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Conexão com MongoDB
client_mongo = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client_mongo['arquivos_planejamento']
collection = db['planejamentos_campanha']

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

# Função para salvar no MongoDB
def save_to_mongo(briefing, estrategia_geral, midias_pagas, email_marketing, assessoria_imprensa, endomarketing, metricas, nome_campanha):
    id_planejamento = gerar_id_planejamento()
    
    task_outputs = {
        "id_planejamento": 'Campanha_' + nome_campanha + '_' + id_planejamento,
        "nome_campanha": nome_campanha,
        "tipo_plano": 'Plano de Campanha',
        "data_criacao": datetime.now(),
        "briefing": briefing,
        "estrategia_geral": estrategia_geral,
        "midias_pagas": midias_pagas,
        "email_marketing": email_marketing,
        "assessoria_imprensa": assessoria_imprensa,
        "endomarketing": endomarketing,
        "metricas": metricas
    }

    collection.insert_one(task_outputs)
    st.success(f"Planejamento de campanha salvo com sucesso! ID: {id_planejamento}")

def planejamento_campanha_page():
    st.title("Planejamento de Campanha para Holambra")
    st.markdown("""
    **Crie planejamentos de campanha completos considerando as especificidades de Holambra e o briefing fornecido.**
    """)
    
    with st.expander("📋 Instruções"):
        st.markdown("""
        1. Preencha todos os campos do briefing abaixo
        2. Clique em 'Gerar Planejamento'
        3. Revise os resultados
        4. Salve no banco de dados
        """)
    
    # Formulário de briefing
    with st.form("briefing_form"):
        st.subheader("Briefing da Campanha")
        
        nome_campanha = st.text_input("Nome da Campanha*", help="Ex: Lançamento Relatório de Sustentabilidade 2024")
        data_evento = st.date_input("Data do Evento/Lançamento*")
        objetivo_principal = st.text_area("Objetivo Principal*", help="O que a campanha precisa alcançar?")
        publico_alvo = st.text_area("Público-Alvo*", help="Quem queremos atingir? Descreva detalhadamente")
        metricas = st.text_area("Métricas de Sucesso*", help="Como vamos medir o sucesso? Quais KPIs?")
        orcamento = st.number_input("Orçamento Total (R$)*", min_value=0)
        frentes_atuacao = st.multiselect("Frentes de Atuação*", 
                                        ["Redes Sociais", "Mídias Pagas", "E-mail Marketing", 
                                         "Assessoria de Imprensa", "Endomarketing", "Outros"],
                                        default=["Redes Sociais", "Mídias Pagas"])
        informacoes_adicionais = st.text_area("Informações Adicionais", help="Contexto extra, restrições, etc.")
        
        submitted = st.form_submit_button("Gerar Planejamento")
    
    if submitted:
        if not nome_campanha or not objetivo_principal or not publico_alvo or not metricas:
            st.error("Por favor, preencha todos os campos obrigatórios (*)")
        else:
            with st.spinner('Criando planejamento de campanha...'):
                # Construindo o prompt completo
                prompt_briefing = f"""
                **Contexto**: Holambra é uma cooperativa com forte atuação no agronegócio, conhecida por sua produção de flores e plantas ornamentais, com compromisso com sustentabilidade e inovação.

                **Briefing da Campanha**:
                - Nome: {nome_campanha}
                - Data: {data_evento}
                - Objetivo: {objetivo_principal}
                - Público-Alvo: {publico_alvo}
                - Métricas: {metricas}
                - Orçamento: R${orcamento:,.2f}
                - Frentes: {", ".join(frentes_atuacao)}
                - Informações Adicionais: {informacoes_adicionais}

                **Instruções**:
                Como especialista em marketing digital com foco no agronegócio, crie um planejamento de campanha completo para Holambra considerando:
                1. As melhores práticas de marketing digital
                2. As especificidades do setor agrícola e do público de Holambra
                3. O briefing fornecido
                4. Destaque especialmente a defesa de mídias pagas quando aplicável
                5. Considere diferentes níveis de orçamento quando relevante

                Retorne o planejamento com as seguintes seções:
                """

                # Geração das seções do planejamento
                estrategia_geral = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"""
                    {prompt_briefing}
                    
                    **Estratégia Geral de Campanha**:
                    - Desenvolva uma estratégia integrada considerando o briefing
                    - Destaque o posicionamento de marca
                    - Proponha uma narrativa central
                    - Defina os pilares da campanha
                    - Considere o timing e fases da campanha
                    """]
                ).text

                midias_pagas = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"""
                    {prompt_briefing}
                    
                    **Plano de Mídias Pagas** (defenda fortemente esta frente quando aplicável):
                    - Plataformas recomendadas (Meta Ads, Google Ads, LinkedIn etc.)
                    - Estratégia de segmentação detalhada
                    - Tipos de anúncios recomendados
                    - Proposta de investimento (considerando diferentes cenários de orçamento)
                    - Argumentos para justificar o investimento em mídia paga
                    - Previsão de resultados
                    """]
                ).text

                email_marketing = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"""
                    {prompt_briefing}
                    
                    **Estratégia de E-mail Marketing**:
                    - Proposta de régua de e-mails
                    - Segmentação da base
                    - Conteúdo dos e-mails
                    - Cronograma de disparos
                    - Métricas específicas para acompanhamento
                    """]
                ).text

                assessoria_imprensa = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"""
                    {prompt_briefing}
                    
                    **Estratégia de Assessoria de Imprensa**:
                    - Proposta de release (estrutura e ângulos)
                    - Lista de veículos e jornalistas a abordar
                    - Sugestão de pautas adicionais
                    - Cronograma de divulgação
                    """]
                ).text

                endomarketing = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"""
                    {prompt_briefing}
                    
                    **Ações de Endomarketing**:
                    - Ideias para engajamento interno
                    - Proposta de comunicação com colaboradores
                    - Ativações criativas
                    - Cronograma de ações
                    """]
                ).text

                metricas_detalhadas = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"""
                    {prompt_briefing}
                    
                    **Detalhamento de Métricas e ROI**:
                    - Métricas por frente de atuação
                    - Metas específicas
                    - Como mensurar cada KPI
                    - Projeção de ROI
                    - Ferramentas de acompanhamento recomendadas
                    """]
                ).text

                # Exibição dos resultados
                st.success("Planejamento gerado com sucesso!")
                
                st.subheader("📋 Briefing Resumido")
                st.markdown(f"""
                - **Campanha**: {nome_campanha}
                - **Data**: {data_evento}
                - **Objetivo**: {objetivo_principal}
                - **Público**: {publico_alvo}
                - **Orçamento**: R${orcamento:,.2f}
                """)
                
                st.subheader("🎯 Estratégia Geral")
                st.markdown(estrategia_geral)
                
                if "Mídias Pagas" in frentes_atuacao:
                    st.subheader("📢 Mídias Pagas")
                    st.markdown(midias_pagas)
                
                if "E-mail Marketing" in frentes_atuacao:
                    st.subheader("✉️ E-mail Marketing")
                    st.markdown(email_marketing)
                
                if "Assessoria de Imprensa" in frentes_atuacao:
                    st.subheader("📰 Assessoria de Imprensa")
                    st.markdown(assessoria_imprensa)
                
                if "Endomarketing" in frentes_atuacao:
                    st.subheader("🏢 Endomarketing")
                    st.markdown(endomarketing)
                
                st.subheader("📊 Métricas Detalhadas")
                st.markdown(metricas_detalhadas)
                
                # Botão para salvar no MongoDB
                if st.button("💾 Salvar Planejamento"):
                    save_to_mongo(
                        briefing={
                            "nome_campanha": nome_campanha,
                            "data_evento": str(data_evento),
                            "objetivo": objetivo_principal,
                            "publico_alvo": publico_alvo,
                            "metricas": metricas,
                            "orcamento": orcamento,
                            "frentes": frentes_atuacao,
                            "informacoes_adicionais": informacoes_adicionais
                        },
                        estrategia_geral=estrategia_geral,
                        midias_pagas=midias_pagas if "Mídias Pagas" in frentes_atuacao else "Não aplicável",
                        email_marketing=email_marketing if "E-mail Marketing" in frentes_atuacao else "Não aplicável",
                        assessoria_imprensa=assessoria_imprensa if "Assessoria de Imprensa" in frentes_atuacao else "Não aplicável",
                        endomarketing=endomarketing if "Endomarketing" in frentes_atuacao else "Não aplicável",
                        metricas=metricas_detalhadas,
                        nome_campanha=nome_campanha
                    )
