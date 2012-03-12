from flask import Flask, render_template
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')

class Icd10Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(5), unique=True) # Order number
    icd10code = db.Column(db.String(5), unique=True) # ICD-10-CM or ICD-10-PCS code. Dots are not included
    ub04_valid = db.Column(db.Boolean, default=False) # Valid for submission on a UB04
    short_desc = db.Column(db.String(60)) # Short description
    long_desc = db.Column(db.String(300)) # Long description

class Icd10Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forward = db.Column(db.Boolean, default=False)
    icd10code = db.Column(db.String(5))
    icd9code = db.Column(db.String(5))
    approximate = db.Column(db.Boolean, default=False)
    no_map = db.Column(db.Boolean, default=False)
    combination = db.Column(db.Boolean, default=False)
    scenario = db.Column(db.Integer)
    choice_list = db.Column(db.Integer)

if __name__ == "__main__":
    app.run()
