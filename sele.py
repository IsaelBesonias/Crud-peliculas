from sele import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  
        self.driver.get("http://localhost:5500/index.html")  

    def test_login_camino_feliz(self):
        driver = self.driver
        driver.find_element(By.ID, "login-user").send_keys("Isael")
        driver.find_element(By.ID, "login-pass").send_keys("12345")
        driver.find_element(By.CSS_SELECTOR, "#login-form button").click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, "app-container").is_displayed())

    def test_login_incorrecto(self):
        driver = self.driver
        driver.find_element(By.ID, "login-user").send_keys("admin")
        driver.find_element(By.ID, "login-pass").send_keys("12")
        driver.find_element(By.CSS_SELECTOR, "#login-form button").click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, "login-container").is_displayed())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
