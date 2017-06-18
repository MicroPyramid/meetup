import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class GitHubLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.wait = WebDriverWait(self.driver, 10)

    def test_title(self):
        self.driver.get('https://github.com/login')
        email = self.driver.find_element_by_id("login_field")
        email.send_keys("ravi@micropyramid.com")
        pwd = self.driver.find_element_by_id("password")
        pwd.send_keys("selenium123")
        pwd.send_keys(Keys.RETURN)
        try:
            self.driver.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "site-footer-mark")))
        except TimeoutException:
            raise Exception('Page not loaded')

        self.assertIn("ravigadila", self.driver.page_source)


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()