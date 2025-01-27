import streamlit as st
from pymongo import MongoClient

def visualizar_planejamentos():
    # Conectar ao MongoDB
    client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/")
    db = client['arquivos_planejamento']  # Nome do seu banco de dados
    collection = db['auto_doc']
    
    # Obter todos os documentos e verificar se há documentos
    planejamentos = list(collection.find({}, {"_id": 1, "id_planejamento": 1}))  # Buscar apenas _id e id_planejamento

    # Se não houver documentos registrados
    if len(planejamentos) == 0:
        st.write("Não há planejamentos registrados.")
        client.close()
        return

    # Listar 'id_planejamento' para o selectbox
    id_planejamentos = [planejamento['id_planejamento'] for planejamento in planejamentos]

    # Criar o selectbox para o usuário escolher um id_planejamento
    selected_id = st.selectbox("Selecione um planejamento:", id_planejamentos)

    # Se um planejamento foi selecionado, fazer a consulta
    if selected_id:
        # Encontrar o planejamento selecionado
        selected_planejamento = collection.find_one({"id_planejamento": selected_id})

        if selected_planejamento:
            # Exibindo todos os dados do planejamento de forma dinâmica
            st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano', 'N/A')}")
            st.subheader(f"Cliente: {selected_planejamento.get('nome_cliente', 'N/A')}")

            # Exibindo todos os campos do planejamento, exceto o _id
            for key, value in selected_planejamento.items():
                if key != "_id":  # Ignorar o campo "_id"
                    st.subheader(f"{key.replace('_', ' ').title()}:")
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value if value else 'N/A'}")
        else:
            st.write("Planejamento não encontrado.")
    else:
        st.write("Selecione um planejamento para visualizar.")

    # Fechar a conexão com o MongoDB
    client.close()
