import unittest

from func.pdf_reader import read_pdf


class MyTestCase(unittest.TestCase):
    def test_read_szablon(self):
        file_name = "../Szablon wypełniony.pdf"
        read_pdf(file_name)
        # self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
