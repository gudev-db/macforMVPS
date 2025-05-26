import streamlit as st
from google import genai
import os
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

model_id = "gemini-2.0-flash"

google_search_tool = Tool(
    google_search=GoogleSearch()
)

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

    st.subheader("Opções de Trends:")
    st.write('''
    Você pode escolher entre nossas sugestões de trends ou criar sua própria trend personalizada com nome e descrição únicos.
    ''')

    # Opção para escolher entre trends pré-definidas ou personalizada
    opcao_trend = st.radio(
        "Como deseja prosseguir?",
        ["Usar uma trend pré-definida", "Criar uma trend personalizada"],
        index=0
    )

    if opcao_trend == "Usar uma trend pré-definida":
        tipo_trend = st.selectbox(
            "Escolha o tipo de Trend:",
            [
                "Música que toca na minha cabeça",
                "Quem é você?",
                "Primeira semana do mês em 4 fotos",
                "Quer se juntar à minha religião?"
            ]
        )
        
        # Mostrar descrição das trends pré-definidas
        if tipo_trend == "Música que toca na minha cabeça":
            st.info("Uma trend com uma afirmação de alguma situação do dia a dia que possa acontecer. Afirmações de rotina são a maioria, e o áudio mais usado é o da música Thunderstruck do AC/DC.")
        elif tipo_trend == "Quem é você?":
            st.info("Trend usada para falar sobre características pessoais num tom de apresentação. Uma ótima oportunidade de humanizar a marca e se aproximar do público.")
        elif tipo_trend == "Primeira semana do mês em 4 fotos":
            st.info("A trend consiste em postar no Instagram 'sua vez' com 4 fotos da primeira semana do mês, mostrando momentos relevantes da semana.")
        elif tipo_trend == "Quer se juntar à minha religião?":
            st.info("Essa trend faz alusão a um produto/serviço que, de tão bom, passou a ser considerado um estilo de vida.")
            
    else:  # Trend personalizada
        tipo_trend = st.text_input("Nome da sua Trend Personalizada:", help="Dê um nome criativo para sua trend")
        descricao_trend = st.text_area(
            "Descreva sua Trend:",
            help="Descreva em detalhes como essa trend funciona, qual o formato, estilo e objetivo",
            height=150
        )
        if not tipo_trend:
            st.warning("Por favor, dê um nome para sua trend personalizada")

    # Coleta de informações do usuário
    st.subheader("Informações do Cliente")
    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente")
    site_cliente = st.text_input('Site do Cliente:', help="Digite o site do cliente")
    ramo_atuacao = st.text_input('Ramo de Atuação do Cliente:', help="Qual é o ramo de atuação do cliente?")
    referencia_marca = st.text_area('Referência de Marca:', help="Quais são as referências de marca do cliente?", height=200)
    publico = st.text_input('Público-Alvo:', help="Qual é o público-alvo do cliente?")
    objetivos = st.text_input('Objetivos do Cliente:', help="Quais são os objetivos do cliente com essa campanha?")
    obs = st.text_input('Observações:', help="Utilize esse campo para melhorar a saída.")

    if st.button("Gerar Trend"):
        if not nome_cliente or not site_cliente or not ramo_atuacao or not referencia_marca or not publico or not objetivos:
            st.error("Por favor, preencha todas as informações do cliente.")
        elif opcao_trend == "Criar uma trend personalizada" and not tipo_trend:
            st.error("Por favor, defina um nome para sua trend personalizada")
        else:
            with st.spinner('Gerando conteúdo de Trend...'):
                novids = client.models.generate_content(
                    model=model_id,
                    contents=f'''Novidades e inovações e tendências no ramo de atuação: {ramo_atuacao}?''',
                    config=GenerateContentConfig(
                        tools=[google_search_tool],
                        response_modalities=["TEXT"],
                    )
                )
                
                # Criar o prompt com base na escolha da trend
                if opcao_trend == "Usar uma trend pré-definida":
                    trend_desc = {
                        "Música que toca na minha cabeça": "Uma trend com uma afirmação de alguma situação do dia a dia que possa acontecer. Afirmações de rotina são a maioria, e o áudio mais usado é o da música Thunderstruck do AC/DC.",
                        "Quem é você?": "Trend usada para falar sobre características pessoais num tom de apresentação. Uma ótima oportunidade de humanizar a marca e se aproximar do público.",
                        "Primeira semana do mês em 4 fotos": "A trend consiste em postar no Instagram 'sua vez' com 4 fotos da primeira semana do mês, mostrando momentos relevantes da semana.",
                        "Quer se juntar à minha religião?": "Essa trend faz alusão a um produto/serviço que, de tão bom, passou a ser considerado um estilo de vida."
                    }[tipo_trend]
                else:
                    trend_desc = descricao_trend

                prompt = f'''
                Tendências, ou 'trends', são comportamentos, estilos ou interesses que capturam a atenção do público em um determinado momento. Engajar-se com essas tendências é crucial para marcas que desejam aumentar sua visibilidade e conexão com a audiência de forma relevante. Participar ativamente das tendências não apenas demonstra que a marca está atualizada, mas também potencializa o alcance e engajamento em redes sociais.

                Considere que trends são postadas no Instagram e TikTok. Se atente a formatos que atendam a essas plataformas. Você trabalha para uma empresa de marketing digital.
                
                Considerando as diretrizes de tendências de redes sociais e comportamentos que estão capturando a atenção do público, crie um conteúdo para o cliente {nome_cliente}, que atua no ramo de {ramo_atuacao} com um público-alvo de {publico}. O site do cliente é {site_cliente} e as referências de marca incluem {referencia_marca}. Os objetivos principais são {objetivos}. 
                
                O tipo de trend solicitado é: {tipo_trend}
                Descrição da trend: {trend_desc}
                
                Considere novidades de mercado explicitadas em: {novids};

                Seja único, original, perspicaz. Crie um conteúdo que se encaixe perfeitamente na trend descrita, mas que também seja autêntico para a marca {nome_cliente}.

                Observações: {obs}
                '''
                
                # Gerar o conteúdo com o modelo
                resultado_trend = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt]
                ).text

                # Exibir o conteúdo gerado
                st.subheader(f"Trend gerada: '{tipo_trend}'")
                st.markdown(resultado_trend)
