import pandas as pd
import os
from sqlalchemy import create_engine
import psycopg2
from time import time
import argparse

def main(params):
    user = params.user
    pwd = params.pwd
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    parquet_name = 'output.parquet'
    csv_name = 'output.csv'

    engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db}')
    engine.connect()

    os.system(f"wget {url} -O {parquet_name}")

    df = pd.read_parquet(parquet_name)
    df.to_csv(csv_name)

    #print(pd.io.sql.get_schema(df, name= 'yellow_taxi_data',con=engine))

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    while True:
        t_start = time()
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print ('inserted another chunk..., took %.3f second' % (t_end - t_start))

        df = next(df_iter)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    #user, pwd, host, port, db, table_name, url
    parser.add_argument('--user', help = 'username for postgres')
    parser.add_argument('--pwd', help = 'password for postgres')
    parser.add_argument('--host', help = 'host for postgres')
    parser.add_argument('--port', help = 'port for postgres')
    parser.add_argument('--db', help = 'database name for postgres')
    parser.add_argument('--table_name', help = 'name of the table where we will write the results to')
    parser.add_argument('--url', help = 'url of the csv file')

    args = parser.parse_args()

    main(args)
