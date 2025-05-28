# 📚 Library Management CLI

A modular, extensible, and testable command-line interface (CLI) application for managing a library system. Built with Python and SQLite, this project handles book inventory, member registration, loan tracking, and fine calculation — all from the terminal.

---

## ⚙️ Features

- 🔍 **Book Management**: Add, update, delete, and query books.
- 👤 **User Management**: Register, update, and track users.
- 📆 **Loan System**: Track borrow/return actions and enforce active loan limits.
- 💸 **Fine Management**: Automatically calculate overdue fines.
- 🔐 **Authentication**: Secure command-line access for admins.
- 🧪 **Testing Framework**: Modular test suite for validation, models, and CLI.
- 🗃️ **Database Scripts**: Easy setup and seeding for dev environments.

---

## 🏗️ Project Structure

```bash
Library/
├── cli/                  # Command-line interface logic
│   ├── admin.py
│   ├── cli.py
│   └── member.py
│
├── models/               # Data models, validation, and business logic
│   ├── author.py
│   ├── book.py
│   ├── category.py
│   ├── exceptions.py
│   ├── fine.py
│   ├── loan.py
│   ├── user.py
│   ├── validators.py
│   └── __init__.py
│
├── auth.py               # Authentication mechanism
├── db.py                 # DB connection handler
├── main.py               # CLI entry point
├── seed_database.py      # Populate database with sample data
├── schema.sql            # SQL schema definition
├── admin_trigger.sql     # SQL triggers for admin actions
├── example_env.txt       # Sample env file
├── database_config.sh    # DB setup script
├── run_tests.sh          # Test runner
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT license
└── .gitignore            # Ignore rules
````

---

## 🚀 Getting Started

Follow the steps below to get the Library CLI up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/AFrenchWrench/Library.git
cd Library
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment

Copy the example environment file and update values as needed:

```bash
cp example_env.txt .env
```

> ⚠️ Make sure the `.env` file points to your SQLite database path or other environment-specific configs.

### 5. Initialize the Database

Run the following scripts to create and seed the database:

```bash
bash database_config.sh
python seed_database.py
```

### 6. Start the Application

Launch the CLI:

```bash
python main.py
```

Use the prompts to:

* Log in as an admin or member
* Manage books and members
* Track loans and fines
* Borrow a book
* See available books

---

## 🧪 Running Tests

To run the test suite:

```bash
bash run_tests.sh
```

This executes unit and integration tests for your CLI and models.

---

## 📜 License

MIT License. See [`LICENSE`](LICENSE) for full details.

---

## 🤝 Contributing

Pull requests and issues are welcome. Please follow the established structure and include test coverage for new features.

---

## ✍️ Author

Made with ⚙️ by [AFrenchWrench](https://github.com/AFrenchWrench)
