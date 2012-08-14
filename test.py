import unittest
from db import Icd9Code, Icd10Code, Mapper
from sqlalchemy import func

class TestIcd9Code(unittest.TestCase):

    def test_is_valid_code(self):
        self.assertTrue(Icd9Code.is_valid_code(code='015.20', diagnosis=True))
        self.assertFalse(Icd9Code.is_valid_code(code='ABCD', diagnosis=True))

class TestMapper(unittest.TestCase):

    def test_get_mapped_codes(self):
        self.assertEqual(len(Mapper.get_mapped_codes(code='015.20', forward=True, diagnosis=True)), 1)

if __name__ == '__main__':
    unittest.main()
