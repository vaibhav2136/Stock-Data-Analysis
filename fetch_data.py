import pandas as pd
import psycopg2

#connecting to the database
conn = psycopg2.connect(
    dbname = "trade",
    user = "postgres",
    password = "vibhu97%",
    host = "localhost",
    port = "5432"
)
#fetching data from database
def fetch_trade_data(tablename):
    query = f"SELECT * FROM {tablename} "
    df = pd.read_sql(query,conn)
    return df
