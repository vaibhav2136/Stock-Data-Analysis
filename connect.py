import psycopg2

#connecting to the database
def connection():

    conn = psycopg2.connect(
        dbname = "trade",
        user = "postgres",
        password = "vibhu97%",
        host = "localhost",
        port = "5432"
    )
    return conn