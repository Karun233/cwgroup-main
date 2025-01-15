import subprocess
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import sys

# Hardcode the path to your ChromeDriver executable here
driver_path = r'C:\chromedrivers\chromedriver-win64\chromedriver.exe'  # Update this path accordingly

class SeleniumTestCase(StaticLiveServerTestCase):
    """
    Base class for Selenium tests
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the webdriver
        """
        super().setUpClass()

        cls.server_process = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    # Allow the server some time to start
        time.sleep(3)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")
        
        # Use the hardcoded driver_path in the Service
        service = Service(driver_path)
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        """
        Quit the webdriver
        """
        cls.driver.quit()

        cls.server_process.terminate()
        cls.server_process.wait()
        
        super().tearDownClass()

    def tearDown(self):
        """
        Take a screenshot if the test failed
        """
        if sys.exc_info()[0]:
            test_method_name = self._testMethodName
            self.driver.save_screenshot(f"selenium-error-{test_method_name}.png")
        super().tearDown()
