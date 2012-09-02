from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://brian:br1@n@localhost/icd10'
db = SQLAlchemy(app)


db = SQLAlchemy(app)

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

    @classmethod
    def is_valid_code(cls, code, diagnosis):
        return cls.query.filter(and_(cls.code==code, cls.diagnosis==diagnosis)).count() > 0

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

    class InvalidIcdCode(Exception):
        pass

    class InvalidIcd9Code(InvalidIcdCode):
        pass

    class InvalidIcd10Code(InvalidIcdCode):
        pass

    @classmethod
    def get_mapped_codes(cls, code='', forward=True, diagnosis=True):
        """ Note that ICD9 code must be passed in with the dot, but
        the dot must be stripped for Mapper. """
        if forward:
            if not Icd9Code.is_valid_code(code=code, diagnosis=diagnosis):
                raise cls.InvalidIcd9Code('%s is an invalid ICD9 code.' % code)

            matches = Mapper.query.filter(
                    and_(
                        Mapper.forward==True,
                        Mapper.icd9code==code.replace('.', ''),
                        Mapper.diagnosis==diagnosis,)
                ).all()
        else:
            if not Icd10Code.query.filter(and_(Icd10Code.code==code, Icd10Code.diagnosis==diagnosis)).count() == 1:
                raise cls.InvalidIcd10Code('Invalid ICD10 code.')

            matches = Mapper.query.filter(
                    and_(
                        Mapper.forward==False,
                        Mapper.icd10code==code.replace('.', ''),
                        Mapper.diagnosis==diagnosis,)
                ).all()

        return matches

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
