#!/bin/bash

# Configuration variables (adjust these paths and names as needed)
BACKUP_DIR="/c/backups"         # Directory where backups will be stored
DB_CONTAINER="db"   # Typically the service name in docker-compose, e.g., 'db'
DB_NAME="mydb" # Put in the credentials from the .env here.
DB_USER="myuser"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create a timestamped backup file (YYYY-MM-DD)
TIMESTAMP=$(date +%F)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Run pg_dump inside the container and compress the output
docker exec -t "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

echo "Backup created: $BACKUP_FILE"

# Delete older backups, keeping only the three most recent files
cd "$BACKUP_DIR" || exit
ls -1t | tail -n +4 | xargs -r rm -f

echo "Old backups cleaned up; only the 3 most recent backups remain."
