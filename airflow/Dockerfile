FROM apache/airflow:2.9.2

# Install Postgres driver as 'airflow' user with constraints
USER airflow
RUN pip install --no-cache-dir "psycopg2-binary==2.9.9" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.11.txt"