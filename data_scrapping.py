import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# def parse_card(card):
#     """Parsuje pojedynczą kartę i zwraca dane jako słownik."""
#     area_element = card.find('span', {'class': 'css-643j0o'})
#     area = area_element.get_text(strip=True).split()[0].replace(",", ".") if area_element else None

#     price_element = card.find('p', {'data-testid': 'ad-price'})
#     price = ''.join(filter(str.isdigit, price_element.get_text(strip=True))) if price_element else None

#     location_element = card.find('p', {'data-testid': 'location-date'})
#     location = location_element.get_text(strip=True).split("-")[0] if location_element else None
    
#     return {
#         'area': float(area) if area else None,
#         'price': int(price) if price else None,
#         'location': location
#     }

# def get_cards_from_page(url, session):
#     """Pobiera i przetwarza karty z pojedynczej strony."""
#     try:
#         response = session.get(url, timeout=10)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         time.sleep(5)
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')
#     cards = soup.find_all('div', {'data-cy': 'l-card', 'data-testid': 'l-card'})
#     return [parse_card(card) for card in cards]

# # main part
# universal_url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/wroclaw/?page={}"
# list_of_pages = [universal_url.format(i) for i in range(1, 26)]

# records = []  # Lista na wszystkie rekordy

# with requests.Session() as session:
#     for url in list_of_pages:
#         records.extend(get_cards_from_page(url, session))

# # Konwersja rekordów do DataFrame i zapis do pliku CSV
# df = pd.DataFrame(records)
# print(df.head())
# df.to_csv('olx_wroclaw.csv', index=False)

# def parse_offer(offer):
#     pass

# def get_offer_from_url(url, session):
#     """Pobiera i przetwarza oferty z pojedynczej strony."""
#     try:
#         response = session.get(url, timeout=10)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         time.sleep(5)
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')
#     offers = soup.find_all('div', {'class': 'offer-item-details'})
#     return [parse_offer(offer) for offer in offers]

# universla_url = "https://wroclaw.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Wrocław&q=&p={}"
# list_of_pages = [universla_url.format(i) for i in range(1, 101)]

# records = []  # Lista na wszystkie rekordy

# with requests.Session() as session:
#     for url in list_of_pages:
#         records.extend(get_offer_from_url(url, session))


def get_offers(web_site_content):
    """Pobiera oferty z zawartości strony."""
    soup = BeautifulSoup(web_site_content, 'html.parser')
    offers = soup.find_all('div', {'class': 'offer-item-details'})
    return offers

def open_website(url, max_retries=5, delay=5):
    """Otwiera stronę internetową i zwraca jej zawartość."""
    # Definiowanie nagłówków przeglądarki, aby symulować zwykłe zapytanie przeglądarki
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for attempt in range(max_retries):
        try:
            # Wykonywanie zapytania GET z dodanymi nagłówkami
            response = requests.get(url, headers=headers)
            
            # Sprawdzanie, czy zapytanie się powiodło
            if response.status_code == 200:
                print("Sukces! Strona została otwarta.")
                return response.content
            elif response.status_code == 503:
                # Obsługa tymczasowej niedostępności serwera
                print(f"Serwis tymczasowo niedostępny. Status: {response.status_code}. Próba {attempt+1} z {max_retries}. Ponawiam próbę po {delay} sekundach...")
                time.sleep(delay)  # Odczekanie przed kolejną próbą
            else:
                # Obsługa innych odpowiedzi serwera
                print(f"Błąd: Otrzymano status {response.status_code}. Przerwanie prób.")
                break
        except requests.exceptions.RequestException as e:
            # Obsługa wyjątków, takich jak problemy z siecią
            print(f"RequestException: {e}. Próba {attempt+1} z {max_retries}.")
            time.sleep(delay)

    print("Nie udało się otworzyć strony po maksymalnej liczbie prób.")
    return None

# Adres URL strony z ogłoszeniami
universal_url = "https://wroclaw.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Wrocław&q={}"
# Tworzenie linkow wszystkich kart
list_of_pages = [universal_url.format(i) for i in range(1, 101)]
# Wywołanie funkcji otwierającej stronę
for url in list_of_pages:
    web_site_content = open_website(url)
    if web_site_content is not None:
        offers = get_offers(web_site_content)
        for offer in offers:
            print(offer)

