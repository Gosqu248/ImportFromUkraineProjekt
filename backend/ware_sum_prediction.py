import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import mplcursors
from matplotlib.dates import num2date
from backend.db_config import get_db_engine
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

engine = get_db_engine()

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0f mln' % (x * 1e-6)  # Change the scale factor to 1e-9

formatter = FuncFormatter(millions)

def plot_year_values_with_forecast(name, trend=24, months_prediction=81, start_year=2010):
    # Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
    query = "SELECT * FROM import_ukraine.data"

    # Wczytaj dane do DataFrame
    df = pd.read_sql_query(query, engine)
    df = df.dropna(axis=1, how='all')

    # Convert 'Wartosc' and 'miesiac' columns to numeric
    df['Wartosc'] = pd.to_numeric(df['Wartosc'], errors='coerce')

    month_dict = {'Styczeń': 1, 'Luty': 2, 'Marzec': 3, 'Kwiecień': 4, 'Maj': 5, 'Czerwiec': 6,
                  'Lipiec': 7, 'Sierpień': 8, 'Wrzesień': 9, 'Październik': 10, 'Listopad': 11, 'Grudzień': 12}
    df['miesiac'] = df['miesiac'].map(month_dict)

    df['SITC-R4.nazwa'] = df['SITC-R4.nazwa'].str.strip()

    df = df[df['SITC-R4.nazwa'] == name]

    # Group by year and month and calculate sum
    grouped = df.groupby(['rok', 'miesiac']).sum().reset_index()

    # Define x here before using it in np.arange
    x = grouped['rok'] + grouped['miesiac'] / 12

    # SARIMAX model
    model = SARIMAX(grouped['Wartosc'], order=(1, 1, 1), seasonal_order=(1, 1, 1, trend))
    results = model.fit()

    # Forecast next months_prediction months
    forecast = results.get_forecast(steps=months_prediction)
    forecast_index = np.arange(x.iloc[-1] + 1 / 12, x.iloc[-1] + months_prediction / 12 + 1 / 12,
                               1 / 12)  # Forecast up to the end of months_prediction months

    # Filter the data to include only years 2020 and later for plotting
    grouped_plot = grouped[grouped['rok'] >= start_year]
    x_plot = grouped_plot['rok'] + grouped_plot['miesiac'] / 12

    # Tworzenie wykresu
    fig = plt.figure(figsize=(10, 6))
    line, = plt.plot(x_plot, grouped_plot['Wartosc'], label='Rzeczywiste dane')  # Removed marker='o'
    forecast_plot, = plt.plot(forecast_index, forecast.predicted_mean, label='Prognoza', linestyle='-', color='red')


    # Connect the real data plot with the forecast using a red line
    last_real_data_point = x_plot.iloc[-1], grouped_plot['Wartosc'].iloc[-1]
    first_forecast_point = forecast_index[0], forecast.predicted_mean.iloc[0]
    plt.plot([last_real_data_point[0], first_forecast_point[0]], [last_real_data_point[1], first_forecast_point[1]],
             color='red')

    # Obliczanie R^2
    predicted = results.fittedvalues
    mae = mean_absolute_error(grouped['Wartosc'], predicted)
    rmse = np.sqrt(mean_squared_error(grouped['Wartosc'], predicted))
    mape = mean_absolute_percentage_error(grouped['Wartosc'], predicted)
    r2 = r2_score(grouped['Wartosc'], predicted)

    # Format the MAE, RMSE, MAPE and R^2 values
    formatted_mae = f'{mae:,.2f}'.replace(',', ' ')
    formatted_rmse = f'{rmse:,.2f}'.replace(',', ' ')
    formatted_mape = f'{mape:,.2f}'
    formatted_r2 = f'{r2:,.2f}'

    # Create a string for the x-label
    xlabel_string = f'Suma wartości \n\nR2 score: {formatted_r2} \n\nMAE: {formatted_mae} \n\nRMSE: {formatted_rmse} \n\nMAPE: {formatted_mape}%'

    # Dostosowanie wykresu
    plt.xlabel(xlabel_string, fontsize=12, ha='center')

    # Dostosowanie wykresu
    plt.xlabel('Rok', fontsize=12)
    plt.ylabel(xlabel_string, rotation=0, labelpad=70, fontsize=12)
    plt.title(f'Prognoza sumy wartości dla ({name}) na kolejne {months_prediction} miesięcy (trend = {trend} miesiecy)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), fancybox=True, shadow=True, ncol=5)
    plt.gca().yaxis.tick_right()
    plt.gca().yaxis.set_label_position("left")

    # Increase the size of the y-axis values
    plt.tick_params(axis='y', labelsize=10)
    plt.tick_params(axis='x', labelsize=8)  # Adjust label size for better spacing

    plt.grid(True)

    plt.gca().yaxis.set_major_formatter(formatter)

    # Add interactive cursor
    cursor = mplcursors.cursor([line, forecast_plot], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Rok: {int(sel.target[0])}\nMiesiąc: {int((sel.target[0] % 1) * 12) + 1}\nWartość: {int(sel.target[1]):,}'.replace(
            ',', ' ')))

    #plt.show()  # Commented out to prevent displaying the plot

    return fig


# Example usage
#plot_year_values_with_forecast("Olej sojowy i jego frakcje")
