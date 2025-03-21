# EZPostgres

---

## Overview of the Application

EZPostgres is a utility tool that simplifies PostgreSQL database setup, deployment, and testing. The application allows users to:
- Define database schemas using simple YAML configuration
- Generate PostgreSQL initialization scripts
- Deploy databases to local Docker environment or cloud
- Verify database schema against configuration
- Backup database contents with one command
- Test database connectivity and schema compliance

---

## Instructions on Setting Up the Development Environment

### Prerequisites

1. **Python** (3.6 or newer)
2. **Docker** and **Docker Compose** (for local deployment)
3. **PostgreSQL** client (for testing and verification)
4. **PyYAML**, **python-dotenv** and other dependencies

---
### Deploy

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mskhalsa/ezpostgres
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Your Database**
   - Edit `config.yaml` to define your database schema
   - Create a `.env` file for sensitive information (optional)

4. **Generate SQL Initialization Script**
   ```bash
   python generate_psql.py
   ```
   
   **Note:** This will create an `init.sql` file with your database schema

5. **Deploy Database Locally**
   ```bash
   docker-compose up -d
   ```
   
   **Note:** The PostgreSQL database will be available at localhost:5432

6. **Test Your Database**
   ```bash
   python test_db.py
   ```

7. **Deploy to Cloud (if desired)**
   ```bash
   python deploy.py
   ```

8. **Backup Your Database**
   ```bash
   ./backup.sh
   ```

9. **Shutdown Local Environment**
   ```bash
   docker-compose down
   ```

---
### Environment Configuration

1. **Configure Environment Variables**
   Create a `.env` file with the following variables:
   ```
   DB_USERNAME=postgres
   DB_PASSWORD=your_secure_password
   DB_DATABASE=your_database_name
   # Add cloud provider credentials if using deploy.py
   ```

2. **Configure Database Schema**
   Edit `config.yaml` to define your tables and columns:
   ```yaml
   username: postgres
   password: default_password
   database: my_database
   
   tables:
     - name: users
       columns:
         - name: id
           type: SERIAL
           primary_key: true
         - name: username
           type: VARCHAR(50)
           not_null: true
           unique: true
         - name: email
           type: VARCHAR(100)
           unique: true
         - name: created_at
           type: TIMESTAMP
           default: CURRENT_TIMESTAMP
   ```

---

## Project Structure

```
├── README.md          # Documentation
├── config.yaml        # Database schema configuration
├── generate_psql.py   # Script to generate PostgreSQL init SQL
├── init.sql           # Generated SQL initialization script
├── deploy.py          # Script to deploy to cloud providers
├── test_db.py         # Validation script for database
├── backup.sh          # Database backup utility
├── docker-compose.yml # Local deployment configuration
└── requirements.txt   # Python dependencies
```

---

## Commands Reference

```bash
# Generate PostgreSQL initialization script
python generate_psql.py

# Deploy locally with Docker
docker-compose up -d

# Test database schema and connectivity
python test_db.py

# Deploy to cloud provider
python deploy.py

# Create database backup
./backup.sh

# Stop local database
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Configuration Options

The `config.yaml` file supports the following options for columns:

| Option | Description | Example |
|--------|-------------|---------|
| name | Column name | `username` |
| type | PostgreSQL data type | `VARCHAR(50)` |
| not_null | Set NOT NULL constraint | `true` |
| primary_key | Set as PRIMARY KEY | `true` |
| unique | Set UNIQUE constraint | `true` |
| default | Set default value | `CURRENT_TIMESTAMP` |

---

## Environment Variables

The following environment variables can be set in `.env` to override `config.yaml`:

| Variable | Description |
|----------|-------------|
| DB_USERNAME | Database username |
| DB_PASSWORD | Database password (sensitive) |
| DB_DATABASE | Database name |

---

## Cloud Deployment

The `deploy.py` script supports deploying your database to various cloud providers:

- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- Digital Ocean Managed Databases

Configure your cloud credentials in the `.env` file before running deployment.

---

## Backup and Restore

The `backup.sh` script creates a timestamped backup of your database:

- Backups are stored in a `backups/` directory
- Follows PostgreSQL dump format
- Can be restored using standard PostgreSQL tools

---

## Testing

The `test_db.py` script verifies:

- Database connectivity
- Table existence
- Column definitions match configuration
- Constraint validation

Run tests after deployment to ensure your database is correctly configured.

---

## License

MIT License