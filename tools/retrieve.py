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

    # Mostrar o ID selecionado (apenas para depuração)
    st.write(f"Você selecionou o id: {selected_id}")

    # Encontrar o planejamento selecionado
    selected_planejamento = collection.find_one({"id_planejamento": selected_id})

    # Verificar se o planejamento foi encontrado
    if selected_planejamento:
        # Exibindo todos os campos do planejamento
        st.header(f"Planejamento para: {selected_planejamento.get('tipo_plano', 'N/A')}")
        st.subheader(f"Cliente: {selected_planejamento.get('nome_cliente', 'N/A')}")

        # Exibir todos os campos encontrados no documento
        for key, value in selected_planejamento.items():
            if key != "_id":  # Ignorar o campo "_id"
                st.subheader(f"{key.replace('_', ' ').title()}:")
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value if value else 'N/A'}")
    else:
        st.write("Planejamento não encontrado.")
