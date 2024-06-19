import pandas as pd
from db_config import get_db_engine
import mplcursors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0f mln' % (x * 1e-6)  # Change the scale factor to 1e-9

formatter = FuncFormatter(millions)

def get_unique_top_items(start_year=2010, end_year=2023):
    top_items_list = []

    for year in range(start_year, end_year + 1):
        # Select data for the given year
        df_year = df[df["rok"] == year]

        # Group data by item name and sum the values
        grouped = df_year.groupby("SITC-R4.nazwa")["Wartosc"].sum()

        # Sort the data in descending order and select the top 5 items
        top_items = grouped.sort_values(ascending=False).head(10)

        # Add the top items to the list
        top_items_list.extend(top_items.index.tolist())

    # Remove duplicates
    unique_top_items = list(set(top_items_list))

    return unique_top_items

# Test the function
unique_top_items = get_unique_top_items()
print(f"Unique top items from 2010 to 2023: {unique_top_items}")