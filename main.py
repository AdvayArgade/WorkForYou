from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mcks0963@localhost/WorkForYou"
db.init_app(app)
books = []
results = []


class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Worker {self.name}>'


class RequestMessages(db.Model):
    __tablename__ = 'RequestMessages'
    sr_no = db.Column(db.Integer, primary_key = True)
    employer_id = db.Column(db.Integer, nullable = False)
    worker_id = db.Column(db.Integer, nullable = False)
    content = db.Column(db.String(200), nullable = False)
    timestamp = db.Column(db.Time, nullable = True)



class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Company {self.name}>'


with app.app_context():

    db.create_all()

w1 = Worker(name='Ramesh Jadhav', profession='Carpenter', location='Alandi')
w2 = Worker(name='Madhav Pawar', profession='Plumber', location='Katraj')
w3 = Worker(name='Harshit Jawale', profession='Car cleaner', location='Bibwewadi')
w4 = Worker(name='Chandrakant Patil', profession='Plumber', location='Wagholi')
w5 = Worker(name='Ganesh Chopade', profession='Carpenter', location='Alandi')
# with app.app_context():
#
#     db.session.add(w1)
#     db.session.commit()

#with app.app_context():
    # db.session.add(w2)
    # db.session.commit()
    #
    # db.session.add(w3)
    # db.session.commit()
    # db.session.add(w4)
    # db.session.commit()
    # db.session.add(w5)
    # db.session.commit()




@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/companies')
def companies():
    return render_template("Companies.html")


@app.route('/wnearu')
def wnearu():
    return render_template("WnearU.html")


@app.route('/search', methods=['POST'])
def search():
    global results
    profession = request.form.get('workersprofession')
    location = request.form.get('Workerslocation')
    if profession == 'notselected' and location == 'notselected':
        return f"No results."

    elif profession == 'notselected':
        with app.app_context():
            results_objs = db.session.execute(db.select(Worker).where(Worker.location == location)).scalars()
            results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                       for row in results_objs]
            if len(results) == 0:
                return f"No results"
            return redirect(url_for('show_results'))

    elif location == 'notselected':
        with app.app_context():
            results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession)).scalars()
            results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                       for row in results_objs]
            if len(results) == 0:
                return f"No results"
            return redirect(url_for('show_results'))

    else:
        with app.app_context():
            results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession and
                                                                      Worker.location==location)).scalars()
            results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                       for row in results_objs]
            if len(results) == 0:
                return f"No results"
            return redirect(url_for('show_results'))

@app.route('/searchResults')
def show_results():
    print(results)
    return render_template("searchResults.html", results=results)


@app.route('/sendMsg', methods=['POST'])
def send_msg():
    name = request.form['w_name']
    text = request.form['msg_text']
    emp_id = request.form['emp_id']
    w_id = request.form['w_id']
    emp_id = int(emp_id.replace('/',''))
    w_id = int(w_id.replace('/', ''))
    #Add timestamp
    message = RequestMessages(employer_id=emp_id, worker_id=w_id, content=text, )
    with app.app_context():
        db.session.add(message)
        db.session.commit()

    with app.app_context():
        all_messages = db.session.execute(db.select(RequestMessages)).scalars()
    return f"{name}, {text}"
app.run(debug=True)

