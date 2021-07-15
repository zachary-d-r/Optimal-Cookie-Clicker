import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib3.packages.six import b
from time import sleep

class Clicker:

    buildings = ["Cursor", "Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard tower", "Shipment", "Alchemy lab", "Portal", "Time machine", "Antimatter condenser", "Prism", "Chancemaker", "Fractal engine", "Javascript console", "Idleverse"]
    clickingRate = 10


    def __init__(self):
        PATH = 'C:\Program Files (x86)\chromedriver.exe'  # Path to chrome driver
        URL = 'https://orteil.dashnet.org/cookieclicker/'  # URL

        self.driver = webdriver.Chrome(PATH)  # Chrome driver

        self.driver.get(URL)  # Open URL In driver
        WebDriverWait(self.driver, 3).until(lambda d: d.find_element_by_tag_name("span"))  # Wait for page to load
    

    # Return number of cookies player has
    def getCookies(self):
        return self.driver.execute_script("return Game.cookies")


    # Get price of any building
    def getPrice(self, building):
        for i in range(len(self.buildings)):
            if self.buildings[i].__contains__(building):
                return self.driver.execute_script(f'return Game.Objects[\"{self.buildings[i]}\"].bulkPrice')
        
        return None


    # Get cps of any building
    def getCPS(self, building):
        for i in range(len(self.buildings)):
            if self.buildings[i].__contains__(building):
                return self.driver.execute_script(f'return Game.Objects[\"{self.buildings[i]}\"].storedCps')
        
        return None


    # Click the cookie
    def clickCookie(self):
        sleep(1 / self.clickingRate)
        self.driver.find_element_by_id("bigCookie").click()


    # Find how long it will be to buy any building
    def getTimeUntilBuy(self, building):
        try:
            return ((self.getPrice(building) - self.getCookies()) / (self.getCPS(building)+self.clickingRate))
        except:
            return 100


    # Choose which building to buy
    def chooseBuilding(self):

        optimalBuildings = []  # If the building is within certain paramaters it will appear here
        timeThreshold = 100
        score = 0

        # If we can purchase the building in less than timeThreshold and is optimal based off of crabtrees equasion, add it to the optimalBuildings list
        for i in range(len(self.buildings)):
            if self.getTimeUntilBuy(f'{self.buildings[i]}') <= timeThreshold and (self.getCPS(self.buildings[i]) / self.getPrice(self.buildings[i])) >= score:
                optimalBuildings.append(self.buildings[i])

                score = (self.getCPS(self.buildings[i]) / self.getPrice(self.buildings[i]))

            # Exit out of the loop once you can't get a building in <timeThreshold seconds
            else:
                break
        
        
        try:
            buildingToClick = f'product{self.buildings.index(optimalBuildings[len(optimalBuildings) - 1])}'  # Get the building with the highest cps to click

            print(f'{optimalBuildings[len(optimalBuildings) - 1]} : {self.getTimeUntilBuy(optimalBuildings[len(optimalBuildings)-1])}')

            # Check if we can click it
            if self.getTimeUntilBuy(optimalBuildings[len(optimalBuildings)-1]) <= 0:
                self.driver.find_element_by_id(buildingToClick).click()
        
        except:
            pass
