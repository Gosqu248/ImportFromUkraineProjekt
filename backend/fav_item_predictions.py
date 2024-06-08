import pandas as pd
import matplotlib.pyplot as plt
from db_config import get_db_engine
import textwrap
import mplcursors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from matplotlib.ticker import FuncFormatter, MaxNLocator
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from fav_item_data import plot_top_items, wrap_labels

engine = get_db_engine()
query = "SELECT * FROM import_ukraine.data"


df = pd.read_sql_query(query, engine)

# Konwersja kolumny "Wartosc" na format numeryczny
df["Wartosc"] = pd.to_numeric(df["Wartosc"], errors='coerce')


def prediction_5_items(year=2024, model_type='Linear', start_year=2023, start_month=3):
    # Filter data up to end_year
    df_filtered = df[df['rok'] <= year]

    # Convert 'Wartosc' column to numeric
    df_filtered.loc[:, 'Wartosc'] = pd.to_numeric(df_filtered['Wartosc'], errors='coerce')

    grouped = df_filtered.groupby(["rok", "SITC-R4.nazwa"])["Wartosc"].sum().reset_index()

    # Prepare data for regression
    X = grouped['rok'].values.reshape(-1, 1)  # Reshape necessary for single feature
    y = grouped['Wartosc'].values


    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Fit regression model
    if model_type == 'Linear':
        model = LinearRegression()
    elif model_type == 'DecisionTree':
        model = DecisionTreeRegressor()
    elif model_type == 'RandomForest':
        model = RandomForestRegressor()
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

    # Predict for the given year
    prediction_data = {'rok': X_test.flatten(), 'SITC-R4.nazwa': grouped.loc[X_test.flatten() - grouped['rok'].min(), 'SITC-R4.nazwa']}
    predictions_df = pd.DataFrame(prediction_data)
    predicted_values = model.predict(predictions_df['rok'].values.reshape(-1, 1))

    # Prepare DataFrame with predictions
    predictions_df['Wartosc'] = predicted_values

    # Group by SITC-R4.nazwa and sum the values
    grouped_items = predictions_df.groupby("SITC-R4.nazwa")["Wartosc"].sum()

    # Sort descending and select top 5 items
    top_items = grouped_items.sort_values(ascending=False).head(5)

    return top_items



def plot_prediction_items(year=2025, model_type='Linear'):
    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    top_items = prediction_5_items(year, model_type)
    bars = top_items.plot(kind='bar', ax=ax, color='skyblue')

    # Set the title and labels
    ax.set_title('Top 5 Predicted Items for Given Year')
    ax.set_xlabel('Item Name')
    ax.set_ylabel('Predicted Value')

    # Format y-axis labels as millions
    ax.yaxis.set_major_formatter(lambda x, pos: '{:,.0f}'.format(x / 1e6) + 'M')

    # Set x-axis labels with item names
    ax.set_xticklabels(wrap_labels(top_items.index, 40, max_length=70))

    # Remove x-axis labels
    ax.set_xticklabels([])

    # Add item names above the bars
    for i, (item, value) in enumerate(top_items.items()):
        wrapped_label = wrap_labels([item], 40, max_length=70)[0]
        ax.text(i, value, wrapped_label, ha='center', va='bottom', fontsize=9, rotation=0)

    # Add interactive cursor
    cursor = mplcursors.cursor(bars, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{top_items.index[sel.index]}: {sel.target[1]:,.0f}'))

    # Show the plot
    plt.show()

    # Return the figure
    return fig
