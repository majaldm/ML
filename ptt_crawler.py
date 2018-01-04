
# coding: utf-8

# In[82]:


#!pip install --user --upgrade requests beautifulsoup4 lxml html5lib==1.0b8

import os
import json
import requests
from uuid import uuid4
from bs4 import BeautifulSoup


class PttCrawler:
    
    def __init__(self, board, page, write=False):
        self.ptt_url = 'https://www.ptt.cc'
        self.board = board
        self.page = page
        
        self.session = requests.Session()
        self.session.cookies.update({
            'over18': '1'
        })
        
        self.write = write
        
    def run(self):
        
        url = self.ptt_url + '/bbs/' + self.board
        post_link_list = self.fetchPostLinkList(url)
        post_list = [self.fetchPost(post_link) for post_link in post_link_list]
        
        #for post in post_list:
        #    print(post)
        
        #NB self is never paszsed as an argument
        
        return post_list
        
    def fetchPostLinkList(self, url):

        #resp = requests.get(
        #    url,
        #    cookies = self.session.cookies
        #)
           
        resp = self.session.get(
            url
        )
        
        soup = BeautifulSoup( resp.text.encode( "utf-8" ), "lxml" )

        post_list = soup.find('div', {'class': 'r-list-container action-bar-margin bbs-screen'})
        link_list = [tag.get('href') for tag in post_list.find_all('a')]
        
        if self.page > 0:
            paging_group = soup.find('div', {'class': 'btn-group btn-group-paging'})
            previous_link = self.ptt_url + paging_group.find_all('a')[1].get('href')
        
            self.page -= 1
            previous_post_link_list = self.fetchPostLinkList(previous_link)
            #BECAUSE IT OPERATES INSIDE THE CLASS DEFINITION self SPECIFIES THE METHOD ("NOT THE ARGUMENTS")
            if previous_post_link_list:
                link_list.extend(previous_post_link_list)
        
        return link_list
    
    def fetchPost(self, url):

        url = self.ptt_url + url

        resp = self.session.get(
            url
        )
        
        soup = BeautifulSoup( resp.text.encode( "utf-8" ), "lxml" )
        
        metadata = soup.find_all('div', {'class': 'article-metaline'})
        
        try:
            author = metadata[0].find('span', {'class': 'article-meta-value'}).text # find() RETURNS AN OBJECT WITH text MEMBER
        except:
            author = None
        
        try:
            title = metadata[1].find('span', {'class': 'article-meta-value'}).text
        except:
            title = None
        
        try:
            date = metadata[2].find('span', {'class': 'article-meta-value'}).text
        except:
            date = None

        try:
            content = metadata[-1].next_sibling # [-1] STANDS FOR LAST OF THE LIST
        except:
            content = None

        return {'title': title, 'author': author, 'date': date, 'content': content}



# In[86]:


#instance = PttCrawler('Gossiping', 3)
#post_list = instance.run()
#for post in post_list:
#    print(post)

