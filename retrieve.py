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
        # Display the selected planejamento
        st.subheader(f"Planejamento para: {selected_planejamento.get('cliente')}")
        
        
        # Exibindo as informações dos campos de planejamento (como SWOT, GC, etc.)
        st.markdown(f"**SWOT:** {selected_planejamento.get('SWOT')}")
        st.markdown(f"**GC:** {selected_planejamento.get('GC')}")
        st.markdown(f"**Posicionamento de Marca:** {selected_planejamento.get('Posicionamento_Marca')}")
        st.markdown(f"**Brand Persona:** {selected_planejamento.get('Brand_Persona')}")
        st.markdown(f"**Buyer Persona:** {selected_planejamento.get('Buyer_Persona')}")
        st.markdown(f"**Tom de Voz:** {selected_planejamento.get('Tom_Voz')}")
        st.markdown(f"**PEST:** {selected_planejamento.get('PEST')}")
        st.markdown(f"**Revisão:** {selected_planejamento.get('Revisao')}")
        st.markdown(f"**Estratégia de Conteúdo:** {selected_planejamento.get('Estrategia_Conteudo')}")
        st.markdown(f"**Plano SEO:** {selected_planejamento.get('Plano_SEO')}")
    else:
        st.write("Planejamento não encontrado.")




