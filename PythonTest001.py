
import sqlite3

DATABASE = "hospital.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        address TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT,
        time TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        amount REAL,
        description TEXT,
        bill_date TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)

    cursor.execute(
        "SELECT id FROM users WHERE username = ?", ("admin",)
    )

    if not cursor.fetchone():
        from werkzeug.security import generate_password_hash

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", generate_password_hash("admin123"))
        )

    conn.commit()
    conn.close()



from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from werkzeug.security import check_password_hash
from database import get_db, init_db
from functools import wraps
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

init_db()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()

    patients = conn.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    doctors = conn.execute(
        "SELECT COUNT(*) FROM doctors"
    ).fetchone()[0]

    appointments = conn.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]

    bills = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM bills"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        patients=patients,
        doctors=doctors,
        appointments=appointments,
        bills=bills
    )


# PATIENTS
@app.route("/patients")
@login_required
def patients():
    conn = get_db()
    data = conn.execute(
        "SELECT * FROM patients ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("patients.html", patients=data)


@app.route("/add_patient", methods=["GET", "POST"])
@login_required
def add_patient():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        address = request.form["address"]

        if not name.strip():
            flash("Patient name is required", "danger")
            return redirect(url_for("add_patient"))

        conn = get_db()
        conn.execute("""
            INSERT INTO patients
            (name, age, gender, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, gender, phone, address))

        conn.commit()
        conn.close()

        flash("Patient added successfully", "success")
        return redirect(url_for("patients"))

    return render_template("add_patient.html")


@app.route("/delete_patient/<int:id>", methods=["POST"])
@login_required
def delete_patient(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM appointments WHERE patient_id=?", (id,)
    )
    conn.execute(
        "DELETE FROM bills WHERE patient_id=?", (id,)
    )
    conn.execute(
        "DELETE FROM patients WHERE id=?", (id,)
    )

    conn.commit()
    conn.close()

    flash("Patient deleted", "success")
    return redirect(url_for("patients"))


# DOCTORS
@app.route("/doctors")
@login_required
def doctors():
    conn = get_db()
    data = conn.execute(
        "SELECT * FROM doctors ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("doctors.html", doctors=data)


@app.route("/add_doctor", methods=["GET", "POST"])
@login_required
def add_doctor():
    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]

        conn = get_db()
        conn.execute("""
            INSERT INTO doctors (name, specialization, phone)
            VALUES (?, ?, ?)
        """, (name, specialization, phone))

        conn.commit()
        conn.close()

        flash("Doctor added successfully", "success")
        return redirect(url_for("doctors"))

    return render_template("add_doctor.html")


@app.route("/delete_doctor/<int:id>", methods=["POST"])
@login_required
def delete_doctor(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM appointments WHERE doctor_id=?", (id,)
    )
    conn.execute("DELETE FROM doctors WHERE id=?", (id,))

    conn.commit()
    conn.close()

    flash("Doctor deleted", "success")
    return redirect(url_for("doctors"))


# APPOINTMENTS
@app.route("/appointments")
@login_required
def appointments():
    conn = get_db()

    data = conn.execute("""
        SELECT appointments.*,
        patients.name AS patient_name,
        doctors.name AS doctor_name
        FROM appointments
        LEFT JOIN patients
        ON appointments.patient_id = patients.id
        LEFT JOIN doctors
        ON appointments.doctor_id = doctors.id
        ORDER BY appointments.id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "appointments.html", appointments=data
    )


@app.route("/add_appointment", methods=["GET", "POST"])
@login_required
def add_appointment():
    conn = get_db()

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        doctor_id = request.form["doctor_id"]
        appointment_date = request.form["date"]
        appointment_time = request.form["time"]

        if appointment_date < date.today().isoformat():
            flash("Appointment date cannot be in the past", "danger")
            conn.close()
            return redirect(url_for("add_appointment"))

        conn.execute("""
            INSERT INTO appointments
            (patient_id, doctor_id, date, time)
            VALUES (?, ?, ?, ?)
        """, (
            patient_id, doctor_id,
            appointment_date, appointment_time
        ))

        conn.commit()
        conn.close()

        flash("Appointment booked", "success")
        return redirect(url_for("appointments"))

    patients = conn.execute(
        "SELECT * FROM patients"
    ).fetchall()

    doctors = conn.execute(
        "SELECT * FROM doctors"
    ).fetchall()

    conn.close()

    return render_template(
        "add_appointment.html",
        patients=patients,
        doctors=doctors
    )


@app.route("/appointment_status/<int:id>", methods=["POST"])
@login_required
def appointment_status(id):
    status = request.form["status"]

    if status not in ["Pending", "Confirmed", "Completed", "Cancelled"]:
        flash("Invalid appointment status", "danger")
        return redirect(url_for("appointments"))

    conn = get_db()
    conn.execute(
        "UPDATE appointments SET status=? WHERE id=?",
        (status, id)
    )
    conn.commit()
    conn.close()

    flash("Appointment status updated", "success")
    return redirect(url_for("appointments"))


# BILLING
@app.route("/billing")
@login_required
def billing():
    conn = get_db()

    data = conn.execute("""
        SELECT bills.*, patients.name AS patient_name
        FROM bills
        LEFT JOIN patients ON bills.patient_id=patients.id
        ORDER BY bills.id DESC
    """).fetchall()

    conn.close()

    return render_template("billing.html", bills=data)


@app.route("/add_bill", methods=["GET", "POST"])
@login_required
def add_bill():
    conn = get_db()

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        amount = request.form["amount"]
        description = request.form["description"]

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Enter a valid positive bill amount", "danger")
            conn.close()
            return redirect(url_for("add_bill"))

        conn.execute("""
            INSERT INTO bills
            (patient_id, amount, description, bill_date)
            VALUES (?, ?, ?, ?)
        """, (
            patient_id, amount,
            description, date.today().isoformat()
        ))

        conn.commit()
        conn.close()

        flash("Bill generated successfully", "success")
        return redirect(url_for("billing"))

    patients = conn.execute(
        "SELECT * FROM patients"
    ).fetchall()

    conn.close()

    return render_template("add_bill.html", patients=patients)


if __name__ == "__main__":
    app.run(debug=True)




<!DOCTYPE html>
<html>
<head>
    <title>Hospital Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

{% if session.get('user') %}
<nav class="navbar navbar-dark bg-primary px-4">
    <a class="navbar-brand" href="{{ url_for('dashboard') }}">
        Hospital Management
    </a>
    <a href="{{ url_for('logout') }}" class="btn btn-light">
        Logout
    </a>
</nav>

<div class="container-fluid">
    <div class="row">
        <aside class="col-md-2 bg-light sidebar p-3">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('patients') }}">Patients</a>
            <a href="{{ url_for('doctors') }}">Doctors</a>
            <a href="{{ url_for('appointments') }}">Appointments</a>
            <a href="{{ url_for('billing') }}">Billing</a>
        </aside>

        <main class="col-md-10 p-4">
{% else %}
<main class="container p-4">
{% endif %}

