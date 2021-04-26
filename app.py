from flask import Flask, render_template, request, redirect;
from flask_sqlalchemy import SQLAlchemy;
from datetime import datetime;

# set up application
app = Flask(__name__)
# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# 3/ is relative path; 4/ is absolute path
db = SQLAlchemy(app);
# db init

class Todo(db.Model):
    # database constructor
    id = db.Column(db.Integer, primary_key=True);
    content = db.Column(db.String(200), nullable=False)
    # 200 characters max, nullable is false (dont allow users to create empty task)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # auto set time created

    def __repr__(self):
    # method to represent object as string
        return '<Task %r>' % self.id
        # return task and id of task everytime new object is created

 # CREATE
# route,  input url/string of route, callback methods
@app.route('/', methods=['POST', 'GET'])

# function
def index():

    if request.method == 'POST':
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        # create db model for task object
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/');
        except: 
            return 'Issue with adding task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # find all content by date created
        return render_template('index.html', tasks = tasks)

 # DELETE
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/');
    except:
        return 'error 202: task not found to delete'

# UPDATE
@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form["content"]
            
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'error 203: task failed to update'
    
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
    # reveals any errors