
#!/bin/bash

read -p "Are you sure you want to restore the backup? This will overwrite the current database and media files. (y/n): " confirmation
if [[ $confirmation != "y" ]]; then
    echo "Restore cancelled."
    exit 0
fi 

read -p "Enter the name of the database backup file (e.g., backup.sql): " backup_file
if [[ ! -f "backups/$backup_file" ]]; then
    echo "Backup file not found!"
    exit 1
fi 

read -p "Enter the name of the media file to restore (e.g., media_backup.tar.gz): " media_file
if [[ ! -f "backups/$media_file" ]]; then
    echo "Media backup file not found!"
    exit 1
fi

# Restore the database and media files


echo "Dropping database $DJANGO_DB_NAME if it exists..."
dropdb $DJANGO_DB_NAME -U $DJANGO_DB_USER -h DB -p 5432 -f

echo "Creating database $DJANGO_DB_NAME..."
createdb $DJANGO_DB_NAME -p 5432 -U $DJANGO_DB_USER -h DB

echo "Granting privileges on database $DJANGO_DB_NAME to user $DJANGO_DB_USER..."
psql -U $DJANGO_DB_USER -h DB -p 5432 -c "GRANT ALL PRIVILEGES ON DATABASE $DJANGO_DB_NAME TO $DJANGO_DB_USER;"

echo "Restoring database from $backup_file..."

psql -U $DJANGO_DB_USER -d $DJANGO_DB_NAME -h DB -p 5432 -f backups/$backup_file

if [ $? -ne 0 ]; then
    echo "Failed to restore database. Aborting."
    exit 1
fi

echo "Restoring media files from $media_file..."
# Delete existing media files
rm -rf /app/media/*

# Extract the media backup
tar -xvf backups/$media_file -C media/

# Ensure correct permissions
chmod -R 755 media/

# Run the commands to reinitialize the database and collect static files
echo "Running migrations and setup..."
python manage.py migrate --settings=memorymap_toolkit.settings.production
python manage.py shell < mmt_setup.py --settings=memorymap_toolkit.settings.production 

echo "Restore completed successfully."

exit 0