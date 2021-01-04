from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import pyinputplus as pyip


WANT_TO_READ_BOOKS = []
READ_BOOKS = []


def sign_in(browser, username, pw):
    browser.find_element_by_id('userSignInFormEmail').send_keys(username)
    browser.find_element_by_id('user_password').send_keys(pw + Keys.RETURN)


def add_books_to_shelf(browser, books, action_elem):
    for i, book in enumerate(books):
        print('.................')
        if i == 0:
            homepage_search_elem = wait.until(
                presence_of_element_located((By.CLASS_NAME, 'searchBox__input--currentlyReading')))
            homepage_search_elem.send_keys(books[0])
            homepage_search_elem.submit()
        else:
            search_elem = wait.until(presence_of_element_located((By.ID, 'search_query_main')))
            search_elem.clear()
            search_elem.send_keys(book)
            print(f'Book #{i}: {book}')
            search_elem.submit()

        try:
            if book in READ_BOOKS:
                browser.find_element_by_class_name('wtrShelfButton').click()
                add_to_shelf_elem = browser.find_element_by_class_name(action_elem)
                add_to_shelf_elem.click()
            else:
                add_to_shelf_elem = browser.find_element_by_class_name(action_elem)
                add_to_shelf_elem.submit()
        except Exception as exc:
            print('There was a problem: %s' % (exc))


if __name__ == '__main__':
    print('Input email', end=': ')
    username = pyip.inputEmail()
    print('Input password', end=': ')
    pw = pyip.inputPassword()

    with webdriver.Chrome() as browser:
        wait = ui.WebDriverWait(browser, 10)
        browser.get('https://www.goodreads.com/')
        sign_in(browser, username, pw)

        if len(WANT_TO_READ_BOOKS) > 0:
            add_books_to_shelf(browser, WANT_TO_READ_BOOKS, 'wtrToRead')

        if len(READ_BOOKS) > 0:
            add_books_to_shelf(browser, READ_BOOKS, 'wtrExclusiveShelf')
