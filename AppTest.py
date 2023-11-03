from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'csa_grp2_dbms-Advay12210523'
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:mcks0963@localhost/WorkForYou"
db.init_app(app)
results = []

@app.route('/')
def account_type():
    return render_template('account_type.html')
