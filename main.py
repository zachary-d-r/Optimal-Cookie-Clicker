import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import clicker as c

clicker = c.Clicker()  # Clicker object

def main():
    clicker.clickCookie()
    clicker.chooseBuilding()



# Idk what it does but its important
if __name__ == '__main__':
    while True:
        main()