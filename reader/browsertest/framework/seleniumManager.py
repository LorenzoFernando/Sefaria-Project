# -*- coding: utf-8 -*-

import os
import random
import requests

from selenium import webdriver

import logging
logger = logging.getLogger(__name__)

class SeleniumDriverManager(object):
    """
    SeleniumDriver manages the creation and testing of Selenium Drivers. 
    We will likely place Appium Driver management in a different class

    TODO:
      - Deal with passing in different capabilities
    """

    def __init__(self, seleniumServerUrl="http://localhost:4444/wd/hub"):
        #print("checking envvars")
        #self.ensureEnvVars() # Make sure the required envvars are available
        self.seleniumServerUrl = seleniumServerUrl
        print("Using Selenium server at {}.".format(seleniumServerUrl))
        print("ensuring driver functionality")
        try:
            initTestDriver = self.createFirefoxDriver(self.seleniumServerUrl)
            self.ensureDriverFunctionality(initTestDriver)
            initTestDriver.quit()
            print("Driver created and tested successfully")
        except Exception as e:
            print(e)

        return

    # self -> driver
    def createDriver(self):
        return self.createFirefoxDriver(self.seleniumServerUrl)

    def createFirefoxDriver(self, seleniumServerUrl="http://localhost:4444/wd/hub",):
        """
        createFirefoxDriver creates a firefox driver

        For now, doesn't require credentials. 
        This is a plain driver meant to target a selenium runner
        """
        logger.info("Creating Firefox driver...")
        fopt = webdriver.FirefoxOptions()
        fopt.add_argument('--headless')
        return webdriver.Remote(command_executor=seleniumServerUrl, options=fopt)

    def ensureDriverFunctionality(self, driver):
        """
        Make sure the webdriver can make requests. 
        DO NOT run this for each driver, just once on startup
        """
        logger.info("Testing driver functionality")
        try:
            logger.info("Trying to access google.com")
            driver.get("https://google.com")
            assert driver.title == "Google"
        except Exception as e:
            logger.info("Driver could not make a web request. Please check its functionality", exception=e)
            exit(1)
        else: 
            logger.info("The driver successfullly made a web request. Proceeding.")
