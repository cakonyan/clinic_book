import unittest
import sync as calendar

class TestAcceptance(unittest.TestCase):

    def test_one(self):
        output = calendar.unique_Id()
        self.assertTrue(5, len(output))


if __name__ == '__main__':
    unittest.main()