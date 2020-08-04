#!/usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver

from . import constants

def get_tides_from_meteofrance():

    options = webdriver.ChromeOptions()
    options.headless = True
    
    driver = webdriver.Chrome(options = options)

    driver.get(constants.METEOFRANCE_OUISTREHAM_URL)

    elem = driver.find_element_by_id('planning-tide')
    content = elem.get_attribute('innerHTML')
    driver.quit()

    soup = BeautifulSoup(content, 'lxml')
    entries = soup.find_all('tr')[1:]

    return [ et.get_text() for et in entries ]