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
st.write("""Enter website URL you want to check for grammar""")

def get_url(url):
    url = st.text_input("URL", "")
    return url

check_url=st.button('Check URL')

