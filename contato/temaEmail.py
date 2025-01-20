import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

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
    
    st.subheader("Informações do(s) destinatário(s)")
    destinatarios = st.text_input("Caracterize os destinatários:")
    
    if st.button("Gerar Temas de Emails"):
        if not nome_cliente or not ramo_atuacao or not destinatarios:
            st.warning("Por favor, preencha todas as informações.")
        else:
            with st.spinner("Gerando temas e emails..."):
                # Generate email themes using the Gemini model
                prompt = f"""
                Crie um cronograma anual de temas de emails específicos para CADA UMA das segmentações de leads conforme {destinatarios} com fins de nutrição de leads. 
                O remetente dos emails é {nome_cliente}, que atua no ramo de {ramo_atuacao}. 

                Extraia de todo o seu conhecimento as especificidades de cada segmento dos destinatários e entenda o que de fato, em cada mês, iria pegar as suas atenções
                no que se diz respeito a datas comemorativas e características locais. Engaja, nutre, conquiste os leads.
                
                Considere incluir datas comemorativas relevantes e temáticas gerais apropriadas ao público-alvo.
                Você segue o princípio de atuação GLOCAL. Pensar GLOBALMENTE e agir LOCALMENTE. Organize a saída em formato de tabela. Se atente às especificidades de cada segmentação.
                Seja claro, preciso e prático. Não me dê diretrizes, crie os temas que eu preciso para eu colocar diretamente em produção.
                """
                try:
                    response = llm.generate_content(prompt)
                    st.success("Temas e emails gerados com sucesso!")
                    st.subheader("Temas")
                    st.markdown(response.text)
                    
                    # Allow user to select a theme for email generation
                    tema_selecionado = st.selectbox("Escolha um tema para gerar emails", response.text.split("\n"))
                    
                    # Generate 5 email suggestions based on the selected theme
                    if tema_selecionado:
                        st.subheader("Sugestões de Emails")
                        email_prompt = f'''
                        Com base no tema selecionado: "{tema_selecionado}", escreva 5 sugestões de emails detalhados para enviar aos leads.
                        O remetente dos emails é {nome_cliente}, e o objetivo é nutrir e engajar os leads de forma personalizada.
                        '''
                        try:
                            email_suggestions = llm.generate_content(email_prompt)
                            st.markdown(email_suggestions.text)
                        except Exception as e:
                            st.error(f"Erro ao gerar sugestões de emails: {e}")
                    
                except Exception as e:
                    st.error(f"Erro ao gerar temas e emails: {e}")

