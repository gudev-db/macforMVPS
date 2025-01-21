import streamlit as st
import google.generativeai as genai
import uuid
import os
from pymongo import MongoClient

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini

# Conexão com MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']
collection = db['auto_doc']
banco = client["arquivos_planejamento"]
db_clientes = banco["clientes"]  # info clientes

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

# Função para salvar no MongoDB
def save_to_mongo_midias(kv_output, redes_output, criativos_output, palavras_chave_output, estrategia_conteudo_output, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepara o documento a ser inserido no MongoDB
    task_outputs = {
        "id_planejamento": 'Plano de Mídias' + '_' + nome_cliente + '_' + id_planejamento,
        "nome_cliente": nome_cliente,
        "tipo_plano": 'Plano de Mídias',
        "KV": kv_output,
        "Plano_Redes": redes_output,
        "Plano_Criativos": criativos_output,
        "Plano_Palavras_Chave": palavras_chave_output,
        "Estrategia_Conteudo": estrategia_conteudo_output,
    }

    # Insere o documento no MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Planejamento gerado com sucesso e salvo no banco de dados com ID: {id_planejamento}!")

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def planej_midias_page():
    st.subheader('Planejamento de Mídias e Redes')
    st.text('Aqui geramos plano para criativos, análise de saúde do site, sugestões de palavras chave, plano de CRM, plano de Design/Marca e estratégia de conteúdo.')

    # Buscar todos os clientes do banco de dados
    clientes = list(db_clientes.find({}, {"_id": 0, "nome": 1, "site": 1, "ramo": 1}))
    opcoes_clientes = [cliente["nome"] for cliente in clientes]

    # Selectbox para escolher o cliente
    nome_cliente = st.selectbox('Selecione o Cliente:', opcoes_clientes, key="nome_cliente")

    # Obter as informações do cliente selecionado
    cliente_info = next((cliente for cliente in clientes if cliente["nome"] == nome_cliente), None)
    site_cliente = cliente_info["site"] if cliente_info else ""
    ramo_atuacao = cliente_info["ramo"] if cliente_info else ""

    # Exibir os campos preenchidos com os dados do cliente
    st.text_input('Site do Cliente:', value=site_cliente, key="site_cliente")
    st.text_input('Ramo de Atuação:', value=ramo_atuacao, key="ramo_atuacao")
    intuito_plano = st.text_input('Intuito do Plano Estratégico:', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre")
    publico_alvo = st.text_input('Público-Alvo:', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda")
    concorrentes = st.text_input('Concorrentes:', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C")
    site_concorrentes = st.text_input('Site dos Concorrentes:', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br")

    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]

    objetivos_de_marca = st.selectbox('Selecione os objetivos de marca', objetivos_opcoes, key="objetivos_marca")
    referencia_da_marca = st.text_area('O que a marca faz, quais seus diferenciais, seus objetivos, quem é a marca?', key="referencias_marca", placeholder="Ex: A marca X oferece roupas sustentáveis com foco em conforto e estilo.", height=200)

    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)

    if pest_files is not None:
        if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
            st.subheader("Relatório Gerado")
            for tarefa in st.session_state.resultados_tarefas:
                st.markdown(f"**Arquivo**: {tarefa['output_file']}")
                st.markdown(tarefa["output"])
            
            # Botão para limpar o estado
            if st.button("Gerar Novo Relatório"):
                limpar_estado()
                st.experimental_rerun()
        else:
            if st.button('Iniciar Planejamento'):
                if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    with st.spinner('Gerando o planejamento de mídias...'):

                        # Geração dos conteúdos com o modelo Gemini

                        prompt_kv = f"""
                        Defina o Key Visual para a marca {nome_cliente}, levando em consideração os seguintes pontos:

                        - O ramo de atuação da empresa: {ramo_atuacao}.
                        - O intuito estratégico do plano de marketing: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        
                        O Key Visual deve ser a representação visual central para campanhas de marketing, refletindo a identidade da marca e ressoando com o público-alvo. Ele deve ser aplicável em diferentes materiais de comunicação, como anúncios, redes sociais, e embalagens.
                        
                        A definição do Key Visual deve ser detalhada da seguinte forma:
                        
                        1. **Imagem Conceito:** Defina a imagem que encapsula os valores e o propósito da marca. Justifique a escolha com base em elementos visuais comumente utilizados no ramo de atuação {ramo_atuacao} e como isso se conecta ao público-alvo {publico_alvo}. Explique por que essa imagem foi escolhida, incluindo referências culturais, psicológicas e comportamentais.
                        
                        2. **Tipografia:** Escolha uma fonte tipográfica que complemente a imagem conceito. Detalhe a escolha e a forma como a tipografia reflete a identidade da marca, levando em conta a legibilidade e a conexão emocional com o público. Explique as escolhas de estilo, espessura e espaçamento.
                        
                        3. **Cores:** Selecione uma paleta de cores específica para o Key Visual. Justifique as escolhas com base em psicologia das cores e tendências do mercado no ramo de atuação {ramo_atuacao}. Detalhe como essas cores evocam emoções e criam uma identidade visual forte e coesa.
                        
                        4. **Elementos Gráficos:** Defina quais elementos gráficos, como formas, ícones ou texturas, são fundamentais para compor o Key Visual. Justifique a escolha desses elementos em relação à consistência da identidade visual e à relevância para o público-alvo.

                        """
                        kv_output = modelo_linguagem.generate_content(prompt_kv).text
                        # Adicionando uma verificação
                        if not kv_output:
                            st.error("Erro ao gerar o Key Visual. Tente novamente.")
                            return

                        prompt_redes = f"""
                        Crie uma estratégia de redes sociais detalhada para {nome_cliente}, com base nas seguintes informações:

                        - O ramo de atuação: {ramo_atuacao}.
                        - O intuito estratégico do plano: {intuito_plano}.
                        - O público-alvo: {publico_alvo}.
                        - A referência da marca: {referencia_da_marca}.
                        """
                        redes_output = modelo_linguagem.generate_content(prompt_redes).text
                        if not redes_output:
                            st.error("Erro ao gerar a estratégia de redes sociais. Tente novamente.")
                            return

                        # Repita esse processo para os outros prompts:
                        criativos_output = modelo_linguagem.generate_content(prompt_criativos).text
                        palavras_chave_output = modelo_linguagem.generate_content(prompt_palavras_chave).text
                        estrategia_conteudo_output = modelo_linguagem.generate_content(prompt_estrategia_conteudo).text

                        # Verificação adicional para garantir que os outputs não estão vazios
                        if not criativos_output or not palavras_chave_output or not estrategia_conteudo_output:
                            st.error("Erro ao gerar parte do planejamento. Tente novamente.")
                            return

                        # Exibe os resultados na interface
                        st.header('Plano de Redes Sociais e Mídias')
                        st.subheader('1. Plano de Key Visual')
                        st.markdown(kv_output)
                        st.subheader('2. Plano para Redes')
                        st.markdown(redes_output)
                        st.subheader('3. Plano para Criativos')
                        st.markdown(criativos_output)
                        st.subheader('4. SEO')
                        st.markdown(palavras_chave_output)
                        st.subheader('5. Estratégia de Conteúdo')
                        st.markdown(estrategia_conteudo_output)

                        # Salva o planejamento no MongoDB
                        save_to_mongo_midias(kv_output, redes_output, criativos_output, palavras_chave_output, estrategia_conteudo_output, nome_cliente)
