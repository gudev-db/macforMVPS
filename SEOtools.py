import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def check_website_performance(base_url):
      """
    Função para verificar a saúde do site com métricas detalhadas de SEO, desempenho e estrutura.

    Parâmetros:
        base_url (str): O URL base do site.

    Retorna:
        str: Relatório detalhado sobre a saúde do site.
    """
    try:
        # Medir desempenho do URL base
        start_time = time.time()
        response = requests.get(base_url)
        base_load_time = time.time() - start_time

        if response.status_code != 200:
            return f"Erro ao acessar {base_url}. Código de status: {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar links na página
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') or base_url in href:
                links.add(href if base_url in href else base_url + href)

        # Verificar arquivos robots.txt e sitemap.xml
        robots_url = base_url.rstrip('/') + "/robots.txt"
        sitemap_url = base_url.rstrip('/') + "/sitemap.xml"
        robots_status = requests.get(robots_url).status_code
        sitemap_status = requests.get(sitemap_url).status_code

        # Coletar dados de todas as páginas
        data = []
        for link in links:
            try:
                start_time = time.time()
                page_response = requests.get(link)
                load_time = time.time() - start_time

                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')

                    # Extração de métricas detalhadas
                    title = page_soup.title.string if page_soup.title else "Sem título"
                    meta_description = page_soup.find("meta", attrs={"name": "description"})
                    meta_description = meta_description["content"] if meta_description else "Sem descrição meta"
                    h_tags = {f"H{i}": len(page_soup.find_all(f"h{i}")) for i in range(1, 7)}
                    word_count = len(page_soup.get_text().split())
                    robots_meta = page_soup.find("meta", attrs={"name": "robots"})
                    robots_meta = robots_meta["content"] if robots_meta else "Sem meta de robôs"
                    canonical_tag = page_soup.find("link", attrs={"rel": "canonical"})
                    canonical_tag = canonical_tag["href"] if canonical_tag else "Sem tag canônica"
                    links_internal = len([a['href'] for a in page_soup.find_all('a', href=True) if base_url in a['href']])
                    links_external = len([a['href'] for a in page_soup.find_all('a', href=True) if base_url not in a['href']])
                    https_status = "HTTPS Ativo" if "https://" in link else "Sem HTTPS"
                    content_length = round(len(page_response.content) / 1024, 2)

                    data.append(
                        f"URL: {link}\n"
                        f"Status Code: {page_response.status_code}\n"
                        f"Tempo de Carregamento: {round(load_time, 2)}s\n"
                        f"Tamanho do Conteúdo: {content_length} KB\n"
                        f"Título: {title}\n"
                        f"Meta Descrição: {meta_description}\n"
                        f"Hierarquia de Cabeçalhos: {h_tags}\n"
                        f"Contagem de Palavras: {word_count}\n"
                        f"Links Internos: {links_internal}\n"
                        f"Links Externos: {links_external}\n"
                        f"Meta de Robôs: {robots_meta}\n"
                        f"Tag Canônica: {canonical_tag}\n"
                        f"HTTPS: {https_status}\n\n"
                    )
                else:
                    data.append(f"URL: {link} - Erro ao carregar. Código de status: {page_response.status_code}\n\n")

            except Exception as e:
                data.append(f"Erro ao acessar {link}: {e}\n\n")

        # Resumo do site
        summary = (
            f"Robots.txt Status: {'Encontrado' if robots_status == 200 else 'Não Encontrado'}\n"
            f"Sitemap.xml Status: {'Encontrado' if sitemap_status == 200 else 'Não Encontrado'}\n\n"
        )

        # Unir os dados
        result = summary + "\n".join(data)
        return result

    except Exception as e:
        return f"Ocorreu um erro: {e}"

def scrape_all_texts(base_url):
    """
    Function to scrape all texts from all pages linked from the base URL and save to a text file.

    Parameters:
        base_url (str): The base URL of the website.

    Returns:
        str: All scraped text as a single string.
    """
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Error accessing {base_url}, Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the page
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') or base_url in href:
                links.add(href if base_url in href else base_url + href)

        # Scrape text from all links
        all_text = ""
        document_structure = []

        for link in links:
            try:
                page_response = requests.get(link)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    page_title = page_soup.title.string if page_soup.title else "No Title"
                    page_text = page_soup.get_text(separator='\n', strip=True)
                    all_text += f"### {page_title} ({link})\n\n{page_text}\n\n"
                    document_structure.append(f"### {page_title} ({link})\n\n{page_text}\n\n")
            except Exception as e:
                print(f"Error scraping {link}: {e}")

        # Save to text file
        with open('website_texts.txt', 'w', encoding='utf-8') as file:
            for section in document_structure:
                file.write(section)

        print("All website texts saved to 'website_texts.txt'")
        return all_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return


