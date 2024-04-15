import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


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

        title = soup.find('h2', class_='header-e').text.strip() if soup.find('h2', class_='header-e') else 'Not provided'
        primary_price = soup.find('span', class_='info-primary-price').text.strip().replace('\xa0', ' ') if soup.find('span', class_='info-primary-price') else 'Not provided'
        area = soup.find('span', class_='info-area').text.strip().replace('\xa0', ' ') if soup.find('span', class_='info-area') else 'Not provided'
        interest_level = soup.find('p', class_='par-a').text.strip() if soup.find('p', class_='par-a') else 'Not provided'

        basic_info = soup.find_all('div', class_='box__attributes--content')
        basic_info = [info.get_text(separator=" ").strip() for info in basic_info]

        details_lists = soup.find_all('ul', class_=lambda value: value and value.startswith('list-h'))
        details = {}
        for details_list in details_lists:
            for li in details_list.find_all('li'):
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
    # define headers for the request to avoid 403 error
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print("Successfully opened the website.")
                return response.content
            elif response.status_code == 503:
                # temporary unavailable
                print(f"Status code 503. Attempt {attempt+1} of {max_retries}.")
                time.sleep(delay)
            else:
                # other status codes
                print(f"Error: {response.status_code}. Attempt {attempt+1} of {max_retries}.")
                break
        except requests.exceptions.RequestException as e:
            # other exceptions such as timeout
            print(f"RequestException: {e}. Attempt {attempt+1} of {max_retries}.")
            time.sleep(delay)

    print("Unable to open the website after max retries attempts.")
    return None

if __name__ == '__main__':
    universal_url = "https://wroclaw.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Wrocław:17876&p={}&q=%7B%7D"

    list_of_pages = [universal_url.format(i) for i in range(1, 181)]
    all_offer_links = []

    for url in list_of_pages:
        web_site_content = open_website(url)
        if web_site_content is not None:
            offer_links = get_offers(web_site_content)
            all_offer_links.extend(offer_links)

    for offer_link in all_offer_links:
        save_to_csv(scrape_offer_details(offer_link))
