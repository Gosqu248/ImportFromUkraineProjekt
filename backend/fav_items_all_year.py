import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import mplcursors
from sklearn.metrics import r2_score
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import num2date
from backend.db_config import get_db_engine
import textwrap

def plot_top_items_with_year():
    engine = get_db_engine()
    query = "SELECT * FROM import_ukraine.data"
    df = pd.read_sql_query(query, engine)
    df = df.dropna(axis=1, how='all')

    df_filtered = df[df['rok'] < 2024]
    df_filtered['Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')
    grouped = df_filtered.groupby(['rok'])['Wartosc'].sum().reset_index()  # Group by 'rok' only
    grouped['date'] = pd.to_datetime(grouped['rok'], format='%Y')  # Convert 'rok' to datetime
    grouped.set_index('date', inplace=True)
    grouped = grouped.asfreq('YS')  # Use 'YS' frequency for yearly start
    grouped.sort_index(inplace=True)

    top_items = df_filtered.groupby("SITC-R4.nazwa")["Wartosc"].sum().nlargest(6)  # Top 5 przedmiotów
    top_items = top_items.iloc[1:]  # Usuń pierwszy element (największy)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = top_items.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_title(f"Top 5 towarów pod względem wartości ze wszystkich lat")
    ax.set_ylabel("Wartość", fontsize=12)
    ax.set_xlabel("Nazwa towaru", fontsize=12)
    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x / 1e6) + 'M')
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.tick_right()
    ax.set_xticklabels([])

    for i, v in enumerate(top_items):
        wrapped_text = textwrap.fill(top_items.index[i], width=30)  # zawijanie do maksymalnie 20 znaków
        ax.text(i, v, wrapped_text, color='black', ha='center', va='bottom',
                bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.5'))

    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{top_items.index[sel.target.index]}: {sel.target[1]:,.0f}'))
    return fig

plot_top_items_with_year()
