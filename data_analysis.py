import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def load_data() -> pd.DataFrame:
    """Function to load the cleaned and formatted data."""
    return pd.read_csv('data_cleaned_formated.csv')


def show_unique_values(df: pd.DataFrame, column: str) -> None:
    """Function to show unique values and their counts in a column."""
    # print(df[column].value_counts())
    print(f"{'-' * 15} {column} {'-' * 15}")
    for i in df[column].value_counts().index:
        print(i, df[column].value_counts()[i])
    print()


def plot_data(df: pd.DataFrame, column: str) -> None:
    """Function to plot the data."""
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=column)
    plt.title(f'{column} distribution')
    plt.show()

def price_area_stats_for_each_location() -> None:
    """Function to show the price and area statistics for each location."""
     # For each location print max, min price and area
    locations = df['location'].unique()
    for location in locations:
        print(f"{'-' * 15} {location} {'-' * 15}")
        print(f"Max price: {df[df['location'] == location]['price'].max()}")
        print(f"Min price: {df[df['location'] == location]['price'].min()}")
        print(f"Max area: {df[df['location'] == location]['area'].max()}")
        print(f"Min area: {df[df['location'] == location]['area'].min()}")
        print()

    # Plot price vs area for each location
    # for location in locations:
    #     plt.figure(figsize=(10, 6))
    #     sns.scatterplot(data=df[df['location'] == location], x='area', y='price')
    #     plt.title(f'Price vs Area in {location}')
    #     plt.show()
    # Plot price vs are for each location on one figure

    plt.figure(figsize=(10, 6))
    for location in locations:
        sns.scatterplot(data=df[df['location'] == location], x='area', y='price', label=location)
    plt.title('Price vs Area for each location')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    df = load_data()

    print(df.head(5))


    # Show unique values in the location, rooms, floor, year, parking, state, furnished, market
    columns_to_show = ['location', 'rooms', 'floor', 'year', 'parking', 'state', 'furnished', 'market']
    for element in columns_to_show:
        show_unique_values(df, element)

    # Plot the data
    columns_to_exclude = ['year', 'state']
    for element in columns_to_show:
        if element not in columns_to_exclude:
            plot_data(df, element)

    # Price and area statistics for each location
    price_area_stats_for_each_location()


   