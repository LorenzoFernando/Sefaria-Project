# __package__ = "reader.browsertest"

## TO DO
# make sure there is mongo access before running and handle

import django
django.setup() # required to use sefaria.models

from selenium import webdriver
import os
import requests
import structlog

from reader.browsertest import basic_tests
from reader.browsertest.framework import Trial
from reader.browsertest.framework import elements


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import title_contains, presence_of_element_located, staleness_of,\
        element_to_be_clickable, visibility_of_element_located, invisibility_of_element_located, \
    text_to_be_present_in_element, _find_element, StaleElementReferenceException, visibility_of_any_elements_located



# Use environment variables for tests

# Arguments
# * Selenium Server Hostname
# * Application Hostname

CAPABILITIES = [
    {'browser': 'Firefox'},
]
logger = structlog.get_logger()

def ensureEnvVars():
    if 'SELENIUM_SERVER_URL' not in os.environ:
        logger.info("Please set the SELENIUM_SERVER_HOSTNAME environment variable and rerun.")
        exit(1)

    if 'APPLICATION_HOSTNAME' not in os.environ:
        logger.info("Please set the APPLICATION_HOSTNAME environment variable and rerun.")
        exit(1)
    logger.info("The requird environment variables are present. Proceeding.")


def ensureServerReachability():
    # Check reachability of named servers
    for site in [os.environ['APPLICATION_HOSTNAME'], os.environ['SELENIUM_SERVER_URL']]:
        resp = requests.get(site).status_code
        if resp > 399:
            logger.info("Site {} not reachable. Please make sure it is running and rerun this script".format(site))
            exit(1)
        else:
            logger.info("Site {} is reachable.".format(site))

def ensureSeleniumCapabilities():
    """
    Make sure the target Selenium server has the capabilities we need. 
    """
    return

def ensureDriverFunctionality(driver):
    """
    Make sure the webdriver can make requests
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

def createFirefoxDriver(seleniumServerUrl="http://localhost:4444/wd/hub",):
    """
    createFirefoxDriver creates a firefox driver

    For now, doesn't require credentials
    """
    logger.info("Creating Firefox driver...")
    fopt = webdriver.FirefoxOptions()
    fopt.add_argument('--headless')
    return webdriver.Remote(command_executor=seleniumServerUrl, options=fopt)

def setup():
    ensureEnvVars()
    ensureServerReachability()
    ensureSeleniumCapabilities()

    # Create and test driver
    seleniumServerUrl = os.environ['SELENIUM_SERVER_URL']
    driver = createFirefoxDriver(seleniumServerUrl=seleniumServerUrl)
    ensureDriverFunctionality(driver)

    # get homepage and get title, and test
    logger.info("Testing connectivity of the target server")

    # Generate the application URL from the gitsha if its available. 
    # If it's not available, use APPLICATION_HOSTNAME

    commitSha = os.getenv('GITHUB_SHA')
    if commitSha is not None:
        applicationUrl = "https://{}.cauldron.sefaria.org/".format(commitSha[:6])
    else:
        applicationUrl = os.environ['APPLICATION_HOSTNAME'] # maybe add trailing slash if missing
    
    driver.get(applicationUrl)
    logger.info("Current URL: {}".format(driver.current_url))
    logger.info("Current title: {}".format(driver.title))

    assert driver.current_url == applicationUrl
    assert driver.title == "Sefaria: a Living Library of Jewish Texts Online"

    logger.info("Preliminary tests finished")
    return driver

def run_single_test(driver, testName,):
    """
    run_single_test
    Inputs:
      * Driver -- performs the webdriver tests
      * name of the test to run

    Outputs:
      * test results (a dict?)

    """
    return

def getAtomicTests():
    """
    Returns an array of classes whose direct superclass is elements.AtomicTest
    """
    return elements.AtomicTest.__subclasses__()

def getPageLoadSuite():
    return [cls for cls in elements.AtomicTest.__subclasses__() if cls.suite_class == basic_tests.PageloadSuite]
    


def testsAgainstDriver(driver, tests=[], target="http://localhost:80"):
    # NB: The documentation suggests a new driver per test
    # https://www.selenium.dev/documentation/en/guidelines_and_recommendations/fresh_browser_per_test/
    results = []
    for test in tests:
        driver.delete_all_cookies()
        #print(driver.get_cookies())
        t = test(driver, target, {'browser': 'Firefox'})
        result = t.run()

        results.append(result)
        print("TEST COMPLETE")


        #driver.delete_cookie("_ga")
    
    return results

# def load_toc(self, my_temper=None):
#     my_temper = my_temper or TEMPER  # This is used at startup, which can be sluggish on iPhone.
#     self.driver.get(self.base_url + "/texts")
#     WebDriverWait(self.driver, 30).until(element_to_be_clickable((By.CSS_SELECTOR, ".readerNavCategory")))
#     self.set_modal_cookie()
#     return self

def load_toc(driver, wait):
    driver.get("https://vecino.cauldron.sefaria.org/texts")
    logger.info("Starting wait")
    WebDriverWait(driver, wait).until(element_to_be_clickable((By.CSS_SELECTOR, ".readerNavCategory")))
    logger.info("Ending wait")


if __name__ == "__main__":
    """
    Script entrypoint

    Example invocation:
    SELENIUM_SERVER_URL="http://localhost:4444/wd/hub" APPLICATION_HOSTNAME="https://vecino.cauldron.sefaria.org/" python3 ./run_test.py
    """
    driver = setup()
    targetAppUrl = os.environ['APPLICATION_HOSTNAME']
    results = testsAgainstDriver(driver, getPageLoadSuite(), targetAppUrl)
    
    for result in results:
        print(result.word_status())

    exit(0)
    print(driver.get_cookies())
    driver.quit()


# from reader.browsertest import zzRun_test
# driver = zzRun_test.setup()
# driver.get("https://vecino.cauldron.sefaria.org/texts")
# z = SectionContentAsExpectedChapter(driver, "https://vecino.cauldron.sefaria.org",{'browser': 'Firefox'})
# result = z.run()
# result.success


## Consider moving driver and target URL population to the AbstractTest.run() function, instead of __init__()
## Drivers are NOT threadsafe
## Don't print test errors to STDOUT -- just record it as part of the test result