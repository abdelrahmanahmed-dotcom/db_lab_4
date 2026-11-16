# Lab 4: Search Queries in SQL

Introduction to Database Systems, Alexandria National University, Fall 2026.

## 1. Author

| Name                                            | ID      | Did what  |
| ----------------------------------------------- | ------- | --------- |
| عمرو خالد عبدالرحيم            | 2304078 | backend   |
| عبدالرحمن أحمد السيد محمد | 2304056 | front end |



## 2. What is in this repository

```
lab3-2304056/
    the SQL and the output/error of Q1.1, Q1.2, Q1.3
   problem2_DDL.sql       DDL of the six-table library database (Problem 2)
   problem2_DML.sql       seed data for authors, publishers, categories, books, members and loans
   problem2_Queries.sql   SQL for F2.1-F2.6
  website/               my Lab 2 website (login + to-do) with the new library pages
  README.md              this file
```

**Technology:** MySQL, Python 3 + Flask (blueprints, sessions), PyMySQL (plain SQL, no ORM), bcrypt,
HTML (Jinja templates), CSS, JavaScript (validation).

## 3. How to run it (from an empty machine)

1. Install **Python 3.10+**, **MySQL Server** (and the `mysql` client) and **Git**.
   Make sure the `mysql` command works in your terminal.
2. Get the code and enter the folder (use the address of your own repository):
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   cd YOUR-REPOSITORY/lab3-2304056      # if the files are at the top of the repository: cd YOUR-REPOSITORY
   ```

### Part A: Problem 1 (COMPANY database), only SQL

```bash
mysql -u root -p < problem1_DDL.sql      # builds the database `company` and its tables (re-runnable)
mysql -u root -p < problem1_DML.sql      # inserts the rows
mysql -u root -p company                 # type queries by hand (see problem1_Answers.txt)
```

### Part B: Problem 2 (library) and the website

1. Build the databases. Run all three from the `lab3-2304056` folder:
   ```bash
   mysql -u root -p < problem2_DDL.sql          # database `library` (six tables)
   mysql -u root -p < problem2_DML.sql          # seed data for all six tables
   mysql -u root -p < problem2_Queries.sql      # run the F2.1-F2.6 examples
   mysql -u root -p < website/database/schema.sql   # database `registration` (Lab 2: users, todos)
   ```
2. Go to the website folder, create a virtual environment and install the packages:
   ```bash
   cd website
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy the settings file and write your MySQL password in it (`DB_PASSWORD`):
   ```bash
   cp .env.example .env            # Windows: copy .env.example .env
   ```
