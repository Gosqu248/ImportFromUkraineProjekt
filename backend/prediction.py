import pandas as pd
from db_config import get_db_engine
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.ticker as ticker
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)

df = df.dropna()

# Convert 'miesiac' column to numerical format
month_dict = {'Styczeń': 1, 'Luty': 2, 'Marzec': 3, 'Kwiecień': 4, 'Maj': 5, 'Czerwiec': 6,
              'Lipiec': 7, 'Sierpień': 8, 'Wrzesień': 9, 'Październik': 10, 'Listopad': 11, 'Grudzień': 12}
df['miesiac'] = df['miesiac'].map(month_dict)

def predict_sum_for_years(start_year, start_month, end_year, model_type='Linear'):
    predictions = {}

    # Filter data up to end_year
    df_filtered = df[df['rok'] <= end_year]

    # Convert 'Wartosc' column to numeric
    df_filtered.loc[:, 'Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')

    # Group by year and month and calculate sum
    grouped = df_filtered.groupby(['rok', 'miesiac']).sum().reset_index()

    # Prepare data for regression
    X = grouped[['rok', 'miesiac']]
    y = grouped['Wartosc']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Fit regression model
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
    model.fit(X_train, y_train)

    # Make prediction for each month of each year
    year = start_year
    month = start_month
    while year < end_year or (year == end_year and month <= 12):
        prediction_data = pd.DataFrame([[year, month]], columns=['rok', 'miesiac'])
        prediction = model.predict(prediction_data)
        predictions[(year, month)] = prediction[0]
        print(f"Przewidywana suma dla {month} miesiąca {year} roku: {prediction[0]}")
        month += 1
        if month > 12:
            month = 1
            year += 1

    return predictions, model

# Example usage of function

def plot_predictions(end_year, model_type='Linear', start_year=2023, start_month=3):
    # Get predicted sum for each month of each year and regression model
    predicted_sums, model = predict_sum_for_years(start_year, start_month, end_year, model_type)

    # Prepare data for plot
    df_filtered = df[df['rok'] <= end_year]
    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')
    grouped = df_filtered.groupby(['rok', 'miesiac']).sum().reset_index()

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Actual data
    x = grouped['rok'] + grouped['miesiac'] / 12
    y = grouped['Wartosc']
    ax.plot(x, y, 'b-', label='Rzeczywiste dane')

    # Add predicted values to data
    x_pred = []
    y_pred = []
    for (year, month), value in predicted_sums.items():
        x_pred.append(year + month / 12)
        y_pred.append(value)
    ax.plot(x_pred, y_pred, 'r-', label='Przewidywane wartości')

    # Add regression line for entire period
    x_full = pd.DataFrame(
        [[year, month] for year in range(int(grouped['rok'].min()), end_year + 1) for month in range(1, 13)],
        columns=['rok', 'miesiac'])
    y_pred_full = model.predict(x_full)
    ax.plot(x_full['rok'] + x_full['miesiac'] / 12, y_pred_full, color='orange', label='Linia regresji')

    # Adjust plot
    ax.set_xlabel('Rok')
    ax.yaxis.set_label_position("right")
    ax.set_ylabel('Suma wartości', rotation=0, labelpad=15)
    ax.set_title(f'Porównanie sumy wartości w danych latach z przewidywaniami: {model_type} regression',
                 fontweight='bold')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    ax.grid(True)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)

    return fig

# Example usage of function
#plot_predictions(2026, 'Linear')
