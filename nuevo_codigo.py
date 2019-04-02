from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import random

url_1 = "https://www.youtube.com/watch?v=1ybGgBD3Q4E"
#funcion para enviar las urls y bajarnos los comentarios
def recolecta_comentarios(url):
	driver = webdriver.Firefox()
	driver.get(url)	
	##parar el video
	video2 = driver.find_element_by_class_name("ytp-play-button.ytp-button")
	video2.click()	
	i=0
	ultima_medida = driver.execute_script("return document.documentElement.scrollHeight;")
	#bucle para desplazarnos hacia abajo
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
	body = driver.find_element_by_xpath("/html/body")
	#buscamos los id more-text que es para ver las contestaciones
	more_text = driver.find_elements_by_xpath("//*[@id='more-text']")
	
	#damos click a todas los comentarios con contestación
	for dale in more_text:
		dale.click()
		time.sleep(0.5)		
	#el nombre lo cogemos del link del video para saber de donde viene
	nombre_fichero=url[url.index("=") + 1: ]+".txt"
	f = open(nombre_fichero,'w')
	#recogemos los comentarios
	comentarios = driver.find_elements_by_xpath("//*[@id='content-text']")
	#for para recolectar los comentarios parece que no tiene orden
	for item in comentarios:	
		print(item.text,file = f)
		print("-"*80,file = f)
	driver.close()

recolecta_comentarios(url_1)

		

