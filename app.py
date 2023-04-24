from flask import Flask , render_template,request
from flask import redirect, flash, url_for
from flask import make_response, session
import sqlite3 as sql
app=Flask(__name__)
app.secret_key='fg'

def get_query(query):
    dbname='record.db'
    con=sql.connect(dbname)
    cursor=con.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return result

@app.route('/')
def login():
    email=session.get('email',None)
    if email:
        result=get_query(f"SELECT * FROM user WHERE email='{email}'")[0]
        try:
            marks=get_query(f"SELECT * FROM students_marks WHERE email='{email}'")
            if len(marks)==0:
                flash('Enter Marks for percenatge')
            else:
                for i in marks:
                    percentages=sum(i[1:])/5
                return render_template('userhome.html',username=result[2],percentage=percentages)
        except sql.IntegrityError:
            flash('Enter Marks for percenatge')
        return render_template('userhome.html',username=result[2])
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/mk_signup',methods=['POST'])
def mk_signup():
    name=request.form.get('name',None)
    email=request.form.get('email',None)
    password=request.form.get('password',None)
    if all([name,email,password]):
        name=name.strip().strip()
        email=email.strip().lower()

        try:
            query=f"INSERT INTO user(email,password,name) VALUES('{email}','{password}','{name}')"
            get_query(query)
            flash("Account Successfully Created please Sign-In")
            return redirect(url_for('login'))
        except sql.IntegrityError:
            flash('!Error Account Already Exists')
            return redirect(url_for('login'))
    else:
        flash('Invalid Data Please Check Again!')
    return redirect(url_for('signup'))

@app.route('/login',methods=['POST'])
def data():
    email=request.form.get('email',None)
    password=request.form.get('password',None)
    if all([email,password]):
        email=email.strip().lower()
        query=f"SELECT * FROM user WHERE email='{email}'"
        result=get_query(query)
        if len(result)==0:
            flash('Error! No Such Account Exists!')
            flash('Please Sign-up or Check Your Details Again')
        else:
            db_password=result[0][1]
            if db_password==password:
                session.update(email=email)
                return redirect(url_for('login'))
            else:
                flash('Error! Invalid Password Try Again!')
                return redirect(url_for('login'))
    else:
        flash("Error! Invalid Form Data Please Try Again!")
    return redirect(url_for('login'))

@app.route('/entry',methods=["POST"])
def entry():
    email=session.get('email',None)
    if email:
        hindi=request.form.get('hindi',None)
        english=request.form.get('english',None)
        maths=request.form.get('maths',None)
        chemistry=request.form.get('chemistry',None)
        physics=request.form.get('physics',None)
        print(english)
        if all([hindi,english,maths,chemistry,physics]):
            try:
                query=f"INSERT INTO students_marks(email,hindi,english,maths,chemistry,physics) VALUES('{email}',{hindi},{english},{maths},{chemistry},{physics})"
                get_query(query)
                flash("Data Has Been saved  ")
                return redirect(url_for('login'))
            except sql.IntegrityError:
                flash('You Cannot Change Your Marks ,Please Contact To School Administration')
                return redirect(url_for('login'))   
        else:
            flash("FILL THE INFORMATION CORRECTLY ")
    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__=='__main__':
    app.run(debug=True)