FROM python

RUN apt-get install wget
RUN pip install pandas sqlalchemy pyarrow psycopg2-binary

WORKDIR /app
copy ingest_data.py ingest_data.py

#ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "python", "ingest_data.py" ]