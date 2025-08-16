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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reporte_pruebas")
SCREENSHOT_DIR = os.path.join(REPORT_DIR, "capturas")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class PlanPruebasBiblioteca(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

    def login(self, user=USER, password=PASS):
        """Realiza login en el sistema y acepta cualquier alert que aparezca"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "login-user"))).clear()
        self.driver.find_element(By.ID, "login-user").send_keys(user)
        self.driver.find_element(By.ID, "login-pass").clear()
        self.driver.find_element(By.ID, "login-pass").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "#login-form button").click()
        time.sleep(0.5)

        try:
            alert = self.wait.until(EC.alert_is_present())
            print("Texto de alerta:", alert.text) 
            alert.accept()
        except:
            pass  
    def limpiar_lista(self):
        """Elimina todas las películas existentes"""
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
                         imagen="https://images.plex.tv/photo?size=large-720&scale=2&url=https:%2F%2Fmetadata-static.plex.tv%2F9%2Fgracenote%2F9bf4dcb36fbc5259254737e1946dd52c.jpg"):
        """Agrega una película"""
        self.wait.until(EC.visibility_of_element_located((By.ID, "title"))).send_keys(titulo)
        self.driver.find_element(By.ID, "director").send_keys(director)
        self.driver.find_element(By.ID, "year").send_keys(anio)
        self.driver.find_element(By.ID, "image").send_keys(imagen)
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        time.sleep(0.3)

    def agregar_varias_peliculas(self):
        """Agrega varias películas para pruebas masivas"""
        peliculas = [
            ("Matrix", "Wachowski", "1999", "https://images.plex.tv/photo?size=large-720&scale=2&url=https:%2F%2Fmetadata-static.plex.tv%2F9%2Fgracenote%2F9bf4dcb36fbc5259254737e1946dd52c.jpg"),
            ("Inception", "Nolan", "2010", "https://m.media-amazon.com/images/M/MV5BMTM0MjUzNjkwMl5BMl5BanBnXkFtZTcwNjY0OTk1Mw@@._V1_.jpg"),
            ("Interstellar", "Nolan", "2014", "https://i.pinimg.com/originals/d2/70/89/d270896d9bfbc63513d1090224070e8b.jpg"),
        ]
        for titulo, director, anio, imagen in peliculas:
            self.agregar_pelicula(titulo, director, anio, imagen)

    def tomar_captura(self, test_name):
        """Guarda una captura de pantalla con el nombre del test"""
        filename = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
        self.driver.save_screenshot(filename)


    def test_login_camino_feliz(self):
        self.login()
        self.assertTrue(self.wait.until(EC.presence_of_element_located((By.ID, "app-container"))))

    def test_login_negativo(self):
        self.login(user="mal", password="mal")
        self.assertTrue(self.driver.find_element(By.ID, "login-container").is_displayed())

    def test_login_limite(self):
        self.login(user="", password="")
        self.assertTrue(self.driver.find_element(By.ID, "login-container").is_displayed())

    def test_agregar_varias_peliculas(self):
        self.login()
        self.limpiar_lista()
        self.agregar_varias_peliculas()
        self.assertIn("Matrix", self.driver.page_source)
        self.assertIn("Inception", self.driver.page_source)
        self.assertIn("Interstellar", self.driver.page_source)

    def test_agregar_pelicula_negativo(self):
        self.login()
        self.limpiar_lista()
        self.driver.find_element(By.ID, "title").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        self.assertNotIn("<li>", self.driver.page_source)

    def test_editar_pelicula(self):
        self.login()
        self.limpiar_lista()
        self.agregar_varias_peliculas()
        self.driver.find_element(By.CLASS_NAME, "edit-button").click()
        title_input = self.wait.until(EC.visibility_of_element_located((By.ID, "title")))
        title_input.clear()
        title_input.send_keys("Pelicula Editada")
        self.driver.find_element(By.CSS_SELECTOR, "#movie-form button").click()
        self.assertIn("Pelicula Editada", self.driver.page_source)

    def test_eliminar_pelicula(self):
        self.login()
        self.limpiar_lista()
        self.agregar_varias_peliculas()
        self.driver.find_element(By.CLASS_NAME, "delete-button").click()
        time.sleep(0.3)
        self.assertNotIn("Matrix", self.driver.page_source)

    def test_buscar_pelicula(self):
        self.login()
        self.limpiar_lista()
        self.agregar_varias_peliculas()
        self.driver.find_element(By.ID, "search").send_keys("Interstellar")
        self.assertIn("Interstellar", self.driver.page_source)

    def tearDown(self):
        test_name = self.id().split(".")[-1]
        self.tomar_captura(test_name)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output=REPORT_DIR,
            report_name="reporte_pruebas",
            combine_reports=True,
            add_timestamp=True
        )
    )
