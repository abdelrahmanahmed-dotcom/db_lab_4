USE library;

INSERT INTO author (author_id, name, country) VALUES
    (1, 'Naguib Mahfouz', 'Egypt'),
    (2, 'Agatha Christie', 'United Kingdom'),
    (3, 'J. K. Rowling', 'United Kingdom'),
    (4, 'Gabriel Garcia Marquez', 'Colombia'),
    (5, 'Toni Morrison', 'United States');

INSERT INTO publisher (publisher_id, name, country) VALUES
    (1, 'Nile House', 'Egypt'),
    (2, 'Penguin Classics', 'United Kingdom'),
    (3, 'Andes Press', 'Colombia');

INSERT INTO category (category_id, name) VALUES
    (1, 'Literary Fiction'),
    (2, 'Mystery'),
    (3, 'Fantasy'),
    (4, 'History');

INSERT INTO book (book_id, title, price, publish_year, author_id, publisher_id, category_id) VALUES
    (1, 'Palace Walk', 18.50, 1956, 1, 1, 1),
    (2, 'Palace of Desire', 22.00, 1957, 1, 1, 1),
    (3, 'Murder on the Orient Express', 16.75, 1934, 2, 2, 2),
    (4, 'And Then There Were None', 19.99, 1939, 2, 2, 2),
    (5, 'Harry Potter and the Philosopher Stone', 25.00, 1997, 3, 2, 3),
    (6, 'Harry Potter and the Chamber of Secrets', 24.50, 1998, 3, 2, 3),
    (7, 'One Hundred Years of Solitude', 20.00, 1967, 4, 3, 1),
    (8, 'Love in the Time of Cholera', 21.25, 1985, 4, 3, 1),
    (9, 'Beloved', 17.50, 1987, 5, 1, 1),
    (10, 'The Unborrowed Chronicle', 14.00, 2024, 1, 1, 4);

INSERT INTO member (member_id, name, email, join_date) VALUES
    (1, 'Mariam Hassan', 'mariam@example.com', '2026-01-10'),
    (2, 'Omar Adel', 'omar@example.com', '2026-02-14'),
    (3, 'Salma Nabil', 'salma@example.com', '2026-03-20'),
    (4, 'Youssef Samir', 'youssef@example.com', '2026-04-02'),
    (5, 'Hana Fathy', 'hana@example.com', '2026-05-11');

INSERT INTO loan (loan_id, book_id, member_id, loan_date, return_date) VALUES
    (1, 1, 1, '2026-09-01', '2026-09-10'),
    (2, 1, 2, '2026-10-01', NULL),
    (3, 2, 1, '2026-08-03', '2026-08-15'),
    (4, 3, 2, '2026-09-05', '2026-09-15'),
    (5, 3, 3, '2026-10-04', NULL),
    (6, 4, 1, '2026-07-07', '2026-07-20'),
    (7, 4, 2, '2026-08-07', '2026-08-18'),
    (8, 5, 3, '2026-09-12', NULL),
    (9, 5, 4, '2026-10-12', NULL),
    (10, 6, 1, '2026-06-10', '2026-06-22'),
    (11, 7, 4, '2026-08-25', '2026-09-02'),
    (12, 8, 2, '2026-09-28', NULL);
