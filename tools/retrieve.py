import os
import streamlit as st
from pymongo import MongoClient


def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")

    db = client['arquivos_planejamento']  # Substitua pelo nome do seu banco de dados
    collection = db['auto_doc']
    
    # Obter o planejamento mais recente. Ordenar por _id em ordem decrescente.
    # O MongoDB usa o campo _id para criar documentos, e ele contém um timestamp, então o mais recente estará no topo
    planejamento_recente = collection.find_one({}, sort=[("_id", -1)])  # O -1 ordena em ordem decrescente

    # Se não houver documentos encontrados
    if not planejamento_recente:
        st.write("Não há planejamentos registrados.")
        return

    # Exibindo o nome do cliente e o tipo de plano
    st.header(f"Planejamento para: {planejamento_recente.get('tipo_plano')}")
    st.subheader(f"Cliente: {planejamento_recente.get('nome_cliente')}")
    
    # Exibindo as seções do planejamento com subheaders e os dados respectivos
    st.header('1. Etapa de Pesquisa de Mercado')
    st.subheader('1.1 Análise SWOT')
    st.markdown(f"**SWOT:** {planejamento_recente.get('SWOT')}")
    
    st.subheader('1.2 Análise PEST')
    st.markdown(f"**P:** {planejamento_recente.get('P')}")
    st.markdown(f"**E:** {planejamento_recente.get('E')}")
    st.markdown(f"**S:** {planejamento_recente.get('S')}")
    st.markdown(f"**T:** {planejamento_recente.get('T')}")
    
    st.subheader('1.3 Tendências de Mercado')
    st.markdown(f"**Tendências:** {planejamento_recente.get('Tendencias')}")
    
    st.header('2. Etapa Estratégica')
    st.subheader('2.1 Golden Circle')
    st.markdown(f"**GC:** {planejamento_recente.get('GC')}")
    
    st.subheader('2.2 Posicionamento de Marca')
    st.markdown(f"**Posicionamento de Marca:** {planejamento_recente.get('Posicionamento_Marca')}")
    
    st.subheader('2.3 Brand Persona')
    st.markdown(f"**Brand Persona:** {planejamento_recente.get('Brand_Persona')}")
    
    st.subheader('2.4 Buyer Persona')
    st.markdown(f"**Buyer Persona:** {planejamento_recente.get('Buyer_Persona')}")
    
    st.subheader('2.5 Tom de Voz')
    st.markdown(f"**Tom de Voz:** {planejamento_recente.get('Tom_Voz')}")
    
    st.header('3. Etapa de Planejamento de Mídias e Redes Sociais')

    st.subheader('3.1 Visual')
    st.markdown(f"**Estruturação do KV:** {planejamento_recente.get('KV')}")
    st.markdown(f"**Plano de Redes Sociais:** {planejamento_recente.get('Plano_Redes')}")
    
    st.subheader('3.2 Plano para Criativos')
    st.markdown(f"**Criativos:** {planejamento_recente.get('Plano_Criativos')}")
    
    st.subheader('3.3 Plano de SEO')
    st.markdown(f"**Plano de Palavras Chave:** {planejamento_recente.get('Plano_Palavras_Chave')}")

    st.subheader('3.4 Plano de CRM')
    st.markdown(f"**Estratégia Geral de CRM:** {planejamento_recente.get('Plano_Estrategia_CRM')}")
    st.markdown(f"**Fluxo Geral de CRM:** {planejamento_recente.get('Plano_Fluxo_CRM')}")
    st.markdown(f"**Gestão de Contato com o Cliente - Email:** {planejamento_recente.get('Plano_Contato_Email')}")
    st.markdown(f"**Gestão de Contato com o Cliente - SMS/WhatsApp:** {planejamento_recente.get('Plano_Contato_SMS_WhatsApp')}")
    st.markdown(f"**Gestão de Contato com o Cliente - NPS:** {planejamento_recente.get('Plano_Contato_NPS')}")
    st.markdown(f"**Softwares Recomendados:** {planejamento_recente.get('Recomend_Software')}")
