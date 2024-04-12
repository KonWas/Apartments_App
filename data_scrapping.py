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
    offers = soup.find_all('div', class_=lambda value: value and value.startswith('tile tile-tile'))[:-1]
    offer_links = [offer.find('a', class_='tabCtrl')['href'] for offer in offers if offer.find('a', class_='tabCtrl')]
    return offer_links

def scrape_offer_details(url):
    """Scrapuje szczegóły oferty z podanego adresu URL."""
    content = open_website(url)
    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        # Extracting the offer header/title
        title = soup.find('h2', class_='header-e').text.strip() if soup.find('h2', class_='header-e') else 'Not provided'

        # Extracting the primary price
        primary_price = soup.find('span', class_='info-primary-price').text.strip().replace('\xa0', ' ') if soup.find('span', class_='info-primary-price') else 'Not provided'

        # Extracting the area
        area = soup.find('span', class_='info-area').text.strip().replace('\xa0', ' ') if soup.find('span', class_='info-area') else 'Not provided'

        # Extracting the level of interest
        interest_level = soup.find('p', class_='par-a').text.strip() if soup.find('p', class_='par-a') else 'Not provided'

        # Basic information
        basic_info = soup.find_all('div', class_='box__attributes--content')
        basic_info = [info.get_text(separator=" ").strip() for info in basic_info]

        # Extracting details from the list
        # details_list = soup.find('ul', class_='list-h')
        # details = {}
        # for li in details_list.find_all('li'):
        #     strong_tag = li.find('strong')
        #     if strong_tag and strong_tag.next_sibling:
        #         key = strong_tag.text.strip().rstrip(':')
        #         value = strong_tag.next_sibling.strip()
        #         details[key] = value
        details_lists = soup.find_all('ul', class_=lambda value: value and value.startswith('list-h'))
        details = {}
        for details_list in details_lists:
            for li in details_list.find_all('li'):
                # Splitting based on the structure of the 'li' elements
                key = li.find('strong').text.strip().rstrip(':') if li.find('strong') else None
                value = li.find('span').text.strip() if li.find('span') else 'Not provided'
                if key:
                    details[key] = value

        offer_details = {
            'title': title,
            'price': primary_price,
            'area': area,
            'interest_level': interest_level,
            'basic_info': basic_info,
            'details': details
        }
    return offer_details

def save_to_csv(offer_details):
    """Zapisuje szczegóły oferty do pliku CSV."""
    if offer_details:
        df = pd.DataFrame([offer_details])
        df.to_csv('offer_details.csv', index=False, mode='a', header=False)

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
                # print("Sukces! Strona została otwarta.")
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
# universal_url = "https://wroclaw.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Wrocław&q={}"
universal_url = "https://wroclaw.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Wrocław:17876&p={}&q=%7B%7D"

# Tworzenie linkow wszystkich kart
# Pierwsza partia linków 21-60
list_of_pages = [universal_url.format(i) for i in range(137, 181)]

# Lista wszystkich ofert
all_offer_links = []
#print(scrape_offer_details("https://wroclaw.nieruchomosci-online.pl/mieszkanie,z-aneksem-kuchennym/24679701.html"))
# Wywołanie funkcji otwierającej stronę
page_number = 137
for url in list_of_pages:
    web_site_content = open_website(url)
    if web_site_content is not None:
        offer_links = get_offers(web_site_content)
        # print(f"Number of offers: {len(offer_links)} On page: {url[-3:]}")
        all_offer_links.extend(offer_links)
        print(f"Page {page_number} scraped. Number of offers: {len(offer_links)}")
        page_number += 1

# # Scrappowanie szczegolow ofert
for offer_link in all_offer_links:
    save_to_csv(scrape_offer_details(offer_link))
