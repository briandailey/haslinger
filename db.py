from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_

class Icd10Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(5)) # Order number
    code = db.Column(db.String(8)) # ICD-10-CM or ICD-10-PCS code. Dots are not included
    ub04_valid = db.Column(db.Boolean, default=False) # Valid for submission on a UB04
    description = db.Column(db.String(60)) # Short description
    long_desc = db.Column(db.String(300)) # Long description
    diagnosis = db.Column(db.Boolean, default=False) # If not a diagnosis, then a procedure.

class Icd9Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6))
    description = db.Column(db.String(255))
    diagnosis = db.Column(db.Boolean, default=False)

class Mapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forward = db.Column(db.Boolean, default=False)
    icd10code = db.Column(db.String(8))
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
