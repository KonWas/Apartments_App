# read data from csv change all polish letters to english and make all strings title case
import pandas as pd

df = pd.read_csv('data_cleaned_formated.csv', encoding='utf-8')

dictionary = {
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ł': 'l',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ź': 'z',
    'ż': 'z'
}

# change location names
df['location'] = df['location'].str.lower()
for key, value in dictionary.items():
    df['location'] = df['location'].str.replace(key, value)
df['location'] = df['location'].str.title()

# change state names
df['state'] = df['state'].str.lower()
for key, value in dictionary.items():
    df['state'] = df['state'].str.replace(key, value)
df['state'] = df['state'].str.title()

# change market primary to Pierwotny and secondary to Wtórny
df['market'] = df['market'].str.lower()
df['market'] = df['market'].str.replace('primary', 'Pierwotny')
df['market'] = df['market'].str.replace('secondary', 'Wtorny')

df.to_csv('apartments.txt', index=True, sep='\t', encoding='utf-8')