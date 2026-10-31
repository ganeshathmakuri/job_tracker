from flask import Flask, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='sql password',
        database='jobtracker'
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET'])
def add():
    return render_template('add.html')

@app.route('/submit', methods=['POST'])
def submit():
    company = request.form['company']
    role = request.form['role']
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO applications (company, role,status) VALUES (%s, %s, %s)',
              (company, role, request.form.get('status','Applied')))
    conn.commit()
    conn.close()
    return redirect(url_for('jobs'))

@app.route('/jobs')
def jobs():
    conn = get_db()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT * FROM applications ORDER BY id DESC')
    apps = c.fetchall()
    conn.close()
    return render_template('jobs.html', applications=apps)

@app.route('/edit/<int:app_id>', methods=['GET', 'POST'])
def edit(app_id):
    db = get_db()
    cur = db.cursor(dictionary=True)

    if request.method == 'POST':
        cur.execute(
            "UPDATE applications SET company=%s, role=%s, status=%s WHERE id=%s",
            (request.form['company'], request.form['role'], request.form['status'], app_id)
        )
        db.commit()
        return redirect(url_for('jobs'))

    cur.execute("SELECT * FROM applications WHERE id=%s", (app_id,))
    app_data = cur.fetchone()
    return render_template('edit.html', app=app_data)


@app.route('/delete/<int:app_id>')
def delete(app_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM applications WHERE id=%s", (app_id,))
    db.commit()
    return redirect(url_for('jobs'))

if __name__ == '__main__':
    app.run(debug=True)