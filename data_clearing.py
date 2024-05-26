import pandas as pd
import ast
from typing import Optional


def extract_information() -> None:
    """Function to extract information from the `basic_info` and `detailed_info` columns.
    1. Extract the number of rooms, floor, total floors, year, parking, and state from the `basic_info` column.
    2. Extract the furnished and market information from the `detailed_info` column.
    3. Drop unnecessary columns.
    4. Save the cleaned data to a new CSV file.
    """
    
    # Load data
    data = pd.read_csv('offer_details.csv')

    # Function to extract information from the `basic_info` column
    def extract_from_basic_info(info: str, key: str) -> Optional[str]:
        try:
            info_dict = ast.literal_eval(info)
            for item in info_dict:
                if key in item:
                    return item.split(': ')[1].strip()
        except (ValueError, SyntaxError):
            return None

    # Function to extract information from the `detailed_info` column
    def extract_from_detailed_info(info: str, key: str) -> str:
        try:
            info_dict = ast.literal_eval(info.replace('\xa0', ' '))
            return info_dict.get(key, 'N/A')
        except (ValueError, SyntaxError):
            return 'N/A'

    # Extracting information from the `basic_info` and `detailed_info` columns
    data['rooms'] = data['basic_info'].apply(lambda x: extract_from_basic_info(x, 'Liczba pokoi'))
    data['floor'] = data['basic_info'].apply(lambda x: extract_from_basic_info(x, 'Piętro').split(' / ')[0] if extract_from_basic_info(x, 'Piętro') else None)
    data['total_floors'] = data['basic_info'].apply(lambda x: extract_from_basic_info(x, 'Piętro').split(' / ')[1] if '/' in extract_from_basic_info(x, 'Piętro') else None)
    data['year'] = data['basic_info'].apply(lambda x: extract_from_basic_info(x, 'Rok budowy'))
    data['parking'] = data['basic_info'].apply(lambda x: extract_from_basic_info(x, 'Miejsce parkingowe'))
    data['state'] = data['basic_info'].apply(lambda x: extract_from_basic_info(x, 'Stan mieszkania'))

    data['furnished'] = data['detailed_info'].apply(lambda x: 'Tak' if 'umeblowane' in x else 'Nie')
    data['market'] = data['detailed_info'].apply(lambda x: extract_from_detailed_info(x, 'Rynek'))

    # Dropping unnecessary columns
    data.drop(['basic_info', 'detailed_info', 'call'], axis=1, inplace=True)

    # Saving the cleaned data to a new CSV file
    data.to_csv('data_cleaned.csv', index=False)
    print(data.head())


def clear_format_data() -> None:
    """Function to format the dataset.
    1. Remove missing values.
    2. Change 'parter' to 0 in the 'floor' column.
    3. Set all values to the correct data types.
    4. Save the cleaned and formatted data to a new CSV file.
    """
    
    # Load cleared data
    data = pd.read_csv('data_cleaned.csv')

    # Basic information about the dataset
    print(data.info())

    # Check for missing values
    data_clean = data.dropna()
    data_clean = data_clean[~data_clean.isin(['-', 'N/A', 'N/A ']).any(axis=1)]

    # Display the number of records after removing missing values
    print(f"Number of records after removing missing data: {len(data_clean)}")

    # Change 'parter' to 0 in the 'floor' column
    data_clean['floor'] = data_clean['floor'].apply(lambda x: 0 if x == 'parter' else x)

    # Setting all values to correct data types
    data_clean['price'] = data_clean['price'].str.replace(' zł', '').str.replace(' ', '').str.replace(',', '.').astype(float)
    data_clean['area'] = data_clean['area'].str.replace(' m²', '').str.replace(' ', '').str.replace(',', '.').astype(float)
    data_clean['rooms'] = data_clean['rooms'].astype(int)
    data_clean['floor'] = data_clean['floor'].astype(int)
    data_clean['total_floors'] = data_clean['total_floors'].astype(int)
    data_clean['year'] = data_clean['year'].astype(int)

    # Change location to district only
    data_clean['location'] = data_clean['location'].apply(lambda x: x.split(',')[1].strip() if len(x.split(',')) == 4 else x.split(',')[0].strip())

    # Change parking to 1 if 'tak' or "garaż" else 0
    data_clean['parking'] = data_clean['parking'].apply(lambda x: 1 if 'tak' in x.lower() or 'garaż' in x.lower() else 0)

    # Map state values to standardized categories
    data_clean['state'] = data_clean['state'].apply(lambda x: 'bardzo dobry' if 'wysoki standard' in x.lower() or 'nowe wykończone' in x.lower() else 'do remontu' if 'do odświeżenia' in x.lower() else x)

    # Change furnished to 1 if 'tak' else 0
    data_clean['furnished'] = data_clean['furnished'].apply(lambda x: 1 if 'tak' in x.lower() else 0)

    # Change market to primary or secondary
    data_clean['market'] = data_clean['market'].apply(lambda x: 'primary' if 'pierwotny' in x.lower() else 'secondary')

    # Save cleaned and formatted data to a new CSV file
    data_clean.to_csv('data_cleaned_formated.csv', index=False)

    # Display the first 5 records of the cleaned and formatted data
    print(data_clean.head())


def location_to_district() -> None:
    """Function to change the location to the district only.
    1. If the location is split by a comma and the length is 4, take the second element.
    2. If the location is split by a comma and the length is not 4, take the first element.
    3. Save the cleaned data to a new CSV file.
    """
    
    # Load cleaned and formatted data
    data = pd.read_csv('data_cleaned_formated.csv')

    # Define districts and their corresponding locations
    districts = {
        "Stare Miasto": ["Stare Miasto", "Ołbin", "Wrocław", "Świdnicka", "Więzienna", "Nożownicza", "Włodkowica"],
        "Krzyki": ["Krzyki", "Partynice", "Wojszyce", "Klecina", "Borek", "Tarnogaj", "Oporów", "Jagodno", "Gaj", "Krzyk", "Księże Małe", "Księże Wielkie", "Poświętne", "Ołtaszyn", "Przedmieście Oławskie"],
        "Fabryczna": ["Fabryczna", "Grabiszyn", "Grabiszyn-Grabiszynek", "Muchobór Wielki", "Nowy Dwór", "Fabryczna", "Gądów Mały", "Gądów-Popowice Południowe", "Muchobór Mały", "Pilczyce", "Żerniki", "Maślice", "Stabłowice", "Zakrzów"],
        "Psie Pole": ["Psie Pole", "Swojczyce", "Różanka", "Kowale", "Sołtysowice", "Osobowice", "Karłowice", "Kleczków", "Lipa Piotrowska", "Popowice", "Kępa Mieszczańska", "Brochów", "Bieńkowice", "Szczepin"],
        "Śródmieście": ["Nadodrze", "Śródmieście", "Plac Grunwaldzki", "Huby", "Przedmieście Świdnickie", "Zaporoska"]
    }

    # Function to find the district based on location
    def find_district(location: str) -> str:
        for district, locations in districts.items():
            if location in locations:
                return district
        return "Inne"

    data['location'] = data['location'].apply(find_district)

    print(data['location'].value_counts())

    # Save the cleaned data to a new CSV file
    data.to_csv('data_cleaned_formated.csv', index=False)


if __name__ == '__main__':
    extract_information()
    clear_format_data()
    location_to_district()
    df = pd.read_csv('data_cleaned_formated.csv')
    print(df.info())
    print(df.head())
