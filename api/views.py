import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.http import JsonResponse
import re
import json


# Função para gerar o endpoint com o ano e mês vigentes
def generate_endpoint():
    now = datetime.now()
    year = now.year
    month = now.strftime('%m')  # Formato MM
    return f"https://crimesnewsrj.blogspot.com/{year}/{month}/"

# Caminho para o arquivo TXT que armazenará os subdomínios
subdomains_file = "subdomains.txt"

# Função para carregar subdomínios existentes
def load_existing_subdomains():
    if os.path.exists(subdomains_file):
        with open(subdomains_file, 'r') as file:
            return set(file.read().splitlines())
    return set()

# Função para salvar novos subdomínios
def save_new_subdomains(new_subdomains):
    with open(subdomains_file, 'a') as file:
        for subdomain in new_subdomains:
            file.write(f"{subdomain}\n")

# Função para filtrar links válidos de notícias
def filter_news_links(links):
    now = datetime.now()
    year = now.year
    month = now.strftime('%m')
    
    # Regex para validar o padrão de notícias
    pattern = re.compile(rf'^https://crimesnewsrj\.blogspot\.com/{year}/{month}/[^/]+\.html$')
    
    valid_links = set()
    for link in links:
        # Remove fragmentos como #comments
        clean_link = link.split('#')[0]
        
        # Verifica se o link corresponde ao padrão de notícias
        if pattern.match(clean_link):
            valid_links.add(clean_link)
    
    return valid_links

# Função para fazer scraping dos links
def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            links.add(href)

    return links

# Função principal
def pegar_dados_CN(request):
    # Gerar o endpoint com o ano e mês vigentes
    base_url = generate_endpoint()
    print(f"Endpoint atual: {base_url}")

    existing_subdomains = load_existing_subdomains()
    current_subdomains = scrape_links(base_url)

    # Filtrar apenas links válidos de notícias
    valid_subdomains = filter_news_links(current_subdomains)

    # Encontrar novos subdomínios
    new_subdomains = valid_subdomains - existing_subdomains

    if new_subdomains:
        print(f"Novos subdomínios encontrados: {new_subdomains}")
        save_new_subdomains(new_subdomains)

        # Processar cada novo subdomínio
        results = {}
        for subdomain in new_subdomains:
            print(f"Processando o subdomínio: {subdomain}")
            # Chama a função pegar_dados_CN_original diretamente
            response = pegar_dados_CN_original(request, subdomain)
            results[subdomain] = response.content.decode('utf-8')  # Decodifica o JSON

        print("Resultados da view:")
        print(results)
        return JsonResponse(results)
    else:
        print("Nenhum novo subdomínio encontrado.")
        return JsonResponse({"message": "Nenhum novo subdomínio encontrado."})

# Sua view original para scraping de notícias
def pegar_dados_CN_original(request, url=None):
    context = {}
    headers = {'User-Agent': 'Mozilla/5.0'}

    # URL passada como parâmetro
    if not url:
        url = request.POST.get('url')
        if not url:
            return JsonResponse({"error": "URL não fornecida"}, status=400)

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return JsonResponse({"error": "Falha ao obter notícias"}, status=500)

    soup = BeautifulSoup(response.text, 'html.parser')
    news1 = soup.find(class_='post-body entry-content float-container')
    
    context['news1'] = news1.text.strip() if news1 else "Não disponível"

    return JsonResponse(context)



