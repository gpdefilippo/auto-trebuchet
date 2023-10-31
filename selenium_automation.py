from typing import Union, Tuple

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SelTrebuchet:
    def __init__(self, browser: str):
        self.browser = browser
        self.driver = self.configure_webdriver()
        self.driver.get('https://virtualtrebuchet.com/')

        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.increase_playspeed()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def configure_webdriver(self):
        if self.browser == 'chrome':
            self.options = ChromeOptions()
            self.options.add_argument('--headless=new')
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        elif self.browser == 'firefox':
            self.options = FirefoxOptions()
            self.options.add_argument("--headless")
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=self.options)
        elif self.browser == 'edge':
            return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    def increase_playspeed(self):
        """
        If animation is playing, this shortens its length.
        not necessary but for the sake of having fun with selenium
        """
        speed = self.driver.find_element(By.ID, "playSpeed")
        for _ in range(5):
            speed.send_keys(Keys.ARROW_RIGHT)

    def enter_to_element(self, element_id: str, value: Union[str, int, float]) -> None:
        """
        Enter a value to field at specified element ID and press return key
        """
        element = self.driver.find_element(By.ID, element_id)
        element.clear()
        element.send_keys(f"{value}", Keys.RETURN)

    def simulate(self, shortarm_len: float, weight_mass: float, release_angle: float) -> Tuple[float, float, float]:
        """
        Simulate virtual trebuchet with given parameters.

        Args:
            shortarm_len (float): Length of the short arm in ft
            weight_mass (float): Mass of the weight in lbs
            release_angle (float): Release angle in degrees.

        Returns:
            Tuple[float, float, float]: A tuple containing max (distance, height, time) of trebuchet launch.
        """
        self.enter_to_element("lengthArmShort", shortarm_len)
        self.enter_to_element("massWeight", weight_mass)
        self.enter_to_element("releaseAngle", release_angle)

        button = self.driver.find_elements(By.TAG_NAME, 'button')[0]
        button.click()

        distance = self.driver.find_element(By.XPATH,
            "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[1]/td[2]").text
        distance = float(distance.split(' ')[0])
        height = self.driver.find_element(By.XPATH,
            "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[2]/td[2]").text
        height = float(height.split(' ')[0])
        time_ = self.driver.find_element(By.XPATH,
            "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]").text
        time_ = float(time_.split(' ')[0])

        return distance, height, time_
