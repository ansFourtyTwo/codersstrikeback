import unittest
from codersstrikeback import (Point, Vector)

class TestPoint(unittest.TestCase):
    def test_string_representation(self):
        p = Point(-0.3, 0.5)
        
        self.assertTrue(str(p) == 'Point(-0.3, 0.5)')
        
    def test_from_list(self):
        p = Point.from_list([0.4, 0.6])
        
        self.assertTrue(p.x == 0.4)
        self.assertTrue(p.y == 0.6)
        
    def test_to_list(self):
        p = Point(0.8, 0.3)
        
        self.assertTrue(p.to_list() == [0.8, 0.3])
        
    def test_equality(self):
        p1 = Point(0.5, 0.3)
        p2 = Point(0.5, 0.3)
        p3 = Point(0.4, 0.2)
        
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        
        
class TestVector(unittest.TestCase):
    def test_string_representation(self):
        v = Vector(-0.3, 0.5)
        
        self.assertTrue(str(v) == 'Vector(-0.3, 0.5)')
        
    def test_from_list(self):
        v = Vector.from_list([0.4, 0.6])
        
        self.assertTrue(v.x == 0.4)
        self.assertTrue(v.y == 0.6)
        
    def test_to_list(self):
        v = Vector(0.8, 0.3)
        
        self.assertTrue(v.to_list() == [0.8, 0.3])
        
    def test_negative_vector(self):
        v = Vector(0.4, 0.5)
        result = -v
        
        self.assertEqual(result.x, -0.4)
        self.assertEqual(result.y, -0.5)
        
    def test_summation_with_vector(self):
        v1 = Vector(0.3, 0.5)
        v2 = Vector(0.6, 0.3)
        result = v1 + v2
        
        self.assertAlmostEqual(v1.x+v2.x, result.x)
        self.assertAlmostEqual(v1.y+v2.y, result.y)
        
    def test_summation_with_scalar(self):
        v = Vector(1.2, 1.5)
        s = 0.6
        result = v + s
        result_r = s + v
        
        self.assertAlmostEqual(result.x, result_r.x)
        self.assertAlmostEqual(result.y, result_r.y)
        self.assertAlmostEqual(v.x + s, result.x)
        self.assertAlmostEqual(v.y + s, result.y)
        
    def test_subtraction_with_vector(self):
        v1 = Vector(0.3, 0.5)
        v2 = Vector(0.6, 0.3)
        result = v1 - v2
        
        self.assertAlmostEqual(v1.x-v2.x, result.x)
        self.assertAlmostEqual(v1.y-v2.y, result.y)
        
    def test_subtraction_with_scalar(self):
        v = Vector(1.2, 1.5)
        s = 0.6
        result = v - s
        result_r = s - v
        
        self.assertAlmostEqual(result.x, result_r.x)
        self.assertAlmostEqual(result.y, result_r.y)
        self.assertAlmostEqual(v.x - s, result.x)
        self.assertAlmostEqual(v.y - s, result.y)
        
    def test_multiplication_with_vector(self):
        v1 = Vector(2.0, 3.0)
        v2 = Vector(1.5, -1.0)
        result = v1 * v2
        
        self.assertAlmostEqual(v1.x * v2.x, result.x)
        self.assertAlmostEqual(v1.y * v2.y, result.y)
    
    def test_multiplication_with_scalar(self):
        v = Vector(2.0, 3.0)
        s = -1.2
        result = v * s
        result_r = s * v
      
        self.assertAlmostEqual(result.x, result_r.x)
        self.assertAlmostEqual(result.y, result_r.y)
        self.assertAlmostEqual(v.y * s, result.y)
        self.assertAlmostEqual(v.x * s, result.x)
        
     
        
        
if __name__ == '__main__':
    unittest.main()