from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def isLoggedIn(driver):
    driver.get("http://www.evanfalkenstine.net/")
    time.sleep(1)
    header = driver.find_element_by_class_name("top-menu")
    if  header.text.find("Logout") == -1: # does not contain logout
        res = False
    else:
        res = True
    time.sleep(1)
    return res
    
def logIn(driver):
    if isLoggedIn(driver):
        return True

    driver.get("http://www.evanfalkenstine.net/login")
    userEmail = driver.find_element_by_id("identifierId")
    userEmail.send_keys("")
    driver.find_element_by_id("identifierNext").click()

    userPW = driver.find_element_by_id("password")
    userPW = userPW.find_element_by_name("password")
    userPW.send_keys("")
    userPW.send_keys(Keys.RETURN)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.title_is("Item Catalog")
        )
    finally:
        time.sleep(1)
        return isLoggedIn(driver)

def addCategory(driver, category_name):
    if isLoggedIn(driver) == False:
        return False
    driver.get("http://www.evanfalkenstine.net/item_catalog/categories/add")
    inputName = driver.find_element_by_id("catName")
    inputName.send_keys(category_name)
    time.sleep(1)
    inputName.submit()
    time.sleep(1)
    return True

def categoryExists(driver, category_name):
    driver.get("http://www.evanfalkenstine.net/item_catalog/")
    all_a_tags = driver.find_elements_by_tag_name("a")
    for anchor in all_a_tags:
        if anchor.text == category_name:
            time.sleep(1)
            return True
    time.sleep(1)            
    return False

def deleteCategory(driver, category_name):
    if isLoggedIn(driver) == False:
        time.sleep(1)
        return False

    driver.get("http://www.evanfalkenstine.net/item_catalog/")
    all_a_tags = driver.find_elements_by_tag_name("a")
    for anchor in all_a_tags:
        if anchor.text == category_name:
            collapse_name = anchor.get_attribute("href")[45:]
            anchor.click()
            break

    card_body = driver.find_element_by_id(collapse_name)
    links = card_body.find_elements_by_tag_name("a")
    for link in links:
        if link.text == "Delete":
            link.click()
            break
    time.sleep(1)
    driver.find_element_by_tag_name("input").click()
    time.sleep(1)
    return True

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    example_name = "Job Interview Supplies"

    if logIn(driver):
       print("Successfully Logged In")
    else:
       print("Login Failed")

    if categoryExists(driver, example_name):
        print("Category Found")
    else:
        print("Category Not Found")

    if addCategory(driver, example_name):
        print("Category Added")
    else:
        print("Failed to Add Category")

    if categoryExists(driver, example_name):
        print("Category Found")
    else:
        print("Category Not Found")

    if deleteCategory(driver, example_name):
        print("Category Deleted")
    else:
        print("Failed to Delete Category")

    if categoryExists(driver, example_name):
        print("Category Found")
    else:
        print("Category Not Found")