from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key_here'  # Replace with a real secret key

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('timeflow_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Determine table and columns based on role
        if role == 'supervisor':
            table = 'Supervisors'
            email_col = 'supervisor_email'
            pwd_col = 'supervisor_pwd'
            id_col = 'supervisor_id'
        else:
            table = 'Employees'
            email_col = 'employee_email'
            pwd_col = 'employee_pwd'
            id_col = 'employee_id'

        try:
            conn = get_db_connection()
            user = conn.execute(
                f'SELECT {id_col} FROM {table} WHERE {email_col} = ? AND {pwd_col} = ?',
                (email, password)
            ).fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user[id_col]
                session['role'] = role
                return redirect(url_for('boss_dashboard' if role == 'supervisor' else 'employee_dashboard'))
            
            return render_template('login.html', error='Invalid credentials')
        except Exception as e:
            print(f"Database error: {str(e)}")
            return render_template('login.html', error='Database error occurred')

    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'user_id' not in session or session['role'] != 'employee':
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        employee = conn.execute(
            'SELECT * FROM Employees WHERE employee_id = ?',
            (session['user_id'],)
        ).fetchone()
        conn.close()
        
        return render_template('employee_dashboard.html', employee=employee)
    except Exception as e:
        return redirect(url_for('login'))

@app.route('/boss_dashboard')
def boss_dashboard():
    if 'user_id' not in session or session['role'] != 'supervisor':
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        supervisor = conn.execute(
            'SELECT * FROM Supervisors WHERE supervisor_id = ?',
            (session['user_id'],)
        ).fetchone()
        
        employees = conn.execute(
            'SELECT * FROM Employees WHERE supervisor_id = ?',
            (session['user_id'],)
        ).fetchall()
        conn.close()
        
        return render_template('boss_dashboard.html', 
                             supervisor=supervisor,
                             employees=employees)
    except Exception as e:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)