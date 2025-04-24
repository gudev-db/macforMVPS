import os
import streamlit as st
from pymongo import MongoClient

def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")
    db = client['arquivos_planejamento']  # Substitua pelo nome do seu banco de dados
    collection = db['auto_doc']

    planejamentos = collection.find({}, {"_id": 1, "id_planejamento": 1})  # Buscar apenas _id e id_planejamento

    # Se não houver documentos encontrados
    if collection.count_documents({}) == 0:
        st.write("Não há planejamentos registrados.")
        return

    # Lista de 'id_planejamento' para o selectbox
    id_planejamentos = [planejamento['id_planejamento'] for planejamento in planejamentos]

    # Usar session_state para manter a seleção persistente
    if 'selected_id' not in st.session_state:
        st.session_state.selected_id = None

    # Criar um selectbox para o usuário escolher um id_planejamento específico
    selected_id = st.selectbox("Selecione um planejamento:", id_planejamentos, key="id_planejamento")

    # Atualizar a seleção armazenada na session_state
    st.session_state.selected_id = selected_id

    # Verificar se um id_planejamento foi selecionado
    if st.session_state.selected_id:
        # Buscar o planejamento completo com base no id_planejamento selecionado
        selected_planejamento = collection.find_one({"id_planejamento": st.session_state.selected_id})

        if selected_planejamento:
            # Exibindo o nome do cliente e o tipo de plano
            st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano', '')}")
            st.subheader(f"Cliente: {selected_planejamento.get('nome_cliente', '')}")

            # Exibindo as seções do planejamento com subheaders e os dados respectivos
            st.header('1. Etapa de Pesquisa de Mercado')
            
            # Verificar se a estrutura Etapa_1_Pesquisa_Mercado existe
            etapa1 = selected_planejamento.get('Etapa_1_Pesquisa_Mercado', {})
            
            st.subheader('1.1 Análise SWOT')
            st.markdown(f"**Análise SWOT:** {etapa1.get('Análise_SWOT', '')}")

            st.subheader('1.2 Análise PEST')
            st.markdown(f"**Análise PEST:** {etapa1.get('Análise_PEST', '')}")

            st.subheader('1.3 Análise de Concorrência')
            st.markdown(f"**Análise de Concorrência:** {etapa1.get('Análise_Concorrência', '')}")

            st.header('2. Etapa Estratégica')
            # Verificar se a estrutura Etapa_2_Estrategica existe
            etapa2 = selected_planejamento.get('Etapa_2_Estrategica', {})
            
            st.subheader('2.1 Golden Circle')
            st.markdown(f"**Golden Circle:** {etapa2.get('Golden_Circle', '')}")

            st.subheader('2.2 Posicionamento de Marca')
            st.markdown(f"**Posicionamento de Marca:** {etapa2.get('Posicionamento_Marca', '')}")

            st.subheader('2.3 Brand Persona')
            st.markdown(f"**Brand Persona:** {etapa2.get('Brand_Persona', '')}")

            st.subheader('2.4 Buyer Persona')
            st.markdown(f"**Buyer Persona:** {etapa2.get('Buyer_Persona', '')}")

            st.subheader('2.5 Tom de Voz')
            st.markdown(f"**Tom de Voz:** {etapa2.get('Tom_de_Voz', '')}")
            
        else:
            st.write("Planejamento não encontrado.")