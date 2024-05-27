import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediction_models import remove_outliers_wider
import os

# Get the directory of the current file
current_dir = os.path.dirname(__file__)
# Go up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(current_dir, '..'))
# Construct the path to the data_cleaned_formated.csv file
data_path = os.path.join(project_root, 'data_cleaned_formated.csv')
data = pd.read_csv(data_path)

data = remove_outliers_wider(data)
data = data[(data['price'] <= 1250000)]
data = data[(data['price'] >= 100000)]
data = data[(data['area'] <= 80)]
data = data[(data['floor'] <= 29)]
data = data[(data['rooms'] <= 7)]
data = data[(data['year'] >= 1925)]

def price_vs_area() -> plt.Figure:
    """Create a scatter plot of price vs area."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=data, x='area', y='price', ax=ax)
    ax.set_title('Cena vs Powierzchnia')
    ax.set_xlabel('Powierzchnia (m²)')
    ax.set_ylabel('Cena (PLN)')
    ax.grid(True)
    return fig

def avg_price_per_district() -> plt.Figure:
    """Create a bar plot of average price per district."""
    fig, ax = plt.subplots(figsize=(8, 4))
    avg_price_per_district = data.groupby('location')['price'].mean().sort_values()
    avg_price_per_district.plot(kind='bar', ax=ax)
    ax.set_title('Średnia Cena w Dzielnicy')
    ax.set_xlabel('Dzielnica')
    ax.set_ylabel('Średnia Cena (PLN)')
    ax.grid(True)
    return fig

def price_distribution() -> plt.Figure:
    """Create a histogram of price distribution."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data['price'], kde=True, ax=ax)
    ax.set_title('Rozkład Cen')
    ax.set_xlabel('Cena (PLN)')
    ax.set_ylabel('Częstotliwość')
    ax.grid(True)
    return fig

def price_vs_rooms() -> plt.Figure:
    """Create a box plot of price vs number of rooms."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=data, x='rooms', y='price', ax=ax)
    ax.set_title('Cena vs Liczba Pokoi')
    ax.set_xlabel('Liczba Pokoi')
    ax.set_ylabel('Cena (PLN)')
    ax.grid(True)
    return fig

def price_vs_year() -> plt.Figure:
    """Create a scatter plot of price vs year of construction."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=data, x='year', y='price', ax=ax)
    ax.set_title('Cena vs Rok Budowy')
    ax.set_xlabel('Rok Budowy')
    ax.set_ylabel('Cena (PLN)')
    ax.grid(True)
    return fig

def price_vs_floor() -> plt.Figure:
    """Create a box plot of price vs floor."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=data, x='floor', y='price', ax=ax)
    ax.set_title('Cena vs Piętro')
    ax.set_xlabel('Piętro')
    ax.set_ylabel('Cena (PLN)')
    ax.grid(True)
    return fig