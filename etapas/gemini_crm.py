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

def gerar_fluxo_etapa(nome_cliente, ramo_atuacao, intuito_plano, publico_alvo, concorrentes, site_concorrentes, objetivos_de_marca, referencia_da_marca, possui_ferramenta_crm, maturidade_crm, canais_disponiveis, perfil_empresa, metas_crm, tamanho_base, tom_voz, fluxos_ou_emails, sla_entre_marketing_vendas, fluxo_anterior, etapa, nivel_detalhamento):
    prompt = f"""
    Em português brasileiro, crie um plano detalhado para a etapa '{etapa}' do fluxo de CRM.
    
    - Nome do Cliente: {nome_cliente}
    - Ramo de Atuação: {ramo_atuacao}
    - Intuito do Plano: {intuito_plano}
    - Público-Alvo: {publico_alvo}
    - Concorrentes: {concorrentes}
    - Sites dos Concorrentes: {site_concorrentes}
    - Objetivo de Marca: {objetivos_de_marca}
    - Referência da Marca: {referencia_da_marca}
    - Possui ferramenta de CRM: {possui_ferramenta_crm}
    - Maturidade CRM: {maturidade_crm}
    - Canais disponíveis: {canais_disponiveis}
    - Perfil da empresa: {perfil_empresa}
    - Metas do CRM: {metas_crm}
    - Tamanho da base de clientes: {tamanho_base}
    - Tom de voz: {tom_voz}
    - Fluxos e e-mails desejados: {fluxos_ou_emails}
    - SLA entre Marketing e Vendas: {sla_entre_marketing_vendas}
    
    Desenvolva ações personalizadas para essa etapa considerando as características da empresa. Inclua:
    - Objetivo específico dessa etapa.
    - Principais ações necessárias.
    - Ferramentas recomendadas.
    - Estratégias específicas para otimizar resultados.
    - Exemplos práticos.
    """
    output = modelo_linguagem.generate_content(prompt).text
    for _ in range(nivel_detalhamento - 1):
        prompt_aprofundamento = f"Aprofunde mais os detalhes dessa etapa considerando melhores práticas e otimização."
        output += "\n" + modelo_linguagem.generate_content(prompt_aprofundamento).text
    return output

def planej_crm_page():
    st.subheader('Planejamento de CRM')
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    nome_cliente = st.text_input('Nome do cliente')
    cliente_info = next((c for c in clientes if c["nome"] == nome_cliente), None)
    site_cliente = cliente_info["site"] if cliente_info else ""
    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""
    intuito_plano = st.text_input('Intuito do Plano Estratégico')
    publico_alvo = st.text_input('Público-Alvo')
    concorrentes = st.text_input('Concorrentes')
    site_concorrentes = st.text_input('Site dos Concorrentes')
    objetivos_de_marca = st.selectbox('Selecione os objetivos de marca', ['Criar ou aumentar relevância', 'Entregar potenciais consumidores', 'Venda', 'Fidelizar', 'Engajamento'])
    referencia_da_marca = st.text_area('O que a marca faz?')
    possui_ferramenta_crm = st.selectbox('A empresa possui ferramenta de CRM?', ['Sim', 'Não'])
    maturidade_crm = st.selectbox('Nível de maturidade em CRM?', ['Iniciante', 'Intermediário', 'Avançado'])
    canais_disponiveis = st.text_input('Canais de comunicação disponíveis')
    perfil_empresa = st.selectbox('Perfil da empresa', ['B2B', 'B2C'])
    metas_crm = st.text_input('Metas do CRM')
    tamanho_base = st.selectbox('Tamanho da base de clientes', ['Pequena', 'Média', 'Grande'])
    tom_voz = st.text_area('Tom de voz desejado')
    fluxos_ou_emails = st.text_area('Fluxos e/ou e-mails desejados')
    sla_entre_marketing_vendas = st.selectbox('SLA entre marketing e vendas?', ['Sim', 'Não'])
