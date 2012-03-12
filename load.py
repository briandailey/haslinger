from icd10helper import Icd10Code, db, Icd10Map

def read_icd10_codes():
    with open('sources/icd10cm_order_2012.txt', 'r') as f:
        for line in f.readlines():
            code = Icd10Code(
                    order_no=line[0:5],
                    icd10code=line[6:13].strip(),
                    ub04_valid=line[14:15],
                    short_desc=line[17:75].strip(),
                    long_desc=line[77:].strip()
            )
            db.session.add(code)
        db.session.commit()

def read_icd10_gem_file():
    with open('sources/2012_I10gem.txt', 'r') as f:
        for line in f.readlines():
            code = Icd10Map(
                    forward = False,
                    icd10code = line[0:7].strip(),
                    icd9code = line[8:13].strip(),
                    approximate = line[14:15],
                    no_map = line[15:16],
                    combination = line[16:17],
                    scenario = line[17:18],
                    choice_list = line[18:19]
            )
            db.session.add(code)
        db.session.commit()

def read_icd9_gem_file():
    with open('sources/2012_I9gem.txt', 'r') as f:
        for line in f.readlines():
            code = Icd10Map(
                    forward = True,
                    icd9code = line[0:7].strip(),
                    icd10code = line[8:13].strip(),
                    approximate = line[14:15],
                    no_map = line[15:16],
                    combination = line[16:17],
                    scenario = line[17:18],
                    choice_list = line[18:19]
            )
            db.session.add(code)
        db.session.commit()

if __name__ == "__main__":
    read_icd10_gem_file()
    read_icd9_gem_file()
