import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from db_config import get_db_engine

# Fetching data
engine = get_db_engine()
query = "SELECT * FROM import_ukraine.data"
df = pd.read_sql_query(query, engine)
df = df.dropna()

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
def plot_top_items(trend=12):
    # Group data by item name and sum values
    grouped = df.groupby("SITC-R4.nazwa")["Wartosc"].sum()

    # Get all unique items
    unique_items = grouped.index.unique()

    forecasted_data = []

    # For each unique item
    for item in unique_items:
        # If the item is not in unique_top_items, skip this iteration
        if item not in unique_top_items:
            continue

        item_data = df[df["SITC-R4.nazwa"] == item]["Wartosc"]

        # Convert item_data to numeric and drop NaN values
        item_data = pd.to_numeric(item_data, errors='coerce').dropna()

        # Check if item_data has more than one unique value and enough data points
        if len(item_data.unique()) > 1 and len(item_data) > (1 + 1 + 1 + 1 * trend):  # order=(1,1,1), seasonal_order=(1,1,1,trend)
            # SARIMAX model
            model = SARIMAX(item_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, trend))
            try:
                results = model.fit(disp=False)
                # Forecast for the next 7 years
                steps = 7  # Set steps to 7
                forecast = results.get_forecast(steps=steps)
                forecasted_value = forecast.predicted_mean.iloc[-1]
            except Exception as e:
                print(f"Could not fit SARIMAX model for {item}: {e}")
                forecasted_value = item_data.iloc[-1]  # Fall back to last known value
        else:
            forecasted_value = item_data.iloc[-1]

        forecasted_data.append((item, forecasted_value))

    # Convert the forecasted data to a DataFrame
    forecasted_df = pd.DataFrame(forecasted_data, columns=["SITC-R4.nazwa", "Wartosc"])

    # Sort the forecasted data in descending order and select the top 5 items
    top_items = forecasted_df.sort_values(by="Wartosc", ascending=False).head(5)

    print("Top 5 items for the next 7 years:")
    print(top_items)

# Call the function to test it
plot_top_items()