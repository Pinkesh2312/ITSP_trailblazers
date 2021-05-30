from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def parser(unparsed_text):

    soup = BeautifulSoup(unparsed_text, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output

# from selenium.webdriver.common.action_chains import ActionChains
opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)
opts.headless = True
driver = webdriver.Chrome(options=opts)

# opening webmail
driver.get("https://webmail.iitb.ac.in/")
driver.implicitly_wait(20)

# taking login credentials from user
ldap=input("Enter your ldap")
password=input("Enter your ldap password")

# logging into webmail
username_element=driver.find_element_by_id("rcmloginuser")
username_element.send_keys(ldap)
password_element=driver.find_element_by_id("rcmloginpwd")
password_element.send_keys(password)
login_element=driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/p/input')
login_element.click()

unread_mails=[]
unread_mails_element=[]
try:
    all_mails = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/table[2]/tbody/tr'))
    )
except:
    print('make sure you are connected to VPN and if you are already connected, please check your login credentials.')
    driver.quit()

# reading the sender's name and subject of all unread mails

for i in range(50):
    if not all_mails[i].get_attribute("class")=="message":
        unread_mails_element.append(all_mails[i])

print(unread_mails_element)
for mails_element in unread_mails_element:
    sender_name= mails_element.find_element_by_xpath('td[1]/span[1]/span/span').get_attribute("innerHTML")
    subject_string= mails_element.find_element_by_xpath('td[1]/span[3]/a/span').get_attribute("innerHTML")
    mails_element.click()
    driver.switch_to.frame('messagecontframe')
    html_document=driver.find_element_by_id('messagepreview')
    unparsed_text=html_document.get_attribute("innerHTML")
    driver.switch_to.default_content()
    unread_mails.append({"name": sender_name ,  "subject": subject_string, "body": parser(unparsed_text) })

logout=driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a').click()
driver.quit()

for mail in unread_mails:
    print(mail['name'])
    print(mail['subject'])
    print(mail['body'])

#hello world! 