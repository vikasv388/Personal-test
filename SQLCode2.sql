
CREATE TABLE Students (
    id INT,
    name VARCHAR(50),
    age INT
);

INSERT INTO Students VALUES
(1, 'Rahul', 22),
(2, 'Priya', 21),
(3, 'Aman', 23);

-- Check all records
SELECT * FROM Students;

-- Check specific record
SELECT * FROM Students WHERE id = 1;

-- Check duplicate IDs
SELECT id, COUNT(*)
FROM Students
GROUP BY id
HAVING COUNT(*) > 1;

-- Check NULL values
SELECT * FROM Students WHERE name IS NULL;

-- Count records
SELECT COUNT(*) FROM Students;
