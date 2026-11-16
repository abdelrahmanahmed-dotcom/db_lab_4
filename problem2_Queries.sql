USE library;

-- F2.1 Search books: replace the example values with form parameters.
SET @title_keyword = '';
SET @minimum_price = 0;
SET @maximum_price = 1000000;
SET @category_id = NULL;
-- F2.1
SELECT b.title, b.price, a.name AS author_name, p.name AS publisher_name, c.name AS category_name
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
JOIN category c ON b.category_id = c.category_id
WHERE b.title LIKE CONCAT('%', @title_keyword, '%')
  AND b.price BETWEEN @minimum_price AND @maximum_price
  AND (@category_id IS NULL OR b.category_id = @category_id)
ORDER BY b.price ASC;

-- F2.2
SELECT b.title, b.price, b.publish_year, a.name AS author_name,
       p.name AS publisher_name, c.name AS category_name
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
JOIN category c ON b.category_id = c.category_id
ORDER BY b.title;

-- F2.3a
SELECT c.name AS category_name, COUNT(b.book_id) AS book_count, AVG(b.price) AS average_price
FROM category c
LEFT JOIN book b ON b.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY c.name;

-- F2.3b
SELECT a.name AS author_name, COUNT(b.book_id) AS book_count
FROM author a
JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2
ORDER BY book_count DESC;

-- F2.3c
SELECT SUM(price) AS total_price, MIN(price) AS lowest_price, MAX(price) AS highest_price
FROM book;

-- F2.4a
SELECT b.title, m.name AS member_name, l.loan_date
FROM loan l
JOIN book b ON l.book_id = b.book_id
JOIN member m ON l.member_id = m.member_id
WHERE l.return_date IS NULL
ORDER BY l.loan_date DESC;

-- F2.4b
SELECT m.name, m.email
FROM member m
LEFT JOIN loan l ON l.member_id = m.member_id
WHERE l.loan_id IS NULL
ORDER BY m.name;

-- F2.4c
SELECT b.title
FROM book b
LEFT JOIN loan l ON l.book_id = b.book_id
WHERE l.loan_id IS NULL
ORDER BY b.title;

-- F2.5a
SELECT b.title, COUNT(l.loan_id) AS loan_count
FROM book b
JOIN loan l ON l.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY loan_count DESC, b.title
LIMIT 3;

-- F2.5b
SELECT m.name AS member_name, COUNT(l.loan_id) AS loan_count
FROM member m
JOIN loan l ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
ORDER BY loan_count DESC, m.name
LIMIT 1;

-- F2.6a
SELECT a.name AS author_name, a.country, COUNT(b.book_id) AS book_count
FROM author a
LEFT JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name, a.country
ORDER BY a.name;

-- F2.6b
SELECT b.title, a.name AS author_name, p.name AS publisher_name, a.country
FROM book b
JOIN author a ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country
ORDER BY b.title;
