import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.mp_app.common.log import logger
from src.mp_app.constants import config
from typing import Dict


class ChromeDriver:
    def __init__(self, dict_arg: Dict):
        self.service = Service(executable_path=config.CHROME_EXECUTABLE_PATH)
        self.load_arguments(dict_arg)
        self.load_driver()

    def load_arguments(self, dict_arg: Dict, *args):
        self._options = webdriver.ChromeOptions()
        self._options.add_argument(f"--user-data-dir={config.CHROME_PROFILE_DIR}")
        for key, value in dict_arg.items():
            if key == "profile-directory":
                self._profile_name = {"profile": value}
            self._options.add_argument(f"--{key}={value}")
        for arg in args:
            self._options.add_argument(arg)
        logger.info(f"👉 Option: {self._options.to_capabilities()}", extra=self._profile_name)
        return self._options

    def load_driver(self):
        logger.info(f"👉 Load driver", extra=self._profile_name)
        self._driver = webdriver.Chrome(service=self.service, options=self._options)
        self._driver.set_window_size(600, 600)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @property
    def driver(self) -> object:
        return self._driver

    @driver.setter
    def driver(self, value):
        self.driver = value

    @property
    def profile_name(self):
        return self._profile_name

    def close_driver(self):
        self._driver.close()

    def health_check(self):
        self.driver.get("https://www.google.com/")
        time.sleep(5)
        self.close_driver()


if __name__ == "__main__":
    chrome_driver_instance = ChromeDriver({"profile-directory": "Profile 1"})
    chrome_driver_instance.health_check()
    print(chrome_driver_instance.profile_name)
