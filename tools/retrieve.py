import os
import streamlit as st
from pymongo import MongoClient

def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")

    db = client['arquivos_planejamento']  # Substitua pelo nome do seu banco de dados
    collection = db['auto_doc']
    
    # Obter todos os IDs dos documentos (presumindo que 'id_planejamento' seja o identificador único)
    planejamentos = collection.find({}, {"_id": 1, "id_planejamento": 1})  # Buscar apenas _id e id_planejamento

    # Se não houver documentos encontrados
    if collection.count_documents({}) == 0:
        st.write("Não há planejamentos registrados.")
        return

    # Lista de 'id_planejamento' para o selectbox
    id_planejamentos = [planejamento['id_planejamento'] for planejamento in planejamentos]

    # Criar um selectbox para o usuário escolher um id_planejamento específico
    selected_id = st.selectbox("Selecione um planejamento:", id_planejamentos, key="id_planejamento")

    # Verificar se um id_planejamento foi selecionado
    if selected_id:
        # Buscar o planejamento completo com base no id_planejamento selecionado
        selected_planejamento = collection.find_one({"id_planejamento": selected_id})

        if selected_planejamento:
            # Exibindo o nome do cliente e o tipo de plano
            st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano')}")
            st.subheader(f"Cliente: {selected_planejamento.get('nome_cliente')}")
            
            # Exibindo as seções do planejamento com subheaders e os dados respectivos
            st.header('1. Etapa de Pesquisa de Mercado')
            st.subheader('1.1 Análise SWOT')
            st.markdown(f"**SWOT:** {selected_planejamento.get('SWOT')}")
            
            st.subheader('1.2 Análise PEST')
            st.markdown(f"**P:** {selected_planejamento.get('P')}")
            st.markdown(f"**E:** {selected_planejamento.get('E')}")
            st.markdown(f"**S:** {selected_planejamento.get('S')}")
            st.markdown(f"**T:** {selected_planejamento.get('T')}")
            
            st.subheader('1.3 Tendências de Mercado')
            st.markdown(f"**Tendências:** {selected_planejamento.get('Tendencias')}")
            
            st.header('2. Etapa Estratégica')
            st.subheader('2.1 Golden Circle')
            st.markdown(f"**GC:** {selected_planejamento.get('GC')}")
            
            st.subheader('2.2 Posicionamento de Marca')
            st.markdown(f"**Posicionamento de Marca:** {selected_planejamento.get('Posicionamento_Marca')}")
            
            st.subheader('2.3 Brand Persona')
            st.markdown(f"**Brand Persona:** {selected_planejamento.get('Brand_Persona')}")
            
            st.subheader('2.4 Buyer Persona')
            st.markdown(f"**Buyer Persona:** {selected_planejamento.get('Buyer_Persona')}")
            
            st.subheader('2.5 Tom de Voz')
            st.markdown(f"**Tom de Voz:** {selected_planejamento.get('Tom_Voz')}")
            
            st.header('3. Etapa de Planejamento de Mídias e Redes Sociais')
            st.subheader('3.1 Visual')
            st.markdown(f"**Estruturação do KV:** {selected_planejamento.get('KV')}")
            st.markdown(f"**Plano de Redes Sociais:** {selected_planejamento.get('Plano_Redes')}")
            
            st.subheader('3.2 Plano para Criativos')
            st.markdown(f"**Criativos:** {selected_planejamento.get('Plano_Criativos')}")
            
            st.subheader('3.3 Plano de SEO')
            st.markdown(f"**Plano de Palavras Chave:** {selected_planejamento.get('Plano_Palavras_Chave')}")
            
            st.subheader('3.4 Plano de CRM')
            st.markdown(f"**Estratégia Geral de CRM:** {selected_planejamento.get('Plano_Estrategia_CRM')}")
            st.markdown(f"**Fluxo Geral de CRM:** {selected_planejamento.get('Plano_Fluxo_CRM')}")
            st.markdown(f"**Gestão de Contato com o Cliente - Email:** {selected_planejamento.get('Plano_Contato_Email')}")
            st.markdown(f"**Gestão de Contato com o Cliente - SMS/WhatsApp:** {selected_planejamento.get('Plano_Contato_SMS_WhatsApp')}")
            st.markdown(f"**Gestão de Contato com o Cliente - NPS:** {selected_planejamento.get('Plano_Contato_NPS')}")
            st.markdown(f"**Softwares Recomendados:** {selected_planejamento.get('Recomend_Software')}")
        else:
            st.write("Planejamento não encontrado.")
