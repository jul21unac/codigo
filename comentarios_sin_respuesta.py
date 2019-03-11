from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Firefox()
driver.get("https://www.youtube.com/watch?v=1ybGgBD3Q4E")
##parar el video
video2 = driver.find_element_by_class_name("ytp-play-button.ytp-button")
video2.click()

##scroleamos a tope
driver.execute_script("window.scrollTo(0,5)")
driver.execute_script("window.scrollTo(0,10)")
driver.execute_script("window.scrollTo(0,500)")
driver.execute_script("window.scrollTo(0,600)")
driver.execute_script("window.scrollTo(0,800)")
driver.execute_script("window.scrollTo(0,900)")
driver.execute_script("window.scrollTo(0,100080)")
driver.execute_script("window.scrollTo(0,100999)")
###guardamos el html
html = driver.find_element_by_xpath("/html")
f = open('you_2.txt','w')
print(html.text,file = f)
##chimpun
