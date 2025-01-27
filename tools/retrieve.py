import os
import streamlit as st
from pymongo import MongoClient


import streamlit as st
from pymongo import MongoClient

def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")
    db = client['arquivos_planejamento']  # Nome do seu banco de dados
    collection = db['auto_doc']

    # Teste de conexão
    try:
        client.admin.command('ping')
        st.write("Conexão bem-sucedida com o MongoDB!")
    except Exception as e:
        st.write("Erro ao conectar ao MongoDB:", e)
        return
    
    # Obter todos os documentos e verificar se há documentos
    planejamentos = collection.find({}, {"_id": 1, "id_planejamento": 1})  # Buscar apenas _id e id_planejamento

    # Verificar se a coleção tem documentos
    if collection.count_documents({}) == 0:
        st.write("Não há planejamentos registrados.")
        return

    # Listar 'id_planejamento' para o selectbox
    id_planejamentos = [planejamento.get('id_planejamento', 'N/A') for planejamento in planejamentos]

    # Verificar se a lista de id_planejamentos não está vazia
    if not id_planejamentos:
        st.write("Não há 'id_planejamento' disponíveis para seleção.")
        return

    # Criar o selectbox para o usuário escolher o id_planejamento
    selected_id = st.selectbox("Selecione um planejamento:", id_planejamentos)

    # Encontrar o planejamento selecionado
    selected_planejamento = collection.find_one({"id_planejamento": selected_id})

    if selected_planejamento:
        # Exibindo o nome do cliente
        st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano', 'N/A')}")
        st.subheader(f"Cliente: {selected_planejamento.get('nome_cliente', 'N/A')}")

        # Etapa de Pesquisa de Mercado
        if 'SWOT' in selected_planejamento:
            st.header('1. Etapa de Pesquisa de Mercado')
            st.subheader('1.1 Análise SWOT')
            st.markdown(f"**SWOT:** {selected_planejamento.get('SWOT', 'N/A')}")

        if 'P' in selected_planejamento or 'E' in selected_planejamento or 'S' in selected_planejamento or 'T' in selected_planejamento:
            st.subheader('1.2 Análise PEST')
            st.subheader('Política')
            st.markdown(f"**PEST (Política):** {selected_planejamento.get('P', 'N/A')}")
            st.subheader('Econômica')
            st.markdown(f"**PEST (Econômica):** {selected_planejamento.get('E', 'N/A')}")
            st.subheader('Social')
            st.markdown(f"**PEST (Social):** {selected_planejamento.get('S', 'N/A')}")
            st.subheader('Tecnológica')
            st.markdown(f"**PEST (Tecnológica):** {selected_planejamento.get('T', 'N/A')}")

        if 'Tendencias' in selected_planejamento:
            st.subheader('1.3 Tendências de Mercado')
            st.markdown(f"**Tendências:** {selected_planejamento.get('Tendencias', 'N/A')}")

        # Etapa Estratégica
        if 'GC' in selected_planejamento or 'Posicionamento_Marca' in selected_planejamento or 'Brand_Persona' in selected_planejamento or 'Buyer_Persona' in selected_planejamento or 'Tom_Voz' in selected_planejamento:
            st.header('2. Etapa de Estratégia')

            if 'GC' in selected_planejamento:
                st.subheader('2.1 Golden Circle')
                st.markdown(f"**GC:** {selected_planejamento.get('GC', 'N/A')}")

            if 'Posicionamento_Marca' in selected_planejamento:
                st.subheader('2.2 Posicionamento de Marca')
                st.markdown(f"**Posicionamento de Marca:** {selected_planejamento.get('Posicionamento_Marca', 'N/A')}")

            if 'Brand_Persona' in selected_planejamento:
                st.subheader('2.3 Brand Persona')
                st.markdown(f"**Brand Persona:** {selected_planejamento.get('Brand_Persona', 'N/A')}")

            if 'Buyer_Persona' in selected_planejamento:
                st.subheader('2.4 Buyer Persona')
                st.markdown(f"**Buyer Persona:** {selected_planejamento.get('Buyer_Persona', 'N/A')}")

            if 'Tom_Voz' in selected_planejamento:
                st.subheader('2.5 Tom de Voz')
                st.markdown(f"**Tom de Voz:** {selected_planejamento.get('Tom_Voz', 'N/A')}")

        # Etapa de Planejamento de Mídias e Redes Sociais
        if 'KV' in selected_planejamento or 'Plano_Redes' in selected_planejamento or 'Plano_Criativos' in selected_planejamento or 'Plano_Palavras_Chave' in selected_planejamento:
            st.header('3. Etapa de Planejamento de Mídias e Redes Sociais')

            if 'KV' in selected_planejamento:
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
