from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

app = Flask(__name__)
app.secret_key = 'csa_grp2_dbms-Advay12210523'
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mcks0963@localhost/WorkForYou"
db.init_app(app)
results = []


class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    DOB = db.Column(db.Date)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f'<Worker {self.name}>'


class RequestMessages(db.Model):
    __tablename__ = 'RequestMessages'
    sr_no = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, nullable=False)
    worker_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.Time, nullable=True)
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
    DOB = db.Column(db.Date)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))


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
#
#     db.session.commit()

# with app.app_context():
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
w_id = None
c_id = None


@app.context_processor
def set_global_vars():
    global c_logged_in, c_name, w_logged_in, w_name
    if w_name != None:
        username = w_name

    elif c_name != None:
        username = c_name

    else:
        username = None
    return dict(c_logged_in=c_logged_in, w_logged_in=w_logged_in, username=username)


@app.route('/')
def account_type():
    global c_logged_in, w_logged_in, c_name, w_name, results, profile_results
    c_logged_in = False
    w_logged_in = False
    c_name = None
    w_name = None
    results = []
    profile_results = []
    return render_template('account_type_styled.html')


@app.route('/home')
def home():
    if w_logged_in:
        return render_template("index.html", c_logged_in=c_logged_in, w_logged_in=w_logged_in, username=w_name)

    if c_logged_in:
        return render_template("index.html", c_logged_in=c_logged_in, w_logged_in=w_logged_in, username=c_name)


@app.route('/about')
def about():
    if w_logged_in:
        return render_template("about.html", c_logged_in=c_logged_in, w_logged_in=w_logged_in, username=w_name)

    if c_logged_in:
        return render_template("about.html", c_logged_in=c_logged_in, w_logged_in=w_logged_in, username=c_name)


