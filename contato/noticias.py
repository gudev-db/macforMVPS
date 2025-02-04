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

# Configuração do ambiente da API
api_key = os.getenv("OPENAI_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")



# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini
client1 = TavilyClient(api_key='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')


# Conexão com MongoDB
client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
db = client['arquivos_planejamento']
collection = db['auto_doc']
banco = client["arquivos_planejamento"]
db_clientes = banco["clientes"]  # info clientes

# Função para gerar um ID único para o planejamento
def gerar_id_planejamento():
    return str(uuid.uuid4())


# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def pesquisa():
    st.subheader('Pesquisa de tendências')

    


 
    
    # Intuito do Plano Estratégico
    assunto_interesse = st.text_input('Digite aqui o seu assunto de i")
    
    
   


  
    if 1==1:
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
                if 1==1:
                    with st.spinner('Gerando o planejamento de mídias...'):


                            #DUCK DUCK GO SEARCH de tendências

                        url = "https://duckduckgo8.p.rapidapi.com/"
                            
                        querystring = {"q":f"tendencias em {assunto_interesse}"}
                            
                        headers = {
                                "x-rapidapi-key": rapid_key,
                                "x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
                            }
                            
                        response = requests.get(url, headers=headers, params=querystring)
                            
                        tend_novids2 = response.text


                       

                            #TAVILY PEST
                            
                        politic = client1.search(
                                f'''Como está a situação política no brasil atualmente em um contexto geral e de forma detalhada para planejamento 
                                estratégico de marketing digital no contexto do ramo de atuação: {assunto_interesse}?''',
                                days=90, 
                                max_results=20
                            )
                            
                      
                        # Aqui vamos gerar as respostas usando o modelo Gemini

                        prompt_SWOT = f'''Dado os retornos da pesquisa de tendências em {tend_novids2}, faça um relatório completo do que foi recebido listando os links de referência.'''
                        SWOT_output = modelo_linguagem.generate_content(prompt_SWOT).text

                        prompt_SWOT2 = f'''Dado os retornos da pesquisa de tendências em {politic}, faça um relatório completo do que foi recebido listando os links de referência.'''
                        SWOT_output2 = modelo_linguagem.generate_content(prompt_SWOT2).text

                        

                        st.header('1. Pesquisa de tendências')
                        st.subheader('1.1 Análise de tendências')
                        st.markdown(SWOT_output)
                        st.subheader('1.2 Análise de tendências 2')
                        st.markdown(SWOT_output2)
                       

                        


