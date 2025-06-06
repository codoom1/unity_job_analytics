"""
db_utils.py
-----------
This module provides utility functions for database operations, such as connecting to databases,
executing queries, and handling data retrieval for the analytics pipeline.

Update this docstring as you add or modify functions/classes in this file.
"""

import duckdb
import pandas as pd

def get_jobs(db_path, min_elapsed=600):
    con = duckdb.connect(db_path)
    df = con.execute(f"SELECT * FROM Jobs WHERE GPUs > 0 AND Elapsed > {min_elapsed}").df()
    return df
