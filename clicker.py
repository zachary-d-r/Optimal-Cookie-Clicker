import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib3.packages.six import b
from time import sleep
import numpy as np

class Clicker:

    buildings = np.array(["Cursor", "Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard tower", "Shipment", "Alchemy lab", "Portal", "Time machine", "Antimatter condenser", "Prism", "Chancemaker", "Fractal engine", "Javascript console", "Idleverse"])
    x2UpgradeIds = np.array([7, 8, 9, 44, 110, 192, 294, 307, 428, 480, 506, 700])  # Upgrade ID's for grandma x2
    timeThreshold = 100

    clickingRate = 10


    def __init__(self):
        PATH = 'C:\Program Files (x86)\chromedriver.exe'  # Path to chrome driver
        URL = 'https://orteil.dashnet.org/cookieclicker/'  # URL

        self.driver = webdriver.Chrome(PATH)  # Chrome driver

        self.driver.get(URL)  # Open URL In driver
        WebDriverWait(self.driver, 3).until(lambda d: d.find_element_by_tag_name("span"))  # Wait for page to load
        self.driver.implicitly_wait(10)
    

    # Return number of cookies player has
    def getCookies(self):
        return self.driver.execute_script("return Game.cookies")


    # Get price of any building
    def getPrice(self, building):
        for i in range(self.buildings.size):
            if self.buildings[i].__contains__(building):
                return self.driver.execute_script(f'return Game.Objects[\"{self.buildings[i]}\"].bulkPrice')
        
        return None


    # Get cps of any building
    def getCPS(self, building):
        for i in range(self.buildings.size):
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
            
    
    # Get score of a building
    def getBuildingScore(self, building=None):
        return self.getCPS(building) / self.getPrice(building)

    # Gives the total amount of buildings
    def getBuildingAmount(self, building): 
        for i in range(self.buildings.size):

            if self.buildings[i].__contains__(building):
                return self.driver.execute_script(f'return Game.Objects[\"{self.buildings[i]}\"].amount')

    #  Gets upgrade prices  (This function is Charlies)
    def getUpgradePrice(self, upgradeId): 
        return self.driver.execute_script(f'return Game.UpgradesById[{upgradeId}].basePrice')

    def getUpgradeScore(self, building, upgradeID):
        return (self.getBuildingAmount(building) * self.getCPS(building) * 2) / self.getUpgradePrice(upgradeID)

    def canBuy(self, upgrade):
        return self.driver.execute_script(f"return Game.UpgradesById[{upgrade}].canBuy()")

    def giveCookies(self, num):
        self.driver.execute_script(f'Game.cookies = {num}')

    # Choose which building to buy
    def chooseBuilding(self):

        optimalBuildings = np.array([])  # If the building is within certain paramaters it will appear here
        score = 0

        # If we can purchase the building in less than timeThreshold and is optimal based off of crabtrees equasion, add it to the optimalBuildings list
        for i in range(self.buildings.size):
            if self.getTimeUntilBuy(f'{self.buildings[i]}') <= self.timeThreshold and self.getBuildingScore(self.buildings[i]) >= score:
                optimalBuildings = np.append(optimalBuildings, self.buildings[i])

                score = (self.getCPS(self.buildings[i]) / self.getPrice(self.buildings[i]))

            # Exit out of the loop once you can't get a building in <timeThreshold seconds
            else:
                break
        
        
        try:
            buildingToClick = f'product{str(np.where(self.buildings == optimalBuildings[optimalBuildings.size - 1])).split("[")[1].split("]")[0]}'  # Get the building with the highest cps to click

            print(f'{optimalBuildings[optimalBuildings.size-1]} : {self.getTimeUntilBuy(optimalBuildings[optimalBuildings.size-1])}')

            # Check if we can click it
            if self.getTimeUntilBuy(optimalBuildings[optimalBuildings.size-1]) <= 0:
                self.driver.find_element_by_id(buildingToClick).click()
        
        except:
            pass


    # This function is largely based off of crabtrees code
    def getUpgrade(self):

        for i in range(self.x2UpgradeIds.size):

            if self.canBuy(self.x2UpgradeIds[i]):

                # Is upgrade a grandma?
                if i in range(0, 12):
                    self.driver.execute_script(f"Game.UpgradesById[{self.x2UpgradeIds[i]}].buy()")
                    print("Upgrade Purchased : Grandma")     
        
