-- Create Superset metadata DB
CREATE DATABASE superset OWNER airflow;

-- Analytics schema/tables in the Airflow DB (executed automatically at init)
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.pipeline_runs (
  dag_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  execution_date TIMESTAMPTZ,
  start_date TIMESTAMPTZ,
  end_date TIMESTAMPTZ,
  duration_sec INTEGER,
  state TEXT,
  PRIMARY KEY (dag_id, run_id)
);

CREATE TABLE IF NOT EXISTS analytics.task_failures (
  dag_id TEXT NOT NULL,
  task_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  try_number INTEGER,
  start_date TIMESTAMPTZ,
  end_date TIMESTAMPTZ,
  duration_sec INTEGER,
  state TEXT,
  PRIMARY KEY (dag_id, task_id, run_id, try_number)
);
