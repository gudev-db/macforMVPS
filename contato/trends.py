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
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()

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






# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def gtrends():
    st.subheader('Pesquisa de tendências')

    


 
    
    # Intuito do Plano Estratégico
    assunto_interesse = st.text_input('Assunto de interesse para pesquisar e analisar tendências.', key="intuito_plano", placeholder="Ex: IA no agronegócio.")
    
    
   


  
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
            if st.button('Iniciar'):
                if 1==1:
                    with st.spinner('Pesquisando tendências...'):


                        pytrend.build_payload(kw_list=['Taylor Swift'])
                        # Interest by Region
                        df = pytrend.interest_by_region()
                            
                      
                        # Aqui vamos gerar as respostas usando o modelo Gemini

                        prompt_SWOT = f'''Dado os retornos da pesquisa de tendências em {df}, faça um relatório completo do que foi recebido listando os links de referência. Tire conclusões sobre os retornos, tire insights, veja oportunidades
                        de negócios para isso. Analise o que há de interessante. Analise uma tendência conjunta sobre esses retornos. Analise, extraia informações. Redija um extenso relatório com seus achados com um nível analítico extremamente detalhado.'''
                        SWOT_output = modelo_linguagem.generate_content(prompt_SWOT).text

                        
                        

                        st.header('Pesquisa de tendências')
                        st.subheader('1 Análise de Google Trends')
                        st.markdown(SWOT_output)
                       
                       

                        


