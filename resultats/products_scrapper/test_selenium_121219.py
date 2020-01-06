from selenium import webdriver
#from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from conf import *
import pyautogui


myurl = "http://nba.com"
#MYNAME = "mapagesaved"
MYNAME = "f01"


driver = webdriver.Chrome(chrome_path)
driver.implicitly_wait(20)
driver.get(myurl)

pyautogui.hotkey('ctrl', 's')
time.sleep(1)
#pyautogui.typewrite(MYNAME + '.html')
pyautogui.typewrite(MYNAME)
pyautogui.hotkey('enter')