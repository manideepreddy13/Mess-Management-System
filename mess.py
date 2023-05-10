import sqlite3
from random import randint
from flask import session
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

ref_ids = []


def create_random_ref_id():
    unique = False
    while not unique:
        x = randint(0, 9)
        y = randint(0, 9)
        z = randint(0, 9)
        if (x, y, z) not in ref_ids:
            ref_ids.append((x, y, z))
            new_ref_id = f"RF{x}{y}{z}"
            unique = True
    return new_ref_id


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/', methods=('GET', 'POST'))
def home_page():
    return render_template('home_page.html')


# this is for password change for managers and wardens distinguished
# by their username which is passed as an arg from their respective dashboards


@app.route('/<username>/sign_up', methods=('GET', 'POST'))
def sign_up(username):
    if request.method == 'POST':
        username_entered = request.form['username']
        password_entered = request.form['password']
        repeat_password_entered = request.form['repeat_password']
        if repeat_password_entered == password_entered and username == username_entered:
            conn = get_db_connection()
            try_manager = conn.execute(
                'SELECT * FROM Mess_Login_Creds WHERE Username = ?', (username,)).fetchone()
            try_warden = conn.execute(
                'SELECT * FROM Warden_Login_Creds WHERE Username = ?', (username,)).fetchone()
            try_student = conn.execute(
                'SELECT * FROM Std_Login_Creds WHERE Username = ?', (username,)).fetchone()
            conn.close()
            if try_manager:
                conn = get_db_connection()
                conn.execute('UPDATE Mess_Login_Creds SET Passcode = ?'
                             ' WHERE Username = ?',
                             (password_entered, username))
                conn.commit()
                conn.close()
                flash('Password Changed Successfully')
                return redirect(url_for('login_managers'))

            elif try_warden:
                conn = get_db_connection()
                conn.execute('UPDATE Warden_Login_Creds SET Passcode = ?'
                             ' WHERE Username = ?',
                             (password_entered, username))
                conn.commit()
                conn.close()
                flash('Password Changed Successfully')
                return redirect(url_for('login_wardens'))

            elif try_student:
                conn = get_db_connection()
                conn.execute('UPDATE Std_Login_Creds SET Passcode = ?'
                             ' WHERE Username = ?',
                             (password_entered, username))
                conn.commit()
                conn.close()
                flash('Password Changed Successfully')
                return redirect(url_for('student_login'))
            else:
                flash('Entered Wrong Username')
                return redirect(url_for('sign_up', username=username))
        elif username == username_entered:
            flash('Passwords entered were not the same...Failed to change password')
            return redirect(url_for('sign_up', username=username))
        else:
            flash('Username entered was incorrect...Failed to change password')
            return redirect(url_for('sign_up', username=username))
    return render_template('sign_up.html', username=username)


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['Username']
        password_entered = request.form['Password']
        conn = estab_connection()
        passcode = conn.execute(
            'SELECT Passcode FROM Std_Login_Creds WHERE Username=?', (username,)).fetchone()
        conn.close()
        if passcode == None:
            flash('Entered username does not exist for students!!!')
            return redirect(url_for('student_login'))

        if passcode[0] == password_entered:
            conn = get_db_connection()
            student_id = conn.execute(
                'SELECT Roll_No FROM Student WHERE email=?', (username,)).fetchone()
            student = conn.execute(
                'SELECT * FROM Student WHERE email=?', (username,)).fetchone()
            conn.close()
            return redirect(url_for('student_dashboard', student_id=student_id[0]))
        else:
            flash('Wrong Password')
            return redirect(url_for('student_login'))
    return render_template('student_login.html')


@app.route('/<student_id>/student_dashboard', methods=('GET', 'POST'))
def student_dashboard(student_id):
    if request.method == 'GET':
        conn = get_db_connection()
        student = conn.execute(
            'SELECT * FROM Student WHERE Roll_No=?', (student_id,)).fetchone()
        conn.close()
        return render_template('student_dashboard.html', student=student)
    elif request.method == 'POST':
        return redirect(url_for('mess_allocation_homepage', student_id=student_id))
    return render_template('student_dashboard.html', student=student)


