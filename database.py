import sqlite3
from datetime import date

DATABASE_NAME = "ngo.db"


# -----------------------------
# Database Connection
# -----------------------------

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# -----------------------------
# Create Tables
# -----------------------------

def create_tables():
    connection = get_connection()

    # Beneficiaries
    connection.execute("""
        CREATE TABLE IF NOT EXISTS beneficiaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT,
            vulnerability_category TEXT,
            registration_date TEXT DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'Active'
        )
    """)

    # Projects
    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            location TEXT,
            start_date TEXT,
            end_date TEXT,
            budget REAL DEFAULT 0,
            status TEXT DEFAULT 'Planned'
        )
    """)

    # Resources
    connection.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            unit TEXT,
            quantity REAL DEFAULT 0
        )
    """)

    # Distributions
    connection.execute("""
        CREATE TABLE IF NOT EXISTS distributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beneficiary_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            resource_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            distribution_date TEXT DEFAULT CURRENT_DATE,
            location TEXT,

            FOREIGN KEY (beneficiary_id)
                REFERENCES beneficiaries(id),

            FOREIGN KEY (project_id)
                REFERENCES projects(id),

            FOREIGN KEY (resource_id)
                REFERENCES resources(id)
        )
    """)

    # Volunteers
    connection.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            skills TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    # Volunteer Assignments
    connection.execute("""
        CREATE TABLE IF NOT EXISTS volunteer_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            assignment_date TEXT DEFAULT CURRENT_DATE,
            role TEXT,

            FOREIGN KEY (volunteer_id)
                REFERENCES volunteers(id),

            FOREIGN KEY (project_id)
                REFERENCES projects(id)
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------
# Beneficiary - CREATE
# -----------------------------

def add_beneficiary(
    name,
    age,
    gender,
    phone,
    address,
    vulnerability_category
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO beneficiaries (
            name,
            age,
            gender,
            phone,
            address,
            vulnerability_category,
            registration_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        phone,
        address,
        vulnerability_category,
        date.today().isoformat()
    ))

    beneficiary_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return beneficiary_id


# -----------------------------
# Beneficiary - READ
# -----------------------------

def get_beneficiaries():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            id,
            name,
            age,
            gender,
            phone,
            address,
            vulnerability_category,
            registration_date,
            status
        FROM beneficiaries
        ORDER BY id DESC
    """)

    beneficiaries = cursor.fetchall()

    connection.close()

    return beneficiaries


# -----------------------------
# Beneficiary - UPDATE
# -----------------------------

def update_beneficiary(
    beneficiary_id,
    name,
    age,
    gender,
    phone,
    address,
    vulnerability_category,
    status
):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE beneficiaries
        SET
            name = ?,
            age = ?,
            gender = ?,
            phone = ?,
            address = ?,
            vulnerability_category = ?,
            status = ?
        WHERE id = ?
    """, (
        name,
        age,
        gender,
        phone,
        address,
        vulnerability_category,
        status,
        beneficiary_id
    ))

    connection.commit()
    connection.close()

    return cursor.rowcount


# -----------------------------
# Beneficiary - DEACTIVATE
# -----------------------------

def deactivate_beneficiary(beneficiary_id):
    connection = get_connection()

    cursor = connection.execute("""
        UPDATE beneficiaries
        SET status = 'Inactive'
        WHERE id = ?
    """, (beneficiary_id,))

    connection.commit()
    connection.close()

    return cursor.rowcount


# -----------------------------
# Project - CREATE
# -----------------------------

def add_project(
    name,
    description,
    location,
    start_date,
    end_date,
    budget,
    status="Planned"
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO projects (
            name,
            description,
            location,
            start_date,
            end_date,
            budget,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        description,
        location,
        start_date,
        end_date,
        budget,
        status
    ))

    project_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return project_id


# -----------------------------
# Project - READ
# -----------------------------

def get_projects():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            id,
            name,
            description,
            location,
            start_date,
            end_date,
            budget,
            status
        FROM projects
        ORDER BY id DESC
    """)

    projects = cursor.fetchall()

    connection.close()

    return projects


# -----------------------------
# Resource - CREATE
# -----------------------------

def add_resource(
    name,
    category,
    unit,
    quantity
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO resources (
            name,
            category,
            unit,
            quantity
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        category,
        unit,
        quantity
    ))

    resource_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return resource_id


# -----------------------------
# Resource - READ
# -----------------------------

def get_resources():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            id,
            name,
            category,
            unit,
            quantity
        FROM resources
        ORDER BY id DESC
    """)

    resources = cursor.fetchall()

    connection.close()

    return resources


# -----------------------------
# Volunteer - CREATE
# -----------------------------

def add_volunteer(
    name,
    phone,
    email,
    skills,
    status="Active"
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO volunteers (
            name,
            phone,
            email,
            skills,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        email,
        skills,
        status
    ))

    volunteer_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return volunteer_id


# -----------------------------
# Volunteer - READ
# -----------------------------

def get_volunteers():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            skills,
            status
        FROM volunteers
        ORDER BY id DESC
    """)

    volunteers = cursor.fetchall()

    connection.close()

    return volunteers


# -----------------------------
# Initialize Database
# -----------------------------
def add_distribution(
    beneficiary_id,
    project_id,
    resource_id,
    quantity,
    distribution_date,
    location
):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO distributions (
            beneficiary_id,
            project_id,
            resource_id,
            quantity,
            distribution_date,
            location
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        beneficiary_id,
        project_id,
        resource_id,
        quantity,
        distribution_date,
        location
    ))

    distribution_id = cursor.lastrowid

    connection.execute("""
        UPDATE resources
        SET quantity = quantity - ?
        WHERE id = ?
    """, (
        quantity,
        resource_id
    ))

    connection.commit()
    connection.close()

    return distribution_id


def get_distributions():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT
            d.id,
            b.name,
            p.name,
            r.name,
            d.quantity,
            d.distribution_date,
            d.location
        FROM distributions d
        JOIN beneficiaries b
            ON d.beneficiary_id = b.id
        JOIN projects p
            ON d.project_id = p.id
        JOIN resources r
            ON d.resource_id = r.id
        ORDER BY d.id DESC
    """)

    distributions = cursor.fetchall()

    connection.close()

    return distributions
if __name__ == "__main__":
    create_tables()
    print("Database initialized successfully!")