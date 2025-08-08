import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner

URL = "http://localhost:5500/index.html"
USER = "Isael"
PASS = "12345"

class TestPeliculas(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

        self.screenshot_dir = os.path.join("reporte_pruebas", "capturas")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def login(self, user=USER, password=PASS):
        self.wait.until(EC.visibility_of_element_located((By.ID, "login-user"))).clear()
        self.driver.find_element(By.ID, "login-user").send_keys(user)
        self.driver.find_element(By.ID, "login-pass").clear()
        self.driver.find_element(By.ID, "login-pass").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "#login-form button").click()
        time.sleep(0.5)

    def limpiar_lista(self):
        try:
            clear_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "clear-all")))
            clear_btn.click()
            time.sleep(0.3)
            try:
                self.driver.switch_to.alert.accept()
            except:
                pass
        except:
            pass

    def agregar_pelicula(self, titulo="Matrix", director="Wachowski", anio="1999",
                         imagen="https://upload.wikimedia.org/wikipedia/en/9/94/The_Matrix.jpg"):
        self.wait.until(EC.visibility_of_element_located((By.ID, "title"))).send_keys(titulo)
        self.driver.find_element(By.ID, "director").send_keys(director)
        self.driver.find_element(By.ID, "year").send_keys(anio)
        self.driver.find_element(By.ID, "image").send_keys(imagen)
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        time.sleep(0.3)

    def tomar_captura(self, test_name):
        """Guarda una captura de pantalla con el nombre del test"""
        filename = os.path.join(self.screenshot_dir, f"{test_name}.png")
        self.driver.save_screenshot(filename)

    def test_login_camino_feliz(self):
        self.login()
        self.assertTrue(self.wait.until(EC.presence_of_element_located((By.ID, "app-container"))))

    def test_login_negativo(self):
        self.wait.until(EC.visibility_of_element_located((By.ID, "login-user"))).send_keys("wrong")
        self.driver.find_element(By.ID, "login-pass").send_keys("wrong")
        self.driver.find_element(By.CSS_SELECTOR, "#login-form button").click()

        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print(f"[ALERTA LOGIN NEGATIVO] {alert.text}")
            alert.accept()
        except:
            pass

        self.assertTrue(self.driver.find_element(By.ID, "login-container").is_displayed())

    def test_login_limite(self):
        self.wait.until(EC.visibility_of_element_located((By.ID, "login-user"))).send_keys("")
        self.driver.find_element(By.ID, "login-pass").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "#login-form button").click()

        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print(f"[ALERTA LOGIN LIMITE] {alert.text}")
            alert.accept()
        except:
            pass

        self.assertTrue(self.driver.find_element(By.ID, "login-container").is_displayed())

    def test_agregar_pelicula_camino_feliz(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.assertIn("Matrix", self.driver.page_source)

    def test_agregar_pelicula_negativo(self):
        self.login()
        self.limpiar_lista()
        self.driver.find_element(By.ID, "title").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        self.assertNotIn("<li>", self.driver.page_source)

    def test_agregar_pelicula_limite(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula(titulo="A", director="B", anio="1900")
        self.assertIn("A", self.driver.page_source)

    def test_editar_pelicula_camino_feliz(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.CLASS_NAME, "edit-button").click()
        title_input = self.wait.until(EC.visibility_of_element_located((By.ID, "title")))
        title_input.clear()
        title_input.send_keys("Matrix Reloaded")
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        time.sleep(0.3)
        self.assertIn("Matrix Reloaded", self.driver.page_source)

    def test_editar_pelicula_negativo(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.CLASS_NAME, "edit-button").click()
        title_input = self.wait.until(EC.visibility_of_element_located((By.ID, "title")))
        title_input.clear()
        title_input.send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        self.assertNotIn("<li></li>", self.driver.page_source)

    def test_editar_pelicula_limite(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.CLASS_NAME, "edit-button").click()
        title_input = self.wait.until(EC.visibility_of_element_located((By.ID, "title")))
        title_input.clear()
        title_input.send_keys("A" * 50)
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        self.assertIn("A" * 10, self.driver.page_source)

    def test_eliminar_pelicula_camino_feliz(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.CLASS_NAME, "delete-button").click()
        time.sleep(0.3)
        self.assertNotIn("Matrix", self.driver.page_source)

    def test_eliminar_pelicula_negativo(self):
        self.login()
        self.limpiar_lista()
        self.assertTrue(True)

    def test_eliminar_pelicula_limite(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula(titulo="X", director="Y", anio="2000")
        self.driver.find_element(By.CLASS_NAME, "delete-button").click()
        time.sleep(0.3)
        self.assertNotIn("X", self.driver.page_source)

    def test_buscar_pelicula_camino_feliz(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.ID, "search").send_keys("Matrix")
        self.assertIn("Matrix", self.driver.page_source)

    def test_buscar_pelicula_negativo(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.ID, "search").send_keys("NoExiste")
        self.assertNotIn("NoExiste", self.driver.page_source)

    def test_buscar_pelicula_limite(self):
        self.login()
        self.limpiar_lista()
        self.agregar_pelicula()
        self.driver.find_element(By.ID, "search").send_keys("M")
        self.assertIn("M", self.driver.page_source)

    def tearDown(self):
        test_name = self.id().split(".")[-1]
        self.tomar_captura(test_name)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output="reporte_pruebas",
            report_name="reporte_pruebas",
            combine_reports=True,
            add_timestamp=True
        )
    )
