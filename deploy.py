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
    db_host = os.getenv("DB_HOST", "localhost")  # For cloud, the user should set this to the Azure endpoint.
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_DATABASE")
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    
    connection_string = (
        f"host={db_host} port={db_port} dbname={db_name} "
        f"user={db_user} password={db_password} sslmode=require"
    )
    init_sql_file = "init.sql"
    
    print(f"Deploying '{init_sql_file}' to database at {db_host} ...")
    try:
        subprocess.check_call(["psql", connection_string, "-f", init_sql_file])
        print("Deployment successful!")
    except subprocess.CalledProcessError as e:
        print("Error deploying init.sql to the cloud:")
        print(e)

if __name__ == "__main__":
    deploy_init_sql()
