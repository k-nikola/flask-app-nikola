import unittest
from tests import pages, app_url, driver_location
from selenium import webdriver


class BadRegistrationTestCase(unittest.TestCase):
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
        self.driver.get(self.app_url + "register")

    def test_bad_registration(self):
        register_page = pages.RegisterPage(self.driver)
        register_page.fill_registration_form(username="shorty")
        register_page.click_create_account_button()
        assert (
            "Field must be between 8 and 30 characters long"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )
        register_page.clear_registration_form()
        register_page.fill_registration_form(username="tobedudu")
        register_page.click_create_account_button()
        assert (
            "Username already exists"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )

        register_page.clear_registration_form()
        register_page.fill_registration_form(password="short", confirm_password="short")
        register_page.click_create_account_button()
        assert (
            "Field must be at least 6 characters long"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )
        register_page.clear_registration_form()
        register_page.fill_registration_form(email="test1234@email.com")
        register_page.click_create_account_button()
        assert (
            "Email already in use."
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )
        register_page.clear_registration_form()
        register_page.fill_registration_form(confirm_password="badpasswd")
        register_page.click_create_account_button()
        assert (
            "Field must be equal to password"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )

    def tearDown(self):
        self.driver.close()
