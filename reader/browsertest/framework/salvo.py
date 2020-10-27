# -*- coding: utf-8 -*-

from selenium import webdriver
from appium import webdriver as appium_webdriver
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
        
        return ""

    def _create_driver():
        try: 
            selDriver = webdriver.Remote(
                command_executor=seleniumServerHostname,
                desired_capabilities=['firefox']
            )
            return selDriver
        execept Exception as e:
        p

    def _run_one_test(self, testClassName, capabilities):
        # this should request a driver using self._create_driver()
        dr = self._create_driver()

        # moves the 
        test = test_class(dr, self.targetApplicationUrl, capabilities, root_test=True, mode="multi_panel", seed=random.random(), verbose=True)


        return ""

    def set_tests():
        """
        Define which tests should be run
        """
        return ""

    def _run_all_tests():
        return ""

    def run():
        return ""

    
