from time import sleep
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

__author__ = 'dvirdi'
from selenium import webdriver
"""

This program will add a list of websites to your feedly reader.

---Not done yet.

"""


def enterTextInTextbox(text):
    # select element by id
    try:
        inputElement = driver.find_element_by_id("maxHerculeInput")
        inputElement.clear()
        inputElement.send_keys(text)
        inputElement.click()
        sleep(1)
        print "arrow_down"
        inputElement.send_keys(Keys.ARROW_DOWN)
        print "enter"
        inputElement.send_keys(Keys.ENTER)
    except (NoSuchElementException, StaleElementReferenceException):
        pass


def openFeedlyDiscoverPage(driver):
    driver.get('http://feedly.com/i/discover')


def listOfWebsites():
    f = open('/Users/dvirdi/Desktop/Links/resources/a16z_links_ordered.txt', 'r')
    return f.readlines()


def isError(driver):
    if("No feed found." in driver.page_source):
        driver.back()
        return True
    else:
        return False

def clickGreenFeedlyButton(driver):
    pass



def method_1(lines):
    openFeedlyDiscoverPage(driver)
    for line in lines:
        line = line.split(" ")[0]
        enterTextInTextbox(line)
        if (isError(driver)):
            continue
        clickGreenFeedlyButton(driver)

def addTop3Links():
    pass


def method_2(lines, driver):
    for line in lines:
        line = line.split(" ")[0]
        website = "http://feedly.com/i/spotlight/"+line
        driver.get(website)

        print website
        if(isError(driver)):
            continue
        else:
            addTop3Links()


driver = webdriver.Firefox()
driver.firefox_profile.set_preference("webdriver.load.strategy", "unstable")


lines = listOfWebsites()
# method_1(lines)
method_2(lines,driver)


