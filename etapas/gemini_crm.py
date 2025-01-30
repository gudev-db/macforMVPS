import streamlit as st
import google.generativeai as genai
import uuid
from pymongo import MongoClient
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from datetime import datetime
import os
from tavily import TavilyClient
import requests

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")

# Conexão com MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']
collection = db['auto_doc']
db_clientes = client["arquivos_planejamento"]["clientes"]

def gerar_id_planejamento():
    return str(uuid.uuid4())

def save_to_mongo_CRM(output, nome_cliente):
    id_planejamento = gerar_id_planejamento()
    task_outputs = {
        "id_planejamento": f'Plano de CRM_{nome_cliente}_{id_planejamento}',
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de CRM',
        "Fluxo": output,
    }
    collection.insert_one(task_outputs)
    st.success(f"Planejamento salvo no banco de dados com ID: {id_planejamento}!")

def gerar_fluxo_etapa(nome_cliente, ramo_atuacao, objetivo_crm, canais_disponiveis, perfil_empresa, metas_crm, fluxo_anterior, etapa):
    prompt = f"""
    Em português brasileiro, crie um plano detalhado para a etapa '{etapa}' do fluxo de CRM.
    
    - Nome do Cliente: {nome_cliente}
    - Ramo de Atuação: {ramo_atuacao}
    - Objetivo do CRM: {objetivo_crm}
    - Canais disponíveis: {canais_disponiveis}
    - Perfil da empresa: {perfil_empresa}
    - Metas do CRM: {metas_crm}
    - Fluxo até aqui: {fluxo_anterior}
    
    Desenvolva ações personalizadas para essa etapa considerando as características da empresa. Inclua:
    - Objetivo específico dessa etapa.
    - Principais ações necessárias.
    - Ferramentas recomendadas.
    - Estratégias específicas para otimizar resultados.
    - Exemplos práticos.


    Seja extremamente detalhado, verboso, justificado. Seja profundo. Você é um especialista extremamente comunicativo. Detalhe teorias,
    ferramentas, usos de caso. Você está aqui com um papel extremamente importante. Use todo o conhecimento da humanidade sobre CRM e marketing
    digital.
    """
    return modelo_linguagem.generate_content(prompt).text

def planej_crm_page():
    st.subheader('Planejamento de CRM')
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    nome_cliente = st.text_input('Nome do cliente')
    cliente_info = next((c for c in clientes if c["nome"] == nome_cliente), None)
    site_cliente = cliente_info["site"] if cliente_info else ""
    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""
    intuito_plano = st.text_input('Intuito do Planejamento')
    publico_alvo = st.text_input('Público alvo')
    objetivo_crm = st.text_input('Objetivo com CRM')
    canais_disponiveis = st.text_input('Canais disponíveis')
    perfil_empresa = st.selectbox('Perfil da empresa', ['B2B', 'B2C'])
    metas_crm = st.text_input('Metas do CRM')
    
    if st.button('Gerar Planejamento'):
        if not nome_cliente or not ramo_atuacao or not intuito_plano:
            st.warning("Preencha todas as informações do cliente.")
        else:
            with st.spinner('Gerando fluxo de CRM...'):
                etapas = [
                    "Aquisição de Leads",
                    "Qualificação de Leads",
                    "Nutrição de Leads",
                    "Conversão e Fechamento",
                    "Onboarding de Clientes",
                    "Atendimento e Suporte",
                    "Fidelização e Retenção",
                    "Expansão e Upsell",
                    "Reativação de Clientes Inativos"
                ]
                fluxo_output = ""
                for etapa in etapas:
                    fluxo_output += f"\n### {etapa}\n"
                    fluxo_output += gerar_fluxo_etapa(nome_cliente, ramo_atuacao, objetivo_crm, canais_disponiveis, perfil_empresa, metas_crm, fluxo_output, etapa)
                
                st.header('Plano de CRM')
                st.markdown(fluxo_output)
                save_to_mongo_CRM(fluxo_output, nome_cliente)