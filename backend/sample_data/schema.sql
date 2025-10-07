-- Sample employee schema for demo
CREATE TABLE IF NOT EXISTS departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name TEXT,
    manager_id INT
);

CREATE TABLE IF NOT EXISTS employees (
    emp_id SERIAL PRIMARY KEY,
    full_name TEXT,
    dept_id INT REFERENCES departments(dept_id),
    position TEXT,
    annual_salary NUMERIC,
    join_date DATE,
    office_location TEXT
);

INSERT INTO departments (dept_name, manager_id) VALUES ('Engineering', 1), ('HR', 2);
INSERT INTO employees (full_name, dept_id, position, annual_salary, join_date, office_location)
VALUES 
('Alice Johnson', 1, 'Software Engineer', 120000, '2022-06-15', 'Bengaluru'),
('Bob Smith', 1, 'Senior Engineer', 140000, '2020-03-20', 'Bengaluru'),
('Carol Lee', 2, 'HR Manager', 90000, '2019-11-12', 'Cuttack');
