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
used_cities = []
left_users = []

#функция поиска города
def city_search (used_list, letter):
    city = ''
    bad_words = ['Ь','Ы']
    with open('cities.txt', 'r', encoding='utf8') as cities_list:
        let = letter[-1].upper()
        print('let', let)
        for line in cities_list.readlines():
            if line.strip() not in used_list:
                if line[0] == let and let not in bad_words:
                    city = line.strip()
                    break
                elif let in bad_words:
                    if line[0] == letter[-2].upper():
                        city = line.strip()
                        break
    return city

def choose_user(left_users, users_list):
    user = ''
    for i in users_list:
        if i not in left_users:
            user = i
    return user


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
    time.sleep(1)
    users_button.click()

    users = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Entity__title>a'))
    )
except:
    print('Users page not loaded')
#Берем список юзеров
for i in users:
    a = i.get_attribute('href')
    if f"@{a.split('/')[-1]}" != my_username and f"@{a.split('/')[-1]}" not in users_list:
        users_list.append('@' + a.split('/')[-1])
print(users_list)

close_button = driver.find_element(By.CSS_SELECTOR, '.PopupHeader__closeBtn')
close_button.click()
msg_time = datetime.now()
last_msg = ''
last_user = ''
last_letter = ''
last_by_me = False
input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
input_field.send_keys(f'Я родился')
driver.implicitly_wait(1)
send_msg = driver.find_element(By.XPATH,
                               '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
send_msg.click()
while True:
    time.sleep(1.5)
    print('tick')
    messages = driver.find_elements(By.CSS_SELECTOR, '.im-page--chat-body-wrap-inner._im_peer_history_w .im-mess-stack._im_mess_stack .im-mess--text.wall_module._im_log_body')
    print(messages[-1].text)
    print(users_list)
    if len(users_list) == 0:
        input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
        input_field.send_keys(f'Все игроки выбыли, я ухожу')
        driver.implicitly_wait(1)
        send_msg = driver.find_element(By.XPATH,
                                       '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
        send_msg.click()
        break
    choised_user = random.choice(users_list)
    if last_msg != messages[-1].text:
        if 'Старт' in messages[-1].text and my_username in messages[-1].text:
            city_start = 'Абакан'
            used_cities.append(city_start)
            input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
            input_field.send_keys(f'{city_start}. {choised_user}  тебе на {city_start[-1]}')
            last_user = choised_user
            last_letter = city_start[-1]
            driver.implicitly_wait(1)
            send_msg = driver.find_element(By.XPATH,
                                           '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
            send_msg.click()
            msg_time = datetime.now()
            last_msg = f'{city_start}. {choised_user}  тебе на {city_start[-1]}'
            last_user = choised_user
            last_by_me = True
        elif my_username in messages[-1].text:
            splited = messages[-1].text.split('.')
            city = city_search(used_cities, splited[0])
            used_cities.append(city)
            input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
            input_field.send_keys(f'{city}. {choised_user}  тебе на {city[-1]}')
            driver.implicitly_wait(1)
            last_letter = city[-1]
            print('last letter', last_letter)
            last_user = choised_user
            send_msg = driver.find_element(By.XPATH,
                                           '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
            send_msg.click()
            msg_time = datetime.now()
            last_msg = f'{city}. {choised_user}  тебе на {city[-1]}'
            last_by_me = True
        elif 'выбывает' in messages[-1].text:
            splited = messages[-1].text.split()
            for i in splited:
                if '@' in i:
                    left_users.append(i)
                    if i in users_list:
                        users_list.remove(i)
                        break
            last_msg = messages[-1].text
        else:
            splited = messages[-1].text.split('.')
            used_cities.append(splited[0])
            last_msg = messages[-1].text
            msg_time = datetime.now()
    else:
        curr = datetime.now()
        if (curr - msg_time).total_seconds() >= 5 and last_user != '' and last_by_me == True:
            input_field = driver.find_element(By.CSS_SELECTOR, '.im_editable.im-chat-input--text._im_text')
            buff = random.choice(users_list)
            input_field.send_keys(f'Игрок {last_user} выбывает. {buff} тебе на {last_letter}')
            if last_user in users_list:
                users_list.remove(last_user)
            last_user = buff
            msg_time = datetime.now()
            driver.implicitly_wait(1)
            send_msg = driver.find_element(By.XPATH,
                                           '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button/span[2]')
            send_msg.click()
            last_by_me = True

