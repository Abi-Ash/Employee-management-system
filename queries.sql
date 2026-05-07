-- Active: 1757175701698@@127.0.0.1@3306@employee_db
-- created db
CREATE DATABASE employee_db;

-- main table
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    department VARCHAR(100),
    salary INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- indexing
CREATE INDEX idx_employee_email ON employees(email);

-- audit table
CREATE TABLE employee_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    action_type VARCHAR(50),
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- create trigger
CREATE TRIGGER after_employee_insert 
AFTER INSERT ON employees
FOR EACH ROW 
INSERT INTO employee_logs(employee_id, action_type) VALUES (NEW.id, 'INSERT');


-- stored procedure
DELIMITER//

CREATE PROCEDURE GetAllEmployees()
BEGIN
    SELECT * FROM employees;
END//
DELIMITER;


SELECT * FROM employees;
SELECT * FROM employee_logs;