import unittest
from selenium import webdriver
from tests import pages, app_url, driver_location


class LoginTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.driver_location = driver_location
        self.app_url = app_url
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            options=options, executable_path=self.driver_location
        )
        self.driver.maximize_window()
        self.driver.implicitly_wait(4)
        self.driver.get(self.app_url)
        return super().setUp()

    def test_login_and_book(self):
        main_page = pages.MainPage(self.driver)
        main_page.click_login()
        login_page = pages.LoginPage(self.driver)
        login_page.fill_login_form("test1234", "asdasd")
        login_page.click_login_button()
        assert (
            "Success! You are logged in"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )
        self.driver.get(self.app_url + "reservation")
        reservation_page = pages.ReservationPage(self.driver)
        reservation_page.cancel_existing_booking()
        reservation_page.click_book_button()
        book_page = pages.BookPage(self.driver)
        book_page.fill_book_form()
        book_page.click_book_button()
        assert (
            "Your vacation has been booked"
            in self.driver.find_element_by_xpath("/html/body/div[1]").text
        )

    def tearDown(self) -> None:
        self.driver.close()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
