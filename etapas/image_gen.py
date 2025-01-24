import streamlit as st
import requests
import os

# Configuração da API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
url = "https://api.openai.com/v1/images/generations"

# Função principal do Streamlit
def gen_img():
    st.title("Gerador de Imagens com Link")
    st.markdown("Insira um prompt para gerar uma imagem e receba o link da imagem gerada.")

    # Área de texto para o prompt
    prompt = st.text_area(
        "Digite o prompt para gerar a imagem:",
        placeholder="Descreva o que deseja gerar. Ex: Um campo ensolarado com árvores verdes e céu azul.",
        height=200,
    )

    # Botão para enviar o prompt
    if st.button("Gerar Imagem"):
        if not prompt.strip():
            st.warning("Por favor, insira um prompt antes de gerar a imagem.")
            return

        with st.spinner("Gerando imagem..."):
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                }
                data = {
                    "model": "dall-e-3",  # Ou outro modelo se aplicável
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024",
                }
                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    image_url = result["data"][0]["url"]
                    st.success("Imagem gerada com sucesso!")
                    st.markdown(f"[Clique aqui para ver a imagem gerada.]({image_url})")
                    st.text(f"URL da Imagem: {image_url}")

                    # Exibir a imagem na interface do Streamlit
                    st.image(image_url, caption="Imagem Gerada", use_column_width=True)
                else:
                    st.error(f"Erro na geração da imagem: {response.status_code}")
                    st.text(response.text)
            except Exception as e:
                st.error("Ocorreu um erro ao tentar gerar a imagem.")
                st.text(str(e))