@app.route('/<student_id>/mess_allocation_homepage', methods=('GET', 'POST'))
def mess_allocation_homepage(student_id):

    if request.method == 'POST':
        if request.form['submit_button'] == 'Get Seat in Mess A':
            conn = get_db_connection()
            allocated = conn.execute(
                'SELECT Allocated FROM Mess_Details WHERE Mess_Id=1').fetchone()
            allocated = int(allocated[0])+1
            conn.execute('UPDATE Mess_Details SET Allocated = ?'
                         ' WHERE Mess_Id = ?',
                         (allocated, 1))
            conn.commit()
            conn.close()

            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM Student WHERE Roll_No=?', (student_id,)).fetchone()
            conn.execute('UPDATE Student SET Mess_Id = ?,Ref_Id = ?'
                         ' WHERE Roll_No = ?',
                         (1, create_random_ref_id(), student_id))
            conn.commit()
            conn.close()
            flash('Mess A was successfully alloted!')
            return redirect(url_for('student_dashboard', student_id=student_id))
        elif request.form['submit_button'] == 'Get Seat in Mess B':
            conn = get_db_connection()
            allocated = conn.execute(
                'SELECT Allocated FROM Mess_Details WHERE Mess_Id=2').fetchone()
            allocated = int(allocated[0])+1
            conn.execute('UPDATE Mess_Details SET Allocated = ?'
                         ' WHERE Mess_Id = ?',
                         (allocated, 2))
            conn.commit()
            conn.close()

            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM Student WHERE Roll_No=?', (student_id,)).fetchone()
            conn.execute('UPDATE Student SET Mess_Id = ?,Ref_Id = ?'
                         ' WHERE Roll_No = ?',
                         (2, create_random_ref_id(), student_id))
            conn.commit()
            conn.close()
            flash('Mess B was successfully alloted!')
            return redirect(url_for('student_dashboard', student_id=student_id))
        elif request.form['submit_button'] == 'Get Seat in Mess C':
            conn = get_db_connection()
            allocated = conn.execute(
                'SELECT Allocated FROM Mess_Details WHERE Mess_Id=3').fetchone()
            allocated = int(allocated[0])+1
            conn.execute('UPDATE Mess_Details SET Allocated = ?'
                         ' WHERE Mess_Id = ?',
                         (allocated, 3))

            conn.commit()
            conn.close()
            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM Student WHERE Roll_No=?', (student_id,)).fetchone()
            conn.execute('UPDATE Student SET Mess_Id = ?,Ref_Id = ?'
                         ' WHERE Roll_No = ?',
                         (3, create_random_ref_id(), student_id))
            conn.commit()
            conn.close()
            flash('Mess C was successfully alloted!')
            return redirect(url_for('student_dashboard', student_id=student_id))
        elif request.form['submit_button'] == 'Get Seat in Mess D':
            conn = get_db_connection()
            allocated = conn.execute(
                'SELECT Allocated FROM Mess_Details WHERE Mess_Id=4').fetchone()
            allocated = int(allocated[0])+1
            conn.execute('UPDATE Mess_Details SET Allocated = ?'
                         ' WHERE Mess_Id = ?',
                         (allocated, 4))
            conn.commit()
            conn.close()

            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM Student WHERE Roll_No=?', (student_id,)).fetchone()
            conn.execute('UPDATE Student SET Mess_Id = ?,Ref_Id = ?'
                         ' WHERE Roll_No = ?',
                         (4, create_random_ref_id(), student_id))
            conn.commit()
            conn.close()
            flash('Mess D was successfully alloted!')
            return redirect(url_for('student_dashboard', student_id=student_id))
        elif request.form['submit_button'] == 'Get Seat in Mess E':
            conn = get_db_connection()
            allocated = conn.execute(
                'SELECT Allocated FROM Mess_Details WHERE Mess_Id=5').fetchone()
            allocated = int(allocated[0])+1
            conn.execute('UPDATE Mess_Details SET Allocated = ?'
                         ' WHERE Mess_Id = ?',
                         (allocated, 5))
            conn.commit()
            conn.close()

            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM Student WHERE Roll_No=?', (student_id,)).fetchone()
            conn.execute('UPDATE Student SET Mess_Id = ?,Ref_Id = ?'
                         ' WHERE Roll_No = ?',
                         (5, create_random_ref_id(), student_id))
            conn.commit()
            conn.close()
            flash('Mess E was successfully alloted!')
            return redirect(url_for('student_dashboard', student_id=student_id))

    conn = get_db_connection()
    mess = conn.execute('SELECT * FROM Mess_Details').fetchall()
    conn.close()
    return render_template('mess_allocation_homepage.html', student_id=student_id, mess=mess)


@app.route('/login_managers', methods=('GET', 'POST'))
def login_managers():
    if request.method == 'POST':
        username = request.form['Username']
        password_entered = request.form['Password']
        conn = get_db_connection()
        passcode = conn.execute(
            'SELECT Passcode FROM Mess_Login_Creds WHERE Username=?', (username,)).fetchone()
        conn.close()
        if passcode == None:
            flash('Entered username does not exist for mess managers!!!')
            return redirect(url_for('login_managers'))

        if passcode[0] == password_entered:
            conn = get_db_connection()
            details = conn.execute(
                'SELECT * FROM Mess_Manager WHERE Manager_Id=?', (username,)).fetchone()
            conn.close()
            return redirect(url_for('mess_manager_dashboard', username=username))
        else:
            flash('Wrong Password')
            return redirect(url_for('login_managers'))

    return render_template('login_managers.html')


