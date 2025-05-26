-- users
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  joined_date DATE NOT NULL,
  role ENUM('member', 'admin') NOT NULL DEFAULT 'member'
);

-- authors, publishers, categories
CREATE TABLE IF NOT EXISTS authors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS publishers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL
);

-- books
CREATE TABLE IF NOT EXISTS books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  isbn VARCHAR(20) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  author_id INT,
  publisher_id INT,
  category_id INT,
  total_copies INT DEFAULT 1,
  available_copies INT DEFAULT 1,
  FOREIGN KEY (author_id) REFERENCES authors(id),
  FOREIGN KEY (publisher_id) REFERENCES publishers(id),
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- loans & fines
CREATE TABLE IF NOT EXISTS loans (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  book_id INT,
  loan_date DATE NOT NULL,
  due_date DATE NOT NULL,
  return_date DATE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE TABLE IF NOT EXISTS fines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  loan_id INT,
  amount DECIMAL(6,2),
  paid BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (loan_id) REFERENCES loans(id)
);
