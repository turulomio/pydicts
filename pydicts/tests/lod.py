from pydicts.lod import lod2dictkv
from pydicts.y
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
if __name__ == "__main__":
    from datetime import datetime, date
    from decimal import Decimal
    ld=[]
    ld.append({"a": datetime.now(), "b": date.today(), "c": Decimal(12.32), "d": None, "e": int(12), "f":None, "g":True, "h":False})

    def print_lor(lor):
        print("")
        for row in lor:
            print(row)
            
    print(lod2dictkv(ld, "a","b"))
    
    
    
    print ("-- List dict transposition")
    o=[
        {"year": 2022, "month": 1, "my_sum": 12},
        {"year": 2021, "month": 2, "my_sum": 123},
        {"year": 2019, "month": 5, "my_sum": 1},
        {"year": 2022, "month": 12, "my_sum": 12},
    ]
    print(lod_year_month_value_transposition(o,key_value="my_sum"))
