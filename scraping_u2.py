from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import random
from u2be_json import *

class scraping_u2:
	page_source = ''
	def __init__(self, url_text):
		self.url_text = url_text
	#display all the comments and replays 
	def display_all_the_comments(self):
		self.driver = webdriver.Firefox()
		self.driver.get(self.url_text)	
		##parar el video
		video2 = self.driver.find_element_by_class_name("ytp-play-button.ytp-button")
		video2.click()	
		i=0
		ultima_medida = self.driver.execute_script("return document.documentElement.scrollHeight;")
		#bucle para desplazarnos hacia abajo
		while True:		
			#bucle para desplazarnos poco a poco
			while i <= ultima_medida:
				cadena_medida = "window.scrollTo(0," + str(i) + ");"
				self.driver.execute_script(cadena_medida)
				#el incremento lo hacemos ramdon para que no sospechen		
				incremento = random.randint(50,100)
				i = i + incremento
				#el tiempo de espera tambien
				tiempo_espera = random.uniform(0.4,0.5)
				time.sleep(tiempo_espera)		
			nueva_medida = self.driver.execute_script("return document.documentElement.scrollHeight;")
			if nueva_medida == ultima_medida:
				break
			ultima_medida = nueva_medida
		body = self.driver.find_element_by_xpath("/html/body")
		#buscamos los id more-text que es para ver las contestaciones
		more_text = self.driver.find_elements_by_xpath("//*[@id='more-text']")	
		#damos click a todas los comentarios con contestación
		for dale in more_text:
			dale.click()
			time.sleep(0.5)		
		#comentarios siguientes
		continuacion = self.driver.find_elements_by_xpath("//yt-formatted-string[contains(concat(' ',normalize-space(@class),' '),'style-scope yt-next-continuation')]")
		for conti in continuacion:	
			conti.click()
			time.sleep(0.5)	
		self.page_source =self.driver.page_source
		self.get_comments()
	#get al the comments in a diccionary 
	def get_comments(self):
		#we load the object u2be_json with the source fo the web page
		self.objeto_u2be = u2be_json(self.page_source)
		self.objeto_u2be.load_script()
		self.objeto_u2be.video_data()
		self.objeto_u2be.video_comments()



		

