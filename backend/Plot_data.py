import pandas as pd
from db_config import get_db_engine
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

import numpy as np
import matplotlib.pyplot as plt

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)


def plot_year_values():
    # Convert 'Wartosc' column to numeric
    df['Wartosc'] = pd.to_numeric(df['Wartosc'], errors='coerce')

    # Group by year and calculate sum
    grouped = df.groupby('rok').sum().reset_index()

    # Tworzenie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(grouped['rok'], grouped['Wartosc'], marker='o', label='Rzeczywiste dane')

    # Dostosowanie wykresu
    plt.xlabel('Rok')
    plt.ylabel('Suma wartości')
    plt.title('Suma wartości w danych latach')
    plt.legend()
    plt.grid(True)
    plt.show()


plot_year_values()