import os
import streamlit as st
import google.generativeai as genai
import requests
from datetime import date

# Configure the Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)
rapid_key = os.getenv("RAPID_API")

# Function to generate email themes and display results
def gen_temas_emails():
    llm = genai.GenerativeModel("gemini-1.5-flash")
    st.subheader("Informações do remetente")
    
    # Input fields for sender's details
    nome_cliente = st.text_input("Digite o nome do remetente dos emails:")
    ramo_atuacao = st.text_input("Ramo de Atuação:")
    referencia_da_marca = st.text_area(
        "Referência da Marca:",
        height=200  
    )
    tipo_empresa = st.selectbox("Escolha o tipo de empresa:", ["B2B", "B2C", "B2G"])

    servicos_empresa = st.text_input("Digite aqui os tipos de serviços que a empresa realiza:")

    stakeholders = st.text_input("Stakeholders da comunicação:")


    st.subheader("Informações do(s) destinatário(s)")
    destinatarios = st.text_input("Caracterize os destinatários quanto a sua segmentação:")
    
    if st.button("Gerar Temas de Emails"):
        if not nome_cliente or not ramo_atuacao or not destinatarios:
            st.warning("Por favor, preencha todas as informações.")
        else:
            with st.spinner("Brainstorming..."):


                url = "https://duckduckgo8.p.rapidapi.com/"
                            
                querystring = {"q":f"tendencias e novidades em {ramo_atuacao}"}
                            
                headers = {
                                "x-rapidapi-key": rapid_key,
                                "x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
                            }
                            
                response = requests.get(url, headers=headers, params=querystring)
                            
                tend_novids2 = response.text
                

                # Generate email themes using the Gemini model
                prompt = f"""
                Crie um cronograma (em formato de tabela) anual de temas de emails específicos para CADA UMA das segmentações de leads conforme {destinatarios} com fins de nutrição de leads. 
                O remetente dos emails é {nome_cliente}, que atua no ramo de {ramo_atuacao}. Eis uma breve descrição sobre a marca: {referencia_da_marca}.
                A empresa costuma vender serviços como {servicos_empresa}.;

                Os stakeholders da comunicação são: {stakeholders}.;

                A empresa é do tipo {tipo_empresa}.;

                Considere as novidades do setor de atuação em: {tend_novids2};

    
                
                Extraia de todo o seu conhecimento as especificidades de cada segmento dos destinatários e entenda o que de fato, em cada mês, iria pegar as suas atenções
                no que se diz respeito a datas comemorativas e características locais. Engaja, nutra, conquiste os leads.;
                
                Considere incluir datas comemorativas relevantes e temáticas gerais apropriadas ao público-alvo.;
                Você segue o princípio de atuação GLOCAL. Pensar GLOBALMENTE e agir LOCALMENTE. Organize a saída em formato de tabela. Se atente às especificidades de cada segmentação.
                Seja claro, preciso e prático. Não me dê diretrizes, crie os temas que eu preciso para eu colocar diretamente em produção. Seja inovativo,
                perspicaz e faça uma síntese de todas as informações dadas sobre o cliente e o segmento para a criação dos temas de email. Você é criativo
                e excelente com palavras;
                """
                try:
                    response = llm.generate_content(prompt)
                    st.success("Temas e emails gerados com sucesso!")
                    st.subheader("Temas")
                    st.markdown(response.text)
                    
                    emails = llm.generate_content(f'''Dados os temas em {response.text}, redija um email para cada um deles (Sem resumir ou cortar, faça tudo). Lembre que você é a empresa {nome_cliente} e está
                    nutrindo seus leads. Faça um output organizado em tabela. Redija cada email para cada segmento em cada mês sem falta e sem resumir e sem cortes. Faça para TODOS.''')
                    st.subheader("Emails")
                    st.markdown(emails.text)
                    
                except Exception as e:
                    st.error(f"Erro ao gerar temas e emails: {e}")


