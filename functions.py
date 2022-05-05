import requests
import streamlit as st
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
#from spellchecker import SpellChecker
import json

# def get_url():
#     url = st.text_input("URL", "")
#     return url

# def get_html():
#     url=get_url()
#     response = requests.get(url)
#     response
#     response.status_code
#     test_html = response.text
#     print(test_html)
#     return test_html

# #def get_text(my_text):
#     #soup = BeautifulSoup(get_html(), 'html.parser')
#     #return my_text
# soup = BeautifulSoup(get_html(), 'html.parser')

# def clean_text():
#     text = soup.get_text(separator=' ')
#     cleaned_text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
#     return cleaned_text

# def check():
#     dir(SpellChecker)
#     spell=SpellChecker()
#     splitted_text = clean_text().split()
#     print(splitted_text)
#     for word in splitted_text:
#         a=[]
#         if word != spell.correction(word):
#             a.append(spell.correction(word))
#         print(f'{word}:{a}')
#     return check