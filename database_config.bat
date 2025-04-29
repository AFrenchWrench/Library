@echo off
echo.
echo ========================================
echo    Resetting and Initializing Library DB
echo ========================================
echo.

REM Drop the existing database if it exists
echo Dropping existing 'library' database if it exists...
mysql -u root -p -e "DROP DATABASE IF EXISTS library;"

REM Create the new database
echo Creating a new 'library' database...
mysql -u root -p -e "CREATE DATABASE library;"

:: Set variables
:: Change the address with your own db installation address 
set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
:: Change the first part of the address based on where you cloned the project
set SQL_FILE="F:\Library\schema.sql"
set DB_NAME=library
:: Change the user accordingly
set USER=root

:: Import the schema
echo Importing schema.sql to '%DB_NAME%'...
%MYSQL_PATH% -u %USER% -p %DB_NAME% < %SQL_FILE%

:: Import the trigger to prevent multiple admins
echo Importing the trigger to ensure only one admin...
mysql -u root -p library < "F:\Library\admin_trigger.sql"

echo.
echo ========================================
echo Library database has been reset and initialized.
echo ========================================
pause
