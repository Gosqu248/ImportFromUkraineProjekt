import mplcursors
import pandas as pd
from db_config import get_db_engine
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from matplotlib.ticker import FuncFormatter, MaxNLocator
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)

df = df.dropna(axis=1, how='all')

# Convert 'miesiac' column to numerical format
month_dict = {'Styczeń': 1, 'Luty': 2, 'Marzec': 3, 'Kwiecień': 4, 'Maj': 5, 'Czerwiec': 6,
              'Lipiec': 7, 'Sierpień': 8, 'Wrzesień': 9, 'Październik': 10, 'Listopad': 11, 'Grudzień': 12}
df['miesiac'] = df['miesiac'].map(month_dict)

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0f mln' % (x * 1e-9)  # Change the scale factor to 1e-9

formatter = FuncFormatter(millions)

import numpy as np

def predict_sum_for_years(start_year, start_month, end_year, model_type='Linear'):
    global df
    predictions = {}

    for year in range(start_year, end_year + 1):
        # Filter data up to current year
        df_filtered = df[df['rok'] <= year]

        # Convert 'Wartosc' column to numeric
        df_filtered.loc[:, 'Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')

        # Group by year and month and calculate sum
        grouped = df_filtered.groupby(['rok', 'miesiac']).sum().reset_index()

        # Prepare data for regression
        X = grouped[['rok', 'miesiac']]
        y = grouped['Wartosc']

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

        # Fit regression model
        if model_type == 'Linear':
            model = LinearRegression()
        elif model_type == 'DecisionTree':
            model = DecisionTreeRegressor(random_state=42)
        elif model_type == 'RandomForest':
            model = RandomForestRegressor(random_state=42)
        elif model_type == 'KNeighbors':
            model = KNeighborsRegressor()
        else:
            raise ValueError(f"Invalid model_type: {model_type}")
        model.fit(X_train, y_train)

        # Predict on test data
        y_pred = model.predict(X_test)

        # Evaluate the model
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        # Make prediction for each month of each year
        month = start_month if year == start_year else 1
        while year < end_year or (year == end_year and month <= 12):
            prediction_data = pd.DataFrame([[year, month]], columns=['rok', 'miesiac'])
            prediction = model.predict(prediction_data)

            # Add random noise to prediction
            noise = np.random.normal(0, 1)
            prediction = prediction + noise

            predictions[(year, month)] = prediction[0]
            print(f"Przewidywana suma dla {month} miesiąca {year} roku: {prediction[0]}")
            month += 1
            if month > 12:
                month = 1
                year += 1

        # Display results
        print(f'Mean Absolute Error: {mae:.2f}')
        print(f'Mean Squared Error: {mse:.2f}')
        print(f'Root Mean Squared Error: {rmse:.2f}')
        print(f'R2 Score: {r2:.2f}')

        # Add predictions to the original dataframe for the next iteration
        for (year, month), prediction in predictions.items():
            df = pd.concat([df, pd.DataFrame({'rok': [year], 'miesiac': [month], 'Wartosc': [prediction]})],
                           ignore_index=True)
    return predictions, model, r2

# Example usage of function


def plot_predictions(end_year, model_type='Linear'):
    end_year = end_year - 1
    start_year = 2023
    start_month = 3

    # Get predicted sum for each month of each year and regression model
    predicted_sums, model, r2 = predict_sum_for_years(start_year, start_month, end_year, model_type)

    # Prepare data for plot
    df_filtered = df[df['rok'] <= end_year]
    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')
    grouped = df_filtered.groupby(['rok', 'miesiac']).sum().reset_index()

    # Filter data for plot to only include data from 2020 to March 2023
    grouped_plot = grouped[
        (grouped['rok'] >= 2020) & ((grouped['rok'] < 2023) | ((grouped['rok'] == 2023) & (grouped['miesiac'] <= 3)))]
    fig, ax = plt.subplots(figsize=(25, 20))



    # Add regression line for the period from 2020 onwards
    x_full = pd.DataFrame([[year, month] for year in range(2020, end_year + 1) for month in range(1, 13)],
                          columns=['rok', 'miesiac'])
    y_pred_full = model.predict(x_full)
    line2, = ax.plot(x_full['rok'] + x_full['miesiac'] / 12, y_pred_full, color='orange', label='Linia regresji')

    # Actual data
    x = grouped_plot['rok'] + grouped_plot['miesiac'] / 12
    y = grouped_plot['Wartosc']
    line1, = ax.plot(x, y, 'b-', label='Rzeczywiste dane')

    # Add predictions from March 2023 onwards
    predicted_x = np.array([year + month / 12 for (year, month) in predicted_sums.keys()])
    predicted_y = np.array(list(predicted_sums.values()))
    line3, = ax.plot(predicted_x, predicted_y, 'r--', label='Przewidywane dane')

    # Adjust plot
    ax.set_xlabel('Rok', fontsize=12)
    ax.set_ylabel('Suma wartości', rotation=90, labelpad=15, fontsize=12)
    ax.set_title(f'Porównanie sumy wartości w danych latach z przewidywaniami: {model_type} regression', fontweight='bold')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=5)
    ax.grid(True)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Set maximum number of x-axis labels
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)

    # Move y-axis values to right side
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("left")

    # Increase the size of the y-axis values
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)

    # Format y-axis labels to display in millions
    formatter = plt.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x / 1e6) + 'M')
    ax.yaxis.set_major_formatter(formatter)

    # Add R2 score to the plot
    ax.text(0.5, -0.1, f'Dopasowanie modelu: {r2:.2f}', transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5), ha='center')

    # Add interactive cursor
    cursor = mplcursors.cursor([line1, line2, line3], hover=True)
    cursor.connect("add",
                   lambda sel: sel.annotation.set_text(f'Rok: {int(sel.target[0])}\nMiesiąc: {int((sel.target[0] % 1) * 12) + 1}\nWartość: {sel.target[1]:,.0f}'))

    #plt.show()  # Commented out to prevent displaying the plot

    return fig


# Example usage of function
#plot_predictions(2026, 'RandomForest')


