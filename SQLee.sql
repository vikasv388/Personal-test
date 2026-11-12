CREATE TABLE Student (
    id INT,
    name VARCHAR(20),
    age INT
);

INSERT INTO Student VALUES
(1, 'Rahul', 20),
(2, 'Amit', 21);

SELECT * FROM Student;

UPDATE Student
SET age = 22
WHERE id = 1;

DELETE FROM Student
WHERE id = 2;
