import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def deploy_init_sql():
    """
    Deploys the generated init.sql file to the cloud PostgreSQL instance.
    The connection details are taken from the environment variables.
    """
    # Retrieve connection details
    db_host = os.getenv("DB_HOST", "localhost")  # For cloud, user should set this to the Azure endpoint.
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_DATABASE")
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    
    # Build connection string for psql
    # Note: psql accepts connection strings in the format: "host=... port=... dbname=... user=... password=... sslmode=require"
    connection_string = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password} sslmode=require"
    init_sql_file = "init.sql"
    
    print(f"Deploying '{init_sql_file}' to database at {db_host} ...")
    try:
        subprocess.check_call(["psql", connection_string, "-f", init_sql_file])
        print("Deployment successful!")
    except subprocess.CalledProcessError as e:
        print("Error deploying init.sql to the cloud:")
        print(e)

def test_cloud_connection():
    """
    Tests the cloud database connection and verifies that the tables
    defined in the config.yaml file are present.
    """
    # Import helper functions from test_db.py (or replicate similar logic)
    # Assuming test_db.py has functions: load_config, connect_db, and test_tables
    try:
        from test_db import load_config, connect_db, test_tables
    except ImportError:
        print("Error: Could not import test functions from test_db.py.")
        return

    config = load_config()
    try:
        conn = connect_db()  # This will use the environment variables including DB_HOST.
        print("Successfully connected to the cloud database!")
        test_tables(config, conn)
        conn.close()
    except Exception as e:
        print("Error connecting to or testing the cloud database:")
        print(e)

if __name__ == "__main__":
    # Deploy the SQL file to the cloud DB
    deploy_init_sql()
    # Test the connection and verify the schema
    test_cloud_connection()
