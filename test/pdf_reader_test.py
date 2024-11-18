import unittest

from func.pdf_reader import read_pdf


class MyTestCase(unittest.TestCase):
    def test_pdf_to_html(self):
        file_name = "../Szablon.pdf"
        jsonn = read_pdf(file_name)
        print(jsonn)

if __name__ == '__main__':
    unittest.main()
