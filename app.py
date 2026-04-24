# app.py — HR API main application
from flask import Flask, request, jsonify
import sqlite3
import hashlib
import subprocess
import pickle
import base64
from config import DB_PASSWORD, JWT_SECRET, DEBUG

app = Flask(__name__)
app.config['DEBUG'] = DEBUG

# ============================================================
# DATABASE HELPER — SQL INJECTION VULNERABILITY
# ============================================================
def get_db():
    conn = sqlite3.connect("hr_database.db")
    return conn

@app.route("/api/employee/search", methods=["GET"])
def search_employee():
    """Search employee by name — VULNERABLE to SQL Injection"""
    name = request.args.get("name", "")

    # VULN: raw string concatenation — SQL Injection
    query = "SELECT * FROM employees WHERE name = '" + name + "'"
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query)                # VULN: unsanitized input
    results = cursor.fetchall()
    return jsonify(results)

# ============================================================
# AUTH — WEAK HASHING & NO RATE LIMIT
# ============================================================
@app.route("/api/login", methods=["POST"])
def login():
    """User login — multiple vulnerabilities"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # VULN: MD5 hashing (broken, should use bcrypt/argon2)
    hashed = hashlib.md5(password.encode()).hexdigest()

    # VULN: SQL Injection again in auth
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashed}'"
    conn = get_db()
    result = conn.execute(query).fetchone()

    if result:
        # VULN: JWT secret from config (weak), no expiry set
        import jwt
        token = jwt.encode({"user": username}, JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token, "status": "ok"})
    
    return jsonify({"status": "failed"}), 401

# ============================================================
# FILE OPERATIONS — PATH TRAVERSAL
# ============================================================
@app.route("/api/report/download", methods=["GET"])
def download_report():
    """Download HR report — VULNERABLE to Path Traversal"""
    filename = request.args.get("file")

    # VULN: no path sanitization — attacker can do ?file=../../etc/passwd
    filepath = "/reports/" + filename
    with open(filepath, "r") as f:
        content = f.read()
    return content

# ============================================================
# COMMAND INJECTION
# ============================================================
@app.route("/api/admin/ping", methods=["POST"])
def ping_server():
    """Admin utility — ping a server"""
    data = request.get_json()
    host = data.get("host")

    # VULN: shell=True + unsanitized input = Command Injection
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return jsonify({"output": result.stdout.decode()})

# ============================================================
# INSECURE DESERIALIZATION
# ============================================================
@app.route("/api/session/restore", methods=["POST"])
def restore_session():
    """Restore user session from cookie"""
    data = request.get_json()
    session_data = data.get("session")

    # VULN: pickle.loads on user-supplied data — Remote Code Execution
    decoded = base64.b64decode(session_data)
    session = pickle.loads(decoded)
    return jsonify({"restored": True, "user": session.get("user")})

# ============================================================
# SENSITIVE DATA EXPOSURE
# ============================================================
@app.route("/api/employee/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    """Get employee detail — no authorization check"""
    # VULN: no auth check — any user can access any employee's data (IDOR)
    conn = get_db()
    result = conn.execute(
        "SELECT id, name, email, salary, bank_account, tax_id FROM employees WHERE id=?",
        (emp_id,)
    ).fetchone()
    # VULN: returns salary, bank_account, tax_id without masking
    return jsonify(result)

@app.route("/api/debug/error", methods=["GET"])
def trigger_error():
    """Debug endpoint — exposes stack trace"""
    # VULN: debug endpoint left in production, reveals internal info
    x = 1 / 0

if __name__ == "__main__":
    # VULN: running on 0.0.0.0 exposes to all interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
