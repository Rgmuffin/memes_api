from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LocalStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()


driver = webdriver.Chrome()
driver.get("https://duckduckgo.com")

search = driver.find_element(By.ID, 'search_form_input_homepage')
search.send_keys("Мемасница")

search_button = driver.find_element(By.CLASS_NAME, 'search__button.js-search-button')
search_button.click()

results = driver.find_elements(By.CSS_SELECTOR, 'div[id=links]>div>article')
meme_obj = 0

for i in results:
   check_link = i.find_element(By.CSS_SELECTOR, 'div[class=nrn-react-div]>article>div>div>a')
   #print(check_link.get_attribute('href'))
   if check_link.get_attribute('href') == 'https://meme.gcqadev.ru/':
       link = i.get_attribute('id')
       position = (int(link[-1]) + 1)
       meme_obj = check_link
       break
   else:
       print('Мемасница не найдена в поиске')

print('Мемасница занимает', position, 'место в поиске')
meme_obj.click()
api_token = LocalStorage(driver)
api_token.set("token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDIsImV4cCI6MTY2MjcwOTc4NSwiY3JlYXRlZCI6MTY1NzUyNTc4NX0.9zZfN7-5ydY10ySOb-iS-oybpPVfnaAznIHocUhxlh8")
driver.execute_script("return window.localStorage;")
driver.refresh()

