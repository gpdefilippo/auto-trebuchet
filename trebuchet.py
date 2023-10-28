from selenium import webdriver
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
# firefox_options.headless = True

driver = webdriver.Firefox(options=firefox_options)
driver.get('https://virtualtrebuchet.com/')

button = driver.find_element_by_class_name("svelte-1pi9qli")
button.click()
driver.implicitly_wait(60)

driver.quit()
