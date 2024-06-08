import pandas as pd
from sqlalchemy import create_engine


# Interface implementation for datasource connection and data import
data = pd.read_csv('data/Import.csv', header=0, encoding='latin1')

data = data.apply(lambda x: x.str.encode('latin1').str.decode('utf-8') if x.dtype == "object" else x)


# Utwórz połączenie do bazy danych PostgreSQL
engine = create_engine('postgresql://2023_urban_grzegorz:35240@195.150.230.208:5432/2023_urban_grzegorz')

#data.to_sql('data', engine, schema='import_ukraine', if_exists='replace', index=False)


