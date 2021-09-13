import unittest
from selenium import webdriver
from tests import pages, app_url, driver_location


class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.driver_location = driver_location
        self.app_url = app_url
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            options=options, executable_path=self.driver_location
        )
        self.driver.maximize_window()
        self.driver.implicitly_wait(4)
        self.driver.get(self.app_url)

    def test_registration(self):
        main_page = pages.MainPage(self.driver)
        main_page.click_get_started_button()
        login_page = pages.LoginPage(self.driver)
        login_page.click_register_button()
        register_page = pages.RegisterPage(self.driver)
        register_page.fill_registration_form()
        register_page.click_create_account_button()
        assert (
            "Successfully created an account"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )

    def tearDown(self):
        self.driver.close()
