from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

firefox_options = Options()
# firefox_options.headless = True

driver = webdriver.Firefox(options=firefox_options)
driver.get('https://virtualtrebuchet.com/')

speed = driver.find_element_by_id("playSpeed")
for _ in range(5):
    speed.send_keys(Keys.ARROW_RIGHT)

short_arm = driver.find_element_by_id("lengthArmShort")
short_arm.clear()
short_arm.send_keys("4", Keys.RETURN)

mass_weight = driver.find_element_by_id("massWeight")
mass_weight.clear()
mass_weight.send_keys("70", Keys.RETURN)

release_angle = driver.find_element_by_id("releaseAngle")
release_angle.clear()
release_angle.send_keys("70", Keys.RETURN)


button = driver.find_elements_by_tag_name('button')[0]
button.click()

distance = driver.find_element_by_xpath(
        "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[1]/td[2]").text
height = driver.find_element_by_xpath(
        "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[2]/td[2]").text
time = driver.find_element_by_xpath(
    "/html/body/div/div[1]/main/div[2]/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]").text

driver.quit()
