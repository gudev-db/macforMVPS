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
def save_to_mongo(briefing, estrategia_geral, midias_pagas, email_marketing, assessoria_imprensa, endomarketing,  nome_campanha):
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
    }

    collection.insert_one(task_outputs)
    st.success(f"Planejamento de campanha salvo com sucesso! ID: {id_planejamento}")

def generate_section(prompt, section_name, model="gemini-2.0-flash"):
    """Função auxiliar para gerar seções específicas com prompts segmentados"""
    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt]
        )
        return response.text
    except Exception as e:
        st.error(f"Erro ao gerar a seção {section_name}: {str(e)}")
        return f"Erro na geração desta seção. Por favor, tente novamente."

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
        objetivo_principal = st.text_area("Briefing*", help="O que a campanha precisa alcançar?")
        publico_alvo = st.text_area("Público-Alvo*", help="Quem queremos atingir? Descreva detalhadamente")
        orcamento = st.number_input("Orçamento Total (R$)*", min_value=0)
        frentes_atuacao = st.multiselect("Frentes de Atuação*", 
                                        ["Redes Sociais", "Mídias Pagas", "E-mail Marketing", 
                                         "Assessoria de Imprensa", "Endomarketing", "Outros"],
                                        default=["Redes Sociais", "Mídias Pagas"])
        informacoes_adicionais = st.text_area("Informações Adicionais", help="Contexto extra, restrições, etc.")
        
        submitted = st.form_submit_button("Gerar Planejamento")
    
    if submitted:
        if not nome_campanha or not objetivo_principal or not publico_alvo:
            st.error("Por favor, preencha todos os campos obrigatórios (*)")
        else:
            with st.spinner('Criando planejamento de campanha...'):
                # Construindo o contexto base
                contexto_base = f"""
                **Contexto**: Holambra é uma cooperativa com forte atuação no agronegócio, conhecida por sua produção de flores e plantas ornamentais, com compromisso com sustentabilidade e inovação. Não há qualquer relação com as flores holambra ou a cidade. Se trata apenas da cooperativa agroindustrial.

                **Briefing da Campanha**:
                - Nome: {nome_campanha}
                - Data: {data_evento}
                - Briefing: {objetivo_principal}
                - Público-Alvo: {publico_alvo}
                - Orçamento: R${orcamento:,.2f}
                - Frentes: {", ".join(frentes_atuacao)}
                - Informações Adicionais: {informacoes_adicionais}
                """

                # 1. Estratégia Geral (segmentada em partes menores)
                estrategia_geral = {
                    "posicionamento": generate_section(
                        f"{contexto_base}\n\nDesenvolva o posicionamento de marca para esta campanha, considerando:\n"
                        "- Tom de voz\n- Valores a serem destacados\n- Diferenciais competitivos\n- Como queremos ser percebidos pelo público",
                        "Posicionamento de Marca"
                    ),
                    "narrativa": generate_section(
                        f"{contexto_base}\n\nCrie a narrativa central da campanha com:\n"
                        "- Storytelling principal\n- Mensagens-chave\n- Arco narrativo\n- Conexão emocional com o público",
                        "Narrativa Central"
                    ),
                    "pilares": generate_section(
                        f"{contexto_base}\n\nDefina 3-5 pilares estratégicos para esta campanha, cada um com:\n"
                        "- Nome do pilar\n- Objetivo específico\n- Como será implementado\n- Recursos necessários",
                        "Pilares da Campanha"
                    ),
                    "cronograma": generate_section(
                        f"{contexto_base}\n\nCrie um cronograma detalhado com:\n"
                        "- Fases da campanha (pré-lançamento, lançamento, pós-lançamento)\n"
                        "- Datas importantes\n- Atividades por fase\n- Responsáveis sugeridos",
                        "Cronograma"
                    )
                }

                # 2. Mídias Pagas (se aplicável)
                midias_pagas = {}
                if "Mídias Pagas" in frentes_atuacao:
                    midias_pagas = {
                        "plataformas": generate_section(
                            f"{contexto_base}\n\nRecomendação de plataformas de mídia paga:\n"
                            "- Plataformas mais adequadas\n- Justificativa para cada escolha\n"
                            "- % sugerido do orçamento para cada plataforma",
                            "Plataformas de Mídia Paga"
                        ),
                        "segmentacao": generate_section(
                            f"{contexto_base}\n\nEstratégia de segmentação detalhada:\n"
                            "- Públicos-alvo por plataforma\n- Interesses e comportamentos\n"
                            "- Parâmetros demográficos\n- Lookalike audiences sugeridas",
                            "Segmentação de Mídia Paga"
                        ),
                        "formatos": generate_section(
                            f"{contexto_base}\n\nFormatos de anúncio recomendados:\n"
                            "- Tipos de anúncio por plataforma\n- Especificações técnicas\n"
                            "- Melhores práticas para cada formato\n- Exemplos criativos",
                            "Formatos de Anúncio"
                        ),
                        "investimento": generate_section(
                            f"{contexto_base}\n\nProposta de investimento:\n"
                            "- Distribuição por plataforma\n- Cenários de orçamento\n"
                            "- ROI esperado\n- Argumentos para justificar o investimento",
                            "Investimento em Mídia Paga"
                        )
                    }

                # 3. E-mail Marketing (se aplicável)
                email_marketing = {}
                if "E-mail Marketing" in frentes_atuacao:
                    email_marketing = {
                        "segmentacao": generate_section(
                            f"{contexto_base}\n\nSegmentação para e-mail marketing:\n"
                            "- Divisão da base\n- Critérios de segmentação\n- Personas por segmento",
                            "Segmentação de E-mail"
                        ),
                        "conteudo": generate_section(
                            f"{contexto_base}\n\nConteúdo dos e-mails:\n"
                            "- Assuntos sugeridos\n- Estrutura do conteúdo\n- Chamadas para ação\n"
                            "- Elementos visuais recomendados\n- Personalização sugerida",
                            "Conteúdo de E-mail"
                        ),
                        "cronograma": generate_section(
                            f"{contexto_base}\n\nCronograma de disparos:\n"
                            "- Frequência\n- Timing em relação ao evento\n- Gatilhos para automação",
                            "Cronograma de E-mails"
                        )
                    }

                # 4. Assessoria de Imprensa (se aplicável)
                assessoria_imprensa = {}
                if "Assessoria de Imprensa" in frentes_atuacao:
                    assessoria_imprensa = {
                        "release": generate_section(
                            f"{contexto_base}\n\nEstrutura do release:\n"
                            "- Ângulo principal\n- Destaques\n- Citações sugeridas\n"
                            "- Dados para incluir\n- Contatos para a imprensa",
                            "Release de Imprensa"
                        ),
                        "veiculos": generate_section(
                            f"{contexto_base}\n\nLista de veículos e jornalistas:\n"
                            "- Veículos prioritários\n- Jornalistas especializados\n"
                            "- Bloggers/influencers relevantes\n- Mídias trade",
                            "Lista de Veículos"
                        ),
                        "pautas": generate_section(
                            f"{contexto_base}\n\nPautas adicionais:\n"
                            "- Ideias de pautas derivadas\n- Opiniões de especialistas\n"
                            "- Casos de sucesso relacionados\n- Dados estatísticos relevantes",
                            "Pautas Adicionais"
                        )
                    }

                # 5. Endomarketing (se aplicável)
                endomarketing = {}
                if "Endomarketing" in frentes_atuacao:
                    endomarketing = {
                        "engajamento": generate_section(
                            f"{contexto_base}\n\nEstratégia de engajamento interno:\n"
                            "- Formas de envolver os colaboradores\n- Programas de embaixadores\n"
                            "- Reconhecimento e recompensas\n- Comunicação interna",
                            "Engajamento Interno"
                        ),
                        "acoes": generate_section(
                            f"{contexto_base}\n\nAções de endomarketing:\n"
                            "- Eventos internos\n- Treinamentos\n- Materiais de comunicação\n"
                            "- Ativações criativas\n- Feedback dos colaboradores",
                            "Ações de Endomarketing"
                        )
                    }

                # 6. Métricas Detalhadas
                metricas_detalhadas = {
                    "por_frente": generate_section(
                        f"{contexto_base}\n\nMétricas por frente de atuação:\n"
                        "- KPIs específicos para cada canal\n- Metas quantitativas\n"
                        "- Benchmarks do setor\n- Periodicidade de medição",
                        "Métricas por Frente"
                    ),
                    "ferramentas": generate_section(
                        f"{contexto_base}\n\nFerramentas de acompanhamento:\n"
                        "- Plataformas de analytics\n- Dashboards recomendados\n"
                        "- Relatórios automatizados\n- Integrações sugeridas",
                        "Ferramentas de Métricas"
                    ),
                    "roi": generate_section(
                        f"{contexto_base}\n\nProjeção de ROI:\n"
                        "- Cálculos esperados\n- Cenários otimista/realista/conservador\n"
                        "- Valor do cliente ao longo do tempo\n- Métricas de eficiência",
                        "Projeção de ROI"
                    )
                }

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
                
                # Estratégia Geral
                st.subheader("🎯 Estratégia Geral")
                with st.expander("Posicionamento de Marca"):
                    st.markdown(estrategia_geral["posicionamento"])
                with st.expander("Narrativa Central"):
                    st.markdown(estrategia_geral["narrativa"])
                with st.expander("Pilares da Campanha"):
                    st.markdown(estrategia_geral["pilares"])
                with st.expander("Cronograma Detalhado"):
                    st.markdown(estrategia_geral["cronograma"])
                
                # Mídias Pagas
                if "Mídias Pagas" in frentes_atuacao:
                    st.subheader("📢 Mídias Pagas")
                    with st.expander("Plataformas Recomendadas"):
                        st.markdown(midias_pagas["plataformas"])
                    with st.expander("Estratégia de Segmentação"):
                        st.markdown(midias_pagas["segmentacao"])
                    with st.expander("Formatos de Anúncio"):
                        st.markdown(midias_pagas["formatos"])
                    with st.expander("Investimento e ROI"):
                        st.markdown(midias_pagas["investimento"])
                
                # E-mail Marketing
                if "E-mail Marketing" in frentes_atuacao:
                    st.subheader("✉️ E-mail Marketing")
                    with st.expander("Segmentação e Personas"):
                        st.markdown(email_marketing["segmentacao"])
                    with st.expander("Conteúdo dos E-mails"):
                        st.markdown(email_marketing["conteudo"])
                    with st.expander("Cronograma de Disparos"):
                        st.markdown(email_marketing["cronograma"])
                
                # Assessoria de Imprensa
                if "Assessoria de Imprensa" in frentes_atuacao:
                    st.subheader("📰 Assessoria de Imprensa")
                    with st.expander("Release de Imprensa"):
                        st.markdown(assessoria_imprensa["release"])
                    with st.expander("Veículos e Jornalistas"):
                        st.markdown(assessoria_imprensa["veiculos"])
                    with st.expander("Pautas Adicionais"):
                        st.markdown(assessoria_imprensa["pautas"])
                
                # Endomarketing
                if "Endomarketing" in frentes_atuacao:
                    st.subheader("🏢 Endomarketing")
                    with st.expander("Engajamento Interno"):
                        st.markdown(endomarketing["engajamento"])
                    with st.expander("Ações Específicas"):
                        st.markdown(endomarketing["acoes"])
                
                # Métricas
                st.subheader("📊 Métricas Detalhadas")
                with st.expander("Métricas por Frente"):
                    st.markdown(metricas_detalhadas["por_frente"])
                with st.expander("Ferramentas de Acompanhamento"):
                    st.markdown(metricas_detalhadas["ferramentas"])
                with st.expander("Projeção de ROI"):
                    st.markdown(metricas_detalhadas["roi"])
                
                # Botão para salvar no MongoDB
                if st.button("💾 Salvar Planejamento"):
                    save_to_mongo(
                        briefing={
                            "nome_campanha": nome_campanha,
                            "data_evento": str(data_evento),
                            "objetivo": objetivo_principal,
                            "publico_alvo": publico_alvo,
                            "orcamento": orcamento,
                            "frentes": frentes_atuacao,
                            "informacoes_adicionais": informacoes_adicionais
                        },
                        estrategia_geral=estrategia_geral,
                        midias_pagas=midias_pagas if "Mídias Pagas" in frentes_atuacao else {},
                        email_marketing=email_marketing if "E-mail Marketing" in frentes_atuacao else {},
                        assessoria_imprensa=assessoria_imprensa if "Assessoria de Imprensa" in frentes_atuacao else {},
                        endomarketing=endomarketing if "Endomarketing" in frentes_atuacao else {},
                        metricas=metricas_detalhadas,
                        nome_campanha=nome_campanha
                    )
