import unittest

from func.pdf_reader import pdf_to_html


class MyTestCase(unittest.TestCase):
    def test_pdf_to_html(self):
        file_name = "../Szablon wypełniony.pdf"
        pdf_to_html(file_name,"output.html")

if __name__ == '__main__':
    unittest.main()
