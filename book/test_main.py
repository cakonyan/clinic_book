import unittest
import main

class MyMainTest(unittest.TestCase):
    def test_verify_creds(self):
        output = main.verify_credentials('tlmokabo', '@st', 'user_names/.usernames.txt')
        self.assertEqual(output, True)

    def test_verify_creds_ii(self):
        output = main.verify_credentials('tlmokabo', '@student.wethinkcode.co.za', 'user_names/.usernames.txt')
        self.assertEqual(output, True)

    def test_verify_creds_iii(self):
        output = main.verify_credentials('tlmokabo', '@wethinkcode.co.za', 'user_names/.usernames.txt')
        self.assertEqual(output, True)

    def test_verify_creds_iv(self):
        output = main.verify_credentials('sssss', '@wethinkcode.co.za', 'user_names/.usernames.txt')
        self.assertEqual(output, True)

    def test_verify_creds_v(self):
        output = main.verify_credentials('ssssss', '@student.wethinkcode.co.za', 'user_names/.usernames.txt')
        self.assertEqual(output, True)

if __name__ == "__main__":
    unittest.main()