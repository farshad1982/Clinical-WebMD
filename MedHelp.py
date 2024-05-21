from pyquery import PyQuery as pq
from selenium import webdriver
import pandas as pd
import re
import time


def tweet_scroller(url):
    driver = webdriver.Chrome()
    driver.get(url)
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        #driver.execute_script("window.scrollTo(0, 1)")

        time.sleep(3)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        print(newHeight , lastHeight)
        
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight
        
    html = driver.page_source
    
    
    
    
    return html

# Get a list of issues


def get_list():
    url = 'https://medhelp.org/forums/Bipolar-Disorder/show/160'
    html = tweet_scroller(url)
    doc = pq(html)
    items = doc('.subj_entry .subj_header .subj_info .subj_title').items()
    QuestionList = []
    i = 1
    for item in items:
        q = {
            'Number': 'Q'+str(i),
            'Link': item.find('a').attr('href'),
            'Question': item.find('a').text()}
        QuestionList.append(q)
        i = i+1
    print(type(QuestionList), len(QuestionList))
    return QuestionList

# Get detailed information corresponding to each question


def get_content(QuestionList):
    headers = {
        'Referer': 'https://medhelp.org/forums/Bipolar-Disorder/show/160',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }
    
    urls = 'https://www.medhelp.org'+str(QuestionList['Link'])
    doc = pq(url=urls, headers=headers)
    #print(doc)
    # Organize questions into dictionary format
    q1 = {'QuestionNo': QuestionList['Number'],
          'QuestionTitle': doc('h1').text(),
          'QuestionTime': doc('.mh_timestamp').attr('datetime'),
          'QuestionText': doc('#subject_msg').text()}
          #'QuestionResponse': re.findall(r'\d+', doc('#read_responses').text())[0]}
    # Extract the answer to the question
    items = doc('.mh_vit_resp_ctn').items()
    a1 = []
    i = 1
    for item in items:
        product1 = {
            'AnswerNo': QuestionList['Number']+'-A'+str(i),  # AnswerNumber
            'AnswerName': item.find('.username').text(),  # AnswerName
            'AnswerTime': item.find('time').attr('datetime'),  # AnswerTime
            'AnswerText': item.find('.resp_body').text()}  # AnswerText
        a1.append(product1)
        i = i+1
    return q1, a1


def save_file(Data, FileName):
    df = pd.DataFrame(Data)
    df.to_csv(FileName, index=[])


def main():
    QuestionList = get_list()
    Question = []
    Answer = []
    for i in QuestionList[0:]:
        
        q1, a1 = get_content(i)
        Question.append(q1)
        if a1:
            Answer.extend(a1)
    save_file(Question, 'Bipolar_MedHelp_Question.csv')
    save_file(Answer, 'Bipolar_MedHelp_Answer.csv')








if __name__ == "__main__":
    main()
