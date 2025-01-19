import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Function to generate email themes and display results
def gen_temas_emails():
    st.subheader("Informações do remetente")
    
    # Input fields for sender's details
    nome_cliente = st.text_input("Digite o nome do remetente dos emails:")
    ramo_atuacao = st.text_input("Ramo de Atuação:")
    referencia_da_marca = st.text_area(
        "Referência da Marca:",
        height=200  
    )
    
    st.subheader("Informações do(s) destinatário(s)")
    destinatarios = st.text_input("Caracterize os destinatários:")
    
    if st.button("Gerar Temas e Emails"):
        if not nome_cliente or not ramo_atuacao or not destinatarios:
            st.warning("Por favor, preencha todas as informações.")
        else:
            with st.spinner("Gerando temas e emails..."):
                # Generate email themes using the Gemini model
                prompt = f"""
                Crie temas de emails específicos para as segmentações de leads conforme {destinatarios}. 
                O remetente dos emails é {nome_cliente}, que atua no ramo de {ramo_atuacao}. 
                Considere incluir datas comemorativas relevantes e temáticas gerais apropriadas ao público-alvo.
                """
                try:
                    response = genai.generate_text(prompt, model="gemini-1.5-flash")
                    st.success("Temas e emails gerados com sucesso!")
                    st.subheader("Temas e Emails")
                    st.markdown(response.result)
                except Exception as e:
                    st.error(f"Erro ao gerar temas e emails: {e}")



