import duckdb
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Database path (absolute path based on project structure)
db_path = os.path.join(project_root, "data", "raw", "slurm_data_small.db")
output_dir = os.path.join(project_root, "data", "processed", "csv_output")

# Connect to the database
conn = duckdb.connect(db_path)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get list of all tables
tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()

# Export each table to CSV
for (table_name,) in tables:
    print(f"Exporting {table_name} to CSV...")
    csv_path = os.path.join(output_dir, f"{table_name}.csv")

    query = f"COPY (SELECT * FROM {table_name}) TO '{csv_path}' (HEADER, DELIMITER ',')"
    conn.execute(query)

print(f"Export complete! CSV files are in the {output_dir} directory.")
conn.close()

