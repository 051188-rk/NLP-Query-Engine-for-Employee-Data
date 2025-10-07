import random
import psycopg2
from datetime import date, timedelta

# --- CONFIGURATION ---
# Format: postgresql://username:password@localhost:port/database
DB_URI = "postgresql://postgres:admin123@localhost:5432/company_db"
# --- CONNECTION ---
conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

# --- SAMPLE DATA ---
departments = [
    "Engineering", "Human Resources", "Finance", "Marketing", "Sales",
    "Operations", "Support", "Research", "IT", "Design"
]

# Insert 10 departments
cur.execute("DELETE FROM employees;")
cur.execute("DELETE FROM departments;")
for d in departments:
    manager_id = random.randint(1, 50)
    cur.execute("INSERT INTO departments (dept_name, manager_id) VALUES (%s, %s);", (d, manager_id))

# Fetch all department IDs for reference
cur.execute("SELECT dept_id FROM departments;")
dept_ids = [row[0] for row in cur.fetchall()]

positions = [
    "Software Engineer", "Data Analyst", "Project Manager", "HR Executive",
    "Marketing Specialist", "Sales Executive", "System Admin",
    "Product Designer", "Finance Associate", "QA Engineer"
]

cities = ["Bhubaneswar", "Cuttack", "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi"]

# Insert 30 employees
for i in range(1, 31):
    name = f"Employee {i}"
    dept = random.choice(dept_ids)
    position = random.choice(positions)
    salary = random.randint(50000, 180000)
    join_date = date.today() - timedelta(days=random.randint(100, 2000))
    city = random.choice(cities)
    cur.execute(
        "INSERT INTO employees (full_name, dept_id, position, annual_salary, join_date, office_location) VALUES (%s, %s, %s, %s, %s, %s);",
        (name, dept, position, salary, join_date, city)
    )

conn.commit()
cur.close()
conn.close()
print("✅ Inserted 10 departments and 30 employees successfully!")
