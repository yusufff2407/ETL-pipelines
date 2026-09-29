import sqlite3
conn = sqlite3.connect("college.db")
print("Database created succesfully")

students = """ CREATE TABLE IF NOT EXISTS STUDENT_SY1 (
NAME TEXT,
ADDRESS TEXT,
AGE INT, 
PERCENTAGE_12TH REAL
); """

conn.execute(students)
print("Table Succcessfully created")

conn.close