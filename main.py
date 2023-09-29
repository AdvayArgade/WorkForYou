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
    status = db.Column(db.Integer, default=0)
    # 0 -> sent
    # 1 -> accepted
    # 2 -> contract done
    # 3 -> rejected

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Company {self.name}>'


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    location = db.Column(db.String(50), nullable=False)


# class Contracts(db.Model):
#     __tablename__ = 'contracts'
#     id = db.Column(db.Integer, primary_key=True)
#     worker_id =

with app.app_context():

    db.create_all()

w1 = Worker(name='Ramesh Jadhav', profession='Carpenter', location='Alandi')
w2 = Worker(name='Madhav Pawar', profession='Plumber', location='Katraj')
w3 = Worker(name='Harshit Jawale', profession='Car cleaner', location='Bibwewadi')
w4 = Worker(name='Chandrakant Patil', profession='Plumber', location='Wagholi')
w5 = Worker(name='Ganesh Chopade', profession='Carpenter', location='Alandi')

c1 = Customer(name='Advay', location='Sahakarnagar', password='1234')
c2 = Customer(name='Aditya', location='Nagar', password='adideo03')

# with app.app_context():
#
#     db.session.add(c1)
#     db.session.add(c2)
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



c_logged_in = False
c_name = None
w_logged_in = False
w_name = None
@app.route('/home')
def home():
    return render_template("index.html", w_logged_in=w_logged_in, c_logged_in=c_logged_in)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/companies')
def companies():
    return render_template("Companies.html")



# ----------------------------------------Searching--------------------------------
profession = None
location = None
@app.route('/customer/wnearu', methods=['POST', 'GET'])
def wnearu():
    global profession, location
    profession = request.form.get('workersprofession')
    location = request.form.get('Workerslocation')
    if profession==None and location==None:
        print("Fields are none")
        return render_template('WNearYou2.html')
    else:
        global results

        print(profession, location)
        if profession == 'notselected' and location == 'notselected':
            profession = None
            location = None
            return render_template('WNearYou2.html')

        elif profession == 'notselected':
            with app.app_context():
                results_objs = db.session.execute(db.select(Worker).where(Worker.location == location)).scalars()
                results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                           for row in results_objs]
                if len(results) == 0:
                    return f"No results"
                return render_template('WNearYou2.html', results=results, location=location, profession=profession)

        elif location == 'notselected':
            with app.app_context():
                results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession)).scalars()
                results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                           for row in results_objs]
                if len(results) == 0:
                    return f"No results"
                return render_template('WNearYou2.html', results=results, location=location, profession=profession)

        else:
            with app.app_context():
                results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession and
                                                                          Worker.location == location)).scalars()
                results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                           for row in results_objs]
                if len(results) == 0:
                    return f"No results"
                return render_template('WNearYou2.html', results=results, location=location, profession=profession)
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
    return render_template("searchResults1.html", results=results)

#-------------------------------------Messaging --------------------------------
@app.route('/sendMsg', methods=['POST'])
def send_msg():
    name = request.form['w_name']
    text = request.form['msg_text']
    emp_id = request.form['emp_id']
    w_id = request.form['w_id']
    emp_id = int(emp_id.replace('/',''))
    w_id = int(w_id.replace('/', ''))
    with app.app_context():
        emp_id = db.session.query(Customer).filter(Customer.name==c_name)
        for e in emp_id:
            emp_id = e.id
    #Add timestamp
    message = RequestMessages(employer_id=emp_id, worker_id=w_id, content=text, )
    with app.app_context():
        db.session.add(message)
        db.session.commit()

    with app.app_context():
        all_messages = db.session.execute(db.select(RequestMessages)).scalars()
    return f"{name}, {text}"



@app.route('/')
def account_type():
    return render_template('account_type.html')

@app.route('/login', methods=['POST'])
def login():
    global c_logged_in, w_logged_in
    account_type = request.form['account_type']
    if account_type=='Service Provider':
        w_logged_in = False
        return render_template('hi.html')

    else:
        c_logged_in = False
        print(c_logged_in)
        return render_template('customerLogin.html')



@app.route('/customer/Messages', methods=['POST'])
def customerMessages():
    global c_logged_in, c_name
    c_name = request.form['c_name'].strip()
    print(c_name)
    c_logged_in = True


    with app.app_context():
        result = db.session.query(Customer).filter(Customer.name==c_name)
        for r in result:
            id = r.id
        messages = db.session.query(RequestMessages).filter(RequestMessages.employer_id==id).order_by(RequestMessages.status)
        msg_list = []
        existing_w_ids = {}
        for m in messages:
            if m.worker_id not in existing_w_ids:
                w_name = db.session.query(Worker).filter(Worker.id==m.worker_id)
                for w in w_name:
                    w_name = w.name
                existing_w_ids[m.worker_id] = w_name
            else:
                w_name = existing_w_ids[m.worker_id]
            new_dict = {"msg_id": m.sr_no,
                        "w_id": m.worker_id,
                        "w_name": w_name,
                        "sender_id": m.employer_id,
                        "content": m.content,
                        "status": m.status,
                        }
            msg_list.append(new_dict)
            print(new_dict)

    return render_template('customerMessages.html', all_msgs=msg_list)



@app.route('/messages', methods=['POST', 'GET'])
def show_messages():
    global w_logged_in, w_name
    if w_logged_in==False:
        w_name = request.form['w_name'].strip()
        print(w_name)
        w_logged_in = True
    else:
        # Call respective functions for rejecting, accepting or marking a contract as done
        if 'accept' in request.form:
            msg_id = request.form['m_id']
            with app.app_context():
                msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no == msg_id)
                for m in msg:
                    m.status = 1
                db.session.commit()

        elif 'reject' in request.form:
            msg_id = request.form['m_id']
            with app.app_context():
                msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no == msg_id)
                for m in msg:
                    m.status = 3
                db.session.commit()

    with app.app_context():
        result = db.session.query(Worker).filter(Worker.name==w_name)
        for r in result:
            id = r.id
        messages = db.session.query(RequestMessages).filter(RequestMessages.worker_id==id).order_by(RequestMessages.status)
        msg_list = []
        for m in messages:
            new_dict = {"msg_id": m.sr_no,
                        "w_id": m.worker_id,
                        "sender_id": m.employer_id ,
                        "content": m.content,
                        "status": m.status,
                        }
            msg_list.append(new_dict)
            print(new_dict)

    return render_template("messages1.html", all_msgs=msg_list)


@app.route('/contracts', methods=['POST'])
def create_contract():
    msg_id = request.form['m_id']
    with app.app_context():
        msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no==msg_id)
        for m in msg:
            m.status = 1
        db.session.commit()
    return f"Message {msg_id} is accepted."


@app.route('/acceptedContracts/<w_id>')
def show_accepted_contracts(w_id):
    with app.app_context():
        result = db.session.query(RequestMessages).filter((RequestMessages.worker_id == w_id) &
                                                          (RequestMessages.status == 1)).all()
        msg_list = []
        for r in result:
            new_dict = {"msg_id": r.sr_no, "w_id": r.worker_id, "sender_id": r.employer_id, "content": r.content}
            msg_list.append(new_dict)

    print(msg_list)
    return render_template('acceptedMessages1.html', accepted_msgs=msg_list)


@app.route('/markAsDone', methods=['POST'])
def mark_contract_asdone():
    msg_id = request.form['m_id']
    with app.app_context():
        msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no==msg_id)
        for m in msg:
            m.status = 2
        db.session.commit()
    return f"Message {msg_id} is marked as done."


app.run(debug=True)
