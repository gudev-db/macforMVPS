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

def gerar_fluxo_etapa(nome_cliente, ramo_atuacao, referencia_da_marca, objetivo_crm, canais_disponiveis, perfil_empresa, metas_crm, fluxo_anterior,publico_alvo,tamanho_base,tom_voz,fluxos_ou_emails, etapa, nivel_detalhamento):
    prompt = f"""
    Em português brasileiro, crie um plano detalhado para a etapa '{etapa}' do fluxo de CRM.
    
    - Nome do Cliente: {nome_cliente}
    - Ramo de Atuação: {ramo_atuacao}
    - Referência de marca: {referencia_da_marca}
    - Objetivo do CRM: {objetivo_crm}
    - Ferramentas de comunicação disponíveis: {canais_disponiveis}
    - Perfil da empresa: {perfil_empresa}
    - Metas do CRM: {metas_crm}
    - Fluxo até aqui: {fluxo_anterior}
    - Público alvo: {publico_alvo}
    - Tamanho da base de clientes existente: {tamanho_base}
    - Tom de voz desejado: {tom_voz}
    - Fluxo desejado: {fluxos_ou_emails}

    
    Desenvolva ações personalizadas para essa etapa considerando as características da empresa. Inclua:
    - Elaborar o fluxo de automação de marketing com cada passo necessário detalhado.
    - Principais ações necessárias.
    - Sugestão de ferramenta complementar
    """
    output = modelo_linguagem.generate_content(prompt).text
    for _ in range(nivel_detalhamento - 1):
        prompt_aprofundamento = f'''Aprofunde mais cada detalhe descrito nessa etapa de uma forma que ela se torne mais prática. Torne esse conteúdo mais
         estratégico. Me dê estratégia de conteúdo. Me diga que tipo de conteúdo (com exemplos) cada etapa deve ter. Nos dê conteúdos
        práticos do que devemos utilizar e como e quando devemos utilizá-los dentro do plano. Você está aqui
        para construir a estratégia que minha empresa deve seguir. Você é o especialista. AJuste a estratégia aos objetivos do cliente. 
        Veja cada um dos pontos e aprofunde mais, e mais, e mais,
        detalhe mais, e mais, e mais. Saia do macro e vá para o micro. Detalhe cada ação. Faça um plano de conteúdo para essa etapa. Detalhe e explique o que deve ser feito com uma estratégia de conteúdo a nível de cronograma.'''
        output += "\n" + modelo_linguagem.generate_content(prompt_aprofundamento).text
    return output

def planej_crm_page():
# CRM

    st.subheader('Planejamento de Inbound Marketing')

    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Esse nome será usado para vincular todos os dados relacionados ao planejamento.")
    cliente_info = next((c for c in clientes if c["nome"] == nome_cliente), None)

    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""
    publico_alvo = st.text_input('Público-Alvo:', help="Descreva o perfil do público que o Inbound Marketing visa atingir. Seja específico quanto a segmentos e comportamentos de clientes.")
    # Objetivos de Marca
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]
    objetivos_de_marca = st.selectbox('Selecione os objetivos de marca:', objetivos_opcoes, help="Escolha o objetivo central que o Inbound Marketing ajudará a alcançar. Por exemplo, aumentar a fidelização ou melhorar a qualificação de leads.")
    referencia_da_marca = st.text_area('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', help="Escreva sobre a essência da marca, seus valores e o que a distingue da concorrência. Isso ajudará a personalizar a estratégia de CRM.")

    # Ferramentas e Processos de CRM

    canais_disponiveis = st.text_input('Quais ferramentas de comunicação estão disponíveis?', help="Liste as ferramentas de comunicação que a empresa utiliza para interagir com seus clientes, como e-mail, telefone, redes sociais, etc.")
    perfil_empresa = st.selectbox('Qual é o perfil da empresa?', ['B2B', 'B2C'], help="Escolha o tipo de relacionamento da empresa com seus clientes: B2B (empresa para empresa) ou B2C (empresa para consumidor).")
    metas_crm = st.text_input('Quais metas a serem alcançadas com o Inbound Marketing?', help="Descreva as metas específicas que você deseja alcançar com a implementação do CRM. Ex: aumentar taxa de conversão de leads em 20%.")
    tamanho_base = st.selectbox('Qual o tamanho da base de dados de clientes?', ['1-100', '100-1000', '1000-'], help="Defina o tamanho da base de dados de clientes. Isso ajudará a escolher as estratégias mais adequadas.")
    tom_voz = st.text_area('Qual o tom de voz desejado para a comunicação?', help="Defina como deve ser a comunicação da marca com seus clientes. Ex: formal, amigável, inspirador.")
    fluxos_ou_emails = st.text_area('Quais fluxos e/ou e-mails deseja trabalhar?', help="Descreva os fluxos de comunicação ou campanhas de e-mail que serão utilizados no CRM, como nutrição de leads ou campanhas de fidelização.")

    
    detalhamento_etapas = {}
    etapas = [
        "Aquisição de Leads", "Qualificação de Leads", "Nutrição de Leads", "Conversão e Fechamento", "Onboarding de Clientes",
        "Atendimento e Suporte", "Fidelização e Retenção", "Expansão e Upsell", "Reativação de Clientes Inativos"
    ]
    for etapa in etapas:
        detalhamento_etapas[etapa] = st.slider(f'Nível de detalhamento para {etapa}', 1, 3, 3)
    
    if st.button('Gerar Planejamento'):
        
        
            with st.spinner('Gerando fluxo de CRM...'):
                fluxo_output = ""
                for etapa in etapas:
                    fluxo_output += f"\n### {etapa}\n"
                    fluxo_output += gerar_fluxo_etapa(
                        nome_cliente,
                        ramo_atuacao,
                        referencia_da_marca,
                        objetivos_de_marca,
                        canais_disponiveis,
                        perfil_empresa,
                        metas_crm,
                        fluxo_output,  # fluxo_anterior
                        publico_alvo,
                        tamanho_base,
                        tom_voz,
                        fluxos_ou_emails,
                        etapa,
                        detalhamento_etapas[etapa]
                    )
                
                st.header('Plano de Inbound Marketing')
                st.markdown(fluxo_output)
                save_to_mongo_CRM(fluxo_output, nome_cliente)