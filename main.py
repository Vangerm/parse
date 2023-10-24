import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

s = Service(executable_path='/Users/apple/Desktop/python_progects/parse/chromedriver_mac64/chromedriver')
driver = webdriver.Chrome(service=s)

