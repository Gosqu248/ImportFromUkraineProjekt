import sqlalchemy

def get_db_engine():
    # Utwórz połączenie do bazy danych PostgreSQL
    engine = sqlalchemy.create_engine('postgresql://2023_urban_grzegorz:35240@195.150.230.208:5432/2023_urban_grzegorz')
    return engine