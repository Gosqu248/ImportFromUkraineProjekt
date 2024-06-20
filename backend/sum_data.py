import pandas as pd
from db_config import get_db_engine
import mplcursors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator


# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0f mln' % (x * 1e-6)  # Change the scale factor to 1e-9

formatter = FuncFormatter(millions)

def plot_year_values():
    # Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
    query = "SELECT * FROM import_ukraine.data"

    # Wczytaj dane do DataFrame
    df = pd.read_sql_query(query, engine)

    # Convert 'Wartosc' and 'miesiac' columns to numeric
    df['Wartosc'] = pd.to_numeric(df['Wartosc'], errors='coerce')
    month_dict = {'Styczeń': 1, 'Luty': 2, 'Marzec': 3, 'Kwiecień': 4, 'Maj': 5, 'Czerwiec': 6,
                  'Lipiec': 7, 'Sierpień': 8, 'Wrzesień': 9, 'Październik': 10, 'Listopad': 11, 'Grudzień': 12}
    df['miesiac'] = df['miesiac'].map(month_dict)

    # Group by year and month and calculate sum
    grouped = df.groupby(['rok', 'miesiac']).sum().reset_index()

    # Tworzenie wykresu
    fig = plt.figure(figsize=(10, 6))
    x = grouped['rok'] + grouped['miesiac'] / 12
    line, = plt.plot(x, grouped['Wartosc'], label='Rzeczywiste dane')  # Removed marker='o'

    # Dostosowanie wykresu
    plt.xlabel('Rok', fontsize=12)
    plt.ylabel('Suma wartości', rotation=90, labelpad=15, fontsize=12)
    plt.title('Suma wartości w danych latach')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=5)
    plt.gca().yaxis.tick_right()
    plt.gca().yaxis.tick_right()
    plt.gca().yaxis.set_label_position("left")

    # Increase the size of the y-axis values
    plt.tick_params(axis='y', labelsize=10)
    plt.tick_params(axis='x', labelsize=10)

    plt.grid(True)

    plt.gca().yaxis.set_major_formatter(formatter)

    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'Rok: {int(sel.target[0])}\nMiesiąc: {int((sel.target[0] % 1) * 12) + 1}\nWartość: {int(sel.target[1]):,}'.replace(
            ',', ' ')))

    # plt.show()  # Commented out to prevent displaying the plot

    return fig


# Example usage of function
# fig = plot_year_values()
# plt.show(fig)  # Uncomment to display the plot
