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
def gen_emails():
    llm = genai.GenerativeModel("gemini-1.5-flash")
    
    
    # Input fields for sender's details
    nome_cliente = st.text_input("Digite o nome do remetente dos emails:")
    dest_email = st.text_input("Digite o nome/segmento do destinatário dos emails:")
    interesse = st.text_input("Digite o interesse do destinatário dos emails em receber contato da Citrosuco:")
    tema = st.text_input("Digite o tema do email")
    tom = st.text_input("Digite o tom do email")

    
    
    if st.button("Gerar Emails"):
        if not nome_cliente or not dest_email or not tema:
            st.warning("Por favor, preencha todas as informações.")
        else:
            with st.spinner("Brainstorming..."):


               
                

                # Generate email themes using the Gemini model
                prompt = f"""
                Redija 5 emails partindo do destinatário {nome_cliente}, para o destinatário {dest_email} com o tema {tema} (o tema deve ter um profundo impacto na composição do email) assumindo o tom {tom}.
                Instigue interação. Faça uma síntese das informaçoes dadas e redija o melhor email possível de uma forma que garanta a retenção do lead.


                """
                try:
                    response = llm.generate_content(prompt)
                    st.success("Emails gerados com sucesso!")
                    st.subheader("Emails")
                    st.markdown(response.text)
                    
                    
                    
                except Exception as e:
                    st.error(f"Erro ao gerar emails: {e}")