@app.route('/companies')
def companies():
    return render_template("Companies.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    global c_logged_in, w_logged_in, c_name, w_name
    if request.method == 'POST':
        account_type = request.form['account_type']
        if account_type == 'Service Provider':
            w_logged_in = True
            g.w_logged_in = False
            c_name = None
            return render_template('finalLogin.html', account_type='Service Provider')  # replace with hi.html

        else:
            c_logged_in = True
            g.c_logged_in = False
            print(c_logged_in)
            w_name = None
            return render_template('finalLogin.html', account_type='Customer')  # replace with customerLogin.html

    else:
        return render_template('finalLogin.html')


@app.route('/SPLogin', methods=['POST', 'GET'])
def spLogin():
    global w_logged_in, w_name, w_id
    if request.method == 'POST':
        username = request.form['w_name']
        password = request.form['w_password']
        print(username, password)
        # Redirect to a different route while passing the username as a URL parameter

        with app.app_context():
            result = db.session.query(Worker).filter(Worker.name == username).first()

            if result is None:
                flash('Account does not exist.')
                return render_template('finalLogin.html', account_type='Service Provider')

            elif result.password != password:
                print(result.name)
                flash('Incorrect username or password.')
                return render_template('finalLogin.html', account_type='Service Provider')

            else:
                w_id = result.id
                w_logged_in = True
                w_name = username
        return redirect(url_for('show_messages', username=username))

    return render_template('hi.html')


@app.route('/customerLogin', methods=['POST', 'GET'])
def customerLogin():
    global c_logged_in, c_name, c_id
    if request.method == 'POST':
        username = request.form['c_name']
        password = request.form['c_password']
        # Redirect to a different route while passing the username as a URL parameter

        with app.app_context():
            result = db.session.query(Customer).filter(Customer.name == username).first()

            if result is None:
                flash('Account does not exist.')
                return render_template('finalLogin.html', account_type='Customer')

            elif result.password != password:
                flash('Incorrect username or password.')
                return render_template('finalLogin.html', account_type='Customer')

            else:
                c_id = result.id
                c_logged_in = True
                c_name = username
        return redirect(url_for('customerMessages', username=username))

    return render_template('customerLogin.html')


@app.route('/customer/signup', methods=['POST', 'GET'])
def Customer_signup():
    import datetime
    if request.method == 'POST':
        global c_name, c_logged_in
        name = request.form['name']
        ph_no = request.form['ph_no']
        password = request.form['password']
        dob = request.form['dob']
        location = request.form['c_location']
        # call create account procedure

        if name == '' or ph_no == '' or password == '' or dob == '' or location == '':
            flash('Please enter all fields.')
            return render_template('CustomerSignup.html')

        try:
            with app.app_context():
                # sql = text("CALL CreateAccCustomer2(:p_name, :p_location, :p_password, :p_dob, :p_phone_number)")
                # db.session.execute(sql, {'p_name': name, 'p_location': location, 'p_password': password,
                #                          'p_dob': dob, 'p_phone_number': ph_no})
                # print(sql)
                age = datetime.date.today().year - int(dob.split('-')[0])
                c1 = Customer(name=name, location=location, password=password, phone=ph_no, DOB=dob, age=age)
                db.session.add(c1)
                db.session.commit()
            c_name = name
            c_logged_in = True
            return redirect(url_for('customerMessages', username=name))

        except ValueError as e:
            flash('Please enter birthdate.')
        #
        except IntegrityError as e:
            # Check if the error message indicates a unique constraint violation
            if "Duplicate entry" in str(e):
                flash("Username already exists.")

            else:
                flash('Database error from IntegrityError block: failed to create account.')

        except OperationalError as e:
            if "PhoneNumberLengthError" in str(e):
                flash('Phone number must be exactly ten digits.')

            if 'AgeError' in str(e):
                flash('Age must be above 18.')

    return render_template('CustomerSignup.html')


@app.route('/serviceProvider/signup', methods=['POST', 'GET'])
def SP_signup():
    if request.method == 'POST':
        global w_name, w_logged_in
        name = request.form['name']
        ph_no = request.form['ph_no']
        password = request.form['password']
        dob = request.form['dob']
        profession = request.form['profession']
        location = request.form['w_location']
        # call create account procedure
        if name == '' or ph_no == '' or password == '' or dob == '' or location == '':
            flash('Please enter all fields.')
            return render_template('CustomerSignup.html')
        try:
            with app.app_context():
                sql = text("CALL CreateAcc5(:p_name, :p_profession, :p_location, :p_password, :p_dob, :p_phone_number)")
                db.session.execute(sql, {'p_name': name, 'p_profession': profession, 'p_location': location,
                                         'p_password': password,
                                         'p_dob': dob, 'p_phone_number': ph_no})
                print(sql)
                db.session.commit()
            w_name = name
            w_logged_in = True
            return redirect(url_for('show_messages', username=name))

        except KeyError as e:
            flash('Please enter all fields.')
            return render_template('SPsignup.html')

        except IntegrityError as e:
            # Check if the error message indicates a unique constraint violation
            if "Duplicate entry" in str(e):
                flash("Username already exists.")

            else:
                flash('Database error from IntegrityError block: failed to create account.')

        # except SQLAlchemyError as e:
        #     if str(e).strip() == 'PhoneNumberLengthError':
        #         flash('Phone number must be exactly ten digits.')
        #
        #     if str(e).strip() == 'AgeError':
        #         flash('Age must be above 18.')
        #
        #     else:
        #         flash('Database error from SQLAlchemyError block: failed to create account.')

        except OperationalError as e:
            if "PhoneNumberLengthError" in str(e):
                flash('Phone number must be exactly ten digits.')

            if 'AgeError' in str(e):
                flash('Age must be above 18.')

    return render_template('SPsignup.html')


profile_results = []


@app.route('/<username>/profile', methods=['POST', 'GET'])
def show_profile(username):
    global w_name, w_logged_in, w_id, c_name, c_logged_in, c_id, profile_results
    if w_logged_in:
        w = db.session.query(Worker).filter(Worker.name == w_name).first()
        print(w)
        if profile_results==[]:
            profile_results = [{'name': w.name, 'ph_no': w.phone, "password": w.password, "dob": w.DOB,
                                "profession": w.profession, "location": w.location}]

            print(profile_results)

    if request.method == 'POST':

        name = request.form['name']
        ph_no = request.form['ph_no']
        password = request.form['password']
        dob = request.form['dob']
        location = request.form['location']

        if w_logged_in:
            profession = request.form['profession']

            if name == '' or ph_no == '' or password == '' or dob == '' or location == '' or profession == '':
                flash('Please enter all fields.')
                return render_template('worker_profile_super_styled.html', profile_results=profile_results)

            try:
                with app.app_context():

                    sql_command = """
                                    UPDATE workers
                                    SET name = :name, phone = :ph_no, password = :password, dob = :dob, 
                                    profession = :profession, location = :location
                                    WHERE id = :w_id
                                """

                    # Execute the SQL command using SQLAlchemy text
                    db.session.execute(text(sql_command),
                                       {"name": name, "ph_no": ph_no, "password": password, "dob": dob,
                                        "profession": profession, "location": location, "w_id": w_id})

                    db.session.commit()
                w_name = name
                w_logged_in = True
                flash('Profile updated successfully!')
                profile_results = [{"name": name, "ph_no": ph_no, "password": password, "dob": dob,
                                        "profession": profession, "location": location, "w_id": w_id}]
                return render_template('worker_profile_super_styled.html', profile_results=profile_results)

            except KeyError as e:
                flash('Please enter all fields.')
                return render_template('worker_profile_super_styled.html', profile_results=profile_results)

            except IntegrityError as e:
                # Check if the error message indicates a unique constraint violation
                if "Duplicate entry" in str(e):
                    flash("Username already exists.")

                else:
                    flash('Database error from IntegrityError block: failed to create account.')

            # except SQLAlchemyError as e:
            #     if str(e).strip() == 'PhoneNumberLengthError':
            #         flash('Phone number must be exactly ten digits.')
            #
            #     if str(e).strip() == 'AgeError':
            #         flash('Age must be above 18.')
            #
            #     else:
            #         flash('Database error from SQLAlchemyError block: failed to create account.')

            except OperationalError as e:
                print('Database error from Oper')
                if "PhoneNumberLengthError" in str(e):
                    flash('Phone number must be exactly ten digits.')

                if 'AgeError' in str(e):
                    flash('Age must be above 18.')

    return render_template('worker_profile_super_styled.html', profile_results=profile_results)


# ----------------------------------------Searching-----------------------------------
profession = None
location = None
results = None


@app.route('/customer/<username>/wnearu', methods=['POST', 'GET'])
def wnearu(username):
    global profession, location, c_logged_in, results
    if request.method == 'POST':
        profession = request.form.get('workersprofession')
        location = request.form.get('Workerslocation')

    if profession == None and location == None:
        print("Fields are none")
        return render_template('WNearYou.html')

    else:

        print(profession, location)
        if profession == 'notselected' and location == 'notselected':
            profession = None
            location = None
            return render_template('WNearYou.html')

        elif profession == 'notselected':
            with app.app_context():
                results_objs = db.session.execute(db.select(Worker).where(Worker.location == location)).scalars()
                results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                           for row in results_objs]

                return render_template('WNearYou.html', results=results, location=location, profession='Not specified')

        elif location == 'notselected':
            with app.app_context():
                results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession)).scalars()
                results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                           for row in results_objs]

                return render_template('WNearYou.html', results=results, location='Not specified',
                                       profession=profession)


        else:
            with app.app_context():
                results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession and
                                                                          Worker.location == location)).scalars()
                results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                           for row in results_objs]

                return render_template('WNearYou.html', results=results, location=location, profession=profession)