@app.route('/<username>/mess_manager_dashboard', methods=('GET', 'POST'))
def mess_manager_dashboard(username):
    conn = get_db_connection()
    details = conn.execute(
        'SELECT * FROM Mess_Manager WHERE Manager_Id=?', (username,)).fetchone()
    mess_id = details[2]
    students = conn.execute(
        'SELECT * FROM Student WHERE Mess_Id=?', (mess_id,)).fetchall()
    mess_details = conn.execute(
        'SELECT * FROM Mess_Details WHERE Mess_Id=?', (mess_id,)).fetchone()

    conn.close()

    return render_template('mess_manager_dashboard.html', details=details, students=students, mess_details=mess_details)


def estab_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def wardendetail(wid):
    conn = estab_connection()
    getwarden = conn.execute(
        'SELECT * FROM Hostel_Warden WHERE Warden_Id=?',).fetchone()
    conn.commit()
    conn.close()

    return getwarden


def getusers(rollno, hostel_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Student WHERE Roll_No LIKE ? AND Hostel_Id = ?", (rollno, hostel_id))
    results = cursor.fetchall()
    conn.close()
    return results


# warden login
@app.route('/login_wardens', methods=['GET', 'POST'])
def login_wardens():
    if request.method == 'POST':
        username = request.form['Username']
        password_entered = request.form['Password']
        conn = estab_connection()
        passcode = conn.execute(
            'SELECT Passcode FROM Warden_Login_Creds WHERE Username=?', (username,)).fetchone()
        conn.close()
        if passcode == None:
            flash('Entered username does not exist for hostel wardens!!!')
            return redirect(url_for('login_wardens'))

        if passcode[0] == password_entered:
            conn = estab_connection()
            details = conn.execute(
                'SELECT * FROM Hostel_Warden WHERE Warden_Id=?', (username,)).fetchone()
            conn.close()
            return redirect(url_for('warden_main', username=username))
        else:
            flash('Wrong Password')
    return render_template('login_wardens.html')


@app.route('/<username>/wardenmain', methods=['GET', 'POST'])
def warden_main(username):
    conn = estab_connection()
    details = conn.execute(
        'SELECT * FROM Hostel_Warden WHERE Warden_Id=?', (username,)).fetchone()
    hostel_id = details[2]
    warden_name = details[1]
    warden_id = details[0]

    if request.method == 'POST':
        return redirect(url_for('S3_user', hostel_id=hostel_id))

    else:
        user = []

    return render_template('warden_dashboard.html', users=user, hid=hostel_id, wname=warden_name, wid=warden_id)


@app.route('/<int:hostel_id>/S3_user', methods=['GET', 'POST'])
def S3_user(hostel_id):
    if request.method == 'POST':
        newroll = request.form['rollno']
        user = getusers(newroll, hostel_id)
    conn = estab_connection()
    warden_id = conn.execute(
        'SELECT Warden_Id FROM Hostel_Warden WHERE Hostel_Id=?', (hostel_id,)).fetchone()
    conn.close()
    return render_template('S3_users.html', users=user, hid=hostel_id, warden_id=warden_id[0])


@app.route('/<int:hostel_id>/<string:rollno>/editdue', methods=['GET', 'POST'])
def edit_due(rollno, hostel_id):
    if request.method == "POST":
        data = dict(request.form)
        user = getusers(rollno, hostel_id)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Student SET Dues=? WHERE Roll_no=?",
                       (data["Number"], rollno))
        conn.commit()
        conn.close()
        conn = estab_connection()
        warden_id = conn.execute(
            'SELECT Warden_Id FROM Hostel_Warden WHERE Hostel_Id=?', (hostel_id,)).fetchone()
        conn.close()
        flash("{} Dues updated successfully".format(rollno))
        return redirect(url_for('warden_main', username=warden_id[0]))

    return render_template("S3_users.html", users=user)


@app.route('/<int:hostel_id>/reset')
def reset(hostel_id):
    conn = estab_connection()
    

    conn.execute(
        'UPDATE Student SET Mess_Id = NULL WHERE Hostel_id = ?', (hostel_id,))
    conn.execute(
        'UPDATE Student SET Ref_Id = NULL WHERE Hostel_id = ?', (hostel_id,))
    
    conn.commit()
    details = conn.execute(
        'SELECT * FROM Hostel_Warden WHERE Hostel_Id=?', (hostel_id,)).fetchone()
    conn.close()
    flash("Reset Successful")
    return redirect(url_for('warden_main', username=details[0]))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
