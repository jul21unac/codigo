"""this class create a json from the source_page of u2be """
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import *
import json

class u2be_json:
    #dictionari will save all the data of the video
    my_dict = {}
    
    #pass the script of u2be web
    def __init__(self, script):
        self.script = script
    #function that create a beatifuSoup object  
    def load_script(self):
        self.soup=BeautifulSoup(self.script,'html.parser')
    #function load principal data from the video 
    def video_data(self):
        #title's video
        self.my_dict = {'title' : self.soup.title.text.strip()}
        #vote's video positive and negative
        votes = self.soup.find_all("yt-formatted-string", {"class": "style-scope ytd-toggle-button-renderer style-text", "id":"text" })
        self.my_dict['positives_votes']=votes[0].text.split()
        self.my_dict['negatives_votes']=votes[1].text.split()
        #find the div that contain author ref and date of the video        
        data_video = self.soup.find("div", {"class": "style-scope ytd-video-secondary-info-renderer", "id":"top-row" })	
        author = data_video.find("a", {"class": "yt-simple-endpoint style-scope yt-formatted-string" })	
        self.my_dict['author']= author.text.split()[0]
        self.my_dict['author_chanel']=author["href"]
        date_script = data_video.find("span", {"class": "date style-scope ytd-video-secondary-info-renderer" })
        date_len = len(date_script.text.split())        
        video_date = datetime.strptime(date_script.text.split()[date_len-3] + date_script.text.split()[date_len-2]+ date_script.text.split()[date_len-1], '%d%b.%Y')
        self.my_dict['video_date'] = video_date.isoformat()
#search all comments from the website
    def video_comments(self):
        comment_here = self.soup.find("div", {"class": "style-scope ytd-item-section-renderer" ,"id":"contents"  })
        #find all the comments in the div with id : body and replies
        mydivs = comment_here.findAll("div", {"class": ["style-scope ytd-comment-renderer", "style-scope ytd-comment-thread-renderer"]  ,"id":["body","replies"]})
        j=0
        comments_array = []
        for i in mydivs:
            if i['id']=='body' and i.parent['class'][1] == 'ytd-comment-thread-renderer':
                data_comment = self.comments_struture(i)
                if j+1 == len(mydivs):
                    break
                if mydivs[j+1]['id']=='replies' :
                    replies_divs =  mydivs[j+1].findAll("div", {"class": ["style-scope ytd-comment-renderer", "style-scope ytd-comment-thread-renderer"]  ,"id":"body"})
                    replies_comment = []
                    for k in replies_divs:
                        replies_comment.append(self.comments_struture(k))
                    data_comment['replies'] = replies_comment
                comments_array.append(data_comment)
            j += 1
        self.my_dict['comments'] = comments_array
	
#			
    def comments_struture(self,div):
        dict_comment = {}
        ###<div class="style-scope ytd-comment-renderer" id="header-author">		
        # first we search the comment's data 
        any_comment = div.find("div", {"class": "style-scope ytd-comment-renderer", "id":"header-author" })
        ###<a class="yt-simple-endpoint style-scope ytd-comment-renderer" href="/channel/UCYpUodCy_0smDdgsgumNcQA" id="author-text">
        comment_author = any_comment.find("a", {"class": "yt-simple-endpoint style-scope ytd-comment-renderer", "id":"author-text" })
        comment_name_author =  comment_author.span.text.splitlines()[1].lstrip()
        dict_comment['author'] = comment_name_author
        comment_href_author = comment_author['href']
        dict_comment['href'] = comment_href_author
        #fecha del comentario que esta en español o ingles
        ###<yt-formatted-string class="published-time-text above-comment style-scope ytd-comment-renderer" has-link-only_="">
        comment_date = any_comment.find("yt-formatted-string", {"class": "published-time-text above-comment style-scope ytd-comment-renderer"})      
        string_date_coment = comment_date.a.text.strip()
        ###hacer una prueba de lo que se quiere hacer en ingles 
        actual_time =datetime.now() 
        j=0
        final_date = ''
        #import ipdb; ipdb.sset_trace()
        for i in string_date_coment.split():	
            #import ipdb; ipdb.sset_trace()
            if i.isnumeric():
                number_date = i
                date_string = string_date_coment.split()[j+1]
                
                if date_string[0:3] == 'mes' or date_string[0:5] == 'month':
                        final_date = self.subst_month(actual_time , number_date)
                elif date_string[0:4] == 'hora' or date_string[0:4] == 'hour':
                        final_date = self.subst_hour(actual_time , number_date)
                elif date_string[0:3] == 'día' or date_string[0:3] == 'day':
                        final_date = self.subst_day(actual_time , number_date)				
                elif date_string[0:6] == 'semana' or date_string[0:4] == 'week':
                        final_date = self.subst_week(actual_time , number_date)
                elif date_string[0:6] == 'minuto' or date_string[0:6] == 'minute':
                        final_date = self.subst_minute(actual_time , number_date)
                elif date_string[0:3] == 'año' or date_string[0:4] == 'year':
                        final_date = self.subst_year(actual_time , number_date)
            j  += 1
        dict_comment['date'] =final_date
        #import ipdb; ipdb.sset_trace()
        ##text of the comment
        ###<yt-formatted-string class="style-scope ytd-comment-renderer" id="content-text"
        text_coment =  div.find("yt-formatted-string", {"class": "style-scope ytd-comment-renderer", "id":"content-text" }).text.strip()        
        dict_comment['text'] = text_coment
        ##votos positivos
        #los negativos no tenemos ninguno en el ejemplo se tiene que hacer la prueba para ver de donde coger los votos negativos
        ### <div class="style-scope ytd-comment-action-buttons-renderer" id="toolbar"> dentro de este div esta un span
        positive_votes_comment = div.find("div", {"class": "style-scope ytd-comment-action-buttons-renderer", "id":"toolbar" })
        dict_comment['positives_votes'] = positive_votes_comment.span.text.strip()        
        return dict_comment	
    ###todo : hacer una prueba de lo que se quiere hacer en ingles 
    ##### funtion that substr
    def subst_month(self,a_current ,a_months):
        return_date = a_current - relativedelta(months = + int(a_months))  
        return return_date.isoformat()  
    def subst_week( self,a_current ,a_weeks):
        return_date = a_current - relativedelta(weeks = + int(a_weeks))
        return return_date.isoformat() 
    def subst_day(self,a_current ,a_days):
        return_date = a_current - relativedelta(days = + int(a_days))
        return return_date.isoformat() 
    def subst_hour(self,a_current ,a_hours):
        return_date = a_current - relativedelta(hours = + int(a_hours))
        return return_date.isoformat() 
    def subst_minute(self,a_current, a_minutes):
        return_date = a_current - relativedelta( minutes= + int(a_minutes))
        return return_date.isoformat() 
    def subst_year(self,a_current, a_year):
        return_date = a_current - relativedelta(years = + int(a_year))
        return return_date.isoformat() 
    def get_json_comment(self):
        dict_dump = json.dumps(self.dict_comment)
        json_comment = json.loads(dict_dump)
        return dict_dump

