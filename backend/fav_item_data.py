import pandas as pd
import matplotlib.pyplot as plt
from db_config import get_db_engine
from matplotlib.ticker import FuncFormatter, MaxNLocator
import textwrap
import mplcursors


engine = get_db_engine()
query = "SELECT * FROM import_ukraine.data"


df = pd.read_sql_query(query, engine)

df = df.dropna()

# Konwersja kolumny "Wartosc" na format numeryczny
df["Wartosc"] = pd.to_numeric(df["Wartosc"], errors='coerce')




# Funkcja do zawijania tekstu
def wrap_labels(labels, width, max_length=50):
    wrapped_labels = []
    for label in labels:
        if len(label) > max_length:
            label = label[:max_length] + '...'  # Przytnij i dodaj '...'
        wrapped_labels.append('\n'.join(textwrap.wrap(label, width)))
    return wrapped_labels



# Funkcja do generowania wykresu kolumnowego dla 5 najczęściej występujących przedmiotów w danym roku
def plot_top_items(year=2020):
    # Wybieramy dane dla danego roku
    df_year = df[df["rok"] == year]

    # Grupujemy dane po nazwie przedmiotu i sumujemy wartości
    grouped = df_year.groupby("SITC-R4.nazwa")["Wartosc"].sum()

    # Sortujemy dane malejąco i wybieramy 5 najczęściej występujących przedmiotów
    top_items = grouped.sort_values(ascending=False).head(6)
    top_items = top_items.iloc[1:]  # Usuń pierwszy element (największy)

    # Tworzymy wykres
    fig, ax = plt.subplots(figsize=(10, 6))  # Utwórz obiekt figury i osi
    bars = top_items.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_title(f"Top 5 towarów pod względem wartości importu w roku {year}")
    ax.set_ylabel("Wartość", fontsize=12)
    ax.set_xlabel("Nazwa towaru", fontsize=12)  # Ustawienie etykiety osi X

    plt.gca().yaxis.tick_right()


    # Dodajemy niestandardowy format dla etykiet osi Y
    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x / 1e6) + 'M')
    ax.yaxis.set_major_formatter(formatter)

    # Usunięcie etykiet osi X
    ax.set_xticklabels([])

    # Dodaj nazwy nad kolumnami, z maksymalną długością 50 znaków
    for i, (item, value) in enumerate(top_items.items()):
        wrapped_label = wrap_labels([item], 40, max_length=70)[0]
        ax.text(i, value, wrapped_label, ha='center', va='bottom', fontsize=9, rotation=0)

        # Dodanie interaktywności
    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{top_items.index[sel.target.index]}: {sel.target[1]:,.0f}'))


    return fig  # Zwróć obiekt figury

# Testowanie funkcji dla roku 2023
#fig = plot_top_items(2023)
#plt.tight_layout()  # Automatycznie dostosuj layout, aby uniknąć przekrycia się elementów
#plt.show()