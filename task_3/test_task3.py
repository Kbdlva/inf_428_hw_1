import unittest
import numpy as np

from solution3 import transform_time_to_cyclic_features, calculate_cyclic_time_difference
class TestTimeTransformation(unittest.TestCase):

    def test_transform_time_to_cyclic_features(self):
        cos, sin = transform_time_to_cyclic_features(0)
        self.assertAlmostEqual(cos, 1.0, places=7)
        self.assertAlmostEqual(sin, 0.0, places=7)

        #When hour is 0, the cosine should be 1.0 
        # (representing the start of the cycle) 
        # and the sine should be 0.0. 
        # The assertions check if the returned values are approximately equal to the expected values.

        cos, sin = transform_time_to_cyclic_features(6)
        self.assertAlmostEqual(cos, 0.0, places=7)
        self.assertAlmostEqual(sin, 1.0, places=7)

        cos, sin = transform_time_to_cyclic_features(12)
        self.assertAlmostEqual(cos, -1.0, places=7)
        self.assertAlmostEqual(sin, 0.0, places=7)

        cos, sin = transform_time_to_cyclic_features(18)
        self.assertAlmostEqual(cos, 0.0, places=7)
        self.assertAlmostEqual(sin, -1.0, places=7)

    def test_invalid_hour_in_transform(self):
        with self.assertRaises(ValueError):
            transform_time_to_cyclic_features(-1)
        with self.assertRaises(ValueError):
            transform_time_to_cyclic_features(24)
    
    def test_calculate_cyclic_time_difference(self):
        self.assertEqual(calculate_cyclic_time_difference(23, 1), 2)
        self.assertEqual(calculate_cyclic_time_difference(1, 23), 22)
        self.assertEqual(calculate_cyclic_time_difference(12, 12), 0)
        self.assertEqual(calculate_cyclic_time_difference(6, 18), 12)

    def test_invalid_hour_in_difference(self):
        with self.assertRaises(ValueError):
            calculate_cyclic_time_difference(-1, 1)
        with self.assertRaises(ValueError):
            calculate_cyclic_time_difference(1, 24)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


    #use variance and other values to check when it is 30, 30, 30, 30, 80 we need to get not just mean value, but see where it is critical 
    # we should be able to run each test separately. 
    # 20 more test cases 