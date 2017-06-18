import unittest
from selenium import webdriver

class AweberTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_title(self):
        self.driver.get('https://www.python.org')
        self.assertEqual(
            self.driver.title,
            'Welcome to Python.org')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()