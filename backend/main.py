import pandas as pd
from db_config import get_db_engine

# Uzyskaj obiekt engine połączenia z bazy danych
engine = get_db_engine()

# Wykonaj zapytanie SQL, aby pobrać dane z tabeli importUkraine.data
query = "SELECT * FROM import_ukraine.data"

# Wczytaj dane do DataFrame
df = pd.read_sql_query(query, engine)

print("Nazwy column:")
for column in df.columns:
    print(column)

print("\n\nPierwsze 5 wierszy:")
print(df.head())

