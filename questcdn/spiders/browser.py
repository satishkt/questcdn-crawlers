from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class Browser:
    def __enter__(self):
        binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_binary=binary,
                                        executable_path="D:\\WebDrivers\\geckodriver.exe",
                                        options=options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
