from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from datetime import datetime
from selenium.webdriver.common.keys import Keys

my_username = '@id38211699'
users_list = []
cities = ['Калининград', 'Дудос']
used_cities = ['Абаза', 'Абакан']

def city_search (used_list, letter):
    city = ''
    with open('cities.txt', 'r', encoding='utf8') as cities_list:
        for line in cities_list.readlines():
            if line[:-1:] not in used_list:
                if line[0] == letter.upper():
                    city = line.strip()
                    break
    return city

#Добавляем подготовленный профиль с авторизацией в VK
option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=C:\\Users\\artem.rakhmatullin\\AppData\\Local\\Google\\Chrome\\User Data\\')
option.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(options=option)
driver.get('https://vk.com/club214769465')
#driver.get('https://vk.com/public214787090')

#Жмем кнопку перехода к чату
club_chat = driver.find_element(By.XPATH, '//*[@id="groups_chats"]/div[2]/div/div/div[1]/a')
club_chat.click()


#Ждем прогрузки окна чата
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.im-page--chat-body-wrap-inner._im_peer_history_w'))
    )
except:
    print('Chat not loaded')


try:
    users_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '._im_chat_members.im-page--members'))
    )
    users_button.click()
    users = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Entity__title>a'))
    )
except:
    print('Users page not loaded')


for i in users:
    a = i.get_attribute('href')
    if f"@{a.split('/')[-1]}" != my_username and f"@{a.split('/')[-1]}" not in users_list:
        users_list.append('@' + a.split('/')[-1])
print(users)

close_button = driver.find_element(By.CSS_SELECTOR, '.PopupHeader__closeBtn')
close_button.click()

search_msg = True
last_msg = ''

while search_msg:
    time.sleep(1.5)
    print('tick')
    messages = driver.find_elements(By.CSS_SELECTOR, '.im-page--chat-body-wrap-inner._im_peer_history_w .im-mess-stack._im_mess_stack .im-mess--text.wall_module._im_log_body')
    start_time = datetime.now()
    msg_time = datetime.now()
    splited = messages[-1].text.split('.')
    print(splited)
    print(splited[0])
    print(used_cities)
    if splited[0] not in used_cities:
        used_cities.append(splited[0])


    if last_msg != messages[-1].text:
        print('curr mess ', messages[-1].text)
        if my_username in messages[-1].text:
            msg = messages[-1].text
            print(msg.split())
            if 'Старт' in msg:
                count_users = len(users_list)
                x = random.randint(0,(count_users)-1)
                city_start = 'Урюпинск'
                used_cities.append(city_start)
                input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
                choised_user = users_list[x]
                input_field.send_keys(f'{city_start}, @id471672657 тебе на {city_start[-1]}')
                driver.implicitly_wait(1)
                send_msg = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
                send_msg.click()
                msg_time = datetime.now()
            else:
                last_letter = msg[-1]
                count_users = len(users_list)
                x = random.randint(0,(count_users)-1)
                input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
                city = city_search(used_cities, last_letter)
                used_cities.append(city)
                print('city', city)
                if len(city) > 0:
                    input_field.send_keys(f'{city}. @id471672657  тебе на {city[-1]}')
                    driver.implicitly_wait(1)
                    send_msg = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
                    send_msg.click()
                    msg_time = datetime.now()
                else:
                    input_field.send_keys(f'Москва. @id471672657  тебе на А')
                    driver.implicitly_wait(1)
                    send_msg = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
                    send_msg.click()
                    msg_time = datetime.now()

        last_msg = messages[-1].text
        print('last_msg', last_msg)
        print(used_cities)


















