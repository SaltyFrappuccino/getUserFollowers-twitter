from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color

print("\nInit\n")

userLogin = input("Введите twitter-login аккаунта \n")
url = "https://twitter.com/" + userLogin + "/followers"
parsed = 0

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "normal"

driver = webdriver.Chrome(desired_capabilities=caps, executable_path='chromedriver.exe')
driver.get(url)

sleep(2)

while True:
    if driver.current_url == ("https://twitter.com/" + userLogin):
        driver.get("https://twitter.com/i/flow/login")
    elif driver.current_url == "https://twitter.com/home":
        driver.get(url)
    elif driver.current_url == url:
        break

sleep(1)

print("\nSuccessful Login\n")

SCROLL_PAUSE_TIME = 3
file = open("accounts.txt", 'w')

last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    sleep(SCROLL_PAUSE_TIME)

    # username = driver.find_element(By.TAG_NAME, 'span')
    # username = driver.find_elements(By.XPATH, '//span[@style="color:"#536471"]')\
    username = driver.find_elements(By.CLASS_NAME, 'css-16my406')

    for i in username:
        try:
            if Color.from_string(i.value_of_css_property('color')).hex == "#71767b" and i.text != "Following":
                # and i.text != "Following" and i.text != "@" + userLogin
                string = i.text
                if string[0] == "@":
                    file.write(i.text + "\n")
                    file.flush()
                    parsed = parsed + 1
                    print("Parsed " + str(parsed))
        except Exception as e:
            print(e)
            pass

    sleep(SCROLL_PAUSE_TIME)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height+100 == last_height:
        break
    last_height = new_height

print("\nClosing file\n")

file.close()
