import streamlit as st
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import uuid
import os
from datetime import datetime
import requests

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def nn_gen():
    st.subheader('Planejamento de Pesquisa e Estratégia')
    st.text('''Aqui é gerado o planejamento de Pesquisa e Estratégia. Geramos análise SWOT, análise PEST, análise de tendências de mercado,
            análise de concorrências, Golden Circle, Posicionamento de marca, Brand Persona, Buyer Pesona e Tom de Voz''')

    # Inputs do usuário
    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente")
    ramo_atuacao = st.text_input('Ramo de Atuação:', key="ramo_atuacao")
    intuito_plano = st.text_input('Intuito do Planejamento estratégico:', key="intuito_plano", 
                                placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre.")
    publico_alvo = st.text_input('Público alvo:', key="publico_alvo", 
                               placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda.")
    concorrentes = st.text_input('Concorrentes:', key="concorrentes", 
                               placeholder="Ex: Loja A, Loja B, Loja C.")
    site_concorrentes = st.text_input('Site dos concorrentes:', key="site_concorrentes", 
                                    placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br")
    
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]
    
    objetivos_de_marca = st.selectbox('Quais são os objetivos da sua marca?', objetivos_opcoes, key="objetivos_marca")
    referencia_da_marca = st.text_area('Referência de marca:', key="referencia_da_marca", 
                                     placeholder="Conte um pouco mais sobre sua marca...")
    sucesso = st.text_input('O que é sucesso para a marca?:', key="sucesso", 
                          help='O que a marca precisa alcançar para considerar que atingiu os seus objetivos?')

    iteracoes_swot = st.slider('Número de iterações para refinamento da SWOT (1-10)', 
                             min_value=1, max_value=10, value=3, 
                             help="Quantas vezes o sistema deve refinar a análise SWOT")

    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", 
                                type=["pdf"], accept_multiple_files=True)

    if st.button('Iniciar Planejamento'):
        if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
            st.error("Por favor, preencha todas as informações do cliente.")
        else:
            with st.spinner('Gerando o planejamento...'):
                try:
                    # Processamento da SWOT com iterações
                    base_prompt = f'''
                    Como especialista em administração de marketing com 20 anos de experiência, crie uma análise SWOT detalhada para:
                    - Cliente: {nome_cliente}
                    - Ramo: {ramo_atuacao}
                    - Objetivos: {objetivos_de_marca}
                    - Definição de sucesso: {sucesso}
                    
                    Contexto adicional:
                    {referencia_da_marca}
                    
                    Requisitos:
                    1. 10 pontos por quadrante (Forças, Fraquezas, Oportunidades, Ameaças)
                    2. Cada ponto com 3-5 frases de análise
                    3. Linguagem profissional em português BR
                    4. Específico para este negócio
                    5. Organizado em bullets
                    '''
                    
                    current_prompt = base_prompt
                    swot_history = []
                    
                    for i in range(iteracoes_swot):
                        with st.spinner(f'Gerando análise SWOT (iteração {i+1}/{iteracoes_swot})...'):
                            # Gera a SWOT
                            current_swot = client.models.generate_content(
                                model="gemini-2.0-flash",
                                contents=[current_prompt]).text
                            swot_history.append(current_swot)
                            
                            if i < iteracoes_swot - 1:
                                # Critica e melhora o prompt
                                critique = client.models.generate_content(
                                    model="gemini-2.0-flash",
                                    contents=[f'''
                                    Analise esta SWOT e sugira melhorias para o PROMPT:
                                    {current_swot}
                                    
                                    Critique:
                                    1. Pontos genéricos
                                    2. Contexto não explorado
                                    3. Sugestões para melhorar
                                    ''']).text
                                
                                current_prompt = client.models.generate_content(
                                    model="gemini-2.0-flash",
                                    contents=[f'''
                                    Melhore este prompt para SWOT com base na crítica:
                                    {critique}
                                    
                                    Prompt original:
                                    {base_prompt}
                                    ''').text
                    
                    # Exibe o resultado final
                    st.subheader("Análise SWOT Final")
                    st.write(swot_history[-1])
                    
                    # Opção para ver histórico
                    if st.checkbox('Mostrar histórico de refinamento'):
                        for idx, version in enumerate(swot_history):
                            st.subheader(f'Iteração {idx+1}')
                            st.write(version)
                            
                except Exception as e:
                    st.error(f"Ocorreu um erro: {str(e)}")
                    st.stop()
