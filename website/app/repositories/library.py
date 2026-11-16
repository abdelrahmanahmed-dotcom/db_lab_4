"""[Lab 3] All SQL about the library database (tables author and book).

Only simple SELECT, INSERT, UPDATE and DELETE (no JOIN). Every statement uses %s
placeholders, so values are never glued into the SQL.
The foreign key book.author_id -> author.author_id has ON DELETE CASCADE, so
deleting an author makes MySQL delete that author's books too.
"""
import pymysql

from app.db import get_library_db

MYSQL_FK_FAILS = 1452  # "a foreign key constraint fails" (book.author_id does not exist)


class UnknownAuthorError(Exception):
    """Raised when a book points at an author_id that is not in the author table."""


# ---------------------------------------------------------------- authors
def list_authors():
    """[F2.1] All authors."""
    with get_library_db().cursor() as cur:
        cur.execute("SELECT author_id, name, country, image FROM author ORDER BY author_id")
        return cur.fetchall()


def get_author(author_id):
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT author_id, name, country, image FROM author WHERE author_id = %s",
            (author_id,),
        )
        return cur.fetchone()  # a dict, or None


def add_author(name, country, image=None):
    """[F2.2] Add an author."""
    with get_library_db().cursor() as cur:
        cur.execute(
            "INSERT INTO author (name, country, image) VALUES (%s, %s, %s)",
            (name, country, image),
        )


def update_author(author_id, name, country, image):
    """[F2.3] Edit an author (image is the file name to keep, or None for no photo)."""
    with get_library_db().cursor() as cur:
        cur.execute(
            "UPDATE author SET name = %s, country = %s, image = %s WHERE author_id = %s",
            (name, country, image, author_id),
        )


def delete_author(author_id):
    """[F2.5] Delete an author. ON DELETE CASCADE deletes all of the author's books too."""
    with get_library_db().cursor() as cur:
        cur.execute("DELETE FROM author WHERE author_id = %s", (author_id,))


# ------------------------------------------------------------------ books
def list_books():
    """[F2.1] All books, with the author_id of each one."""
    with get_library_db().cursor() as cur:
        cur.execute("SELECT book_id, title, price, author_id, image FROM book ORDER BY book_id")
        return cur.fetchall()


def list_books_of_author(author_id):
    """Used before deleting an author, to also remove the cover files of the cascaded books."""
    with get_library_db().cursor() as cur:
        cur.execute("SELECT book_id, image FROM book WHERE author_id = %s", (author_id,))
        return cur.fetchall()


def get_book(book_id):
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT book_id, title, price, author_id, image FROM book WHERE book_id = %s",
            (book_id,),
        )
        return cur.fetchone()


def add_book(title, price, author_id, image=None):
    """[F2.2] Add a book. MySQL refuses an author_id that does not exist (error 1452)."""
    try:
        with get_library_db().cursor() as cur:
            cur.execute(
                "INSERT INTO book (title, price, author_id, image) VALUES (%s, %s, %s, %s)",
                (title, price, author_id, image),
            )
    except pymysql.err.IntegrityError as error:
        if error.args[0] == MYSQL_FK_FAILS:
            raise UnknownAuthorError() from error
        raise


def update_book(book_id, title, price, author_id, image):
    """[F2.3] Edit a book."""
    try:
        with get_library_db().cursor() as cur:
            cur.execute(
                "UPDATE book SET title = %s, price = %s, author_id = %s, image = %s "
                "WHERE book_id = %s",
                (title, price, author_id, image, book_id),
            )
    except pymysql.err.IntegrityError as error:
        if error.args[0] == MYSQL_FK_FAILS:
            raise UnknownAuthorError() from error
        raise


def delete_book(book_id):
    """[F2.4] Delete a book."""
    with get_library_db().cursor() as cur:
        cur.execute("DELETE FROM book WHERE book_id = %s", (book_id,))


# ------------------------------------------------------------- Lab 4 queries
def list_categories():
    with get_library_db().cursor() as cur:
        cur.execute("SELECT category_id, name FROM category ORDER BY name")
        return cur.fetchall()


