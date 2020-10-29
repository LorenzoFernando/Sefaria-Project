# -*- coding: utf-8 -*-

import os
import random
import requests

from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .elements import TestResultSet
from reader.browsertest.framework.elements import get_every_build_tests, get_suites

import logging
logger = logging.getLogger(__name__)


"""

seleniumServer = getSeleniumServerName() #
targetApplication = getTargetApplicationUrl()
sal = Salvo(seleniumServer, targetApplication)
sal.run()
results = sal.results()

print(results.report())


"""


class Salvo(object):
    """
    Salvo manages a battery of tests
    """
    
    def __init__(self, seleniumServerHostname, targetApplicationUrl):
        # How much do I care about whether the selenium server is on Sauce or not
        # 1. Sauce only permits 5 servers at a time
        # 2. 

        # tear out browserstack
        # make it easy to create new drivers, one for each test
        self.targetApplicationUrl = targetApplicationUrl
        self.seleniumServerHostname = seleniumServerHostname
        self.testList = [] # List of test-classes
        self.testResults = TestResultSet()

        # create driver
        # NB: eventually we want to have one driver per test
        # setupDriver includes startup tests
        # in the future, pass in a driver creation function
        self.driver = self.setupDriver()

        # get list of tests to run, if provided
        self.testList = get_every_build_tests(get_suites())

        # return
    





    def _create_driver(self):
        return ""
            

    def _run_one_test(self, testClassName, capabilities):
        # this should request a driver using self._create_driver()
        dr = self._create_driver()

        # moves the 
        test = testClassName(dr, self.targetApplicationUrl, capabilities, root_test=True, mode="multi_panel", seed=random.random(), verbose=True)


        return test

    def set_tests(self):
        """
        Define which tests should be run
        """
        return ""

    def _run_all_tests(self):
        return ""

    def run(self):
        for test in self.testList:
            self.testResults.include(self._test_on_all(test))
        return self

    def results(self):
        return self.results


    #
    #
    # Auxiliary functions. Might not neeed to be part of the class
    #   - Consider moving the driver functions into its own class
    #####################
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

    def createSauceLabsDriver(self):

        return ""

    def getApplicationHostname(self):
        """
        Generate the application hostname. Order of precedence
        1. The APPLICATION_HOSTNAME variable
        2. Generating application hostname based on the GITHUB_SHA
        - We might need to parameterize the subdomain
        """
        if 'APPLICATION_HOSTNAME' in os.environ:
            return os.environ['APPLICATION_HOSTNAME']
        
        elif 'GITHUB_SHA' in os.environ:
            return "https://{}.cauldron.sefaria.org/".format(os.environ['GITHUB_SHA'][:6])
        else:
            logger.info("Please set the APPLICATION_HOSTNAME or GITHUB_SHA environment variable and rerun.")
            exit(1)
        
    def ensureServerReachability(self):
        # Check reachability of named servers
        for site in [self.getApplicationHostname()]:
            resp = requests.get(site).status_code
            if resp > 399:
                logger.info("Site {} not reachable. Please make sure it is running and rerun this script".format(site))
                exit(1)
            else:
                logger.info("Site {} is reachable.".format(site))

        
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


    def ensureEnvVars(self):
        if 'SELENIUM_SERVER_URL' not in os.environ:
            logger.info("Please set the SELENIUM_SERVER_HOSTNAME environment variable and rerun.")
            exit(1)

        if ('APPLICATION_HOSTNAME' not in os.environ) and ('GITHUB_SHA' not in os.environ):
            logger.info("Please set the APPLICATION_HOSTNAME or GITHUB_SHA environment variable and rerun.")
            exit(1)
        logger.info("The requird environment variables are present. Proceeding.")


    def ensureSeleniumCapabilities(self):
        """
        Make sure the target Selenium server has the capabilities we need. 
        """
        return

    def setupDriver(self):
        """
        setup and test a driver. 
        Later, pass in a function that returns the desired driver

        Drivers can be created directly, but this performs a series of startup tests  
        """
        self.ensureEnvVars()
        self.ensureServerReachability()
        self.ensureSeleniumCapabilities()

        # Create and test driver
        seleniumServerUrl = os.environ['SELENIUM_SERVER_URL']
        driver = self.createFirefoxDriver(seleniumServerUrl=seleniumServerUrl)
        self.ensureDriverFunctionality(driver)

        # get homepage and get title, and test
        logger.info("Testing connectivity of the target server")

        # Generate the application URL from the gitsha if its available. 
        # If it's not available, use APPLICATION_HOSTNAME

        applicationUrl = self.getApplicationHostname()
        
        driver.get(applicationUrl)
        logger.info("Current URL: {}".format(driver.current_url))
        logger.info("Current title: {}".format(driver.title))

        assert driver.current_url == applicationUrl
        assert driver.title == "Sefaria: a Living Library of Jewish Texts Online"

        logger.info("Preliminary tests finished")
        return driver