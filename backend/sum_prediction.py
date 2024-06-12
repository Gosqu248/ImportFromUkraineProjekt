import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import mplcursors
from sklearn.metrics import r2_score
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import num2date
from backend.db_config import get_db_engine


def sarima_prediction(year=2023, end_year=2030):
    # Get database engine connection object
    engine = get_db_engine()

    # Execute SQL query to fetch data from importUkraine.data table
    query = "SELECT * FROM import_ukraine.data"

    # Load data into DataFrame
    df = pd.read_sql_query(query, engine)

    # Remove columns with all missing values
    df = df.dropna(axis=1, how='all')

    # Convert 'miesiac' column to numeric format
    month_dict = {'Styczeń': 1, 'Luty': 2, 'Marzec': 3, 'Kwiecień': 4, 'Maj': 5, 'Czerwiec': 6,
                  'Lipiec': 7, 'Sierpień': 8, 'Wrzesień': 9, 'Październik': 10, 'Listopad': 11, 'Grudzień': 12}
    df['miesiac'] = df['miesiac'].map(month_dict)

    # Filter data to a specific year
    df_filtered = df[df['rok'] <= year]

    # Convert 'Wartosc' column to numeric type
    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')

    # Group data by year and month and calculate sum
    grouped = df_filtered.groupby(['rok', 'miesiac'])['Wartosc'].sum().reset_index()

    # Create date column in year-month format
    grouped['date'] = grouped.apply(lambda row: f"{int(row['rok'])}-{int(row['miesiac']):02d}", axis=1)
    grouped['date'] = pd.to_datetime(grouped['date'], format='%Y-%m')

    # Set date column as index
    grouped.set_index('date', inplace=True)

    # Set frequency to monthly
    grouped = grouped.asfreq('MS')

    # Sort index
    grouped.sort_index(inplace=True)

    # SARIMA model parameters
    order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 48)

    # Train SARIMA model
    model = SARIMAX(grouped['Wartosc'], order=order, seasonal_order=seasonal_order, trend='n', mle_regression=True)
    model_fit = model.fit(disp=False)

    # Forecast into the future (until end of end_year)
    forecast_steps = (end_year - year) * 12 + (
                12 - 3) + 2  # number of months from April 2023 to December end_year, +1 to include April 2023
    forecast = model_fit.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start='2023-03-01', periods=forecast_steps, freq='MS')
    forecast_values = forecast.predicted_mean

    # Calculate R-squared value
    y_true = grouped['Wartosc'][-forecast_steps:]  # Assuming the last `forecast_steps` observations are available
    y_pred = forecast_values[:len(y_true)]
    r2 = r2_score(y_true, y_pred) if len(y_true) == len(y_pred) else np.nan

    noise = np.random.normal(0.001, 300000000,
                             len(forecast_values))  # random noise from normal distribution with mean 0 and standard deviation 100000
    forecast_values_noisy = forecast_values + noise

    # Create DataFrame with forecasts
    forecast_df = pd.DataFrame({'date': forecast_index, 'forecast': forecast_values_noisy})
    forecast_df.set_index('date', inplace=True)

    return grouped, forecast_df, r2


from matplotlib.ticker import FuncFormatter

def plot_prediction(end_year):
    # Generate the predictions
    grouped, forecast_df, r2 = sarima_prediction(year=2023, end_year=end_year - 1)

    # Filter data for plot to only include data from 2020 to March 2023
    grouped_plot = grouped[
        (grouped.index.year >= 2020) & (
                (grouped.index.year < 2023) | ((grouped.index.year == 2023) & (grouped.index.month <= 3)))]

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    line1, = ax.plot(grouped_plot.index, grouped_plot['Wartosc'], 'b-', label='Rzeczywiste dane')
    line2, = ax.plot(forecast_df.index, forecast_df['forecast'], 'r-', label='Prognoza')

    # Add a line connecting the real data and the forecast
    ax.plot([grouped_plot.index[-1], forecast_df.index[0]],
            [grouped_plot['Wartosc'].iloc[-1], forecast_df['forecast'].iloc[0]], 'r-')
    # Customize the plot
    ax.set_xlabel('Rok')
    ax.set_ylabel('Wartość')
    ax.set_title('Predykcja sumy wartości importu do roku {} (model SARIMAX)'.format(end_year), fontsize=14)
    ax.grid(True)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)

    # Format y-axis labels to display in millions
    def millions(x, pos):
        'The two args are the value and tick position'
        return '%1.0f mln' % (x * 1e-6)  # Change the scale factor to 1e-6

    formatter = FuncFormatter(millions)
    ax.yaxis.set_major_formatter(formatter)

    # Function to find the nearest date in a sorted datetime index
    def nearest_date(dates, target):
        target_naive = target.replace(tzinfo=None)
        return min(dates, key=lambda x: abs(x - target_naive))

    # Add interactive cursor
    cursor = mplcursors.cursor([line1, line2], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Data: {nearest_date(grouped_plot.index if sel.artist == line1 else forecast_df.index, num2date(sel.target[0])).strftime("%Y-%m")}\nWartość: {sel.target[1]:,.0f}'))

    # Move the legend below the plot
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), shadow=True, ncol=2)

    return fig