@app.route('/search', methods=['POST'])
def search():
    global results
    profession = request.form.get('workersprofession')
    location = request.form.get('Workerslocation')
    if profession == 'notselected' and location == 'notselected':
        return redirect(url_for('show_results'))

    elif profession == 'notselected':
        with app.app_context():
            results_objs = db.session.execute(db.select(Worker).where(Worker.location == location)).scalars()
            results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                       for row in results_objs]

            return redirect(url_for('show_results'))

    elif location == 'notselected':
        with app.app_context():
            results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession)).scalars()
            results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                       for row in results_objs]

            return redirect(url_for('show_results'))

    else:
        with app.app_context():
            results_objs = db.session.execute(db.select(Worker).where(Worker.profession == profession and
                                                                      Worker.location == location)).scalars()
            results = [{'id': row.id, 'name': row.name, 'profession': row.profession, 'location': row.location}
                       for row in results_objs]

            return redirect(url_for('show_results'))


@app.route('/searchResults')
def show_results():
    print(results)
    return render_template("searchResults.html", results=results)


# -------------------------------------Messaging --------------------------------
@app.route('/sendMsg', methods=['POST'])
def send_msg():
    global w_logged_in, w_name
    if w_logged_in:
        flash('Please login with a Customer account to send a message.')
        return redirect(url_for('wnearu', username=w_name))
    name = request.form['w_name']
    text = request.form['msg_text']
    emp_id = request.form['emp_id']
    w_id = request.form['w_id']
    emp_id = int(emp_id.replace('/', ''))
    w_id = int(w_id.replace('/', ''))
    with app.app_context():
        emp_id = db.session.query(Customer).filter(Customer.name == c_name)
        for e in emp_id:
            emp_id = e.id
    # Add timestamp
    message = RequestMessages(employer_id=emp_id, worker_id=w_id, content=text, )
    with app.app_context():
        db.session.add(message)
        db.session.commit()

    flash('Message sent successfully.')

    with app.app_context():
        all_messages = db.session.execute(db.select(RequestMessages)).scalars()
    return redirect(url_for('wnearu', username=c_name))


