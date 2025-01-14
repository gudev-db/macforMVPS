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
        st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano')}")
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
        st.subheader('3.1 Plano para Redes Sociais')
        st.markdown(f"**Redes Sociais:** {selected_planejamento.get('Plano_Redes')}")

        st.subheader('3.2 Plano para Criativos')
        st.markdown(f"**Criativos:** {selected_planejamento.get('Plano_Criativos')}")
        
        st.subheader('3.3 Plano de SEO')
        st.markdown(f"**Relatório de Saúde de Site:** {selected_planejamento.get('Plano_Saude_Site')}")
        st.markdown(f"**Plano de Palavras Chave:** {selected_planejamento.get('Plano_Palavras_Chave')}")

   
        
        st.subheader('3.4 Plano de CRM')
        
        st.markdown(f"**1. Estratégia Geral de CRM:** {selected_planejamento.get('Plano_Estrategia_CRM')}")
        st.markdown(f"**2. Gestão de Contato com o Cliente - Email:** {selected_planejamento.get('Plano_Contato_Email')}")
        st.markdown(f"**3. Gestão de Contato com o Cliente - SMS/WhatsApp:** {selected_planejamento.get('Plano_Contato_SMS_WhatsApp')}")
        st.markdown(f"**4. Gestão de Contato com o Cliente - NPS:** {selected_planejamento.get('Plano_Contato_NPS')}")
        st.markdown(f"**5. Gestão de Análise de Dados de Clientes:** {selected_planejamento.get('Plano_Analise_Dados_CRM')}")
        st.markdown(f"**6. Automação de CRM:** {selected_planejamento.get('Plano_Automacao_CRM')}")


 
        
        st.subheader('3.5 Plano de Design/Marca')
        st.markdown(f"**Plano Design/Marca:** {selected_planejamento.get('Plano_Design')}")
        
        st.subheader('3.6 Estratégia de Conteúdo')
        st.markdown(f"**Estratégia de Conteúdo:** {selected_planejamento.get('Estrategia_Conteudo')}")

       
        
        
    else:
        st.write("Planejamento não encontrado.")




