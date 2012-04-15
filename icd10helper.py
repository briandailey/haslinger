from flask import Flask, render_template, request
from sqlalchemy import or_, and_
from flaskext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/brian/Projects/icd10helper.com/db/test.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/search", methods=['GET'])
def search():
    forward = request.args.get('forward')
    diagnosis = request.args.get('diagnosis')
    q = request.args.get('q')
    if forward == '1':
        matches = Icd9Code.query.filter(
                or_(
                    Icd9Code.code.like("%%%s%%" % q),
                    Icd9Code.description.like("%%%s%%" % q),
                ),

        ).filter(Icd9Code.diagnosis==diagnosis).limit(10)
        # todo: add implied decimal to description
    else:
        matches = Icd10Code.query.filter(
                or_(
                    Icd10Code.code.like("%%%s%%" % q.replace('.', '')),
                    Icd10Code.description.like("%%%s%%" % q),
                ),
        ).all()

    if diagnosis:
        return json.dumps([dict( label="%s.%s - %s" % (m.code[0:3], m.code[3:], m.description), value="%s.%s" % (m.code[0:3], m.code[3:]),) for m in matches])
    else:
        return json.dumps([dict( label="%s.%s - %s" % (m.code[0:2], m.code[2:], m.description), value="%s.%s" % (m.code[0:2], m.code[2:]),) for m in matches])

@app.route("/gem", methods=['GET'])
def gem():
    forward = request.args.get('forward') == "1"
    diagnosis = request.args.get('diagnosis')
    q = request.args.get('q')
    code = q.replace('.', '').strip()
    # If going forward, starting with an icd9 code.

    valid_code = False
    matches = []
    if forward:
        if Icd9Code.query.filter(and_(Icd9Code.code==code, Icd9Code.diagnosis==diagnosis)).count() == 1:
            valid_code = True
            matches = Mapper.query.filter(
                    and_(
                        Mapper.forward==True,
                        Mapper.icd9code==code,
                        Mapper.diagnosis==diagnosis,)
                ).all()
    else:
        if Icd10Code.query.filter(and_(Icd10Code.code==code, Icd10Code.diagnosis==diagnosis)).count() == 1:
            valid_code = True
            matches = Mapper.query.filter(
                    and_(
                        Mapper.forward==False,
                        Mapper.icd10code==code,
                        Mapper.diagnosis==diagnosis,)
                ).all()
    return render_template('gem.html', 
            q=q,
            matches=matches,
            forward=forward,
            diagnosis=diagnosis,
            valid_code=valid_code,
            )

## MODELS ##
class Icd10Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(5)) # Order number
    code = db.Column(db.String(5)) # ICD-10-CM or ICD-10-PCS code. Dots are not included
    ub04_valid = db.Column(db.Boolean, default=False) # Valid for submission on a UB04
    description = db.Column(db.String(60)) # Short description
    long_desc = db.Column(db.String(300)) # Long description
    diagnosis = db.Column(db.Boolean, default=False) # If not a diagnosis, then a procedure.

class Icd9Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16))
    description = db.Column(db.String(255))
    diagnosis = db.Column(db.Boolean, default=False)

    def code_formatted(self):
        if self.diagnosis:
            breakpoint = 2
        else:
            breakpoint = 3
        return "%s.%s" % (self.icd9code[0:breakpoint], self.icd9code[breakpoint:])


class Mapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forward = db.Column(db.Boolean, default=False)
    icd10code = db.Column(db.String(5))
    icd9code = db.Column(db.String(5))
    diagnosis = db.Column(db.Boolean, default=False) # If not a diagnosis, then a procedure.
    approximate = db.Column(db.Boolean, default=False)
    no_map = db.Column(db.Boolean, default=False)
    combination = db.Column(db.Boolean, default=False)
    scenario = db.Column(db.Integer)
    choice_list = db.Column(db.Integer)

    def icd9code_formatted(self):
        if self.icd9code == 'NoDx':
            return self.icd9code
        print self.diagnosis
        if self.diagnosis:
            breakpoint = 2
        else:
            breakpoint = 3
        return "%s.%s" % (self.icd9code[0:breakpoint], self.icd9code[breakpoint:])

    def icd10code_formatted(self):
        if self.icd10code == 'NoDx':
            return self.icd9code
        if self.diagnosis:
            breakpoint = 3
        else:
            breakpoint = 4
        return "%s.%s" % (self.icd10code[0:breakpoint], self.icd10code[breakpoint:])

    def icd10code_description(self):
        """ Not terribly efficient, no. """
        if self.icd10code == 'NoDx':
            return ''
        icd10code = Icd10Code.query.filter(Icd10Code.code==self.icd10code).first()
        if icd10code:
            return icd10code.long_desc
        else:
            return ''

    def icd9code_description(self):
        if self.icd9code == 'NoDx':
            return ''
        icd9code = Icd9Code.query.filter(Icd9Code.code==self.icd9code).first()
        if icd9code:
            return icd9code.description
        else:
            return ''

if __name__ == "__main__":
    app.run(debug=True)
