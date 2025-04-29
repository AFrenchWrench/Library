@echo off
echo.
echo === Importing schema.sql to 'library' database ===

:: Set variables
:: Change the address with your own db installation address 
set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
:: Change the first part of the address based on where you cloned the project
set SQL_FILE="F:\Library\schema.sql"
set DB_NAME=library
:: Change the user accordingly
set USER=root

:: Check if the database exists; create it if it doesn't
echo Checking if the '%DB_NAME%' database exists...
%MYSQL_PATH% -u %USER% -p -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"

:: Import the schema
echo Importing schema.sql to '%DB_NAME%'...
%MYSQL_PATH% -u %USER% -p %DB_NAME% < %SQL_FILE%

echo.
echo === Done! If no errors appeared, your schema is loaded. ===
pause
