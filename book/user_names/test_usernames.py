import usernames
import unittest


class TestMyusernames(unittest.TestCase):
    def test_read_file(self):
        output = usernames.read_file('.usernames.txt')
        self.assertEqual(output[0], 'aali')

    def test_read_file_ii(self):
        output = usernames.read_file('.usernames.txt')
        output = output[::-1]
        self.assertEqual(output[0], 'zsigabi')

if __name__ == "__main__":
    unittest.main()
