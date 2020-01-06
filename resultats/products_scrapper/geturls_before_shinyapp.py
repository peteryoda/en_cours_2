from selenium import webdriver
#from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from conf import *
import pyautogui

import pandas as pd


# NB les fichiers sont sauvegardés dans Téléchargements

# Mettre le fichier .xlsx dans le dossier où est situé "geturls_before_shinyapp.py"

# Lecture du fichier .xlsx
all_sampled = pd.read_excel("all_sampled_100_couples_cos_sim_fasttext.xlsx")[['URL_one','URL_two']]


# On met la liste des urls dans une liste de strings
liste_of_urls = []

# Création du fichier paires.csv
file = open("../shiny_app/data/paires.csv","w")
file.write("a,b\n")

for row in all_sampled.itertuples():
  file.write(row.URL_one + "," + row.URL_two + "\n") 

  if row.URL_one not in liste_of_urls:
    liste_of_urls.append(row.URL_one)
  if row.URL_two not in liste_of_urls:
    liste_of_urls.append(row.URL_two)

file.close() 

# print (len(liste_of_urls))
del all_sampled

# Création du fichier idurl.csv
file = open("../shiny_app/data/shiny_app/data/idurl.csv","w")
file.write("id,url\n")

url_number = 0
for url in liste_of_urls:
	url_number += 1

	file.write(str(url_number) + "," + url + "\n")

	# url = "http://nba.com"

	# MYNAME = "f01"
	MYNAME = "f" + str(url_number)


	driver = webdriver.Chrome(chrome_path)
	driver.implicitly_wait(20)
	driver.get(url)

	pyautogui.hotkey('ctrl', 's')
	time.sleep(1)

	#pyautogui.typewrite(MYNAME + '.html')
	pyautogui.typewrite(MYNAME)
	pyautogui.hotkey('enter')

file.close() 