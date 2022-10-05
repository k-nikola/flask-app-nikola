from selenium import webdriver
import unittest
from tests import pages, driver_location, app_url
from datetime import timedelta, date


class BadBookingTestCase(unittest.TestCase):
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

    def test_bad_booking(self):
        self.driver.get(self.app_url + "login")
        login_page = pages.LoginPage(self.driver)
        login_page.fill_login_form("test1234", "asdasd")
        login_page.click_login_button()
        self.driver.get(self.app_url + "reservation")
        reservation_page = pages.ReservationPage(self.driver)
        reservation_page.cancel_existing_booking()
        reservation_page.click_book_button()
        book_page = pages.BookPage(self.driver)
        book_page.fill_book_form(
            age="17",
            return_date=(date.today() + timedelta(days=-7)).strftime("%m%d%Y"),
        )
        book_page.click_book_button()
        assert (
            "Travelling through time yet isn't possible"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
            or self.driver.find_element_by_xpath("/html/body/div[2]").text
            and "You cannot book an interstellar vacation with that age"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
            or self.driver.find_element_by_xpath("/html/body/div[2]").text
        )
        book_page.clear_book_form()
        book_page.fill_book_form(
            departure_date=(date.today() + timedelta(days=-7)).strftime("%m%d%Y"),
        )
        book_page.click_book_button()
        assert (
            "Travelling through time yet isn't possible"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )

    def tearDown(self):
        self.driver.close()
