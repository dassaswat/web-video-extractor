import time
import json
import logging
import requests
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from config import username, password
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class MagooshVideoDataExtractor:
    def __init__(self):
        self.BASE_URL = 'https://gre.magoosh.com'
        self.TOPIC_URI = ['/lessons?section=85', '/lessons?section=53', '/lessons?section=54', '/lessons?section=63']
        self.intro_category_list = []
        self.quants_category_list = []
        self.verbal_category_list = []
        self.writings_category_list = []
        self.all_intro_subtopics = []
        self.all_quants_subtopics = []
        self.all_verbal_subtopics = []
        self.all_writing_subtopics = []
        self.breakpoints = [
            '', 
            [
                'Plugging In for Word Problems', 
                'Word Problems with Fractions',
                'Ratios and Rates',
                'Integer Properties Strategies',
                'Simplifying with Substitutions',
                'Picking Numbers',
                'Working with Formulas',
                'Geometry Strategies - Part II',
                'Graphs of Quadratics',
                'Percentiles',
                'Counting Strategies',
                'Guessing Strategies',
                'Unconventional Graphs',
                ' Summary of QC Strategies',
            ], [
                'Testing the Answer Choices',
                'Apposition',
                'Reverse Apposition',
                'Advanced Double Blanks',
                'Working Backwards',
                'Difficult Words in Sentence Equivalence',
                'Obscure Vocabulary',
                'Advanced Question Types',
                'Numbers vs. Percents',
                ], 
            [
                'Writing Tips for the 4 Major Scoring Components - II',
                'How to Practice',
                'Argument Task Example',
            ]
        ]
        logging.basicConfig(
                level=logging.NOTSET,
                format="{asctime} {levelname} {message}",
                style='{',
                )
    
    def get_all_categories(self):
        
        logging.info('Getting all categories')
        
        all_categories = []
        for topics in self.TOPIC_URI:
            response = requests.get(self.BASE_URL+ topics)
            soup = BeautifulSoup(response.content, 'html5lib')
            categories = soup.find_all('h4')
            all_categories.append(categories)
        
        for i in range(0, len(all_categories)):
            if i == 0:
                for category in all_categories[i]:
                    self.intro_category_list.append(category.text)
            elif i == 1:
                for category in all_categories[i]:
                    self.quants_category_list.append(category.text)
            elif i == 2:
                for category in all_categories[i]:
                    self.verbal_category_list.append(category.text)
            elif i == 3:
                for category in all_categories[i]:
                    self.writings_category_list.append(category.text)
    
    def extracting_subtopic(self):
        
        logging.info('Extracting Subtopics')
        
        all_categories = []
        val = 0 
        data = {}
        all_urls = []
        new_all_urls = []
        categories_name = {
            0 : 'Intro',
            1 : 'Quants',
            2 : 'Verbal',
            3 : 'Writing'
        }

        for topics in self.TOPIC_URI:
            response = requests.get(self.BASE_URL+ topics)
            soup = BeautifulSoup(response.content, 'html5lib')
            categories = soup.find_all('ul')
            all_categories.append(categories)
            
        for i in range(0, len(all_categories)):
            for value in all_categories[i]:
                for h3 in value.find_all('h3'):
                    data[val] = {
                        'id': val,
                        'topic-name': h3.text,
                        'uri': '',
                        'category': categories_name[i],
                    }
                    val += 1
        
        for i in range(0, len(all_categories)):
            for value in all_categories[i]:
                for a in value.find_all('a'):
                    all_urls.append(a['href'] if a['href'].startswith('/lessons/') else '')

        for link in all_urls:
            if link == '':
                continue
            else:
                new_all_urls.append(self.BASE_URL + link)
        
        for i in range(0, len(new_all_urls)):
            data[i]['uri'] = new_all_urls[i]
        
        for key in data.keys():
            if data[key]['category'] == 'Intro':
                self.all_intro_subtopics.append(data[key])
            elif data[key]['category'] == 'Quants':
                self.all_quants_subtopics.append(data[key])
            elif data[key]['category'] == 'Verbal':
                self.all_verbal_subtopics.append(data[key])
            elif data[key]['category'] == 'Writing':
                self.all_writing_subtopics.append(data[key])

    def destructurer(self, breakpoints: List[List[str]]):
        
        logging.debug('Destructuring all the subtopics onto its appropriate head!')
        
        
        quants_index_list = []
        verbal_index_list = []
        writing_index_list = []
        intro_broken_list = []
        quants_broken_list = []
        verbal_broken_list = []
        writing_broken_list = []

        
        for item in breakpoints:
            if breakpoints.index(item) == 0:
                intro_broken_list.append([item for item in self.all_intro_subtopics])
            
            elif breakpoints.index(item) == 1:
                for i in range(0, len(self.all_quants_subtopics)):
                    if self.all_quants_subtopics[i]['topic-name'] in item:
                        quants_index_list.append(i)
                quants_broken_list.append([topic for topic in self.all_quants_subtopics[0:quants_index_list[0]+1]])
                
                for i in range(0, len(quants_index_list)-1):
                    quants_broken_list.append([topic for topic in self.all_quants_subtopics[quants_index_list[i]+1:quants_index_list[i+1]+1]])
                    
            
            elif breakpoints.index(item) == 2:
                for i in range(0, len(self.all_verbal_subtopics)):
                    if self.all_verbal_subtopics[i]['topic-name'] in item:
                        verbal_index_list.append(i)
                verbal_broken_list.append([topic for topic in self.all_verbal_subtopics[0:verbal_index_list[0]+1]])
                
                for i in range(0, len(verbal_index_list)-1):
                    verbal_broken_list.append([topic for topic in self.all_verbal_subtopics[verbal_index_list[i]+1:verbal_index_list[i+1]+1]])
            
            elif breakpoints.index(item) == 3:
                for i in range(0, len(self.all_writing_subtopics)):
                    if self.all_writing_subtopics[i]['topic-name'] in item:
                        writing_index_list.append(i)
                
                writing_broken_list.append([topic for topic in self.all_writing_subtopics[0:writing_index_list[0]+1]])
                
                for i in range(0, len(writing_index_list)-1):
                    writing_broken_list.append([topic for topic in self.all_writing_subtopics[writing_index_list[i]+1:writing_index_list[i+1]+1]])
        
        return [intro_broken_list, quants_broken_list, verbal_broken_list, writing_broken_list]
    
    def categorizing_and_destructuring_heads(self):
        
        logging.info('Categorizing and Destructuring Headings')

        intro = {
            'name': 'INTRO',
            'category-list': self.intro_category_list,
        }
        quants = {
            'name': 'QUANTS',
            'category-list': self.quants_category_list
        }
        verbal = {
            'name': 'VERBAL',
            'category-list': self.verbal_category_list
        }
        writing = {
            'name': 'WRITING',
            'category-list': self.writings_category_list
        }
        all_topic_list = [intro, quants, verbal, writing]
        list_data = []
        key = 0
        
        for category in all_topic_list:
            for item in category['category-list']:
                list_data.append({
                    'id': key,
                    'category': category['name'],
                    'Head': item,
                    'sub-topics': None
                })
                key += 1
        
        
        self.extracting_subtopic()
        data = self.destructurer(self.breakpoints)
        counter = 0

        for data_item in data:
            for category_topics in data_item:
                list_data[counter]['sub-topics'] = category_topics
                counter += 1
        
        return list_data
        
    def get_data_with_video_urls(self):
        
        logging.info("Welcome! We will establish a connection with magoosh and enter your credentials as provided!/nVerify the captcha if asked and we will iterate through pages to get the video URL.")
        logging.warn("BE PATIENT IT WILL TAKE AROUND 30MINS. MAJORLY DEPEND's ON YOUR NETWORK SPEED!")
        logging.info("For more details visit 'https://github.com/dassaswat' ")

        list_all_access_uri = []
        video_link_list = []
        data = self.categorizing_and_destructuring_heads()

        for item in data:
            for access_link in item['sub-topics']:
                list_all_access_uri.append(access_link['uri'])

        try:
            s=Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s)
            driver.get(self.BASE_URL + '/login')
            username_field = driver.find_element(by='id',value='session_login')
            time.sleep(5)
            username_field.send_keys(username)
            password_field = driver.find_element(by='id', value='session_password')
            time.sleep(5)
            password_field.send_keys(password)
            login_button = driver.find_element(by='xpath', value='//*[@id="invisible-recaptcha-form"]/button')
            time.sleep(5)
            login_button.click()
            time.sleep(30)

            for uri in list_all_access_uri:
                driver.get(uri)
                video_link = driver.find_element(By.CLASS_NAME, value='vjs-tech')
                video_link_list.append(video_link.get_attribute('src'))
                time.sleep(3)
        except Exception as e:
            logging.error("Critical Error: {e}")
            
        logging.info("We have got the video links. Now we will save them to a file.")
        counter = 0
        for items in data:
            for item in items['sub-topics']:
                item['uri'] = video_link_list[counter]
                counter += 1
        
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        logging.info('Data saved to data.json')
        
    
   



    

