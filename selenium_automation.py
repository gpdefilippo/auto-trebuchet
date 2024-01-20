from typing import Union, Tuple, Dict
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.options import ArgOptions
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.service import Service as EdgeService
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SelTrebuchet:
    distance_xpath = (By.XPATH, '//*[@id="output"]/div/div/div[1]/div[1]/table/tbody/tr[1]/td[2]')
    height_xpath = (By.XPATH, '//*[@id="output"]/div/div/div[1]/div[1]/table/tbody/tr[2]/td[2]')
    time_xpath = (By.XPATH, '//*[@id="output"]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]')

    def __init__(self, browser: str, options: ArgOptions = None):
        self.browser = browser
        self.options = options
        self.driver = self.configure_webdriver()
        self.driver.get('https://virtualtrebuchet.com/')

        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        self.increase_playspeed()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def configure_webdriver(self):
        if self.browser == 'chrome':
            if not self.options:
                self.options = ChromeOptions()
                self.options.add_argument('--headless=new')
            # return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
            return webdriver.Chrome(options=self.options)
        elif self.browser == 'firefox':
            if not self.options:
                self.options = FirefoxOptions()
                self.options.add_argument("--headless")
            # return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=self.options)
            return webdriver.Firefox(options=self.options)
        elif self.browser == 'edge':
            # return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            return webdriver.Edge()

    def increase_playspeed(self):
        """
        If animation is playing, this shortens its length.
        not necessary but for the sake of having fun with selenium
        """
        speed = self.driver.find_element(By.ID, "playSpeed")
        for _ in range(5):
            speed.send_keys(Keys.ARROW_RIGHT)

    def send_to_element(self, element_id: str, value: Union[str, int, float]) -> None:
        """
        Enter a value to field at specified element ID
        """
        element = self.driver.find_element(By.ID, element_id)
        element.clear()
        element.send_keys(f"{value}")

    def simulate(self, params: Dict[str, float]) -> Tuple[float, float, float]:
        """
        Simulate virtual trebuchet with given parameters.

        Args:
            params

        Returns:
            Tuple[float, float, float]: A tuple containing max (distance, height, time) of trebuchet launch.
        """
        wait = WebDriverWait(self.driver, 60)
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))

        for param in params:
            self.send_to_element(param, params[param])

        button = self.driver.find_elements(By.TAG_NAME, 'button')[0]
        button.click()

        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located(self.distance_xpath))
            # wait.until(lambda driver: self.wait_for_safe())

            distance = self.driver.find_element(*self.distance_xpath).text
            height = self.driver.find_element(*self.height_xpath).text
            time_ = self.driver.find_element(*self.time_xpath).text
        except StaleElementReferenceException:
            # Single retry if stale element
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located(self.distance_xpath))

            distance = self.driver.find_element(*self.distance_xpath).text
            height = self.driver.find_element(*self.height_xpath).text
            time_ = self.driver.find_element(*self.time_xpath).text

        distance = float(distance.split(' ')[0])
        height = float(height.split(' ')[0])
        time_ = float(time_.split(' ')[0])

        return distance, height, time_

    def wait_for_safe(self) -> bool:
        curr_xpath = (By.XPATH, '//*[@id="output"]/div/div/div[1]/div[1]/table/tbody/tr[1]/td[1]')
        max_xpath = (By.XPATH, '//*[@id="output"]/div/div/div[1]/div[1]/table/tbody/tr[1]/td[2]')

        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located(max_xpath))

        current = self.driver.find_element(*curr_xpath)
        max_ = self.driver.find_element(*max_xpath)

        return current.text != max_.text
