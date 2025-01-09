def check_website_performance(base_url):
    """
    Função para verificar o desempenho do site e métricas de SEO para todas as páginas vinculadas ao URL base.
    Gera uma string formatada com métricas de desempenho e SEO para cada página.

    Parâmetros:
        base_url (str): O URL base do site.

    Retorna:
        str: Uma string formatada com as métricas de desempenho e SEO.
    """
    try:
        # Medir desempenho do URL base
        start_time = time.time()
        response = requests.get(base_url)
        base_load_time = time.time() - start_time

        if response.status_code != 200:
            return f"Erro ao acessar {base_url}. Código de status: {response.status_code}"

        # Analisar conteúdo do URL base
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos os links na página
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') or base_url in href:
                links.add(href if base_url in href else base_url + href)

        # Coletar dados de desempenho e SEO
        data = []
        for link in links:
            try:
                start_time = time.time()
                page_response = requests.get(link)
                load_time = time.time() - start_time

                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')

                    # Extrair métricas
                    title = page_soup.title.string if page_soup.title else "Sem título"
                    meta_description = page_soup.find("meta", attrs={"name": "description"})
                    meta_description = meta_description["content"] if meta_description else "Sem descrição meta"
                    h1_tags = [h1.get_text(strip=True) for h1 in page_soup.find_all("h1")]
                    word_count = len(page_soup.get_text().split())
                    robots_meta = page_soup.find("meta", attrs={"name": "robots"})
                    robots_meta = robots_meta["content"] if robots_meta else "Sem meta de robôs"
                    canonical_tag = page_soup.find("link", attrs={"rel": "canonical"})
                    canonical_tag = canonical_tag["href"] if canonical_tag else "Sem tag canônica"

                    data.append(
                        f"URL: {link}\n"
                        f"Status Code: {page_response.status_code}\n"
                        f"Tempo de Carregamento: {round(load_time, 2)}s\n"
                        f"Tamanho do Conteúdo: {round(len(page_response.content) / 1024, 2)} KB\n"
                        f"Título: {title}\n"
                        f"Meta Descrição: {meta_description}\n"
                        f"Tags H1: {', '.join(h1_tags)}\n"
                        f"Contagem de Palavras: {word_count}\n"
                        f"Meta de Robôs: {robots_meta}\n"
                        f"Tag Canônica: {canonical_tag}\n\n"
                    )
                else:
                    data.append(f"URL: {link} - Erro ao carregar. Código de status: {page_response.status_code}\n\n")
            except Exception as e:
                data.append(f"Erro ao acessar {link}: {e}\n\n")

        return "\n".join(data)

    except Exception as e:
        return f"Ocorreu um erro: {e}"


def scrape_all_texts(base_url):
    """
    Função para raspar todos os textos de todas as páginas vinculadas ao URL base e salvar em um arquivo de texto.

    Parâmetros:
        base_url (str): O URL base do site.

    Retorna:
        str: Todo o texto raspado formatado como uma única string.
    """
    try:
        response = requests.get(base_url)
        if response.status_code != 200:
            return f"Erro ao acessar {base_url}. Código de status: {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos os links na página
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/') or base_url in href:
                links.add(href if base_url in href else base_url + href)

        # Raspar textos
        all_text = ""
        for link in links:
            try:
                page_response = requests.get(link)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    page_title = page_soup.title.string if page_soup.title else "Sem título"
                    page_text = page_soup.get_text(separator='\n', strip=True)
                    all_text += f"### {page_title} ({link})\n\n{page_text}\n\n"
            except Exception as e:
                all_text += f"Erro ao raspar {link}: {e}\n\n"

        # Salvar em um arquivo de texto
        with open('website_texts.txt', 'w', encoding='utf-8') as file:
            file.write(all_text)

        return all_text

    except Exception as e:
        return f"Ocorreu um erro: {e}"
