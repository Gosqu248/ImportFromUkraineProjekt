import textwrap

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

def wrap_labels(labels, width, max_length=50):
    wrapped_labels = []
    for label in labels:
        if len(label) > max_length:
            label = label[:max_length-3] + '...'
        wrapped_labels.append('\n'.join(textwrap.wrap(label, width)))
    return wrapped_labels

def plot_year_values_with_forecast(year=2024):
    # Initialize an empty DataFrame to store the forecasts
    forecast_df = pd.DataFrame()
    years_prediction = 7

    names = [
        'Wyroby walcowane płaskie z żeliwa lub stali niestopowej, nieplaterowane, niepokryte ani niepowleczone, nieobrobione więcej niż walcowane na gorąco',
        'Rudy żelaza aglomerowane (spieki, granulki, brykiety, itp.)', 'Olej sojowy i jego frakcje',
        'Olej z nasion słonecznika lub z krokosza balwierskiego i ich frakcje',
        'Wyroby walcowane płaskie z żeliwa lub stali niestopowej, nieplaterowane, niepokryte ani niepowleczone, nieobrobione więcej niż walcowane na zimno',
        'Pozostałe żelazostopy (z wyłączeniem żelazostopów radioaktywnych)',
        'Materiały pochodzenia roślinnego, gdzie indziej niewymienione ani niewłączone',
        'Kukurydza (z wyłączeniem kukurydzy cukrowej), niezmielona, inna niż nasiona',
        'Nasiona rzepaku, rzepiku lub gorczycy',
        'Makuchy i in. pozostałości stałe (bez osadów), nawet zmielone lub w granulk., z ekstrakcji tłuszczów lub olejów z nasion lub owoców oleistych i zarodków zbóż',
        'Rudy i koncentraty żelaza, nieaglomerowane',
        'Półprodukty z żeliwa lub stali niestopowej, zawierające mniej niż 0,25\xa0% masy węgla',
        'Drut izol., kable itp. izol. przew. el., nawet wypos. w złączki; przew. z włók. opt., z osłoniętych włók., nawet poł. z przewod. prądu el. l. wypos. w złączki']

    for name in names:
        # Execute SQL query to fetch data from importUkraine.data table
        query = "SELECT * FROM import_ukraine.data"

        # Load data into DataFrame
        df = pd.read_sql_query(query, engine)
        df = df.dropna(axis=1, how='all')

        # Convert 'Wartosc' and 'miesiac' columns to numeric
        df['Wartosc'] = pd.to_numeric(df['Wartosc'], errors='coerce')

        df['SITC-R4.nazwa'] = df['SITC-R4.nazwa'].str.strip()

        df = df[df['SITC-R4.nazwa'] == name]

        # Group by year and calculate sum
        grouped = df.groupby(['rok']).sum().reset_index()

        # Define x here before using it in np.arange
        x = grouped['rok']

        model = SARIMAX(grouped['Wartosc'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 10))
        results = model.fit()

        # Calculate R^2, MAE, RMSE, and MAPE
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

        # Print the MAE, RMSE, MAPE and R^2 values
        print(f"R2 score for {name}: {formatted_r2}")
        print(f"MAE for {name}: {formatted_mae}")
        print(f"RMSE for {name}: {formatted_rmse}")
        print(f"MAPE for {name}: {formatted_mape}%")

        # Forecast next years_prediction years
        forecast = results.get_forecast(steps=years_prediction)
        forecast_index = np.arange(x.iloc[-1] + 1, x.iloc[-1] + years_prediction + 1)

        # Append the forecast to the forecast_df DataFrame
        forecast_df = pd.concat([forecast_df, pd.DataFrame({'Nazwa': name, 'rok': forecast_index, 'Wartosc': forecast.predicted_mean})])

    # Reset the index of forecast_df
    forecast_df.reset_index(drop=True, inplace=True)

    data_for_year = forecast_df[forecast_df['rok'] == year]

    top_items = data_for_year.sort_values(by='Wartosc', ascending=False).head(5)

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a bar plot
    bars = top_items.plot(kind='bar', x='Nazwa', y='Wartosc', color='skyblue', ax=ax)

    # Set the title and labels
    ax.set_title(f"Top 5 towarów pod względem wartości importu w roku {year}")
    ax.set_xlabel("Nazwa towaru", fontsize=12)
    ax.set_ylabel("Wartość", fontsize=12)

    plt.gca().yaxis.tick_right()

    # Add custom format for y-axis labels
    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x / 1e6) + 'M')
    ax.yaxis.set_major_formatter(formatter)

    # Remove x-axis labels
    ax.set_xticklabels([])

    # Add names above the bars
    for i, (item, value) in enumerate(zip(top_items['Nazwa'], top_items['Wartosc'])):
        wrapped_label = wrap_labels([item], 40, max_length=70)[0]
        ax.text(i, value, wrapped_label, ha='center', va='bottom', fontsize=9, rotation=0)

    # Add interactivity
    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{top_items.iloc[sel.target.index]["Nazwa"]}: {sel.target[1]:,.0f}'))

    plt.show()

    return fig


top_items_2025 = plot_year_values_with_forecast(2026)

