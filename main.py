# Verifique se o login foi feito antes de exibir o conteúdo
if login():
    st.image('static/macLogo.png', width=300)
    st.text(
        "Empoderada por IA, a Macfor conta com um sistema gerador de documentos "
        "automatizado movido por agentes de inteligência artificial. Preencha os campos abaixo "
        "e gere documentos automáticos para otimizar o tempo de sua equipe. "
        "Foque o seu trabalho em seu diferencial humano e automatize tarefas repetitivas!"
    )

    # Sidebar para escolher entre "Plano Estratégico" ou "Brainstorming"
    selecao_sidebar = st.sidebar.radio(
        "Escolha a seção:",
        ["Plano Estratégico", "Brainstorming", "Documentos Salvos"],
        index=0  # Predefinir como 'Plano Estratégico' ativo
    )

    # Opções para "Plano Estratégico"
    if selecao_sidebar == "Plano Estratégico":
        st.sidebar.subheader("Planos Estratégicos")
        plano_estrategico = st.sidebar.selectbox(
            "Escolha o tipo de plano:",
            [
                "Selecione uma opção",
                "Plano Estratégico e de Pesquisa",
                "Plano Estratégico de Redes e Mídias",
                "Plano de CRM"
            ]
        )

        if plano_estrategico != "Selecione uma opção":
            if plano_estrategico == "Plano Estratégico e de Pesquisa":
                planej_mkt_page()
            elif plano_estrategico == "Plano Estratégico de Redes e Mídias":
                planej_midias_page()
            elif plano_estrategico == "Plano de CRM":
                planej_crm_page()

    # Opções para "Brainstorming"
    elif selecao_sidebar == "Brainstorming":
        st.sidebar.subheader("Brainstorming")
        brainstorming_option = st.sidebar.selectbox(
            "Escolha o tipo de brainstorming:",
            [
                "Selecione uma opção",
                "Brainstorming Conteúdo de Nutrição de Leads",
                "Brainstorming de Anúncios",
                "Brainstorming de Imagem"
            ]
        )

        if brainstorming_option != "Selecione uma opção":
            if brainstorming_option == "Brainstorming Conteúdo de Nutrição de Leads":
                gen_temas_emails()
            elif brainstorming_option == "Brainstorming de Anúncios":
                planej_campanhas()
            elif brainstorming_option == "Brainstorming de Imagem":
                gen_img()

    # Seção para "Documentos Salvos"
    elif selecao_sidebar == "Documentos Salvos":
        st.sidebar.subheader("Visualizar Documentos Salvos")

        # Obter a lista de documentos salvos
        documentos_salvos = visualizar_planejamentos()  # Deve retornar [{"id": 1, "conteudo": "Texto 1"}, ...]

        if documentos_salvos:
            # Criar um selectbox para selecionar o documento pelo ID
            doc_ids_salvos = [doc["id"] for doc in documentos_salvos]
            doc_selecionado_id_salvo = st.sidebar.selectbox(
                "Selecione o documento salvo pelo ID:",
                ["Selecione um ID"] + doc_ids_salvos,
                index=0
            )

            # Exibir o conteúdo do documento selecionado
            if doc_selecionado_id_salvo != "Selecione um ID":
                documento_selecionado_salvo = next(doc for doc in documentos_salvos if doc["id"] == doc_selecionado_id_salvo)
                st.markdown("## Documento Salvo Selecionado")
                st.text_area("Conteúdo do Documento", documento_selecionado_salvo["conteudo"], height=300)
        else:
            st.info("Nenhum documento salvo disponível no momento.")
