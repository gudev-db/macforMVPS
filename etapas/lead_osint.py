import streamlit as st
from google import genai
from tavily import TavilyClient
import requests
import os

# Configuração das APIs
gemini_api_key = os.getenv("GEM_API_KEY")
t_api_key1 = os.getenv("T_API_KEY")
rapid_key = os.getenv("RAPID_API")

# Configura o cliente Gemini
genai.configure(api_key=gemini_api_key)
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")

# Configura o cliente Tavily
client1 = TavilyClient(api_key='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')


def fetch_duckduckgo(query, rapid_key):
    url = "https://duckduckgo-search-api.p.rapidapi.com"
    headers = {
        "x-rapidapi-key": rapid_key,
        "x-rapidapi-host": "duckduckgo-search-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params={"q": query})
    return response.text


# Função para buscar informações no Tavily sobre um único termo
def fetch_tavily(query, client, days=90, max_results=15):
    return client.search(query, days=days, max_results=max_results)


# Funções para cada variável de entrada
def search_target_name(target_name):
    duckduckgo_result = fetch_duckduckgo(f"Information about {target_name}", rapid_key)
    tavily_result = fetch_tavily(f"Details about {target_name}", client1)
    return duckduckgo_result, tavily_result


def search_email(email):
    duckduckgo_result = fetch_duckduckgo(f"{email}", rapid_key)
    tavily_result = fetch_tavily(f"{email}", client1)
    return duckduckgo_result, tavily_result


def search_phone(phone):
    duckduckgo_result = fetch_duckduckgo(f"{phone}", rapid_key)
    tavily_result = fetch_tavily(f"{phone}", client1)
    return duckduckgo_result, tavily_result


def search_profile(profile):
    duckduckgo_result = fetch_duckduckgo(f"{profile}", rapid_key)
    tavily_result = fetch_tavily(f"{profile}", client1)
    return duckduckgo_result, tavily_result


def search_region(region):
    duckduckgo_result = fetch_duckduckgo(f"News about {region}", rapid_key)
    tavily_result = fetch_tavily(f"News about {region}", client1)
    return duckduckgo_result, tavily_result


def search_profession(profession):
    duckduckgo_result = fetch_duckduckgo(f"Information about the profession {profession}", rapid_key)
    tavily_result = fetch_tavily(f"Details about the profession {profession}", client1)
    return duckduckgo_result, tavily_result


def search_employer(employer):
    duckduckgo_result = fetch_duckduckgo(f"Information about the employer {employer}", rapid_key)
    tavily_result = fetch_tavily(f"Details about the employer {employer}", client1)
    return duckduckgo_result, tavily_result


def search_associates(associates):
    duckduckgo_result = fetch_duckduckgo(f"Information about associates {associates}", rapid_key)
    tavily_result = fetch_tavily(f"Details about associates {associates}", client1)
    return duckduckgo_result, tavily_result


import requests

# Função para pegar dados do LinkedIn com base no nome de usuário
def get_linkedin_profile_data(profile_url):
    # URL da API do LinkedIn
    url = "https://linkedin-api8.p.rapidapi.com/get-company-details"

    # Parâmetros da requisição, usando o nome de usuário do LinkedIn
    querystring = {"username": profile_url}

    # Cabeçalhos com a chave de API
    headers = {
        "x-rapidapi-key": "0c5b50def9msh23155782b7fc458p103523jsn427488a01210",
        "x-rapidapi-host": "linkedin-api8.p.rapidapi.com"
    }

    # Envia a requisição GET
    response = requests.get(url, headers=headers, params=querystring)

    # Verifica se a requisição foi bem-sucedida (status code 200)
    if response.status_code == 200:
        # Retorna a resposta JSON diretamente
        return response.json()
    else:
        # Se houver erro, retorna o código de status de erro
        return {"error": f"Erro ao acessar a URL, Status code: {response.status_code}"}

# Função para pegar os posts de uma empresa no LinkedIn
def get_linkedin_company_posts(profile_url, start=0):
    # URL da API do LinkedIn
    url = "https://linkedin-api8.p.rapidapi.com/get-company-posts"

    # Parâmetros da requisição, usando o nome de usuário e a página de início (start)
    querystring = {"username": profile_url, "start": str(start)}

    # Cabeçalhos com a chave de API
    headers = {
        "x-rapidapi-key": "0c5b50def9msh23155782b7fc458p103523jsn427488a01210",
        "x-rapidapi-host": "linkedin-api8.p.rapidapi.com"
    }

    # Envia a requisição GET
    response = requests.get(url, headers=headers, params=querystring)

    # Verifica se a requisição foi bem-sucedida (status code 200)
    if response.status_code == 200:
        # Retorna a resposta JSON diretamente
        return response.json()
    else:
        # Se houver erro, retorna o código de status de erro
        return {"error": f"Erro ao acessar a URL, Status code: {response.status_code}"}

# Função principal para pesquisa OSINT com múltiplos termos
def osint_report():
    st.subheader("Relatório OSINT")

    # Inputs no Streamlit
    inputs = {
        "Nome do Lead": st.text_input("Lead:", key="target"),
        "Perfil Linkedin": st.text_input("Nome de usuário no linkedin (encontrado no link do perfil da empresa):", key="profile"),
        "Região": st.text_input("Região:", key="region"),
        "Área de atuação": st.text_input("Área de Atuação:", key="profession"),
    }

    # Adiciona valores padrão para os campos ausentes, evitando KeyError
    target_name = inputs.get('Nome do Lead', '')
    profile = inputs.get('Perfil Linkedin', '')
    region = inputs.get('Região', '')
    profession = inputs.get('Área de atuação', '')

    # Botão para gerar o relatório
    if st.button("Gerar Plano de Aproximação"):
        if any([target_name, profile, region, profession]):
            with st.spinner("Gerando plano de aproximação..."):
                # Coleta informações do DuckDuckGo e Tavily para cada entrada
                duckduckgo_results = {}
                tavily_results = {}

                if target_name:
                    duckduckgo_results['Target Name'], tavily_results['Target Name'] = search_target_name(target_name)

                if region:
                    duckduckgo_results['Region'], tavily_results['Region'] = search_region(region)
                if profession:
                    duckduckgo_results['Profession'], tavily_results['Profession'] = search_profession(profession)

                # Pega os dados do LinkedIn
                if profile:
                    profile_data = get_linkedin_profile_data(profile)
                    posts_data = get_linkedin_company_posts(profile)
                else:
                    profile_data = "No LinkedIn profile provided."

                # Gera o prompt para o modelo Gemini com todas as variáveis de input
                duckduckgo_summary = "\n".join([f"{key}: {value}" for key, value in duckduckgo_results.items()])
                tavily_summary = "\n".join([f"{key}: {', '.join(value)}" for key, value in tavily_results.items()])

                prompt = f"""
                Você é um especialista em inteligência de mercado e engenharia social. Desenvolva um relatório extremamente detalhado, analítico e profundo de OSINT que chegue ao cerne da pessoa sendo analisada.

                Seu trabalho é analisar e tirar insights e montar uma estratégia de aproximação para mim, uma empresa de marketing, para sermos contradados
                pelo cliente.


                As seguintes são as informações coletadas de diferentes fontes sobre o alvo:

                1. Nome do Alvo: {target_name if target_name else 'Não disponível'}
  
                6. Perfil: {profile if profile else 'Não disponível'}
                7. Região: {region if region else 'Não disponível'}
                8. Profissão: {profession if profession else 'Não disponível'}

                - Perfil no LinkedIn:
                {profile_data}

                - Posts no perfil do LinkedIn:
                {posts_data}

                Com base nessas informações, gere um relatório detalhado, estruturado nas seguintes seções:

                1. Resumo geral do alvo.
                2. Insights relevantes para cada aspecto.
                3. Conclusões e possíveis aplicações estratégicas.
                4. Relacione todos os pontos e traga insights sobre o alvo.

                Cada ponto deve ser explicado em detalhes, com insights profundos e organizados em parágrafos bem estruturados.

                Diga-me os melhores papéis para essa pessoa, a melhor forma de abordá-la. Sugestões e insights sobre sua vida, personalidade, dores. Ensine-me como me comunicar com essa pessoa de uma forma específica às suas características. Não seja razoável. Seja detalhado. Você é um especialista em engenharia social.

                Escreva um texto de 5 parágrafos longos e detalhados sobre insights tirados a partir das informações da empresa. Quais são suas dores?
                O que a ajudaria a alcançar seus objetivos? Como uma empresa de marketing pode se destacar para ser o contratado ideal para ele?
                Qual seus objetivos? O que quer alcançar? No que provavelmente já falhou? Tire inúmeras conclusões sobre o cliente. Quais seus interesses?
                Como posso tirar vantagem disso se quero ser contratado como empresa de marketing digital para eles?

                Também crie a Persona de Abordagem, o tipo de pessoa com a qual ela seria mais receptiva (incluindo gênero, personalidade, posição, estado civil, idade, aparência, tom, trajetória de vida). Como essa persona interage? Que decisões toma? Como é a comunicação dela? Que tipos de post ela faria? Como ela escreve?
                """

                # Gera o relatório com Gemini
                osint_report_output = modelo_linguagem.generate_content(prompt).text

                # Exibe o relatório no Streamlit
                st.subheader("OSINT Report Generated")
                st.markdown(osint_report_output)
        else:
            st.warning("Por favor, preencha pelo menos um campo para gerar o relatório.")
