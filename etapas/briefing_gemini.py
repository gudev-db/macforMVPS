import streamlit as st
import google.generativeai as genai
import uuid
import os
from pymongo import MongoClient
from datetime import datetime
import os
from tavily import TavilyClient
from pymongo import MongoClient
import requests


# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini


# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def briefing():
    st.subheader('Contexto')
    st.text('''Aqui contextualizamos o momento do cliente e o escopo de atuação da Macfor.''')
    

    #Contexto
    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")

    projeto_peca = st.text_input('Qual é o projeto ou peça?:', help="Apresente aqui, resumidamente, o serviço pelo qual o cliente contratou a Macfor para realizar.")

    cenario = st.text_input('Qual o cenário em que o cliente se encontra nesse momento?', help = "Apresentar todo o contexto da solicitação, seu histórico, o cenário a que se encontra que justifique e defenda o projeto.")

    objetivos = st.text_input('Quais são os objetivos do cliente ao contratar a Macfor?', help = "O que queremos alcançar, direta e indiretamente, tangível e intangível. Seja o projeto na totalidade, seja somente sob responsabilidades Macfor.")

    publico = st.text_input('Qual é o nosso público-alvo?', help = "Com quem devemos falar? Qual será nossa segmentação? Temos mailing?")

    periodo = st.text_input('Qual será o nosso período de atuação?', help = "Quando o projeto acontece? Qual período? Quando devemos começar a trabalhar? Quando será a entrega ou publicação do material?")

    verba = st.text_input('Qual será a verba disponível para a Macfor utilizar em sua atuação?', help = "Considerar valor total, que consiste em custos de produção, mídia e ergometria.")

    st.subheader('Criação')
    st.text('''Aqui criamos o documento que guia o processo criativo da Macfor.''')

    oque = st.text_input('O que vamos fazer?', help = "Detalhar quais peças vamos criar, tudo que deve contemplar em nosso plano, segundo expectativas da cliente + sugestão Macfor.")

    KV = st.text_input('Seguir orientação de KV? Qual deverá ser usado?', help = "Validar com o cliente o KV que devemos trabalhar a partir dos materiais da MAKE ou se vamos seguir com alguma referência fora do KV. Caso não tenha um KV, devemos seguir com fotografias, ilustrações? Qual a expectativa visual para essa peça?")

    mensagem = st.text_input('O que vamos dizer na comunicação?', help = "Alinhar as principais mensagens que devemos passar em nossas peças para o público em questão.")

    restricoes = st.text_input('Existe alguma referência, restrição, obrigatoriedade sobre uso de imagens, palavras e termos?', help = "Apresentar qualquer orientação que deve ser seguida.")

    redes = st.text_input('Quais redes sociais deverão ser usadas?', help = "Neste a definição virá em nosso Plano, mas o cliente pode ter algum desejo, recomendação, sugestão. Incluir peças e formatos após aprovação de volumetria. Incluir link da volumetria no Drive.")

    obs = st.text_input('Observações e comentários', help = "Use esse espaço para detalhar ou complementar alguma informação que você considere importante para o desenvolvimento do projeto.")
  

    pest_files = 1



  
    if pest_files is not None:
        if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
            st.subheader("Briefing")
            for tarefa in st.session_state.resultados_tarefas:
                st.markdown(f"**Arquivo**: {tarefa['output_file']}")
                st.markdown(tarefa["output"])
            
            # Botão para limpar o estado
            if st.button("Gerar Briefing"):
                limpar_estado()
                st.experimental_rerun()
        else:
            if st.button('Iniciar Planejamento'):
                if not nome_cliente:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    with st.spinner('Gerando o planejamento...'):





                            



                        prompt_context = f'''Você é um gerente de projetos altamente qualificado com escrita impecável.
                        
                        A empresa de Marketing Digital Macfor foi contratada pelo cliente {nome_cliente}.
                        
                        1. Qual é o projeto ou peça?: {projeto_peca}.

                        2. Qual o cenário em que o cliente se encontra nesse momento?: {cenario}

                        3. Quais são os objetivos do cliente ao contratar a Macfor?: {objetivos}

                        4. Público alvo: {publico}

                        5. Período: {periodo}

                        6. Verba: {verba}

                        Redija um documento de Briefing onde cada etapa possui 2 parágrafos formalmente redigidos de uma forma que o documento possa ser usado como referência para
                        guiar as ações da Macfor ao longo do projeto.
                        
                        
                        '''
                        context_output = modelo_linguagem.generate_content(prompt_context).text


                        prompt_criacao = f'''Você é um gerente de projetos altamente qualificado com escrita impecável.

                        Aqui criamos o documento que guia o processo criativo da Macfor.
                        
                        A empresa de Marketing Digital Macfor foi contratada pelo cliente {nome_cliente}.
                        
                        1. O que vamos fazer?: {oque}.

                        2. Seguir orientação de KV? Qual deverá ser usado?: {KV}

                        3. O que vamos dizer na comunicação?: {mensagem}

                        4. Existe alguma referência, restrição, obrigatoriedade sobre uso de imagens, palavras e termos?: {restricoes}

                        5. Quais redes sociais deverão ser usadas?: {redes}

                        6. Observações e comentários: {obs}


                        Redija um documento de Briefing criativo onde cada etapa possui 2 parágrafos formalmente redigidos de uma forma que o documento possa ser usado como referência para
                        guiar as ações da Macfor ao longo do projeto.
                        
                        
                        '''
                        criacaot_output = modelo_linguagem.generate_content(prompt_criacao).text





                        #Printando Tarefas

                        st.header('1. Etapa Contextual')
                        st.markdown(context_output)

                        
                

                        st.header('2. Etapa Criativa')
                        st.markdown(criacaot_output)

                       
