from flask import Flask, render_template, g, request, session, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/',methods=['GET', 'POST'])
def index():
    db = get_db()
    task = db.execute('select task,descrip,id from ToDo')
    todo_task = task.fetchall()
    task = db.execute('select task,descrip,id from Doing')
    doing_task = task.fetchall()
    task = db.execute('select task,descrip,id from Done')
    done_task = task.fetchall()
    task = db.execute('select count(*) from ToDo')
    c_todo = task.fetchall()
    return render_template('index.html',todo_task = todo_task,doing_task = doing_task,done_task = done_task,c_todo=c_todo)



@app.route('/todo',methods=['GET', 'POST'])
def todo():
    db = get_db()
    if request.method == 'POST':
        task = request.form['task_todo']
        desc = request.form['todo_d']
        print(task,desc)
        db.execute('insert into ToDo(task,descrip)  values (?, ?)',[task,desc])
        db.commit()
        return redirect(url_for('index'))

@app.route('/doing',methods=['GET', 'POST'])
def doing():
    db = get_db()
    if request.method == 'POST':
        task = request.form['doing_task']
        desc = request.form['doing_d']
        print(task,desc)
        db.execute('insert into Doing(task,descrip)  values (?, ?)',[task,desc])
        db.commit()
        return redirect(url_for('index'))
    
@app.route('/done',methods=['GET', 'POST'])
def done():
    db = get_db()
    if request.method == 'POST':
        task = request.form['done_task']
        desc = request.form['done_d']
        print(task,desc)
        db.execute('insert into Done(task,descrip) values (?, ?)',[task,desc])
        db.commit()
        return redirect(url_for('index'))

@app.route('/del_todo/<id>')
def del_todo(id):
    db = get_db()
    db.execute('delete from Todo where id=?',[id])
    db.commit()
    return redirect(url_for('index'))


@app.route('/del_done/<id>')
def del_done(id):
    db = get_db()
    db.execute('delete from Done where id=?',[id])
    db.commit()
    return redirect(url_for('index'))

@app.route('/move_doing/<id>')
def move_doing(id):
    db1 = get_db()
    db2 = get_db()
    db3 = get_db()
    task = db1.execute('select task,descrip from ToDo where id=?',[id])
    t=task.fetchone()
    db2.execute('insert into Doing(task,descrip)  values (?, ?)',[t['task'],t['descrip']])
    db2.commit()
    db3.execute('delete from ToDo where id=?',[id])
    db3.commit()
    return redirect(url_for('index'))

@app.route('/move_todo/<id>')
def move_todo(id):
    db1 = get_db()
    db2 = get_db()
    db3 = get_db()
    task = db1.execute('select task,descrip from Doing where id=?',[id])
    t=task.fetchone()
    db2.execute('insert into ToDo(task,descrip)  values (?, ?)',[t['task'],t['descrip']])
    db2.commit()
    db3.execute('delete from Doing where id=?',[id])
    db3.commit()
    return redirect(url_for('index'))

@app.route('/move_done/<id>')
def move_done(id):
    db1 = get_db()
    db2 = get_db()
    db3 = get_db()
    task = db1.execute('select task,descrip from Doing where id=?',[id])
    t=task.fetchone()
    db2.execute('insert into Done(task,descrip)  values (?, ?)',[t['task'],t['descrip']])
    db2.commit()
    db3.execute('delete from Doing where id=?',[id])
    db3.commit()
    return redirect(url_for('index'))


@app.route('/move_todo1/<id>')
def move_todo1(id):
    db1 = get_db()
    db2 = get_db()
    db3 = get_db()
    task = db1.execute('select task,descrip from Done where id=?',[id])
    t=task.fetchone()
    db2.execute('insert into ToDo(task,descrip)  values (?, ?)',[t['task'],t['descrip']])
    db2.commit()
    db3.execute('delete from Done where id=?',[id])
    db3.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':

    app.run(debug=True)