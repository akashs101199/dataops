import os, time
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "postgresql://airflow:airflow@postgres:5432/airflow")

RUNS_SQL = """
INSERT INTO analytics.pipeline_runs (dag_id, run_id, execution_date, start_date, end_date, duration_sec, state)
SELECT
  dr.dag_id,
  dr.run_id,
  dr.execution_date,
  dr.start_date,
  dr.end_date,
  EXTRACT(EPOCH FROM (dr.end_date - dr.start_date))::int AS duration_sec,
  dr.state
FROM dag_run dr
ON CONFLICT (dag_id, run_id) DO UPDATE
  SET execution_date = EXCLUDED.execution_date,
      start_date = EXCLUDED.start_date,
      end_date = EXCLUDED.end_date,
      duration_sec = EXCLUDED.duration_sec,
      state = EXCLUDED.state;
"""

FAILS_SQL = """
INSERT INTO analytics.task_failures (dag_id, task_id, run_id, try_number, start_date, end_date, duration_sec, state)
SELECT
  ti.dag_id,
  ti.task_id,
  ti.run_id,
  ti.try_number,
  ti.start_date,
  ti.end_date,
  EXTRACT(EPOCH FROM (ti.end_date - ti.start_date))::int AS duration_sec,
  ti.state
FROM task_instance ti
WHERE ti.state = 'failed'
ON CONFLICT (dag_id, task_id, run_id, try_number) DO UPDATE
  SET start_date = EXCLUDED.start_date,
      end_date = EXCLUDED.end_date,
      duration_sec = EXCLUDED.duration_sec,
      state = EXCLUDED.state;
"""

while True:
    try:
        with psycopg2.connect(DB_URL) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(RUNS_SQL)
                cur.execute(FAILS_SQL)
        print("ETL: synced analytics tables")
    except Exception as e:
        print("ETL error:", e)
    time.sleep(30)
