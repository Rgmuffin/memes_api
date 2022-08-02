from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Добавляем подготовленный профиль с авторизацией
option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=C:\\Users\\artem.rakhmatullin\\AppData\\Local\\Google\\Chrome\\User Data\\')
option.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(options=option)
driver.get('https://vk.com/club214769465')

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

messages = driver.find_elements(By.CSS_SELECTOR, '.im-page--chat-body-wrap-inner._im_peer_history_w .im-mess-stack._im_mess_stack .im-mess--text.wall_module._im_log_body')
print(len(messages))

users = ['@user1', '@user2']

try:
    element = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.im-page--chat-body-wrap-inner._im_peer_history_w'),'@username')
    )
    print('Урюпинск ' + users[0] + ' тебе на К')
except:
    print('eerr')

try:
    element = WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]'),'@zxcvbgfdsaqwert')
    )
    print('Урюпинск ' + users[0] + ' тебе на К1')
except:
    print('eerr2')


