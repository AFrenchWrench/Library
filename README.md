# Library Management CLI

A command-line library management system written in Python and backed by MySQL. Members can browse the catalogue, borrow and return books, and see their loans and fines. A single admin account manages the catalogue, users, and fines.

## Features

**Accounts**
- Registration and login, with passwords hashed using bcrypt (via passlib).
- Two roles: `member` and `admin`. A database trigger ensures only one admin can exist.
- Members can update their name, email, and password. Changing the password requires the old one.

**Admin menu**
- Add books, authors, publishers, and categories.
- List books, users, loans, and fines.
- Update users, books, authors, publishers, and categories.
- Mark fines as paid or unpaid.

**Member menu**
- List books with their available copies.
- Borrow a book, view your loans, and return a book.
- View your fines.

**Loan and fine rules**
- Loans are due 14 days after borrowing.
- A member can have at most 3 active (unreturned) loans.
- A member with 2 or more unpaid fines can't borrow.
- A book with no available copies can't be borrowed. Available copies go down on borrow and back up on return.
- When a book is returned more than 3 days after its due date, a fine of 25 per day beyond that grace period is issued.

**Validation**
- Each model validates its data before saving: required fields, English (ASCII) text, email format, password strength (at least 8 characters with upper- and lowercase letters, a digit, and a special character), ISBN and name lengths, and that foreign keys point at existing records.
- Records still referenced by other records (for example, an author with books) can't be deleted. The model raises a descriptive `*InUse` exception instead.

## Tech stack

- Python 3.10+
- MySQL 8
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) for database access
- [passlib](https://pypi.org/project/passlib/) with [bcrypt](https://pypi.org/project/bcrypt/) for password hashing
- [python-dotenv](https://pypi.org/project/python-dotenv/) for configuration
- [Faker](https://pypi.org/project/Faker/) for generating seed data

## Project structure

```
Library/
├── cli/
│   ├── cli.py            # Login / register menu, routes to the admin or member menu
│   ├── admin.py          # Admin menu
│   └── member.py         # Member menu
├── models/
│   ├── author.py
│   ├── book.py
│   ├── category.py
│   ├── fine.py
│   ├── loan.py           # Borrow/return logic and fine calculation
│   ├── publisher.py
│   ├── user.py
│   ├── validators.py     # Validation rules for every model
│   └── exceptions.py     # Custom exceptions raised by the models
├── tests/                # One test script per model
├── auth.py               # Password hashing and verification
├── db.py                 # MySQL connection using settings from .env
├── main.py               # Entry point
├── schema.sql            # Table definitions
├── admin_trigger.sql     # Triggers that allow only one admin
├── database_config.sh    # Drops and recreates the database from the SQL files
├── seed_database.py      # Fills the database with sample data
├── run_tests.sh          # Runs every test script
├── example_env.txt       # Template for .env
└── requirements.txt
```

## Setup

You need Python 3.10 or newer and a running MySQL 8 server.

### 1. Clone and install dependencies

```bash
git clone https://github.com/AFrenchWrench/Library.git
cd Library
python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create the database

```bash
bash database_config.sh
```

This **drops** any existing `library` database, then recreates it from `schema.sql` and `admin_trigger.sql`. It connects with `sudo mysql -u root`, which works with the default root setup on Debian and Ubuntu. If your MySQL root account uses a password instead, run the same steps by hand:

```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS library; CREATE DATABASE library;"
mysql -u root -p library < schema.sql
mysql -u root -p library < admin_trigger.sql
```

### 3. Create a MySQL user for the application

```sql
CREATE USER 'library_app'@'localhost' IDENTIFIED BY 'choose-a-password';
GRANT ALL PRIVILEGES ON library.* TO 'library_app'@'localhost';
```

### 4. Configure the environment

```bash
cp example_env.txt .env
```

Then edit `.env`:

| Variable  | Description                           |
|-----------|---------------------------------------|
| `DB_HOST` | MySQL host, e.g. `localhost`          |
| `DB_USER` | MySQL user created in step 3          |
| `DB_PASS` | That user's password                  |
| `DB_NAME` | Database name (`library`)             |

The connection uses MySQL's default port (3306).

### 5. Seed sample data (optional)

```bash
python seed_database.py
```

This adds 100 each of authors, publishers, categories, members, books, and loans. Some of the returned loans come back late, so a handful of fines are generated too. It takes about a minute. Seeded members get random passwords, so to log in you need to register your own accounts (see below).

## Usage

```bash
python main.py
```

From the start menu you can log in or register. Registration asks for a role. The first account registered as `admin` becomes the library's admin, and any further admin registration is rejected. Log in as the admin to manage the catalogue, or register a member account to borrow books.

## Running tests

```bash
bash run_tests.sh
```

Each file in `tests/` is a plain script that prints ✅ or ❌ for each check. `run_tests.sh` runs them all and exits with a non-zero status if any check fails. To run a single file:

```bash
python -m tests.test_loan
```

The tests use the database configured in `.env`. They create their own records and delete them afterwards. They also expect no admin account to exist yet, because one test creates the admin. Run them on a freshly created database, before registering an admin:

```bash
bash database_config.sh && bash run_tests.sh
```

## License

MIT. See [LICENSE](LICENSE).

## Author

[AFrenchWrench](https://github.com/AFrenchWrench)
