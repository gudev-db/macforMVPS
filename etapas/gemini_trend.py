import streamlit as st
import google.generativeai as genai
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal para geração de trends
def gerar_trend():
    st.title("Gerador de Trends")

    # Explicação sobre o que são trends
    st.subheader("O que são 'Trends'?")
    st.write("Tendências, ou 'trends', são comportamentos, estilos ou interesses que capturam a atenção do público em um determinado momento. Engajar-se com essas tendências é crucial para marcas que desejam aumentar sua visibilidade e conexão com a audiência de forma relevante. Participar ativamente das tendências não apenas demonstra que a marca está atualizada, mas também potencializa o alcance e engajamento em redes sociais.")

    st.subheader("Tipos de Trends:")
    st.write('''
    1. **Música que toca na minha cabeça**: Uma trend com uma afirmação de alguma situação do dia a dia que possa acontecer. Afirmações de rotina são a maioria, e o áudio mais usado é o da música *Thunderstruck* do AC/DC.
    
    2. **Quem é você?**: Trend usada para falar sobre características pessoais num tom de apresentação. Uma ótima oportunidade de humanizar a marca e se aproximar do público.
    
    3. **Primeira semana do mês em 4 fotos**: A trend consiste em postar no Instagram "sua vez" com 4 fotos da primeira semana do mês, mostrando momentos relevantes da semana.
    
    4. **Quer se juntar à minha religião?**: Essa trend faz alusão a um produto/serviço que, de tão bom, passou a ser considerado um estilo de vida. 
    
    Escolha o tipo de trend que deseja gerar.
    ''')

    tipo_trend = st.selectbox("Escolha o tipo de Trend:", 
                              ["Música que toca na minha cabeça", 
                               "Quem é você?", 
                               "Primeira semana do mês em 4 fotos", 
                               "Quer se juntar à minha religião?"])

    # Coleta de informações do usuário
    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente")
    site_cliente = st.text_input('Site do Cliente:', help="Digite o site do cliente")
    ramo_atuacao = st.text_input('Ramo de Atuação do Cliente:', help="Qual é o ramo de atuação do cliente?")
    referencia_marca = st.text_area('Referência de Marca:',  help="Quais são as referências de marca do cliente?",height=200)
    publico = st.text_input('Público-Alvo:', help="Qual é o público-alvo do cliente?")
    objetivos = st.text_input('Objetivos do Cliente:', help="Quais são os objetivos do cliente com essa campanha?")

    if st.button("Gerar Trend"):
        if not nome_cliente or not site_cliente or not ramo_atuacao or not referencia_marca or not publico or not objetivos:
            st.write("Por favor, preencha todas as informações do cliente.")
        else:
            with st.spinner('Gerando conteúdo de Trend...'):
                
                # Criar o prompt com base na escolha da trend
                prompt = f'''

                Tendências, ou 'trends', são comportamentos, estilos ou interesses que capturam a atenção do público em um determinado momento. Engajar-se com essas tendências é crucial para marcas que desejam aumentar sua visibilidade e conexão com a audiência de forma relevante. Participar ativamente das tendências não apenas demonstra que a marca está atualizada, mas também potencializa o alcance e engajamento em redes sociais.

                
                Considerando as diretrizes de tendências de redes sociais e comportamentos que estão capturando a atenção do público, crie um conteúdo para o cliente {nome_cliente}, que atua no ramo de {ramo_atuacao} com um público-alvo de {publico}. O site do cliente é {site_cliente} e as referências de marca incluem {referencia_marca}. Os objetivos principais são {objetivos}. 
                
                Aqui estão os tipos de tendências que podem ser aplicadas:

                1. **Música que toca na minha cabeça**: Uma trend que explora situações do dia a dia de forma engraçada ou relatável.".
                
                2. **Quem é você?**: Uma trend que foca na identidade da marca ou do público.".
                
                3. **Primeira semana do mês em 4 fotos**: Trend baseada em imagens da primeira semana do mês. ".
                
                4. **Quer se juntar à minha religião?**: Trend que faz alusão a um produto/serviço incrível, como se fosse um estilo de vida.".
                
                Com base nesse contexto, crie uma versão criativa de {tipo_trend}.
                '''
                
                # Gerar o conteúdo com o modelo
                resultado_trend = modelo_linguagem.generate_content(prompt).text

                # Exibir o conteúdo gerado
                st.subheader(f"Trend gerada para '{tipo_trend}':")
                st.markdown(resultado_trend)
