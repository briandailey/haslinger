import os
from flask import Flask, render_template, request, json
from db import Icd9Code, Icd10Code, Mapper
from sqlalchemy import or_

app = Flask(__name__)


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
    code_type = 'icd9'
    if forward == '0':
        code_type = 'icd10'
    q = request.args.get('q')
    if forward == '1':
        matches = Icd9Code.query.filter(
            or_(
                Icd9Code.code.like("%%%s%%" % __format_code(code=q, code_type=code_type, diagnosis=(diagnosis == '1'))),
                Icd9Code.description.like("%%%s%%" % q),
            ),
        ).filter(Icd9Code.diagnosis == diagnosis).limit(10)
        # todo: add implied decimal to description
    else:
        matches = Icd10Code.query.filter(
            or_(
                Icd10Code.code.like("%%%s%%" % __format_code(code=q, code_type=code_type, diagnosis=(diagnosis == '1'))),
                Icd10Code.description.like("%%%s%%" % q),
            ),
        ).all()

    if diagnosis:
        return json.dumps([dict(label="%s - %s" % (m.code, m.description), value="%s" % (m.code),) for m in matches])
    else:
        return json.dumps([dict(label="%s - %s" % (m.code, m.description), value="%s" % (m.code),) for m in matches])


@app.route("/gem", methods=['GET'])
def gem():
    forward = request.args.get('forward') == "1"
    diagnosis = request.args.get('diagnosis')
    q = request.args.get('q')
    valid_code = True
    matches = []

    try:
        matches = Mapper.get_mapped_codes(
            code=q,
            forward=forward,
            diagnosis=diagnosis)
    except Mapper.InvalidIcdCode:
        valid_code = False

    return render_template(
        'gem.html',
        q=q,
        matches=matches,
        forward=forward,
        diagnosis=diagnosis,
        valid_code=valid_code,
    )


def __format_code(code='', code_type="icd9", diagnosis=True):
    if code_type == "icd9":
        if diagnosis and len(code) > 3:
            code = "%s.%s" % (code[:3], code[3:])
        elif not diagnosis and len(code) > 2:
            # procedure
            code = "%s.%s" % (code[:2], code[2:])
    else:
        # icd10
        if diagnosis and len(code) > 3:
            code = "%s.%s" % (code[:3], code[3:])
    return code

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', True)
    app.run(host='0.0.0.0', port=port, debug=debug)
