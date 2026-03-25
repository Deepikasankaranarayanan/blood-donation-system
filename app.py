from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta
import csv
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = "blood_secret"


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return sqlite3.connect("database.db")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        if username=="admin" and password=="admin":
            session["user"]="admin"
            return redirect("/")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user",None)
    return redirect("/login")


# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE donated='Yes'")
    donated_students=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE donated='No'")
    available_donors=cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        donated_students=donated_students,
        available_donors=available_donors
    )


# ---------------- ADD STUDENT PAGE ----------------
@app.route("/add_student_page")
def add_student_page():

    if "user" not in session:
        return redirect("/login")

    return render_template("add_student.html")


# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():

    name=request.form["name"]
    reg_no=request.form["reg_no"]
    department=request.form["department"]
    dept_no=request.form["dept_no"]
    year=request.form["year"]
    blood_group=request.form["blood_group"]
    phone=request.form["phone"]
    donated=request.form["donated"]

    last_donated=request.form.get("last_donated")

    next_date=None

    if donated=="Yes" and last_donated:

        last_donated=datetime.strptime(last_donated,"%Y-%m-%d").date()
        next_date=last_donated+timedelta(days=90)

    else:

        last_donated=None
        next_date=None


    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name,reg_no,department,dept_no,year,blood_group,phone,donated,last_donated,next_date)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """,(name,reg_no,department,dept_no,year,blood_group,phone,donated,last_donated,next_date))

    conn.commit()
    conn.close()

    return redirect("/students_database")


# ---------------- STUDENT DATABASE ----------------
@app.route("/students_database")
def students_database():

    if "user" not in session:
        return redirect("/login")

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM students")
    students=cursor.fetchall()

    conn.close()

    return render_template("students_database.html",students=students)


# ---------------- DELETE STUDENT ----------------
@app.route("/delete_student/<int:id>")
def delete_student(id):

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?",(id,))

    conn.commit()
    conn.close()

    return redirect("/students_database")


# ---------------- SEARCH DONORS ----------------
@app.route("/search",methods=["GET","POST"])
def search():

    students=[]

    if request.method=="POST":

        blood_group=request.form["blood_group"]

        conn=get_db()
        cursor=conn.cursor()

        cursor.execute(
        "SELECT * FROM students WHERE blood_group=?",
        (blood_group,)
        )

        students=cursor.fetchall()

        conn.close()

    return render_template("search.html",students=students)


# ---------------- DONATED STUDENTS ----------------
@app.route("/donated")
def donated():

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM students WHERE donated='Yes'")
    students=cursor.fetchall()

    conn.close()

    return render_template("donated_students.html",students=students)
@app.route("/upload_csv", methods=["POST"])
def upload_csv():

    file = request.files["file"]

    if not file:
        return "No file uploaded"

    conn = get_db()
    cursor = conn.cursor()

    csv_file = file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(csv_file)

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

    return redirect("/students_database")

# ---------------- RUN SERVER ----------------
if __name__=="__main__":
    app.run(debug=True)