import psycopg2
from tokens import DATABASE_NAME, DATABASE_PORT, DATABASE_PASSWORD, DATABASE_SERVER
import misc


def connect():
    return psycopg2.connect(user=DATABASE_NAME,
                            password=DATABASE_PASSWORD,
                            host=DATABASE_SERVER,
                            port=DATABASE_PORT,
                            database=DATABASE_NAME)


def check_connection():
    connection = connect()
    pars = connection.get_dsn_parameters()
    print(f"{misc.get_time()} Successfully connected to DB {pars['dbname']} as user {pars['user']}")
    print(f"{misc.get_time()} Host: {pars['host']}")
    connection.close()
