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
        st.subheader(f"Planejamento para: {selected_planejamento.get('nome_cliente')}")
        
        # Exibindo as seções do planejamento com subheaders e os dados respectivos
        st.header('1. Etapa de Pesquisa de Mercado')
        st.subheader('1.1 Análise SWOT')
        st.markdown(f"**SWOT:** {selected_planejamento.get('SWOT')}")
        
        st.subheader('1.2 Análise PEST')
        st.markdown(f"**PEST:** {selected_planejamento.get('PEST')}")
        
        st.header('2. Etapa de Estratégica')
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
        
        st.header('3. Etapa de Planejamento de Mídias')
        st.subheader('3.1 Plano para Criativos')
        st.markdown(f"**Criativos:** {selected_planejamento.get('Plano_Criativos')}")
        
        st.subheader('3.2 Plano de SEO')
        st.markdown(f"**Plano SEO:** {selected_planejamento.get('Plano_SEO')}")
        
        st.subheader('3.3 Plano de CRM')
        st.markdown(f"**Plano CRM:** {selected_planejamento.get('Plano_CRM')}")
        
        st.subheader('3.4 Plano de Design/Marca')
        st.markdown(f"**Plano Design/Marca:** {selected_planejamento.get('Plano_Design')}")
        
        st.subheader('3.5 Estratégia de Conteúdo')
        st.markdown(f"**Estratégia de Conteúdo:** {selected_planejamento.get('Estrategia_Conteudo')}")

       
        
        
    else:
        st.write("Planejamento não encontrado.")




