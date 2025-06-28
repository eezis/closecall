# PostgreSQL Data Restoration Procedure

This document outlines the procedure used to restore the Close Call Database from a production backup file (`closecall_backup.tar`).

## Overview

The restoration process involves backing up the current database, dropping it, recreating it, and restoring from the production backup using `pg_restore`.

## Prerequisites

- PostgreSQL server running
- Database user `eaecc` with appropriate permissions
- Superuser access (`postgres` user) for database creation/deletion
- Production backup file: `closecall_backup.tar`

## Step-by-Step Procedure

### 1. Backup Current Database (Safety Measure)

Before any restoration, create a backup of the current database state:

```bash
PGPASSWORD='current_password' pg_dump -h 127.0.0.1 -U eaecc -d closecall > closecall_backup_before_restore_$(date +%Y%m%d_%H%M).sql
```

### 2. Stop Application Services

Stop Gunicorn to release database connections:

```bash
ps aux | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill
```

### 3. Drop Existing Database

```bash
PGPASSWORD='current_password' dropdb -h 127.0.0.1 -U eaecc closecall
```

**Note:** If you get "database is being accessed by other users", ensure all applications using the database are stopped.

### 4. Create Fresh Database

As PostgreSQL superuser, create a new database:

```bash
sudo -u postgres createdb -O eaecc closecall
```

### 5. Restore from Production Backup

Use `pg_restore` to restore the tar backup:

```bash
PGPASSWORD='current_password' pg_restore -h 127.0.0.1 -U eaecc -d closecall --clean closecall_backup.tar
```

**Expected Behavior:**
- The restore process will show many error messages about non-existent tables/indexes
- These errors are normal when using `--clean` on an empty database
- The actual data restoration will proceed despite these errors
- Final message will show "errors ignored on restore: [number]"

### 6. Verify Data Restoration

Check that the data was successfully restored:

```bash
# Check user count
PGPASSWORD='current_password' psql -h 127.0.0.1 -U eaecc -d closecall -c "SELECT count(*) FROM auth_user;"

# Check incident count  
PGPASSWORD='current_password' psql -h 127.0.0.1 -U eaecc -d closecall -c "SELECT count(*) FROM incident_incident;"

# Verify specific user exists
PGPASSWORD='current_password' psql -h 127.0.0.1 -U eaecc -d closecall -c "SELECT username FROM auth_user WHERE username='eezis';"
```

Expected results from production backup:
- `auth_user`: 24,499 users
- `incident_incident`: 2,436 incidents
- User `eezis` should exist

### 7. Update Database Password (if needed)

If the restoration changes the database user password, update it:

```bash
sudo -u postgres psql -c "ALTER USER eaecc WITH PASSWORD 'your_password';"
```

### 8. Update Application Configuration

Ensure the `.env` file has the correct database password:

```bash
# In .env file
DATABASE_PASSWORD=your_password
```

### 9. Restart Application Services

```bash
source .venv/bin/activate && gunicorn closecall.wsgi:application --config gunicorn-local.conf.py --daemon
```

### 10. Test Application

- Navigate to the application URL
- Test login page loads without database errors
- Attempt login with known user credentials
- Verify admin access works

## Troubleshooting

### Password Authentication Issues

If you encounter "password authentication failed" errors:

1. **Check PostgreSQL user password:**
   ```bash
   sudo -u postgres psql -c "\du"
   ```

2. **Reset password if needed:**
   ```bash
   sudo -u postgres psql -c "ALTER USER eaecc WITH PASSWORD 'new_password';"
   ```

3. **Update .env file to match PostgreSQL password**

4. **Restart application services**

### Special Characters in Passwords

When using passwords with special characters (like `!`), be careful with shell escaping:

```bash
# Use single quotes or escape characters
sudo -u postgres psql -c "ALTER USER eaecc WITH PASSWORD 'CC-5101-\!\!\!';"

# Or enter PostgreSQL prompt directly
sudo -u postgres psql
ALTER USER eaecc WITH PASSWORD 'CC-5101-!!!';
\q
```

### Empty Database After Restore

If the database appears empty after restore:

1. **Check backup file size:**
   ```bash
   ls -lh closecall_backup.tar
   ```

2. **Verify backup file format** (should be tar format for pg_restore)

3. **Try alternative restore method:**
   ```bash
   # For SQL dumps
   PGPASSWORD='password' psql -h 127.0.0.1 -U eaecc -d closecall < backup.sql
   ```

## Important Notes

- **Backup file format matters:** Use `pg_restore` for `.tar`, `.dump` files; use `psql` for `.sql` files
- **Error messages during restore are often normal** when using `--clean` option
- **Always backup before restoration** as a safety measure
- **Test authentication immediately** after restoration
- **Password synchronization** between PostgreSQL and application config is critical

## Files Created During Process

- `closecall_backup_before_restore_YYYYMMDD_HHMM.sql` - Safety backup
- Restored database with production data

## Success Criteria

- [ ] 24,499+ users in `auth_user` table
- [ ] 2,400+ incidents in `incident_incident` table  
- [ ] Login page loads without database errors
- [ ] User authentication works with production credentials
- [ ] Admin interface accessible