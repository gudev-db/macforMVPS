__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from datetime import datetime
from crewai_tools import tool
import os
from tavily import TavilyClient
from pymongo import MongoClient
import google.generativeai as genai


# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")

gemini_api_key = os.getenv("GEM_API_KEY")


client = TavilyClient(api_key=t_api_key1)

genai.configure(api_key=gemini_api_key)
# call gemini model
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash',
                            verbose=True,
                            temperature=0.5,
                            goggle_api_key=api_key)   


client1 = TavilyClient(api_key='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')

# Connect to MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']  # Replace with your database name
collection = db['auto_doc'] #docs gerados

banco = client["arquivos_planejamento"]
db_clientes = banco["clientes"]  #info clientes

db_clientes = banco["temas"]  #temas de emails

import uuid

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())

def save_to_mongo_temas(tarefas_tema, nome_cliente):
    # Gerar o ID único para o planejamento
    id_planejamento = gerar_id_planejamento()
    
    # Prepare the document to be inserted into MongoDB
    task_outputs = {
        "id_planejamento":'Temas e Emails' +'_'+ nome_cliente + '_' + id_planejamento,  # Use o ID gerado como chave
        "nome_cliente": nome_cliente, 
        "temas": tarefas_tema[0].output.raw
     
    }

    # Insert the document into MongoDB
    collection.insert_one(task_outputs)
    st.success(f"Temas e emails gerados com sucesso e salvo no banco de dados com ID: {id_planejamento}!")






def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]





def gen_temas_emails():
    # Buscar todos os clientes do banco de dados

    st.subheader('Informações do remetente')
  
    
    # Selectbox para escolher o cliente
    nome_cliente = st.text_input('Digite o nome do remetente dos emails:')

    # Exibir os campos preenchidos com os dados do cliente
    ramo_atuacao = st.text_input('Ramo de Atuação:')
    referencia_da_marca = st.text_area(
        'Referência da Marca:', 
        height=200  
    )

    st.subheader('Informações do(s) destinatário(s)')
    destinatarios = st.text_input('Caracterize os destinatários:')


  
  
    
    pest_files = 1



  

    if pest_files is not None:
        # Se o relatório já foi gerado, exiba os resultados
        if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
            st.subheader("Relatório Gerado")
            for tarefa in st.session_state.resultados_tarefas:
                st.markdown(f"**Arquivo**: {tarefa['output_file']}")
                st.markdown(tarefa["output"])
            
            # Botão para limpar o estado
            if st.button("Gerar Temas e Emails"):
                limpar_estado()
                st.experimental_rerun()
        else:
            # Validação de entrada e geração de relatório
            if st.button('Iniciar Planejamento'):
                if not nome_cliente or not ramo_atuacao:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    with st.spinner('Gerando o planejamento...'):


                        agentes = [
                            Agent(
                                role="Gerador de conteúdo",
                                goal=f''' Gerar temas e emails partido de: {nome_cliente} para {destinatarios}.''',
                                backstory=f'''Você é um analista de mídias, detalhista, criativo, multicultural. Você regige temas e emails para nutrição de leads''',
                                allow_delegation=False,
                                llm=llm,
                                tools=[])
                           
                        ]

                    

                        # Criando tarefas correspondentes aos agentes
                        tarefas_tema = [
                                
                                Task(
                                    description="Temas e emails de nutrição de leads.",
                                    expected_output=f'''Desenvolva 10 temas (com emails redigidos associados) considerando cada um dos 
                                    segmentos detalhados nos destinatários: {destinatarios}. Os emails partem de {nome_cliente} que atua no ramo de {ramo_atuacao}.''',
                                    agent=agentes[0],
                                    output_file = 'tema_email.md'
                                )
                            ]


                     

                        # Processo do Crew
                        equipe_tema = Crew(
                            agents=agentes,
                            tasks=tarefas_tema,
                            process=Process.hierarchical,
                            manager_llm=llm,
                            language='português brasileiro'
                        )

                      

                        # Executa as tarefas do processo
                        resultado_tema = equipe_tema.kickoff()

                       
                        #Printando Tarefas

                        st.header('Temas e Emails')
                        st.markdown(tarefas_tema[0].output.raw)
                      
                    
                        save_to_mongo_temas(tarefas_tema, nome_cliente)




