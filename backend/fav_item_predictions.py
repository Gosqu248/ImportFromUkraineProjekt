import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import mplcursors
from sklearn.metrics import r2_score
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import num2date
from backend.db_config import get_db_engine

# Zmiana w funkcji sarima_prediction: zwraca również dataframe z danymi do analizy kolumnowej
def sarima_prediction(end_year=2030):
    year = 2023
    engine = get_db_engine()
    query = "SELECT * FROM import_ukraine.data"
    df = pd.read_sql_query(query, engine)
    df = df.dropna(axis=1, how='all')

    # Usunięcie month_dict i wszelkich operacji z nim związanych

    df_filtered = df[df['rok'] <= year]

    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')
    grouped = df_filtered.groupby(['rok'])['Wartosc'].sum().reset_index()  # Group by 'rok' only
    grouped['date'] = pd.to_datetime(grouped['rok'], format='%Y')  # Convert 'rok' to datetime
    grouped.set_index('date', inplace=True)
    grouped = grouped.asfreq('YS')  # Use 'YS' frequency for yearly start
    grouped.sort_index(inplace=True)

    order = (1, 0, 1)
    seasonal_order = (1, 1, 1, 32)

    model = SARIMAX(grouped['Wartosc'], order=order, seasonal_order=seasonal_order, trend='n', mle_regression=True)
    model_fit = model.fit(disp=False)

    forecast_steps = end_year - year + 1  # Adjust forecast_steps for yearly data
    forecast = model_fit.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=str(year), periods=forecast_steps, freq='YS')
    forecast_values = forecast.predicted_mean

    forecast_values_noisy = forecast_values

    forecast_df = pd.DataFrame({'date': forecast_index, 'forecast': forecast_values_noisy})
    forecast_df.set_index('date', inplace=True)

    return grouped, forecast_df, df_filtered  # Dodanie df_filtered do zwracanych danych

# Dodanie nowej funkcji plot_top_items_with_year
def plot_top_items_with_year(selected_year=2024):
    df_filtered = sarima_prediction(end_year=selected_year)[2]  # Pobranie df_filtered z wyników sarima_prediction
    print(df_filtered[df_filtered["SITC-R4.nazwa"]== " Gaz ziemny w stanie gazowym"]["Wartosc"])

    top_items = df_filtered.groupby("SITC-R4.nazwa")["Wartosc"].sum().sort_values(ascending=False).head(6)
    top_items = top_items.iloc[1:]

    print(top_items)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = top_items.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_title(f"Top 5 towarów pod względem wartości importu w roku {selected_year}")
    ax.set_ylabel("Wartość", fontsize=12)
    ax.set_xlabel("Nazwa towaru", fontsize=12)
    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Dodanie etykiet nad kolumnami
    for i, v in enumerate(top_items):
        ax.text(i, v + 0.05 * max(top_items), top_items.index[i], color='black', ha='center')

    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{top_items.index[sel.target.index]}: {sel.target[1]:,.0f}'))
    return fig  # Zwróć obiekt figury

# Przykładowe użycie
selected_year = 2026  # Wpisz dowolny rok
fig = plot_top_items_with_year(selected_year)
plt.show()

selected_year = 2027  # Wpisz dowolny rok
fig = plot_top_items_with_year(selected_year)
plt.show()
