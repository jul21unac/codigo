from scraping_u2 import *
import json
url_text = 'https://www.youtube.com/watch?v=1ybGgBD3Q4E'
objeto_scraping_u2 = scraping_u2(url_text)
objeto_scraping_u2.display_all_the_comments()
fi = open('json_comments_3.txt','w')
json.dump(objeto_scraping_u2.objeto_u2be.my_dict,fi)
fi.close()
