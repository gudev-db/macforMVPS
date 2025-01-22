import os
import streamlit as st
from pymongo import MongoClient


def visualizar_planejamentos():
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")

    db = client['arquivos_planejamento']  # Replace with your database name
    collection = db['auto_doc']
    
    # Get all the documents' IDs (assuming 'id_planejamento' is the unique identifier)
    planejamentos = collection.find({}, {"_id": 1, "id_planejamento": 1})  # Fetch only _id and id_planejamento

    # If no documents are found
    if collection.count_documents({}) == 0:
        st.write("Não há planejamentos registrados.")
        return

    # List of 'id_planejamento' for the selectbox
    id_planejamentos = [planejamento['id_planejamento'] for planejamento in planejamentos]

    # Create a selectbox for the user to choose a specific id_planejamento
    selected_id = st.selectbox("Selecione um planejamento:", id_planejamentos)

    # Find the selected planning document by 'id_planejamento'
    selected_planejamento = collection.find_one({"id_planejamento": selected_id})

    if selected_planejamento:
    # Exibindo o nome do cliente
    st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano', 'N/A')}")
    st.subheader(f"Planejamento para: {selected_planejamento.get('nome_cliente', 'N/A')}")
    
    # Etapa de Pesquisa de Mercado
    if 'Etapa_1_Pesquisa_Mercado' in selected_planejamento:
        st.header('1. Etapa de Pesquisa de Mercado')
        
        if 'Análise_SWOT' in selected_planejamento['Etapa_1_Pesquisa_Mercado']:
            st.subheader('1.1 Análise SWOT')
            st.markdown(f"**SWOT:** {selected_planejamento['Etapa_1_Pesquisa_Mercado'].get('Análise_SWOT', 'N/A')}")
        
        if 'Análise_PEST' in selected_planejamento['Etapa_1_Pesquisa_Mercado']:
            st.subheader('1.2 Análise PEST')
            st.markdown(f"**PEST:** {selected_planejamento['Etapa_1_Pesquisa_Mercado'].get('Análise_PEST', 'N/A')}")
        
        if 'Análise_Tendências' in selected_planejamento['Etapa_1_Pesquisa_Mercado']:
            st.subheader('1.3 Análise de Tendências')
            st.markdown(f"**Tendências:** {selected_planejamento['Etapa_1_Pesquisa_Mercado'].get('Análise_Tendências', 'N/A')}")
    
    # Etapa Estratégica
    if 'Etapa_2_Estrategica' in selected_planejamento:
        st.header('2. Etapa de Estratégia')
        
        if 'Golden_Circle' in selected_planejamento['Etapa_2_Estrategica']:
            st.subheader('2.1 Golden Circle')
            st.markdown(f"**GC:** {selected_planejamento['Etapa_2_Estrategica'].get('Golden_Circle', 'N/A')}")
        
        if 'Posicionamento_Marca' in selected_planejamento['Etapa_2_Estrategica']:
            st.subheader('2.2 Posicionamento de Marca')
            st.markdown(f"**Posicionamento de Marca:** {selected_planejamento['Etapa_2_Estrategica'].get('Posicionamento_Marca', 'N/A')}")
        
        if 'Brand_Persona' in selected_planejamento['Etapa_2_Estrategica']:
            st.subheader('2.3 Brand Persona')
            st.markdown(f"**Brand Persona:** {selected_planejamento['Etapa_2_Estrategica'].get('Brand_Persona', 'N/A')}")
        
        if 'Buyer_Persona' in selected_planejamento['Etapa_2_Estrategica']:
            st.subheader('2.4 Buyer Persona')
            st.markdown(f"**Buyer Persona:** {selected_planejamento['Etapa_2_Estrategica'].get('Buyer_Persona', 'N/A')}")
        
        if 'Tom_de_Voz' in selected_planejamento['Etapa_2_Estrategica']:
            st.subheader('2.5 Tom de Voz')
            st.markdown(f"**Tom de Voz:** {selected_planejamento['Etapa_2_Estrategica'].get('Tom_de_Voz', 'N/A')}")
    
    # Etapa de Planejamento de Mídias e Redes Sociais
    if 'KV' in selected_planejamento:
        st.header('3. Etapa de Planejamento de Mídias e Redes Sociais')
        
        st.subheader('3.1 Visual')
        st.markdown(f"**Estruturação do KV:** {selected_planejamento.get('KV', 'N/A')}")
        
        if 'Plano_Redes' in selected_planejamento:
            st.markdown(f"**Redes Sociais:** {selected_planejamento.get('Plano_Redes', 'N/A')}")
        
        if 'Plano_Criativos' in selected_planejamento:
            st.subheader('3.2 Plano para Criativos')
            st.markdown(f"**Criativos:** {selected_planejamento.get('Plano_Criativos', 'N/A')}")
        
        if 'Plano_Palavras_Chave' in selected_planejamento:
            st.subheader('3.3 Plano de SEO')
            st.markdown(f"**Plano de Palavras Chave:** {selected_planejamento.get('Plano_Palavras_Chave', 'N/A')}")
    
    # Etapa de CRM
    if 'Plano_Estrategia_CRM' in selected_planejamento:
        st.subheader('3.4 Plano de CRM')
        st.markdown(f"**Estratégia Geral de CRM:** {selected_planejamento.get('Plano_Estrategia_CRM', 'N/A')}")
        
        if 'Fluxo' in selected_planejamento:
            st.markdown(f"**Fluxo Geral de CRM:** {selected_planejamento.get('Fluxo', 'N/A')}")
        
        if 'Indicadores' in selected_planejamento:
            st.markdown(f"**Gestão de Contato com o Cliente - Email:** {selected_planejamento.get('Indicadores', 'N/A')}")

        


 

       
        
        
    else:
        st.write("Planejamento não encontrado.")




