To create the tables (SQLite for now)
>>> from icd10helper import db
>>> db.create_all()

Data Sources:

2012 ICD10CM and GEMS
http://www.cms.gov/ICD10/11b14_2012_ICD10CM_and_GEMs.asp

2012 ICD10PCS and GEMS (ICD9 Volume 3 - procedures)
http://www.cms.gov/ICD10/11b15_2012_ICD10PCS.asp#TopOfPage

2011 ICD9-CM Codes
https://www.cms.gov/ICD9ProviderDiagnosticCodes/Downloads/cmsv29_master_descriptions.zip

# TODO
Need to import the V and E codes (ICD9 Diagnosis)

# NOTES
Would it be easier to just import the codes with them preformatted?
    - Yes.
    - No, because then we don't know whether to add a dot 
        - can we only add when searching by code specifically?



Trying to get dot worked out. :(
