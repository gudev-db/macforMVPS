import os
import streamlit as st
from pymongo import MongoClient

def buscar_planejamento_por_id(id_planejamento):
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")

    db = client['arquivos_planejamento']  # Substitua pelo nome do seu banco de dados
    collection = db['auto_doc']
    
    # Buscar o planejamento pelo id_planejamento
    planejamento = collection.find_one({"id_planejamento": id_planejamento})

    return planejamento

def visualizar_planejamentos():
    # Campo de entrada para o usuário inserir o ID do planejamento
    id_planejamento_input = st.text_input("Digite o ID do planejamento para buscar:")
    
    if id_planejamento_input:
        planejamento = buscar_planejamento_por_id(id_planejamento_input)
        
        if planejamento:
            # Exibindo o nome do cliente e o tipo de plano
            st.header(f"Planejamento para: {planejamento.get('tipo_plano')}")
            st.subheader(f"Cliente: {planejamento.get('nome_cliente')}")
            
            # Exibindo as seções do planejamento com subheaders e os dados respectivos
            st.header('1. Etapa de Pesquisa de Mercado')
            st.subheader('1.1 Análise SWOT')
            st.markdown(f"**SWOT:** {planejamento.get('SWOT')}")
            
            st.subheader('1.2 Análise PEST')
            st.markdown(f"**P:** {planejamento.get('P')}")
            st.markdown(f"**E:** {planejamento.get('E')}")
            st.markdown(f"**S:** {planejamento.get('S')}")
            st.markdown(f"**T:** {planejamento.get('T')}")
            
            st.subheader('1.3 Tendências de Mercado')
            st.markdown(f"**Tendências:** {planejamento.get('Tendencias')}")
            
            st.header('2. Etapa Estratégica')
            st.subheader('2.1 Golden Circle')
            st.markdown(f"**GC:** {planejamento.get('GC')}")
            
            st.subheader('2.2 Posicionamento de Marca')
            st.markdown(f"**Posicionamento de Marca:** {planejamento.get('Posicionamento_Marca')}")
            
            st.subheader('2.3 Brand Persona')
            st.markdown(f"**Brand Persona:** {planejamento.get('Brand_Persona')}")
            
            st.subheader('2.4 Buyer Persona')
            st.markdown(f"**Buyer Persona:** {planejamento.get('Buyer_Persona')}")
            
            st.subheader('2.5 Tom de Voz')
            st.markdown(f"**Tom de Voz:** {planejamento.get('Tom_Voz')}")
            
            st.header('3. Etapa de Planejamento de Mídias e Redes Sociais')
            st.subheader('3.1 Visual')
            st.markdown(f"**Estruturação do KV:** {planejamento.get('KV')}")
            st.markdown(f"**Plano de Redes Sociais:** {planejamento.get('Plano_Redes')}")
            
            st.subheader('3.2 Plano para Criativos')
            st.markdown(f"**Criativos:** {planejamento.get('Plano_Criativos')}")
            
            st.subheader('3.3 Plano de SEO')
            st.markdown(f"**Plano de Palavras Chave:** {planejamento.get('Plano_Palavras_Chave')}")
            
            st.subheader('3.4 Plano de CRM')
            st.markdown(f"**Estratégia Geral de CRM:** {planejamento.get('Plano_Estrategia_CRM')}")
            st.markdown(f"**Fluxo Geral de CRM:** {planejamento.get('Plano_Fluxo_CRM')}")
            st.markdown(f"**Gestão de Contato com o Cliente - Email:** {planejamento.get('Plano_Contato_Email')}")
            st.markdown(f"**Gestão de Contato com o Cliente - SMS/WhatsApp:** {planejamento.get('Plano_Contato_SMS_WhatsApp')}")
            st.markdown(f"**Gestão de Contato com o Cliente - NPS:** {planejamento.get('Plano_Contato_NPS')}")
            st.markdown(f"**Softwares Recomendados:** {planejamento.get('Recomend_Software')}")
        else:
            st.write("Planejamento não encontrado.")
