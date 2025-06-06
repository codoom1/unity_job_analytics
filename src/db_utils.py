import duckdb
import pandas as pd

def get_jobs(db_path, min_elapsed=600):
    con = duckdb.connect(db_path)
    df = con.execute(f"SELECT * FROM Jobs WHERE GPUs > 0 AND Elapsed > {min_elapsed}").df()
    return df