@app.route('/customer/<username>/Messages', methods=['POST', 'GET'])
def customerMessages(username):
    with app.app_context():
        result = db.session.query(Customer).filter(Customer.name == c_name)
        for r in result:
            try:
                id = r.id
            except UnboundLocalError:
                return render_template('customerLogin.html')

        #        print(id)
        try:
            messages = db.session.query(RequestMessages).filter(RequestMessages.employer_id == id).order_by(
                RequestMessages.status)
        except UnboundLocalError:
            return render_template('customerLogin.html')
        msg_list = []
        existing_w_ids = {}
        for m in messages:
            if m.worker_id not in existing_w_ids:
                w_name = db.session.query(Worker).filter(Worker.id == m.worker_id)
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

    return render_template('customerMessages.html', all_msgs=msg_list, username=c_name)


@app.route('/serviceProvider/<username>/messages', methods=['POST', 'GET'])
def show_messages(username):
    global w_logged_in, w_name
    if w_logged_in == False:
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
        result = db.session.query(Worker).filter(Worker.name == w_name)
        for r in result:
            id = r.id
        messages = db.session.query(RequestMessages).filter(RequestMessages.worker_id == id).order_by(
            RequestMessages.status)
        for message in messages:
            print(message.employer_id, message.worker_id)
        msg_list = []
        existing_c_ids = {}
        for m in messages:
            if m.employer_id not in existing_c_ids:
                c_name = db.session.query(Customer).filter(Customer.id == m.employer_id)
                for c in c_name:
                    c_name = c.name
                existing_c_ids[m.employer_id] = c_name
            else:
                c_name = existing_c_ids[m.employer_id]

            new_dict = {"msg_id": m.sr_no,
                        "w_id": m.worker_id,
                        "c_name": c_name,
                        "sender_id": m.employer_id,
                        "content": m.content,
                        "status": m.status,
                        }
            msg_list.append(new_dict)
            print(new_dict)

    return render_template("messages.html", all_msgs=msg_list)


@app.route('/contracts', methods=['POST'])
def create_contract():
    msg_id = request.form['m_id']
    with app.app_context():
        msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no == msg_id)
        for m in msg:
            m.status = 1
        db.session.commit()
    return f"Message {msg_id} is accepted."


@app.route('/acceptedContracts/<w_name>', methods=['POST', 'GET'])
def show_accepted_contracts(w_name):
    global w_id
    if request.method == 'POST':
        msg_id = request.form['m_id']
        with app.app_context():
            msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no == msg_id)
            for m in msg:
                m.status = 2
            db.session.commit()
        flash('Marked as Done.')

    with app.app_context():
        result = db.session.query(RequestMessages).filter((RequestMessages.worker_id == w_id) &
                                                          (RequestMessages.status == 1)).all()
        msg_list = []
        existing_c_ids = {}
        for r in result:
            if r.employer_id not in existing_c_ids:
                c_name = db.session.query(Customer).filter(Customer.id == r.employer_id)
                for c in c_name:
                    c_name = c.name
                existing_c_ids[r.employer_id] = c_name
            else:
                c_name = existing_c_ids[r.employer_id]
            new_dict = {"msg_id": r.sr_no,
                        "w_id": r.worker_id,
                        "sender_id": r.employer_id,
                        "c_name": c_name,
                        "content": r.content}
            msg_list.append(new_dict)

    print(msg_list)
    return render_template('acceptedMessages.html', accepted_msgs=msg_list)


@app.route('/markAsDone', methods=['POST', 'GET'])
def mark_contract_asdone():
    msg_id = request.form['m_id']
    with app.app_context():
        msg = db.session.query(RequestMessages).filter(RequestMessages.sr_no == msg_id)
        for m in msg:
            m.status = 2
        db.session.commit()
    return f"Message {msg_id} is marked as done."


app.run(debug=True)
