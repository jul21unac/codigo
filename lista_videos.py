from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import random

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/user/CirculosPodemos/videos")
ultima_medida = driver.execute_script("return document.documentElement.scrollHeight;")
i=0
while True:		
	#bucle para desplazarnos poco a poco
	while i <= ultima_medida:
		cadena_medida = "window.scrollTo(0," + str(i) + ");"
		driver.execute_script(cadena_medida)
		#el incremento lo hacemos ramdon para que no sospechen		
		incremento = random.randint(50,100)
		i = i + incremento
		#el tiempo de espera tambien
		tiempo_espera = random.uniform(0.4,0.5)
		time.sleep(tiempo_espera)		
	nueva_medida = driver.execute_script("return document.documentElement.scrollHeight;")
	if nueva_medida == ultima_medida:
		break
	ultima_medida = nueva_medida

videos = driver.find_elements_by_xpath("//*[@id='video-title']")
f = open('links_podemos.txt','w')
#podemos lanzar la funcion de recoleccion de comentarios en vez de guardar los links de los videos
for link in videos:	
	print(link.get_attribute("href"),file = f)
	print("-"*80,file = f)

