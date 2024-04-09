import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def parse_card(card):
    """Parsuje pojedynczą kartę i zwraca dane jako słownik."""
    area_element = card.find('span', {'class': 'css-643j0o'})
    area = area_element.get_text(strip=True).split()[0].replace(",", ".") if area_element else None

    price_element = card.find('p', {'data-testid': 'ad-price'})
    price = ''.join(filter(str.isdigit, price_element.get_text(strip=True))) if price_element else None

    location_element = card.find('p', {'data-testid': 'location-date'})
    location = location_element.get_text(strip=True).split("-")[0] if location_element else None
    
    return {
        'area': float(area) if area else None,
        'price': int(price) if price else None,
        'location': location
    }

def get_cards_from_page(url, session):
    """Pobiera i przetwarza karty z pojedynczej strony."""
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        time.sleep(5)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', {'data-cy': 'l-card', 'data-testid': 'l-card'})
    return [parse_card(card) for card in cards]

# main part
universal_url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/wroclaw/?page={}"
list_of_pages = [universal_url.format(i) for i in range(1, 26)]

records = []  # Lista na wszystkie rekordy

with requests.Session() as session:
    for url in list_of_pages:
        records.extend(get_cards_from_page(url, session))

# Konwersja rekordów do DataFrame i zapis do pliku CSV
df = pd.DataFrame(records)
print(df.head())
df.to_csv('olx_wroclaw.csv', index=False)
