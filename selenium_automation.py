from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class SelTrebuchet:
    def __init__(self, browser: str):
        self.browser = browser

    def __enter__(self):
        self.driver = self.configure_webdriver()
        self.driver.get('https://virtualtrebuchet.com/')
        self.increase_playspeed()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def configure_webdriver(self):
        if self.browser == 'chrome':
            self.options = ChromeOptions()
            self.options.headless = True
            return webdriver.Chrome(options=self.options)
        elif self.browser == 'firefox':
            self.options = FirefoxOptions()
            self.options.headless = True
            return webdriver.Firefox(options=self.options)
        elif self.browser == 'edge':
            return webdriver.Edge()

    def increase_playspeed(self):
        """ If animation is playing, this shortens its length.
            not necessary but for the sake of having fun with selenium
        """
        speed = self.driver.find_element_by_id("playSpeed")
        for _ in range(5):
            speed.send_keys(Keys.ARROW_RIGHT)

    def simulate_with_params(self, len_shortarm: float, mass_weight: float, angle_release: float):
        short_arm = self.driver.find_element_by_id("lengthArmShort")
        short_arm.clear()
        short_arm.send_keys(f"{len_shortarm}", Keys.RETURN)

        weight = self.driver.find_element_by_id("massWeight")
        weight.clear()
        weight.send_keys(f"{mass_weight}", Keys.RETURN)

        angle = self.driver.find_element_by_id("releaseAngle")
        angle.clear()
        angle.send_keys(f"{angle_release}", Keys.RETURN)

        button = self.driver.find_elements_by_tag_name('button')[0]
        button.click()

        distance = self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[1]/td[2]").text
        height = self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[2]/td[2]").text
        time = self.driver.find_element_by_xpath(
            "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]").text

        return distance, height, time
