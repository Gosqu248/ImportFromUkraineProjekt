# Import Forecast Desktop Application

## Overview
This Python-based desktop application provides interactive analysis and forecasting of goods imported from Ukraine to Poland. Leveraging a PostgreSQL database for storage, the app offers data ingestion, visualization of historical trends, and predictive modeling of future import values using the SARIMAX (Seasonal ARIMA with eXogenous variables) algorithm.

## Key Features

- **Data Ingestion & Storage**:  A CSV loader ingests raw import data into a dedicated PostgreSQL schema, and database connectivity is managed via a simple configuration module.

- **Historical Analysis**:
  - **Total Imports**: Line charts display aggregated import values over time (year/​month).
  - **Top Commodities**: Bar plots identify the top 5 imported items for a chosen year or across all years.

- **Predictive Forecasting**:
  - **Aggregate Forecasts**: Monthly import totals are forecasted over a user-defined horizon.
  - **Commodity-Level Forecasts**: Separate SARIMAX models predict future import values for individual goods or top-ranked items.
  - **Performance Metrics**: Each model computes R², MAE, RMSE, and MAPE to assess fit quality.

- **Interactive GUI**: A Tkinter interface lets users configure parameters (trend window, prediction horizon, start year, commodity selection) and embeds Matplotlib charts with interactive tooltips via mplcursors.

## Technical Details

### SARIMAX Forecasting
The core forecasting engine uses the `statsmodels` implementation of SARIMAX, combining:

- **ARIMA components** `(p, d, q)`:
  - **AR (AutoRegressive)** order `p = 1`
  - **I (Integration)** order `d = 1` for differencing
  - **MA (Moving Average)** order `q = 1`

- **Seasonal ARIMA** components `(P, D, Q, s)`:
  - **Seasonal AR** `P = 1`
  - **Seasonal Differencing** `D = 1`
  - **Seasonal MA** `Q = 1`
  - **Period** `s` set to the length of the seasonal cycle (e.g., 12 months for aggregate time series, or a user-selected trend window for commodity-specific models).

After fitting the model to historical import values, forecasts are generated for a specified number of future time steps. Model diagnostics (R², MAE, RMSE, MAPE) ensure transparency in predictive performance.

### Backend Modules
- **Data Loader**: `Add_data_to_DataBase.py` reads `Import.csv`, handles encoding normalization, and writes to the `import_ukraine` PostgreSQL schema.
- **Database Config**: `db_config.py` provides a `get_db_engine()` function to create a SQLAlchemy engine for querying.
- **Analysis & Visualization**:
  - `sum_data.py`: Builds and returns a year-month line chart of total import values.
  - `fav_item_data.py`: Generates bar charts of the top 5 imported goods for a specified year.
  - `fav_items_all_year.py`: Aggregates and plots top commodities across the full historical span.
- **Forecasting Modules**:
  - `sum_prediction.py`: Applies SARIMAX to monthly totals and visualizes historical data alongside forecasts.
  - `fav_item_predictions.py`: Iterates over a list of high-value goods, fits a SARIMAX model for each, prints fit metrics, and plots the top 5 predicted for a chosen year.
  - `ware_sum_prediction.py`: Forecasts for a single commodity selected via the GUI, with customizable trend window, start year, and horizon.

### GUI Application (`main.py`)
- Built with **Tkinter**, the GUI offers:
  - Entry fields for trend length, prediction months, start year, and commodity selection.
  - Buttons triggering real-time data plotting or SARIMAX forecasts.
  - Embedded **Matplotlib** figures rendered via `FigureCanvasTkAgg`.
  - Interactive elements for error handling and data validation.

## Installation & Usage

1. **Install dependencies**:
   ```bash
   pip install pandas numpy sqlalchemy psycopg2-binary statsmodels matplotlib mplcursors scikit-learn pillow
   ```

2. **Configure database**:
   - Update the connection URL in `backend/db/db_config.py` or set environment variables accordingly.

3. **Load data**:
   ```bash
   python Add_data_to_DataBase.py
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

Navigate the GUI to explore historical import trends and generate forward-looking forecasts using the SARIMAX model.
