# import libraries
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


# config setup and set secret key
app = Flask(__name__)

app.config.from_pyfile('config.py')

# database object
db = SQLAlchemy(app)


# class
class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    addr = db.Column(db.String(100))
    city = db.Column(db.String(10))
    pin = db.Column(db.String(10))

    # make init 
    def __init__(self, name, addr, city, pin):
        self.name = name
        self.addr = addr
        self.city = city
        self.pin = pin


@app.route('/')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['addr'] or not request.form['city'] or not request.form['pin']:
            flash('Enter All Fields')
        else:
            student = students(request.form['name'], request.form['addr'], request.form['city'], request.form['pin'])
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        id_info = request.form['dlt']
        students.query.filter(students.id == int(id_info)).delete()
        db.session.commit()
        return render_template('show_all.html', students=students.query.all())


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_info = request.form['id']
        return render_template('update.html', id_info=id_info)


@app.route('/update_info', methods=['POST', 'GET'])
def update_info():
    if request.method == 'POST':
        id_info = request.form['id']
        name = request.form['name']
        addr = request.form['addr']
        city = request.form['city']
        pin = request.form['pin']
        db.session.query(students).filter(students.id == id_info).update(
            {students.name: name, students.addr: addr, students.city: city, students.pin: pin})
        db.session.commit()
        return render_template('show_all.html', students=students.query.all())


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
