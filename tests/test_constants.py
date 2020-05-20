"""
test the functions of the constants module
"""


import unittest
#from pyCEDLAR.constants import *
import numpy as np

class testGenderTest(unittest.TestCase):
    def testFEMALE(self):
        self.assertTrue(genderTest('FEMALE') is 'female')
    def testMALE(self):
        self.assertTrue(genderTest('MALE') is 'male')
    def testFemale(self):
        self.assertTrue(genderTest('Female') is 'female')
    def testMale(self):
        self.assertTrue(genderTest('Male') is 'male')
    def testfemale(self):
        self.assertTrue(genderTest('female') is 'female')
    def testmale(self):
        self.assertTrue(genderTest('male') is 'male')
    def testWrongInput(self):
        with self.assertRaises(TypeError):
            gender = genderTest('foo')
    

class testWeightFunc(unittest.TestCase):
    def test1_FloatMaleBelow20(self):
        self.assertAlmostEqual(weightFunc(2.5,'male'), 15.52, delta=0.001)
    def test2_FloatMaleAbove20(self):
        self.assertAlmostEqual(weightFunc(25.5,'male'), 78.00, delta=0.001)
    def test3_FloatFemaleBelow20(self):
        self.assertAlmostEqual(weightFunc(2.5,'female'), 13.33288, delta=0.001)
    def test4_FloatFemaleAbove20(self):
        self.assertAlmostEqual(weightFunc(25.5,'female'), 63.00, delta=0.001)
    def test5_ListLen(self):
        w = weightFunc([12.5, 25.5], 'male')
        self.assertEqual(len(w), 2)
    def test6_List0(self):
        w = weightFunc([12.5, 25.5], 'male')
        self.assertAlmostEqual(w[0],45.905857,delta=0.001)
    def test7_ListLen1(self):
        w = weightFunc([12.5, 25.5], 'male')
        self.assertAlmostEqual(w[1],78.00,delta=0.001)
            
        
        
        
if __name__ == '__main__':
    unittest.main()