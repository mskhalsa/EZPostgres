import os
import yaml
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def connect_db():
    # Connect to PostgreSQL using credentials from the .env file
    conn = psycopg2.connect(
        dbname=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host="localhost",  # Adjust if your Docker setup differs
        port="5432"
    )
    return conn

def get_table_columns(conn, table_name):
    # Query the information_schema to retrieve columns for the given table
    query = """
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = %s
    ORDER BY ordinal_position;
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (table_name,))
        return cur.fetchall()

def test_tables(config, conn):
    if "tables" in config:
        for table in config["tables"]:
            table_name = table["name"]
            print(f"\nTesting table: {table_name}")
            columns = get_table_columns(conn, table_name)
            if not columns:
                print(f"ERROR: Table '{table_name}' does not exist!")
            else:
                print(f"Table '{table_name}' exists. Columns found:")
                for col in columns:
                    print(f"  - {col['column_name']}: {col['data_type']} (Nullable: {col['is_nullable']})")
    else:
        # Fallback if config has a single table defined at the root level
        table_name = config.get("table")
        print(f"\nTesting table: {table_name}")
        columns = get_table_columns(conn, table_name)
        if not columns:
            print(f"ERROR: Table '{table_name}' does not exist!")
        else:
            print(f"Table '{table_name}' exists. Columns found:")
            for col in columns:
                print(f"  - {col['column_name']}: {col['data_type']} (Nullable: {col['is_nullable']})")

def main():
    load_dotenv()  # Load credentials from .env
    config = load_config()
    try:
        conn = connect_db()
        print("Successfully connected to the database!")
    except Exception as e:
        print("ERROR: Could not connect to the database!")
        print(e)
        return

    test_tables(config, conn)
    conn.close()

if __name__ == "__main__":
    main()
