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

def get_url(url):
    return url

def get_text(page_text):
    return page_text

def clean_text(cleaned_text):
    return cleaned_text

def check_words(words):
    return words

def check_grammar(grammar):
    return grammar