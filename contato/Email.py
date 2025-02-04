import os
import streamlit as st
import google.generativeai as genai
import requests
from datetime import date

ex_email = '''
Versão 1 - reduzida
Assunto: From orchard to innovation: the digital transformation of orange farming
Preheader: Discover how digital tools are revolutionizing citrus farming and boosting efficiency.

[BANNER]
The Next Step in Orange Farming

Estimated reading time: 2 minutes

[INTRODUÇÃO]
The citrus farming industry is experiencing a digital revolution, transforming how growers manage their orchards. From drones monitoring tree health to IoT sensors providing real-time data on irrigation and nutrition, new technologies are making farming smarter, more efficient, and more sustainable.

These advancements are improving yields and helping farmers detect diseases early, optimize resources, and make more informed decisions.


[BLOCO 1]
Drones: A New Eye in the Sky
Identify early signs of diseases like citrus greening.
Capture high-resolution images to guide precise interventions.

[BLOCO 2]
IoT Sensors: Precision in Irrigation and Nutrition
Monitor soil moisture and nutrient levels in real time.
Automate irrigation schedules, reducing water waste.

By leveraging these tools, farmers can stay ahead of challenges, care for their orchards sustainably, and meet growing market demands.



[ENCERRAMENTO]
Digital technologies are transforming the citrus farming industry, helping growers stay ahead of challenges and improve productivity. By embracing drones, IoT sensors, and digital platforms, farmers are well-positioned to meet the growing demand for fresh, high-quality citrus products in an increasingly competitive market.

If you have any questions or want to learn more about how these technologies can help you, feel free to reach out to our team.

Stay connected with Citrosuco
Facebook
Instagram
LinkedIn

www.citrosuco.com/citrosuco-connects/

Versão 2 - full
Assunto: From orchard to innovation: the digital transformation of orange farming
Preheader: Discover how digital tools are revolutionizing citrus farming and boosting efficiency.

[BANNER]
The Next Step in Orange Farming

Estimated reading time: 3 minutes

[INTRODUÇÃO]
The citrus farming industry is experiencing a digital revolution, transforming how growers manage their orchards. From drones monitoring tree health to IoT sensors providing real-time data on irrigation and nutrition, new technologies are making farming smarter, more efficient, and more sustainable.

These advancements are improving yields and helping farmers detect diseases early, optimize resources, and make more informed decisions.

[BLOCO 1]
Drones: Eyes in the Sky for Early Disease Detection
High-tech sensors capture detailed aerial images and thermal data.
Identify early signs of diseases like citrus greening or pathogenic infections.
Enable targeted interventions, saving time and resources.


[BLOCO 2]
IoT Sensors: Real-Time Data for Smarter Decisions
Monitor critical metrics like soil moisture, nutrient levels, and temperature.
Automate irrigation and fertilization schedules to avoid waste.
Contribute to more sustainable farming practices by reducing chemical inputs.


By embracing these tools, growers can stay ahead of challenges, care for their orchards sustainably, and meet the growing market demand for high-quality citrus products.


[INFOGRÁFICO]
An exclusive visual guide to the digital tools transforming orange farming.
Roteiro infográfico aqui

[ENCERRAMENTO]
If you have any questions or want to learn more about how these technologies can help you, feel free to reach out to our team.

Stay connected with Citrosuco
Facebook
Instagram
LinkedIn

www.citrosuco.com/citrosuco-connects/




'''

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
                Instigue interação. Faça uma síntese das informaçoes dadas e redija o melhor email possível de uma forma que garanta a retenção ou aquisição do lead.
                Separe e organize os emails com linhas entre eles. Crie uma conexão forte e profissional entre o destinatário e remetente.

                Exemplos de emails usados hoje que você deve usar como referência para estrutura e tom:{ex_email}

                """
                try:
                    response = llm.generate_content(prompt)
                    st.success("Emails gerados com sucesso!")
                    st.subheader("Emails")
                    st.markdown(response.text)
                    
                    
                    
                except Exception as e:
                    st.error(f"Erro ao gerar emails: {e}")