def search_books(keyword, minimum_price, maximum_price, category_id=None):
    sql = (
        "SELECT b.book_id, b.title, b.price, b.publish_year, "
        "a.name AS author_name, p.name AS publisher_name, c.name AS category_name "
        "FROM book b JOIN author a ON b.author_id = a.author_id "
        "JOIN publisher p ON b.publisher_id = p.publisher_id "
        "JOIN category c ON b.category_id = c.category_id "
        "WHERE b.title LIKE %s AND b.price BETWEEN %s AND %s"
    )
    params = [f"%{keyword}%", minimum_price, maximum_price]
    if category_id is not None:
        sql += " AND b.category_id = %s"
        params.append(category_id)
    sql += " ORDER BY b.price ASC, b.title ASC"
    with get_library_db().cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def catalogue():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT b.book_id, b.title, b.price, b.publish_year, "
            "a.name AS author_name, p.name AS publisher_name, c.name AS category_name "
            "FROM book b JOIN author a ON b.author_id = a.author_id "
            "JOIN publisher p ON b.publisher_id = p.publisher_id "
            "JOIN category c ON b.category_id = c.category_id ORDER BY b.title"
        )
        return cur.fetchall()


def report_category_stats():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT c.name AS category_name, COUNT(b.book_id) AS book_count, AVG(b.price) AS average_price "
            "FROM category c LEFT JOIN book b ON b.category_id = c.category_id "
            "GROUP BY c.category_id, c.name ORDER BY c.name"
        )
        return cur.fetchall()


def report_authors_with_two_books():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT a.name AS author_name, COUNT(b.book_id) AS book_count "
            "FROM author a JOIN book b ON b.author_id = a.author_id "
            "GROUP BY a.author_id, a.name HAVING COUNT(b.book_id) >= 2 "
            "ORDER BY book_count DESC, author_name"
        )
        return cur.fetchall()


def report_price_totals():
    with get_library_db().cursor() as cur:
        cur.execute("SELECT SUM(price) AS total_price, MIN(price) AS lowest_price, MAX(price) AS highest_price FROM book")
        return cur.fetchone()


def current_loans():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT l.loan_id, b.title, m.name AS member_name, l.loan_date "
            "FROM loan l JOIN book b ON l.book_id = b.book_id JOIN member m ON l.member_id = m.member_id "
            "WHERE l.return_date IS NULL ORDER BY l.loan_date DESC"
        )
        return cur.fetchall()


def members_without_loans():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT m.member_id, m.name, m.email FROM member m "
            "LEFT JOIN loan l ON l.member_id = m.member_id WHERE l.loan_id IS NULL ORDER BY m.name"
        )
        return cur.fetchall()


def books_without_loans():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT b.book_id, b.title FROM book b LEFT JOIN loan l ON l.book_id = b.book_id "
            "WHERE l.loan_id IS NULL ORDER BY b.title"
        )
        return cur.fetchall()


def most_borrowed_books():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT b.title, COUNT(l.loan_id) AS loan_count FROM book b JOIN loan l ON l.book_id = b.book_id "
            "GROUP BY b.book_id, b.title ORDER BY loan_count DESC, b.title LIMIT 3"
        )
        return cur.fetchall()


def most_active_members():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT m.name AS member_name, COUNT(l.loan_id) AS loan_count FROM member m "
            "JOIN loan l ON l.member_id = m.member_id GROUP BY m.member_id, m.name "
            "ORDER BY loan_count DESC, member_name LIMIT 1"
        )
        return cur.fetchall()


def authors_with_book_counts():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT a.name AS author_name, a.country, COUNT(b.book_id) AS book_count "
            "FROM author a LEFT JOIN book b ON b.author_id = a.author_id "
            "GROUP BY a.author_id, a.name, a.country ORDER BY a.name"
        )
        return cur.fetchall()


def books_same_country():
    with get_library_db().cursor() as cur:
        cur.execute(
            "SELECT b.title, a.name AS author_name, p.name AS publisher_name, a.country "
            "FROM book b JOIN author a ON b.author_id = a.author_id JOIN publisher p ON b.publisher_id = p.publisher_id "
            "WHERE a.country = p.country ORDER BY b.title"
        )
        return cur.fetchall()
