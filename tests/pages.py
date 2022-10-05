from tests.locators import (
    MainPageLocators,
    RegisterPageLocators,
    LoginPageLocators,
    BookPageLocators,
    ReservationPageLocators,
)
from random import randint
from datetime import date, timedelta
from selenium.webdriver.support.ui import Select


class BasePage(object):
    def __init__(self, driver) -> None:
        self.driver = driver


class MainPage(BasePage):
    def click_get_started_button(self):
        get_started_button = self.driver.find_element(*MainPageLocators.GET_STARTED)
        get_started_button.click()

    def click_login(self):
        login_link = self.driver.find_element(*MainPageLocators.LOGIN)
        login_link.click()


class RegisterPage(BasePage):
    def click_create_account_button(self):
        create_account_button = self.driver.find_element(*RegisterPageLocators.SUBMIT)
        create_account_button.click()

    def fill_registration_form(
        self,
        username: str = "user" + str(randint(1000, 99999)),
        name: str = "name" + str(randint(1000, 99999)),
        email: str = "email" + str(randint(1000, 99999)) + "@mail.com",
        password: str = "passexample",
        confirm_password: str = "passexample",
    ):
        """
        Fills the registration form with valid values.
        Values can be provided and changed aswell.
        """
        username_field = self.driver.find_element(*RegisterPageLocators.USERNAME)
        username_field.send_keys(username)
        name_field = self.driver.find_element(*RegisterPageLocators.NAME)
        name_field.send_keys(name)
        email_field = self.driver.find_element(*RegisterPageLocators.EMAIL)
        email_field.send_keys(email)
        password_field = self.driver.find_element(*RegisterPageLocators.PASSWORD)
        password_field.send_keys(password)
        confirm_password_field = self.driver.find_element(
            *RegisterPageLocators.CONFIRM_PASSWORD
        )
        confirm_password_field.send_keys(confirm_password)

    def clear_registration_form(self):
        """
        Clears the registration form text fields.
        """
        username_field = self.driver.find_element(*RegisterPageLocators.USERNAME)
        username_field.clear()
        name_field = self.driver.find_element(*RegisterPageLocators.NAME)
        name_field.clear()
        email_field = self.driver.find_element(*RegisterPageLocators.EMAIL)
        email_field.clear()
        password_field = self.driver.find_element(*RegisterPageLocators.PASSWORD)
        password_field.clear()
        confirm_password_field = self.driver.find_element(
            *RegisterPageLocators.CONFIRM_PASSWORD
        )
        confirm_password_field.clear()


class BookPage(BasePage):
    def fill_book_form(
        self,
        age: str = "18",
        prev_experience: str = "No",
        destination: str = "TRAPPIST-1 System",
        departure_date: str = date.today().strftime("%m%d%Y"),
        return_date: str = (date.today() + timedelta(days=7)).strftime("%m%d%Y"),
        blackhole_visit: str = "No",
    ):
        """
        Fills the booking form with valid default values.
        Values can be provided and changed aswell.
        """
        age_field = self.driver.find_element(*BookPageLocators.AGE)
        age_field.send_keys(age)
        previous_experience_field = Select(
            self.driver.find_element(*BookPageLocators.PREVIOUS_EXPERIENCE)
        )
        previous_experience_field.select_by_value(prev_experience)
        destination_field = Select(
            self.driver.find_element(*BookPageLocators.DESTINATION)
        )
        destination_field.select_by_value(destination)
        departure_date_field = self.driver.find_element(
            *BookPageLocators.DEPARTURE_DATE
        )
        departure_date_field.send_keys(departure_date)
        return_date_field = self.driver.find_element(*BookPageLocators.RETURN_DATE)
        return_date_field.send_keys(return_date)
        blackhole_visit_field = Select(
            self.driver.find_element(*BookPageLocators.BLACKHOLE_VISIT)
        )
        blackhole_visit_field.select_by_value(blackhole_visit)

    def click_book_button(self):
        book_button = self.driver.find_element(*BookPageLocators.SUBMIT)
        book_button.click()

    def clear_book_form(self):
        """
        No longer clears date fields in the form. Clears only text fields.
        Clears the text and date fields in the form.
        """
        self.driver.find_element(*BookPageLocators.AGE).clear()
        # self.driver.find_element(*BookPageLocators.DEPARTURE_DATE).clear()
        # self.driver.find_element(*BookPageLocators.RETURN_DATE).clear()


class LoginPage(BasePage):
    def click_login_button(self):
        login_button = self.driver.find_element(*LoginPageLocators.LOGIN)
        login_button.click()

    def click_register_button(self):
        register_button = self.driver.find_element(*LoginPageLocators.REGISTER)
        register_button.click()

    def fill_login_form(self, user: str, pwd: str):
        """
        Fills the login form with the credentials provided as arguments.
        """
        username_field = self.driver.find_element(*LoginPageLocators.USERNAME)
        username_field.send_keys(user)
        password_field = self.driver.find_element(*LoginPageLocators.PASSWORD)
        password_field.send_keys(pwd)

    def clear_login_form(self):
        """
        Clears the login form fields.
        """
        username_field = self.driver.find_element(*LoginPageLocators.USERNAME)
        username_field.clear()
        password_field = self.driver.find_element(*LoginPageLocators.PASSWORD)
        password_field.clear()


class ReservationPage(BasePage):
    def cancel_existing_booking(self):
        """
        Checks if there is a booking already and cancels it if it exists.
        """
        try:
            cancel_button = self.driver.find_element(*ReservationPageLocators.CANCEL)
            cancel_button.click()
        except:
            pass

    def click_book_button(self):
        book_button = self.driver.find_element(*ReservationPageLocators.BOOK)
        book_button.click()