4. Start the server and open [http://127.0.0.1:5000/library/](http://127.0.0.1:5000/library/):
   ```bash
   python run.py
   ```

The library pages are open (no login needed). Open these Part II pages:

- [http://127.0.0.1:5000/library/search](http://127.0.0.1:5000/library/search) for F2.1 search books
- [http://127.0.0.1:5000/library/catalogue](http://127.0.0.1:5000/library/catalogue) for F2.2 catalogue
- [http://127.0.0.1:5000/library/reports](http://127.0.0.1:5000/library/reports) for F2.3 reports
- [http://127.0.0.1:5000/library/loans](http://127.0.0.1:5000/library/loans) for F2.4 loans
- [http://127.0.0.1:5000/library/most-borrowed](http://127.0.0.1:5000/library/most-borrowed) for F2.5 most borrowed
- [http://127.0.0.1:5000/library/authors-books](http://127.0.0.1:5000/library/authors-books) for F2.6 authors and books

The Lab 2 to-do pages are at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
(they ask you to register and log in, as in Lab 2).

Optional: `python -m pytest` runs the automated tests (they do not need MySQL).

## 4. Problem 2: the library website

Database `library` (`problem2_DDL.sql`):

| Table         | Columns                                                                                               | Keys                                                                    |
| ------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `author`    | `author_id` INT AUTO_INCREMENT, `name` VARCHAR(100) NOT NULL, `country` VARCHAR(50) NOT NULL    | primary key `author_id`                                               |
| `publisher` | `publisher_id`, `name`, `country`                                                               | primary key `publisher_id`                                            |
| `category`  | `category_id`, `name`                                                                             | primary key `category_id`                                             |
| `book`      | `book_id`, `title`, `price`, `publish_year`, `author_id`, `publisher_id`, `category_id` | primary key `book_id`; author foreign key **ON DELETE CASCADE** |
| `member`    | `member_id`, `name`, `email`, `join_date`                                                     | primary key `member_id`; unique `email`                             |
| `loan`      | `loan_id`, `book_id`, `member_id`, `loan_date`, `return_date`                               | primary key `loan_id`; book foreign key **ON DELETE CASCADE**   |

The foreign key has `ON DELETE CASCADE`, so deleting an author makes MySQL delete all the books of that author.
Both tables also have an optional column `image` (VARCHAR(255), may be NULL) for the bonus pictures.

| #     | Page / feature                                                                                                         | Where                                                        | Status |
| ----- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------ |
| F2.1  | Search books by title, price range and category                                                                        | `/library/search`                                          | Done   |
| F2.2  | Catalogue with author, publisher and category names                                                                    | `/library/catalogue`                                       | Done   |
| F2.3  | Category, author and price reports                                                                                     | `/library/reports`                                         | Done   |
| F2.4  | Active loans, members without loans and books without loans                                                            | `/library/loans`                                           | Done   |
| F2.5  | Three most borrowed books and most active member                                                                       | `/library/most-borrowed`                                   | Done   |
| F2.6  | Author counts and same-country author/publisher books                                                                  | `/library/authors-books`                                   | Done   |
| F2.2  | Add a book / add an author                                                                                             | `/library/books/new`, `/library/authors/new`             | Done   |
| F2.3  | Edit a book / edit an author                                                                                           | `/library/books/<id>/edit`, `/library/authors/<id>/edit` | Done   |
| F2.4  | Remove a book (asks "are you sure?")                                                                                   | button in the books table                                    | Done   |
| F2.5  | Remove an author (asks "are you sure?", the books of the author are deleted too)                                       | button in the authors table                                  | Done   |
| Bonus | Cover for every book and photo for every author (upload when adding or editing; letter placeholder when there is none) | `website/app/uploads.py`                                   | Done   |

Only simple `SELECT`, `INSERT`, `UPDATE` and `DELETE` are used (no JOIN, no GROUP BY). All the SQL is in
`website/app/repositories/library.py`, with `%s` placeholders (never glued into the text).
A book needs an existing author (the form has a drop-down list of authors, and the server also catches
MySQL error 1452). Inputs are checked in the browser and again on the server
(`website/app/validators.py`), for example price: a number, not negative, two decimals at most.

Pictures: PNG, JPG, GIF or WEBP, 2 MB at most; they are saved in `website/app/static/uploads/` with a random
file name, and the old file is removed when a picture is replaced or the book/author is deleted.

## 5. Problem 1: summary of the answers

The full SQL and output are in `problem1_Answers.txt`.

- **Q1.1:** after inserting a department that uses an employee as its manager, `DELETE` of that employee fails with
  error 1451 (parent row is referenced). Nothing is deleted.
- **Q1.2:** inserting a project for a department that does not exist fails with error 1452 (child row has no parent).
- **Q1.3:** with `mgr_ssn` and `Dno` both NOT NULL the two tables wait for each other, so the first row cannot be
  inserted. Solutions: `SET FOREIGN_KEY_CHECKS = 0` for the first inserts, or add the foreign key later with
  `ALTER TABLE`, or allow NULL in one column (what `problem1_DDL.sql` does).

## 6. Lab 2 (still in `website/`)

| #     | Feature                                                                          | Status                                                    |
| ----- | -------------------------------------------------------------------------------- | --------------------------------------------------------- |
| R1    | Register (name, e-mail, password, confirm), `Email Already Exists`, auto login | Done                                                      |
| R2    | Login with one single error message, logout                                      | Done                                                      |
| R3    | Private list, redirect to login, newest first                                    | Done                                                      |
| R4    | Add a to-do                                                                      | Done                                                      |
| R5    | Edit a title                                                                     | Done                                                      |
| R6    | Mark done / not done                                                             | Done                                                      |
| R7    | Delete with "are you sure?"                                                      | Done                                                      |
| R8    | Validation in the browser and on the server with the exact messages              | Done                                                      |
| R9    | bcrypt hashes, parameterised queries only, `user_id` from the session          | Done                                                      |
| R10   | Consistent, responsive UI with feedback and empty state                          | Done                                                      |
| Bonus | Due dates, filters, search, open counter, dark mode, automated tests             | Done                                                      |
| Bonus | Deploy online                                                                    | Files ready (`website/Procfile`, `website/DEPLOY.md`) |

Layers: **routes** (HTTP) call **validators** (rules), then **repositories** (SQL), which use **db** (connection).
SQL exists only in `website/app/repositories/`. Screenshots of Lab 2 are in `website/screenshots/`.

### Lab 2 answers

**(a) Why do UPDATE and DELETE contain `AND user_id = ?`, and what changes if you remove it?**
The to-do number comes from the browser, so anybody can send somebody else's number. `AND user_id = ?` uses the id of the logged-in user (taken from the session), so a to-do that is not yours matches zero rows and nothing changes. Without it, any logged-in user could edit, mark or delete other users' to-dos just by changing the number.

**(b) What happens if you insert a to-do for a `user_id` that does not exist, and which constraint is that?**
MySQL refuses the INSERT with error 1452 (a foreign key constraint fails). It is the **foreign key constraint**, which enforces **referential integrity**: every `todos.user_id` must match an existing `users.user_id`.

**(c) Why do you store a hash and not the password?**
If the database leaks, the attacker must not get the real passwords (people reuse them). A bcrypt hash cannot be reversed, it is salted (equal passwords give different hashes), and it is slow on purpose, which makes guessing very expensive. To log in we compare the typed password with the hash using bcrypt.

**(d) `name` is NOT NULL: why did you still need your own check for an empty name?**
An empty text `''` is a value, not NULL, so `NOT NULL` accepts it (and so does a name made only of spaces). Only our own check (`validate_register` in `website/app/validators.py`, and the same rule in JavaScript) can refuse it.
