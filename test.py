import unittest
from target import Target
import main

# Since my program is mainly a GUI, these are the only methods I can test
class TestTarget(unittest.TestCase):
    def test_target_clicked_in_quadrant_one(self):
        target = Target(0, 0, 10)
        self.assertTrue(target.clicked(5,5))
        self.assertFalse(target.clicked(11,11))

    def test_target_clicked_in_quadrant_two(self):
        target = Target(0, 0, 10)
        self.assertTrue(target.clicked(-5,5))
        self.assertFalse(target.clicked(-11,11))

    def test_target_clicked_in_quadrant_three(self):
        target = Target(0, 0, 10)
        self.assertTrue(target.clicked(-5,-5))
        self.assertFalse(target.clicked(-11,-11))

    def test_target_clicked_in_quadrant_four(self):
        target = Target(0, 0, 10)
        self.assertTrue(target.clicked(5,-5))
        self.assertFalse(target.clicked(11,-11))

class TestMain(unittest.TestCase):
    def test_format_time_on_negative(self):
        with self.assertRaises(ValueError):
            main.format_time(-1)
    
    def test_format_time_on_zero(self):
        self.assertEqual(main.format_time(0), "00:00")
    
    def test_format_time_on_positive(self):
        self.assertEqual(main.format_time(30), "00:30")
        self.assertEqual(main.format_time(60), "01:00")
        self.assertEqual(main.format_time(90), "01:30")

if __name__ == "__main__":
    unittest.main()
