import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

url = "https://miet.ru/search"
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(
    executable_path="C:/Users/Админ/PycharmProjects/test_MIET_search/chromedriver/chromedriver.exe",
    options=chrome_options)


def check_item(item, string, flag):
    if flag == 1:
        if item == string:
            dc_active_item = (driver.find_element(By.CLASS_NAME, "search-bar__list-item")).get_attribute('data-count')
            if dc_active_item != '0':
                raise Exception("The search came up with a non-empty result")
        else:
            raise NoSuchElementException("Error in check item function, flag = 1")
    elif flag == 2:
        if item == string:
            dc_active_item = (driver.find_element(By.CLASS_NAME, "search-bar__list-item")).get_attribute('data-count')
            if dc_active_item == '0':
                raise Exception("The search came up with an empty result")
        else:
            raise NoSuchElementException("Error in check item function, flag = 2")


try:
    driver.get(url=url)
    time.sleep(3)
    search_input = driver.find_element(By.CLASS_NAME, "search-bar__input")

    text_search_input = (driver.find_element(By.CLASS_NAME, "search-bar__input")).get_attribute('placeholder')
    if text_search_input != "Поиск":
        raise Exception("There is no 'Поиск' text in the text box")

    search_input.send_keys("вадыовалшд")
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)
    empty_item = driver.find_elements(By.CLASS_NAME, "search-bar__list-item")
    check_item(empty_item[0].text, "Новости и анонсы", 1)
    check_item(empty_item[1].text, "Люди", 1)
    check_item(empty_item[2].text, "Подразделения", 1)
    check_item(empty_item[3].text, "Страницы", 1)

    driver.find_element(By.CLASS_NAME, "search-bar__input").clear()
    search_input = driver.find_element(By.CLASS_NAME, "search-bar__input")
    search_input.send_keys("Кожухов")
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)
    empty_item = driver.find_elements(By.CLASS_NAME, "search-bar__list-item")
    check_item(empty_item[0].text, "Новости и анонсы", 2)
    check_item(empty_item[1].text, "Люди", 2)
    check_item(empty_item[2].text, "Подразделения", 2)
    news = driver.find_elements(By.CLASS_NAME, "news-list__item")

    link = driver.find_element(By.LINK_TEXT, "Люди")
    link.click()
    time.sleep(3)
    names = driver.find_elements(By.CLASS_NAME, "people-list__item-name")
    if names[0].text != "Кожухов Игорь Борисович":
        raise Exception("The name is not in the People section")

    link = driver.find_element(By.LINK_TEXT, "Подразделения")
    link.click()
    time.sleep(3)
    news_p = driver.find_elements(By.CLASS_NAME, "news-list__item")

except NoSuchElementException as exc:
    print("NoSuchElementException\n", exc)
except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()
