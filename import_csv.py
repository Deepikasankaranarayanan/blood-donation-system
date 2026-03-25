import sqlite3
import csv
from datetime import datetime, timedelta

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

with open("student.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        name = row["name"]
        reg_no = row["reg_no"]
        department = row["department"]
        dept_no = row["dept_no"]
        year = row["year"]
        blood_group = row["blood_group"]
        phone = row["phone"]
        donated = row["donated"]
        last_donated = row["last_donated"]

        next_date = None

        if donated == "Yes" and last_donated:

            last_donated = datetime.strptime(last_donated,"%Y-%m-%d").date()
            next_date = last_donated + timedelta(days=90)

        cursor.execute("""
        INSERT INTO students
        (name,reg_no,department,dept_no,year,blood_group,phone,donated,last_donated,next_date)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,(name,reg_no,department,dept_no,year,blood_group,phone,donated,last_donated,next_date))

conn.commit()
conn.close()

print("CSV imported successfully")