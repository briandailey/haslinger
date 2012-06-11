from icd10helper import Icd10Code, db, Mapper, Icd9Code
import codecs

def read_icd10_codes():
    # Diagnosis
    with open('sources/icd10cm_order_2012.txt', 'r') as f:
        for line in f.readlines():
            code = line[6:13].strip()
            if len(code) > 3:
                code = "%s.%s" % (code[:3], code[3:])
            code = Icd10Code(
                    order_no=line[0:5],
                    code=code,
                    ub04_valid=line[14:15],
                    description=line[16:75].strip(),
                    long_desc=line[77:].strip(),
                    diagnosis=True,
            )
            db.session.add(code)

    # pcs - procedures
    with open('sources/icd10pcs_order_2012.txt', 'r') as f:
        for line in f.readlines():
            code = Icd10Code(
                    order_no=line[0:5],
                    code=line[6:13].strip(),
                    ub04_valid=line[14:15],
                    description=line[16:75].strip(),
                    long_desc=line[77:].strip(),
                    diagnosis=False,
            )
            db.session.add(code)

    db.session.commit()

def read_icd9_codes():
    # dx
    with codecs.open('sources/CMS29_DESC_LONG_DX.101111.txt', 'rb', encoding='latin-1') as f:
        for line in f.readlines():
            code = line[0:6].strip()
            if len(code) > 3:
                code = "%s.%s" % (code[:3], code[3:])
            code = Icd9Code(
                    diagnosis=True,
                    code=code,
                    description=line[6:].strip(),
                )
            db.session.add(code)
    # px
    with codecs.open('sources/CMS29_DESC_LONG_SG.txt', 'rb', encoding='latin-1') as f:
        for line in f.readlines():
            code = line[0:6].strip()
            if len(code) > 2:
                code = "%s.%s" % (code[:2], code[2:])
            code = Icd9Code(
                    diagnosis=False,
                    code=code,
                    description=line[5:].strip()
                )
            db.session.add(code)
    db.session.commit()


def read_icd10_gem_files():
    # DX
    with open('sources/2012_I10gem.txt', 'r') as f:
        for line in f.readlines():
            code = Mapper(
                    forward = False,
                    icd10code = line[0:7].strip(),
                    icd9code = line[8:13].strip(),
                    approximate = line[14:15],
                    no_map = line[15:16],
                    combination = line[16:17],
                    scenario = line[17:18],
                    choice_list = line[18:19],
                    diagnosis = True,
            )
            db.session.add(code)
    # procedures
    with open('sources/gem_pcsi9.txt', 'r') as f:
        for line in f.readlines():
            code = Mapper(
                    forward = False,
                    icd10code = line[0:7].strip(),
                    icd9code = line[8:13].strip(),
                    approximate = line[14:15],
                    no_map = line[15:16],
                    combination = line[16:17],
                    scenario = line[17:18],
                    choice_list = line[18:19],
                    diagnosis = False,
            )
            db.session.add(code)
    db.session.commit()

def read_icd9_gem_files():
    with open('sources/2012_I9gem.txt', 'r') as f:
        for line in f.readlines():
            mapping = Mapper(
                    forward = True,
                    icd9code = line[0:5].strip(),
                    icd10code = line[6:13].strip(),
                    approximate = line[14:15],
                    no_map = line[15:16],
                    combination = line[16:17],
                    scenario = line[17:18],
                    choice_list = line[18:19],
                    diagnosis = True,
            )
            db.session.add(mapping)
    with open('sources/gem_pcsi9.txt', 'r') as f:
        for line in f.readlines():
            mapping = Mapper(
                    forward = True,
                    icd9code = line[0:5].strip(),
                    icd10code = line[6:13].strip(),
                    approximate = line[14:15],
                    no_map = line[15:16],
                    combination = line[16:17],
                    scenario = line[17:18],
                    choice_list = line[18:19],
                    diagnosis = False,

            )
            db.session.add(mapping)
    db.session.commit()

if __name__ == "__main__":
    # read_icd10_gem_files()
    # read_icd9_gem_files()
    read_icd10_codes()
    read_icd9_codes()
