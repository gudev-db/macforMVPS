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

def gerar_fluxo_etapa(nome_cliente, ramo_atuacao, objetivo_crm, canais_disponiveis, perfil_empresa, metas_crm, fluxo_anterior,publico_alvo,maturidade_crm,tamanho_base,tom_voz,fluxos_ou_emails,sla_entre_marketing_vendas, etapa, nivel_detalhamento):
    prompt = f"""
    Em português brasileiro, crie um plano detalhado para a etapa '{etapa}' do fluxo de CRM.
    
    - Nome do Cliente: {nome_cliente}
    - Ramo de Atuação: {ramo_atuacao}
    - Objetivo do CRM: {objetivo_crm}
    - Canais disponíveis: {canais_disponiveis}
    - Perfil da empresa: {perfil_empresa}
    - Metas do CRM: {metas_crm}
    - Fluxo até aqui: {fluxo_anterior}
    - Público alvo: {publico_alvo}
    - Maturidade do CRM existente: {maturidade_crm}
    - Tamanho da base de clientes existente: {tamanho_base}
    - Tom de voz desejado: {tom_voz}
    - Fluxo desejado: {fluxos_ou_emails}
    - Há algum SLA combinado entre marketing e vendas para geração de leads?: {sla_entre_marketing_vendas}

    
    Desenvolva ações personalizadas para essa etapa considerando as características da empresa. Inclua:
    - Objetivo específico dessa etapa.
    - Principais ações necessárias.
    - Ferramentas recomendadas.
    - Estratégias específicas para otimizar resultados.
    - Exemplos práticos.
    """
    output = modelo_linguagem.generate_content(prompt).text
    for _ in range(nivel_detalhamento - 1):
        prompt_aprofundamento = f'''Aprofunde mais cada detalhe descrito nessa etapa de uma forma que ela se torne mais prática. Diga exatamente
        o que deve ser feito em cada detalhe descrito. Seja menos vago, detalhe mais. Aprofunde exatamente o que deve ser feito. Você está aqui
        para construir o plano de ação exato que minha empresa deve seguir. Você é o especialista.'''
        output += "\n" + modelo_linguagem.generate_content(prompt_aprofundamento).text
    return output

def planej_crm_page():
    st.subheader('Planejamento de CRM')
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    nome_cliente = st.text_input('Nome do cliente')
    cliente_info = next((c for c in clientes if c["nome"] == nome_cliente), None)

    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""
    intuito_plano = st.text_input('Intuito do Plano Estratégico')
    publico_alvo = st.text_input('Público-Alvo')

    
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]
    objetivos_de_marca = st.selectbox('Selecione os objetivos de marca', objetivos_opcoes)
    referencia_da_marca = st.text_area('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?')
    possui_ferramenta_crm = st.selectbox('A empresa possui ferramenta de CRM?', ['Sim', 'Não'])
    maturidade_crm = st.selectbox('Qual é o nível de maturidade em CRM (histórico)?', ['Iniciante', 'Intermediário', 'Avançado'])
    canais_disponiveis = st.text_input('Quais canais de comunicação estão disponíveis?')
    perfil_empresa = st.selectbox('Qual é o perfil da empresa?', ['B2B', 'B2C'])
    metas_crm = st.text_input('Quais metas a serem alcançadas com o CRM?')
    tamanho_base = st.selectbox('Qual o tamanho da base de dados de clientes?', ['Pequena', 'Média', 'Grande'])
    tom_voz = st.text_area('Qual o tom de voz desejado para a comunicação?')
    fluxos_ou_emails = st.text_area('Quais fluxos e/ou e-mails deseja trabalhar?')
    sla_entre_marketing_vendas = st.selectbox('Há algum SLA combinado entre marketing e vendas para geração de leads?', ['Sim', 'Não'])
    
    detalhamento_etapas = {}
    etapas = [
        "Aquisição de Leads", "Qualificação de Leads", "Nutrição de Leads", "Conversão e Fechamento", "Onboarding de Clientes",
        "Atendimento e Suporte", "Fidelização e Retenção", "Expansão e Upsell", "Reativação de Clientes Inativos"
    ]
    for etapa in etapas:
        detalhamento_etapas[etapa] = st.slider(f'Nível de detalhamento para {etapa}', 1, 3, 3)
    
    if st.button('Gerar Planejamento'):
        if not nome_cliente or not ramo_atuacao or not intuito_plano:
            st.warning("Preencha todas as informações do cliente.")
        else:
            with st.spinner('Gerando fluxo de CRM...'):
                fluxo_output = ""
                for etapa in etapas:
                    fluxo_output += f"\n### {etapa}\n"
                    fluxo_output += gerar_fluxo_etapa(
                        nome_cliente,
                        ramo_atuacao,
                        objetivos_de_marca,
                        canais_disponiveis,
                        perfil_empresa,
                        metas_crm,
                        fluxo_output,  # fluxo_anterior
                        publico_alvo,
                        maturidade_crm,
                        tamanho_base,
                        tom_voz,
                        fluxos_ou_emails,
                        sla_entre_marketing_vendas,
                        etapa,
                        detalhamento_etapas[etapa]
                    )
                
                st.header('Plano de CRM')
                st.markdown(fluxo_output)
                save_to_mongo_CRM(fluxo_output, nome_cliente)