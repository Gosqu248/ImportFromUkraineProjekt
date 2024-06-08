import pandas as pd
from db_config import get_db_engine
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.ticker as ticker
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)



def predict_sum_for_years(years, model_type='Linear'):
    predictions = {}
    # Filter data up to max year in years
    df_filtered = df[df['rok'] <= max(years)]

    # Convert 'Wartosc' column to numeric
    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')

    # Group by year and calculate sum
    grouped = df_filtered.groupby('rok').sum().reset_index()

    # Prepare data for regression
    X = grouped['rok'].values.reshape(-1, 1)
    y = grouped['Wartosc'].values

    # Fit regression model
    # Fit linear regression model
    if model_type == 'Linear':
        model = LinearRegression()
    elif model_type == 'DecisionTree':
        model = DecisionTreeRegressor()
    elif model_type == 'RandomForest':
        model = RandomForestRegressor()
    elif model_type == 'KNeighbors':
        model = KNeighborsRegressor()
    else:
        raise ValueError(f"Invalid model_type: {model_type}")
    model.fit(X, y)

    # Make prediction for each year
    for year in years:
        prediction = model.predict(np.array([[year]]))
        predictions[year] = prediction[0]
        print(f"Przewidywana suma dla {year} roku: {prediction[0]}")

    return predictions, model


def plot_predictions(end_year, model_type='Linear'):
    # Create a list of years from 2024 to end_year
    years = list(range(2024, end_year + 1))

    # Pobierz przewidywaną wartość dla danego roku oraz model regresji liniowej
    predicted_sums, model = predict_sum_for_years(years, model_type)

    # Przygotowanie danych do wykresu
    df_filtered = df[df['rok'] <= end_year]
    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')
    grouped = df_filtered.groupby('rok').sum().reset_index()

    # Tworzenie wykresu
    plt.figure(figsize=(10, 6))

    # Dodanie linii regresji
    future_years = np.arange(2010, end_year + 1).reshape(-1, 1)
    future_predictions = model.predict(future_years)
    plt.plot(future_years, future_predictions, linestyle='-', color='green', label='Linia regresji')

    # Dodanie przewidywanej wartości do danych
    for year in years:
        all_years = np.append(grouped['rok'].values, year)
        all_values = np.append(grouped['Wartosc'].values, predicted_sums[year])
        plt.plot(all_years, all_values, linestyle='--', color='orange', marker='o', label=f'Przewidywana wartość na rok {year}')

    # Rzeczywiste dane
    plt.plot(grouped['rok'], grouped['Wartosc'], marker='o', label='Rzeczywiste dane')

    # Dostosowanie wykresu
    plt.xlabel('Rok')
    plt.gca().yaxis.set_label_position("right")
    plt.ylabel('Suma wartości', rotation=180, labelpad=15)
    plt.title(f'Porównanie sumy wartości w danych latach z przewidywaniami: {model_type} regression', fontweight='bold')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.subplots_adjust(left=0.1, right=0.9)
    plt.show()


# Przykładowe użycie funkcji
plot_predictions(2026, 'Linear')
