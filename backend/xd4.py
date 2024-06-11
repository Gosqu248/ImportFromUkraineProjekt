import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

from backend.db_config import get_db_engine

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)

# Usunięcie kolumn z samymi brakującymi wartościami
df = df.dropna(axis=1, how='all')

# Konwersja kolumny 'miesiac' na format numeryczny
month_dict = {'Styczeń': 1, 'Luty': 2, 'Marzec': 3, 'Kwiecień': 4, 'Maj': 5, 'Czerwiec': 6,
              'Lipiec': 7, 'Sierpień': 8, 'Wrzesień': 9, 'Październik': 10, 'Listopad': 11, 'Grudzień': 12}
df['miesiac'] = df['miesiac'].map(month_dict)

# Filtracja danych do określonego roku
year = 2023
df_filtered = df[df['rok'] <= year]

# Konwersja kolumny 'Wartosc' na typ numeryczny
df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')

# Grupowanie danych według roku i miesiąca oraz obliczanie sumy
grouped = df_filtered.groupby(['rok', 'miesiac'])['Wartosc'].sum().reset_index()

# Tworzenie kolumny daty w formacie rok-miesiąc
grouped['date'] = grouped.apply(lambda row: f"{int(row['rok'])}-{int(row['miesiac']):02d}", axis=1)
grouped['date'] = pd.to_datetime(grouped['date'], format='%Y-%m')

# Ustawienie kolumny daty jako indeks
grouped.set_index('date', inplace=True)

# Ustawienie częstotliwości na miesięczną
grouped = grouped.asfreq('MS')

# Sortowanie indeksu
grouped.sort_index(inplace=True)

# Parametry modelu SARIMA
order = (2, 1, 2)
seasonal_order = (2, 2, 2, 40)

# Trenowanie modelu SARIMA
model = SARIMAX(grouped['Wartosc'], order=order, seasonal_order=seasonal_order)
model_fit = model.fit(disp=False)

# Prognozowanie na przyszłość (do końca 2030 roku)
forecast_steps = (2030 - 2023) * 12 + (12 - 3) + 1  # liczba miesięcy od kwietnia 2023 do grudnia 2030, +1 aby uwzględnić kwiecień 2023
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start='2023-03-01', periods=forecast_steps, freq='MS')
forecast_values = forecast.predicted_mean

# Tworzenie DataFrame z prognozami
forecast_df = pd.DataFrame({'date': forecast_index, 'forecast': forecast_values})
forecast_df.set_index('date', inplace=True)

# Wizualizacja wyników
plt.figure(figsize=(12, 6))
plt.plot(grouped['Wartosc'], label='Dane historyczne')
plt.plot(forecast_df['forecast'], label='Prognoza', color='red')
plt.legend()
plt.title('Prognoza wartości do 2030 roku')
plt.xlabel('Data')
plt.ylabel('Wartosc')
plt.show()