{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">
            {{ message }}
        </div>
    {% endfor %}
{% endwith %}

{% block content %}{% endblock %}

</main>

</div>
</body>
</html>



{% extends 'base.html' %}
{% block content %}

<div class="login-box">
    <h2>Hospital Admin Login</h2>

    <form method="POST">
        <input name="username" class="form-control mb-3"
               placeholder="Username" required>

        <input name="password" type="password"
               class="form-control mb-3"
               placeholder="Password" required>

        <button class="btn btn-primary w-100">
            Login
        </button>
    </form>

    <p class="mt-3 text-muted">
        Default: admin / admin123
    </p>
</div>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Hospital Dashboard</h2>
<p>Welcome to Hospital Management System</p>

<div class="row g-3 mt-3">

    <div class="col-md-3">
        <div class="card dashboard-card bg-primary text-white">
            <h5>Total Patients</h5>
            <h2>{{ patients }}</h2>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card dashboard-card bg-success text-white">
            <h5>Total Doctors</h5>
            <h2>{{ doctors }}</h2>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card dashboard-card bg-warning">
            <h5>Appointments</h5>
            <h2>{{ appointments }}</h2>
        </div>
    </div>

    <div class="col-md-3">
        <div class="card dashboard-card bg-info text-white">
            <h5>Total Billing</h5>
            <h2>₹{{ bills }}</h2>
        </div>
    </div>

</div>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Patient Management</h2>

<a href="{{ url_for('add_patient') }}"
   class="btn btn-primary mb-3">Add Patient</a>

<table class="table table-bordered table-striped">
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Age</th>
        <th>Gender</th>
        <th>Phone</th>
        <th>Address</th>
        <th>Action</th>
    </tr>

    {% for p in patients %}
    <tr>
        <td>{{ p.id }}</td>
        <td>{{ p.name }}</td>
        <td>{{ p.age }}</td>
        <td>{{ p.gender }}</td>
        <td>{{ p.phone }}</td>
        <td>{{ p.address }}</td>
        <td>
            <form method="POST"
                  action="{{ url_for('delete_patient', id=p.id) }}"
                  onsubmit="return confirm('Delete this patient?')">
                <button class="btn btn-danger btn-sm">
                    Delete
                </button>
            </form>
        </td>
    </tr>
    {% endfor %}
</table>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Add New Patient</h2>

<form method="POST" class="form-box">

    <input name="name" class="form-control mb-3"
           placeholder="Patient Name" required>

    <input name="age" type="number" min="0" max="130"
           class="form-control mb-3" placeholder="Age">

    <select name="gender" class="form-control mb-3">
        <option value="">Select Gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
    </select>

    <input name="phone" class="form-control mb-3"
           placeholder="Phone Number">

    <textarea name="address" class="form-control mb-3"
              placeholder="Address"></textarea>

    <button class="btn btn-success">Save Patient</button>

</form>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Doctor Management</h2>

<a href="{{ url_for('add_doctor') }}"
   class="btn btn-primary mb-3">Add Doctor</a>

<table class="table table-bordered">
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Specialization</th>
        <th>Phone</th>
        <th>Action</th>
    </tr>

    {% for d in doctors %}
    <tr>
        <td>{{ d.id }}</td>
        <td>{{ d.name }}</td>
        <td>{{ d.specialization }}</td>
        <td>{{ d.phone }}</td>
        <td>
            <form method="POST"
                  action="{{ url_for('delete_doctor', id=d.id) }}"
                  onsubmit="return confirm('Delete this doctor?')">
                <button class="btn btn-danger btn-sm">
                    Delete
                </button>
            </form>
        </td>
    </tr>
    {% endfor %}
</table>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Add Doctor</h2>

<form method="POST" class="form-box">

    <input name="name" class="form-control mb-3"
           placeholder="Doctor Name" required>

    <input name="specialization"
           class="form-control mb-3"
           placeholder="Specialization">

    <input name="phone" class="form-control mb-3"
           placeholder="Phone">

    <button class="btn btn-success">Save Doctor</button>

</form>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Appointment Management</h2>

<a href="{{ url_for('add_appointment') }}"
   class="btn btn-primary mb-3">Book Appointment</a>

<table class="table table-bordered">
    <tr>
        <th>ID</th>
        <th>Patient</th>
        <th>Doctor</th>
        <th>Date</th>
        <th>Time</th>
        <th>Status</th>
        <th>Update</th>
    </tr>

    {% for a in appointments %}
    <tr>
        <td>{{ a.id }}</td>
        <td>{{ a.patient_name }}</td>
        <td>{{ a.doctor_name }}</td>
        <td>{{ a.date }}</td>
        <td>{{ a.time }}</td>
        <td>{{ a.status }}</td>
        <td>
            <form method="POST"
                  action="{{ url_for('appointment_status', id=a.id) }}">
                <select name="status" class="form-select mb-1">
                    {% for s in ['Pending','Confirmed','Completed','Cancelled'] %}
                    <option value="{{ s }}"
                        {% if a.status == s %}selected{% endif %}>
                        {{ s }}
                    </option>
                    {% endfor %}
                </select>
                <button class="btn btn-sm btn-success">
                    Update
                </button>
            </form>
        </td>
    </tr>
    {% endfor %}
</table>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Book Appointment</h2>

{% if not patients or not doctors %}
<p class="alert alert-warning">
    Please register at least one patient and one doctor first.
</p>
{% endif %}

<form method="POST" class="form-box">

    <label>Patient</label>
    <select name="patient_id" class="form-control mb-3" required>
        {% for p in patients %}
        <option value="{{ p.id }}">{{ p.name }}</option>
        {% endfor %}
    </select>

    <label>Doctor</label>
    <select name="doctor_id" class="form-control mb-3" required>
        {% for d in doctors %}
        <option value="{{ d.id }}">
            {{ d.name }} - {{ d.specialization }}
        </option>
        {% endfor %}
    </select>

    <label>Date</label>
    <input type="date" name="date"
           min="{{ none }}" class="form-control mb-3" required>

    <label>Time</label>
    <input type="time" name="time"
           class="form-control mb-3" required>

    <button class="btn btn-success"
            {% if not patients or not doctors %}disabled{% endif %}>
        Book Appointment
    </button>

</form>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Billing Management</h2>

<a href="{{ url_for('add_bill') }}"
   class="btn btn-primary mb-3">Generate Bill</a>

<table class="table table-bordered">
    <tr>
        <th>ID</th>
        <th>Patient</th>
        <th>Amount</th>
        <th>Description</th>
        <th>Date</th>
    </tr>

    {% for b in bills %}
    <tr>
        <td>{{ b.id }}</td>
        <td>{{ b.patient_name }}</td>
        <td>₹{{ b.amount }}</td>
        <td>{{ b.description }}</td>
        <td>{{ b.bill_date }}</td>
    </tr>
    {% endfor %}
</table>

{% endblock %}



{% extends 'base.html' %}
{% block content %}

<h2>Generate Patient Bill</h2>

<form method="POST" class="form-box">

    <label>Select Patient</label>
    <select name="patient_id" class="form-control mb-3" required>
        {% for p in patients %}
        <option value="{{ p.id }}">{{ p.name }}</option>
        {% endfor %}
    </select>

    <label>Amount (₹)</label>
    <input type="number" name="amount" step="0.01"
           min="0.01" class="form-control mb-3" required>

    <label>Description</label>
    <textarea name="description"
              class="form-control mb-3"></textarea>

    <button class="btn btn-success">Generate Bill</button>

</form>

{% endblock %}



body {
    background: #f4f7fb;
    font-family: Arial, sans-serif;
}

.sidebar {
    min-height: 90vh;
}

.sidebar a {
    display: block;
    padding: 13px;
    margin-bottom: 8px;
    text-decoration: none;
    color: #222;
    border-radius: 6px;
}

.sidebar a:hover {
    background: #dceaff;
    color: #0d6efd;
}

.dashboard-card {
    padding: 25px;
    border: none;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.form-box {
    max-width: 600px;
    background: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.login-box {
    max-width: 400px;
    margin: 80px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
}

table {
    background: white;
}
