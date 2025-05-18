#!/bin/bash

echo
echo "========================================"
echo "   Resetting and Initializing Library DB"
echo "========================================"
echo

# Set variables
MYSQL_PATH="/usr/bin/mysql"
SQL_FILE="/home/work/Library/schema.sql"
TRIGGER_FILE="/home/work/Library/admin_trigger.sql"
DB_NAME="library"
USER="root"

# Drop the existing database
echo "Dropping existing '$DB_NAME' database if it exists..."
sudo $MYSQL_PATH -u $USER -e "DROP DATABASE IF EXISTS $DB_NAME;"

# Create the new database
echo "Creating a new '$DB_NAME' database..."
sudo $MYSQL_PATH -u $USER -e "CREATE DATABASE $DB_NAME;"

# Import schema
if [ -f "$SQL_FILE" ]; then
    echo "Importing schema.sql to '$DB_NAME'..."
    sudo $MYSQL_PATH -u $USER $DB_NAME < "$SQL_FILE"
else
    echo "Schema file not found: $SQL_FILE"
fi

# Import trigger
if [ -f "$TRIGGER_FILE" ]; then
    echo "Importing the trigger to ensure only one admin..."
    sudo $MYSQL_PATH -u $USER $DB_NAME < "$TRIGGER_FILE"
else
    echo "Trigger file not found: $TRIGGER_FILE"
fi

echo
echo "========================================"
echo " Library database has been reset and initialized."
echo "========================================"
