import streamlit as st
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import uuid
import os
from pymongo import MongoClient
from datetime import datetime
import os
import requests




# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = "gemini-2.0-flash"  # Usando Gemini





# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def nn_gen():
    st.subheader('Planejamento de Pesquisa e Estratégia')
    st.text('''Aqui é gerado o planejamento de Pesquisa e Estratégia. Geramos análise SWOT, análise PEST, análise de tendências de mercado,
            análise de concorrências, Golden Circle, Posicionamento de marca, Brand Persona, Buyer Pesona e Tom de Voz''')
    


    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")
   
    # Exibir os campos preenchidos com os dados do cliente
    site_cliente = st.text_input('Site do Cliente:', key="site_cliente")
    ramo_atuacao = st.text_input('Ramo de Atuação:', key="ramo_atuacao")
    
    # Intuito do Plano Estratégico
    intuito_plano = st.text_input('Intuito do Planejamento estratégico: Utilize esse campo para explicitar quais são as espectativas do cliente no desenvolvimento desse planejamento. Exemplo: Gerar mais leads, aumentar vendas, aumentar reconhecimento em alguma região estratégica, etc', key="intuito_plano", placeholder="Ex: Aumentar as vendas em 30% no próximo trimestre. O que você deseja alcançar com esse plano?")
    
    # Público-Alvo
    publico_alvo = st.text_input('Público alvo: Utilize esse campo para definir qual é o perfil do público alvo que deve ser atingido por esse planejamento estratégico. Seja idade, região, gênero, área de atuação. Aproveite para ser o quão detalhado for necessário.', key="publico_alvo", placeholder="Ex: Jovens de 18 a 25 anos, interessados em moda. Defina o perfil das pessoas que você quer atingir.")
    
    # Concorrentes
    concorrentes = st.text_input('Concorrentes: Utilize esse campo para definir quais são os concorrentes do cliente.', key="concorrentes", placeholder="Ex: Loja A, Loja B, Loja C. Liste os concorrentes que você considera mais relevantes no seu mercado.")
    
    # Sites dos Concorrentes
    site_concorrentes = st.text_input('Site dos concorrentes: Utilize esse campo para colocar os sites dos concorrentes. A forma como decidir dividí-los não importa. Ex (, ou ; ou .)', key="site_concorrentes", placeholder="Ex: www.loja-a.com.br, www.loja-b.com.br, www.loja-c.com.br. Insira os sites dos seus concorrentes para compararmos.")
    
    
    # Objetivos de Marca
    objetivos_opcoes = [
        'Criar ou aumentar relevância, reconhecimento e autoridade para a marca',
        'Entregar potenciais consumidores para a área comercial',
        'Venda, inscrição, cadastros, contratação ou qualquer outra conversão final do público',
        'Fidelizar e reter um público fiel já convertido',
        'Garantir que o público esteja engajado com os canais ou ações da marca'
    ]
    
    objetivos_de_marca = st.selectbox('Quais são os objetivos da sua marca?', objetivos_opcoes, key="objetivos_marca")
    
    # Referência da Marca
    referencia_da_marca = st.text_area('Referência de marca: Utilize esse campo para escrever um texto que define o cliente quanto ao seu ramo de atuação, objetivos e personalidade.', key="referencia_da_marca", placeholder="Conte um pouco mais sobre sua marca, o que ela representa, seus valores e diferenciais no mercado.")

    sucesso = st.text_input('O que é sucesso para a marca?:', key="sucesso", help='Redija aqui um texto que define o que a marca considera como sucesso. O que ela precisa alcançar para considerar que atingiu os seus objetivos?')

    iteracoes_swot = st.slider('Número de iterações para refinamento da SWOT (1-10)', 
                          min_value=1, max_value=10, value=3, 
                          help="Quantas vezes o sistema deve refinar a análise SWOT para melhorar a qualidade")
  
    # Se os arquivos PDF forem carregados
    pest_files = st.file_uploader("Escolha arquivos de PDF para referência de mercado", type=["pdf"], accept_multiple_files=True)

        # Set parameters for the search
    days = 90
    max_results = 15


  
    if pest_files is not None:
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
            if st.button('Iniciar Planejamento'):
                if not nome_cliente or not ramo_atuacao or not intuito_plano or not publico_alvo:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    with st.spinner('Gerando o planejamento...'):

                        model_id = "gemini-2.0-flash"

                        google_search_tool = Tool(
                            google_search = GoogleSearch()
                        )
                        
                        # Agente de pesquisa política
                        pls = client.models.generate_content(
                            model=model_id,
                            contents="Faça uma pesquisa sobre notícias políticas recentes sobre o Brasil",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )
                        
                        # Agente de pesquisa econômica do Brasil
                        dados_econ_brasil = client.models.generate_content(
                            model=model_id,
                            contents="Faça uma pesquisa sobre dados econômicos recentes sobre o Brasil",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )
                        
                        # Agente de notícias sobre concorrentes
                        novids_conc = client.models.generate_content(
                            model=model_id,
                            contents=f"Faça uma pesquisa sobre as notícias mais recentes sobre os concorrentes: {concorrentes}",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )

                        # Agente de pesquisa Social
                        tend_social_duck = client.models.generate_content(
                            model=model_id,
                            contents="Pesquise sobre novidades no âmbito social brasileiro",
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )
                        
                        # Agente de pesquisa tecnológica
                        tec = client.models.generate_content(
                            model=model_id,
                            contents=f'''Pesquise novidades tecnológicas no ramo de atuação: {ramo_atuacao}''',
                            config=GenerateContentConfig(
                                tools=[google_search_tool],
                                response_modalities=["TEXT"],
                            )
                        )





                       





                      

                        base_prompt = f'''
                        - não seja genérico
                        - traga impacto com seu output
                        - você é um especialista em administração de marketing; Você tem todo o conhecimento possível comparavel à Simon Sinek
                        - Você está aqui para fazer a diferença
                        - considerando os objetivos de marca ({objetivos_de_marca})
                        - seja único. una o que torna o cliente {nome_cliente} de diferente em relação ao resto.

                        Como um especialista em administração de marketing, gere um Golden Circle completo com 'how', 'why' e 'what' resumidos 
                                    em uma frase cada. Considerando e sintetizando de forma perspicaz o seguinte contexto 
                                     e o objetivo do planejamento estratégico {intuito_plano},e a referência da marca:
                                    {referencia_da_marca}
                        '''
                        
                        current_prompt = base_prompt
                        swot_history = []  
                        prompt_history = []
                        prompt_history.append(base_prompt)
                        
                        for i in range(iteracoes_swot):
                            with st.spinner(f'Gerando análise SWOT (iteração {i+1}/{iteracoes_swot})...'):
                                # Gera a SWOT com o prompt atual
                                current_swot = client.models.generate_content(
                                    model="gemini-2.0-flash",
                                    contents=[current_prompt]).text
                                swot_history.append(current_swot)
                                
                                if i < iteracoes_swot - 1:  # Não precisa refinar na última iteração
                                    # Critica o resultado para melhorar o prompt
                                    critique = client.models.generate_content(
                                        model="gemini-2.0-flash",
                                        contents=[f'''
                                        Analise esta SWOT e sugira melhorias para o PROMPT (não para o texto):
                                        
                                        SWOT gerada:
                                        {current_swot}
                                        
                                        Critique:
                                        1. Quais aspectos ainda estão genéricos?
                                        2. Que elementos do contexto poderiam ser melhor explorados?
                                        3. Como ajustar o prompt para:
                                           - Maior profundidade
                                           - Mais especificidade
                                           - Melhor conexão com os objetivos
                                        ''']).text
                                    
                                    # Reescreve o prompt
                                    prompt_history.append(current_prompt)
                                    current_prompt = client.models.generate_content(
                                        model="gemini-2.0-flash",
                                        contents=[f'''
                                        Com base nesta crítica:
                                        {critique}
                                        
                                        Reescreva o prompt original abaixo para gerar uma SWOT mais efetiva.
                                        Mantenha a estrutura básica mas adicione orientações mais precisas.
                                        
                                        Prompt original:
                                        {base_prompt}
                                        ''']).text
                        
                        SWOT_output = current_swot
                        
                        st.header("Output History")
                        for idx, version in enumerate(swot_history):
                            st.subheader(f'Iteração {idx+1}')
                            st.write(version)

                        st.header("Prompt History")
                        for idx, version in enumerate(prompt_history):
                            st.subheader(f'Iteração {idx+1}')
                            st.write(version)
                        


                      
