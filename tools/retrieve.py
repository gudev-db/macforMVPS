import os
import streamlit as st
from pymongo import MongoClient
from bson.json_util import dumps

def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")
    db = client['arquivos_planejamento']
    collection = db['auto_doc']

    # Buscar todos os documentos
    planejamentos = list(collection.find({})

    # Se não houver documentos encontrados
    if not planejamentos:
        st.write("Não há planejamentos registrados.")
        return []

    # Mostrar lista de documentos disponíveis
    st.subheader("Documentos disponíveis:")
    
    # Criar abas para cada documento
    tabs = st.tabs([f"Documento {idx+1}" for idx in range(len(planejamentos))])
    
    documentos_salvos = []
    
    for idx, (tab, doc) in enumerate(zip(tabs, planejamentos)):
        with tab:
            st.subheader(f"Conteúdo completo do documento {idx+1}")
            
            # Remover o campo _id para evitar problemas de serialização
            doc.pop('_id', None)
            
            # Mostrar o documento formatado
            st.json(doc)
            
            # Adicionar à lista de documentos salvos
            documentos_salvos.append({
                "id": idx+1,
                "conteudo": dumps(doc, indent=2)
            })
    
    return documentos_salvos
