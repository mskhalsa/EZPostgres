import os
import yaml
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def connect_db(cloud=False):
    """
    Connect to the PostgreSQL database.
    If cloud is True, use DB_HOST from .env; otherwise default to localhost.
    """
    host = os.getenv("DB_HOST", "localhost") if cloud else "localhost"
    conn = psycopg2.connect(
        dbname=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=host,
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

def get_table_columns(conn, table_name):
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
    load_dotenv()  # Load environment variables from .env
    config = load_config()
    # Read CHECKCLOUDDEPLOYMENT variable (default "no")
    check_cloud = os.getenv("CHECKCLOUDDEPLOYMENT", "no").lower() == "yes"
    if check_cloud:
        print("Testing cloud deployment using provided DB_HOST...")
        try:
            conn = connect_db(cloud=True)
            print("Successfully connected to the cloud database!")
            test_tables(config, conn)
            conn.close()
        except Exception as e:
            print("Error connecting to or testing the cloud database:")
            print(e)
    else:
        print("Testing local deployment (DB_HOST=localhost)...")
        try:
            conn = connect_db(cloud=False)
            print("Successfully connected to the local database!")
            test_tables(config, conn)
            conn.close()
        except Exception as e:
            print("Error connecting to or testing the local database:")
            print(e)

if __name__ == "__main__":
    main()
