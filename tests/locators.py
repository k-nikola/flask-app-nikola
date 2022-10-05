from selenium.webdriver.common.by import By


class MainPageLocators:
    GET_STARTED = (By.NAME, "get_started")
    LOGIN = (By.NAME, "login")
    HOME = (By.NAME, "home")
    ABOUT = (By.NAME, "about")
    BOOK = (By.NAME, "book")
    REGISTER = (By.NAME, "register")
    LOGOUT = (By.NAME, "logout")


class LoginPageLocators:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN = (By.ID, "submit")
    REGISTER = (By.NAME, "register")


class RegisterPageLocators:
    USERNAME = (By.ID, "username")
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email_address")
    PASSWORD = (By.ID, "password")
    CONFIRM_PASSWORD = (By.ID, "confirm_password")
    SUBMIT = (By.ID, "submit")


class BookPageLocators:
    AGE = (By.ID, "age")
    PREVIOUS_EXPERIENCE = (By.ID, "previous_experience")
    DESTINATION = (By.ID, "destination")
    DEPARTURE_DATE = (By.ID, "departure_date")
    RETURN_DATE = (By.ID, "return_date")
    BLACKHOLE_VISIT = (By.ID, "blackhole_visit")
    SUBMIT = (By.ID, "submit")


class ReservationPageLocators:
    BOOK = (By.NAME, "book")
    CANCEL = (By.NAME, "cancel")
