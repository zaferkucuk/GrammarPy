#from functions import get_html, get_url
import streamlit as st
import requests
import pandas as pd
import numpy as np
import re
import sklearn 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import urllib.request
import language_tool_python
from spellchecker import SpellChecker
import json

st.set_page_config(page_title='Grammar Checker')

##page=st.sidebar.radio("Tabs", tabs)

##if page=="input":
st.markdown("<h1 style='text-align:center;>Check grammar of your website'</h1>", unsafe_allow_html=True)
st.write("""Enter website URL you want to check for grammar recommendations""")

url=st.text_input("URL", "")
# check_url=st.button('Check URL')
# #if check_url==True:
#     #st.write(get_url()) 

tabs=["Extracted Text", "Check Result"]

def get_html():
    #url=get_url()
    full_url='http://'+url
    #print(url)
    #print(full_url)
    response = requests.get(full_url)    
    #response.status_code
    test_html = response.text
    print(test_html)
    return test_html
get_html()


soup = BeautifulSoup(get_html(), 'html.parser')
text = soup.get_text(separator=' ')
cleaned_text2 = re.sub("([-+@#^/|*(){}$~`<>=_])|(\[)|(\])|([0-9])", "", text)
#cleaned_text2 = int(text).replace("\n","", text)
cleaned_text2

# dir(SpellChecker)
# def check():
#     dir(SpellChecker)
#     spell=SpellChecker()
#     #cleaned_text=clean_text()
#     splitted_text = cleaned_text2.split()
#     print(splitted_text)
#     for word in splitted_text:
#         a=[]
#         if word != spell.correction(word):
#             a.append(spell.correction(word))
#             print(f'{word}:{a}')
#     return check
# check()
st.write("Result:")
## language_tool_python
import language_tool_python
test_text="Photo by Gren Chameleon on Unsplash Transfor Learning came as a game changer for all the NLP researchers, so before diving in let’s quickly revisit what transfer learning is. Transfer learning is a machine learning method where a model developed for a task is reused as the starting point for a model on a second task. Simply it leverages prior knowledge from one domain and task into a different domain and task. Luckily for us, we have various such models, which have prior knowledge about the language and its semantics, so we will just use those knowledgeable models and see how they perform on the task we have in handhere checking grammar. "
tool = language_tool_python.LanguageTool('en-US')
corrected_text=tool.correct(cleaned_text2)
#print(corrected_text)
st.write(corrected_text)
