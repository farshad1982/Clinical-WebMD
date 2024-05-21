from pyquery import PyQuery as pq
from selenium import webdriver
import pandas as pd
import re
import time
import pandas as pd

import openai
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import csv

keyWords = [    
"acetaminophen",
"tramadol" ,
"Methadone", 
"famotidine", 
"diphenhydramine", 
"citalopram" ,
"imipramine" ,
"ibuprofen" ,
"metoclopramide" ,
"glibenclamide" , # Not found
"naltrexone" ,
"amoxicillin" ,
"valproic" ,
"PHENOBARBITAL" ,
"vitamin D" , # Not found
"levothyroxine" ,
"salbutamol" , # Not found
"propranolol"  ,
"digoxin" ,
"diazepam",
"oxycodone"]





def readCSV(file):
    """
    data = pd.read_csv(file)
    q = data["QuestionText"]
    for text in q:
        if keyWords[0] in text:
            print(text)
            print("------------")
    """
    
    for key in keyWords:
        key = key.lower()
        # myFile.write("-++++++++++++++\n")
        # myFile.write("-++++++++++++++\n")
        # myFile.write(key)
        # myFile.write("-********************-\n")
        data = pd.read_csv(file)
        q = data[["QuestionText", "QuestionNo"]]
        res = q[["QuestionText", "QuestionNo"]][q["QuestionText"].str.lower().str.contains(key)]
        res.to_csv("Abuse_filesForGPT/"+key+".csv")
        # for text in res:
            
            # print(text)
            # myFile.write(text+"\n")
            # myFile.write("---------\n")
def main():
   readCSV("Abuse_MedHelp_Question.csv")





# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()
# Define a function for sentiment analysis with 6 labels
def analyze_sentiment(text):
    # Get sentiment scores
    sentiment_scores = analyzer.polarity_scores(text)

    # Define custom label mapping based on compound score
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.5:
        sentiment_label = 'Very Positive'
    elif compound_score >= 0.05:
        sentiment_label = 'Positive'
    elif compound_score <= -0.5:
        sentiment_label = 'Very Negative'
    elif compound_score <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return sentiment_label, sentiment_scores

import os

def sentimentExtraction():
    folder = "/Users/f.toosi/Library/CloudStorage/OneDrive-MunsterTechnologicalUniversity/CIT/CIT/Research/Publications/Alireza/MedHelp/filesForGPT/"
    files = os.listdir(folder)
    overall = open("OverallSenses.txt", 'w')
    for fileName in files:
        data = pd.read_csv(folder+fileName)
        if 'Sentiment' in data.columns:
            overall.write(fileName+"\n--------------\n")
            for cell in data['Sentiment']:
                overall.write(str(cell)+"\n")
                
            input("Continue?")


# sentimentExtraction()



# Example usage
if __name__ == "__main__":
    main()
    




