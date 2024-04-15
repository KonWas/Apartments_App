import pandas as pd

df = pd.read_csv('data_cleaned_formated.csv')

print(df.head(5))

# For column location, parking, state, furnished, market print all unique values and how many times they appear in the dataset
print(df['location'].value_counts())
for i in df['location'].value_counts().index:
    print(i, df['location'].value_counts()[i])
print(df['parking'].value_counts())
print(df['state'].value_counts())
print(df['furnished'].value_counts())
print(df['market'].value_counts())

def district_analysis() -> None:
    """Function to analyze the number of properties in each district."""
    # Change location to one of these: Stare Miast, Krzyki, Fabryczna, Psie Pole, Śródmieście
    osiedla_dzielnice = {
        "Stare Miasto": ["Stare Miasto", "Ołbin", "Wrocław", "Świdnicka", "Więzienna", "Nożownicza", "Włodkowica"],
        "Krzyki": ["Krzyki", "Partynice", "Wojszyce", "Klecina", "Borek", "Tarnogaj", "Oporów", "Jagodno", "Gaj", "Krzyk", "Księże Małe", "Księże Wielkie", "Poświętne", "Ołtaszyn", "Przedmieście Oławskie"],
        "Fabryczna": ["Grabiszyn", "Grabiszyn-Grabiszynek", "Muchobór Wielki", "Nowy Dwór", "Fabryczna", "Gądów Mały", "Gądów-Popowice Południowe", "Muchobór Mały", "Pilczyce", "Żerniki", "Maślice", "Stabłowice", "Zakrzów"],
        "Psie Pole": ["Psie Pole", "Swojczyce", "Różanka", "Kowale", "Sołtysowice", "Osobowice", "Karłowice", "Kleczków", "Lipa Piotrowska", "Popowice", "Kępa Mieszczańska", "Brochów", "Bieńkowice", "Szczepin"],
        "Śródmieście": ["Nadodrze", "Śródmieście", "Plac Grunwaldzki", "Huby", "Przedmieście Świdnickie", "Zaporoska"]
    }

    sum_stare_miasto = 0
    sum_krzyki = 0
    sum_fabryczna = 0
    sum_psie_pole = 0
    sum_srodmiescie = 0
    sum_of_inne = 0

    with open('locations.txt', 'r') as file:
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].rstrip()
        for line in data:
            parts = line.split()
            osiedle = ' '.join(parts[:-1])
            count = int(parts[-1])
            flag = False
            for dzielnica, osiedla in osiedla_dzielnice.items():
                if osiedle in osiedla:
                    if dzielnica == "Stare Miasto":
                        sum_stare_miasto += count
                        flag = True
                    elif dzielnica == "Krzyki":
                        sum_krzyki += count
                        flag = True
                    elif dzielnica == "Fabryczna":
                        sum_fabryczna += count
                        flag = True
                    elif dzielnica == "Psie Pole":
                        sum_psie_pole += count
                        flag = True
                    elif dzielnica == "Śródmieście":
                        sum_srodmiescie += count
                        flag = True
            if not flag:
                sum_of_inne += count
                # print("Nieznana dzielnica:", osiedle, count)

        print("Suma Stare Miasto:", sum_stare_miasto)
        print("Suma Krzyki:", sum_krzyki)
        print("Suma Fabryczna:", sum_fabryczna)
        print("Suma Psie Pole:", sum_psie_pole)
        print("Suma Śródmieście:", sum_srodmiescie)
        print("Suma Inne:", sum_of_inne)
