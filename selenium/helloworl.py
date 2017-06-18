from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()
 
# navigate to the application home page
driver.get("https://www.google.com")
 
# get the search textbox
search_field = driver.find_element_by_name("q")
 
# enter search keyword and submit
search_field.send_keys("Hello World")
search_field.submit()
 
# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name  method
lists= driver.find_elements_by_class_name("r")

# iterate through result
for item in lists:
   print (item.text)

time.sleep(5) 

driver.quit()
