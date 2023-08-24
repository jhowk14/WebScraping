import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_totalcorner_data_csv(url_input=None):
    if url_input == '' or url_input is None:
        url_input = "https://www.totalcorner.com/league/view/13321/"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198 Safari / 537.36"}

    page = 1
    data = []

    while True:
        print("Obtendo Dados... ")
        url = f'{url_input}/page:{page}?copy=yes'
        site = requests.get(url, headers=headers)

        if site.status_code != 200:
            print(f"Request falhou para a página {page}. Encerrando loop.")
            break

        soup = BeautifulSoup(site.content, 'html.parser')
        table_body = soup.find('tbody')

        if not table_body:
            print(f"Elemento 'tbody' não encontrado na página {page}. Encerrando loop.")
            break

        table_rows = table_body.find_all('tr')

        for row in table_rows:
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td'])]
            if row_data:
                data.append(row_data)
        print(f"Dados da página {page} extraídos com sucesso.")
        page += 1

        columns = [
            "start_time", "match_status", "home_team", "home_goal", "away_goal",
            "away_team", "handicap", "home_corner", "away_corner", "ht_home_corner",
            "ht_away_corner", "asian_corner", "corner_o_u", "goals", "goals_o_u",
            "home_attack", "away_attack", "home_shots", "away_shots"
        ]

        df = pd.DataFrame(data, columns=columns)

        excel_filename = "match_data.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Arquivo CSV criado com sucesso!")

input_url = input('Informe a URL base (ou pressione Enter para usar a padrão: https://www.totalcorner.com/league/view/13321/): \n')
scrape_totalcorner_data_csv(input_url)



