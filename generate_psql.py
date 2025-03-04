import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

# Load configuration from config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Override values in the config with environment variables if available
config["username"] = os.getenv("DB_USERNAME", config.get("username"))
config["password"] = os.getenv("DB_PASSWORD", config.get("password"))
config["database"] = os.getenv("DB_DATABASE", config.get("database"))

def create_column_definition(col):
    col_def = f"{col['name']} {col['type']}"
    if col.get("not_null"):
        col_def += " NOT NULL"
    if col.get("primary_key"):
        col_def += " PRIMARY KEY"
    if col.get("unique"):
        col_def += " UNIQUE"
    if col.get("default"):
        col_def += f" DEFAULT {col['default']}"
    # Additional properties like 'comment' or 'foreign_key' could be handled here
    return col_def

sql_statements = []

# Support for multiple tables in the config file
if "tables" in config:
    for table in config["tables"]:
        columns = table.get("columns", [])
        column_defs = [create_column_definition(col) for col in columns]
        sql = f"CREATE TABLE {table['name']} (\n    " + ",\n    ".join(column_defs) + "\n);"
        sql_statements.append(sql)
else:
    # Fallback: if a single table is defined at the root level
    table_name = config.get("table")
    columns = config.get("columns", [])
    column_defs = [create_column_definition(col) for col in columns]
    sql = f"CREATE TABLE {table_name} (\n    " + ",\n    ".join(column_defs) + "\n);"
    sql_statements.append(sql)

# Write the SQL initialization file
with open("init.sql", "w") as f:
    f.write("\n\n".join(sql_statements))

print("SQL initialization file 'init.sql' generated successfully:")
for stmt in sql_statements:
    print(stmt)
