#!/bin/bash

# Stop on the first failed command so a broken setup isn't reported as success
set -e

echo
echo "========================================"
echo "   Resetting and Initializing Library DB"
echo "========================================"
echo

# Set variables
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SQL_FILE="$SCRIPT_DIR/schema.sql"
TRIGGER_FILE="$SCRIPT_DIR/admin_trigger.sql"
DB_NAME="library"
USER="root"

# Drop the existing database
echo "Dropping existing '$DB_NAME' database if it exists..."
sudo mysql -u $USER -e "DROP DATABASE IF EXISTS $DB_NAME;"

# Create the new database
echo "Creating a new '$DB_NAME' database..."
sudo mysql -u $USER -e "CREATE DATABASE $DB_NAME;"

# Import schema
echo "Importing schema.sql to '$DB_NAME'..."
sudo mysql -u $USER $DB_NAME < "$SQL_FILE"

# Import trigger
echo "Importing the trigger to ensure only one admin..."
sudo mysql -u $USER $DB_NAME < "$TRIGGER_FILE"

echo
echo "========================================"
echo " Library database has been reset and initialized."
echo "========================================"
