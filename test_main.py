import unittest
import clinic
from sync import unique_Id

class TestAcceptance(unittest.TestCase):

    def test_one(self):
        with clinic.suppress_output():
            output = unique_Id()
            self.assertTrue(5, len(output))


if __name__ == '__main__':
    unittest.main()
