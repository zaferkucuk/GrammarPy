#from functions import get_html, get_url
from tkinter import UNDERLINE
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
import time
from annotated_text import annotated_text, annotation
from PIL import Image

#------print-------#



#------print-------#
logo_small=Image.open("logo2.png")
st.set_page_config(page_title='GrammarPy', page_icon=logo_small)

##page=st.sidebar.radio("Tabs", tabs)

##if page=="input":
from PIL import Image
image = Image.open('GrammarPy_Logo1.png')

st.image(image, width=160)
st.markdown("<h1 style='text-align:center;>Check grammar of your website'</h1>", unsafe_allow_html=True)
st.write("""Enter website URL you want to check for grammar recommendations""")



url=st.text_input("URL", "")
check_url=st.button('Check Grammar')
if check_url==True:
         
        col1, col2, col3, col4 = st.columns(4)
        with col1:
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
            #progress bar
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1)

        soup = BeautifulSoup(get_html(), 'html.parser')
        text = soup.get_text(separator=' ')
        cleaned_text2 = re.sub("([+#^/|*(){}$~`<>=_])|(\[)|(\])", "", text)
        #cleaned_text2 = re.sub("([-+@#^/|*(){}$~`<>=_])|(\[)|(\])|([0-9])", "", text)
        #cleaned_text2 = int(text).replace("\n","", text)
        #cleaned_text2
                #progress bar
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        ##---------original/corrected sentences-------##
        #st.write("Result:")
        ## language_tool_python
        import language_tool_python
        tool = language_tool_python.LanguageTool('en-US')
        corrected_text=tool.correct(cleaned_text2)
        #st.write(corrected_text)
                #progress bar
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        with st.expander("See original text"):
            st.write(cleaned_text2)
        st.download_button('Download original text', cleaned_text2, 'text/csv')
        with st.expander("See corrected text"):
            st.write(corrected_text)
        st.download_button('Download corrected text', cleaned_text2, 'text/csv')
        ##---------original/corrected sentences-------##

        
        #st.write("Misspelled words:")
        words_original = cleaned_text2.split()
        st.write(words_original)

        words_corrected = corrected_text.split()
        st.write(words_corrected)

        wrong_words=[]
        for word in words_original:
            if word not in words_corrected:
                wrong_words.append(word)
            else:
                pass
        st.write(wrong_words)
        


##-------split sentences-----##
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences
splitted_sentences_original=split_into_sentences(cleaned_text2)
#splitted_sentences_original

splitted_sentences_corrected=split_into_sentences(corrected_text)
#splitted_sentences_corrected

false_words=[]
for word in splitted_sentences_original:
    if word not in splitted_sentences_corrected:
        false_words.append(word)
false_words  

original_words = cleaned_text2.split()
corrected_words = corrected_text.split()

wordle = pd.DataFrame(corrected_words)
wordle.to_csv('file2.csv', index=False, header=False)
#original_words.to_csv('C:/Users\Guest1\Projects\grammar_checker\wordle_words\"wordle".csv')
#st.download_button('send words', original_words, 'wordle/csv')

st.write("try")
underlined_sentence=[]
for sentence in splitted_sentences_original:
    if sentence not in splitted_sentences_corrected:
        underlined_sentence.append((sentence, "#8ef"))
    else:
         underlined_sentence.append(sentence)

underlined_words=[]
for word in words_original:
    if word not in words_corrected:
        underlined_words.append((word, "#afa"))
    else:
         underlined_words.append(word)

underlined_sentence2=[]

# for sentence in splitted_sentences_original:
#     if sentence not in splitted_sentences_corrected:
#         underlined_words2=[]
#         for i in sentence:
#             if i not in words_corrected:
#                 underlined_words2.append((i, "#afa"))
#             underlined_sentence2.extend((sentence, underlined_words2))
#     else:
#          underlined_sentence2.append(sentence)

with st.echo():
    for sentence in underlined_sentence2:
        annotated_text(sentence)


with st.echo():
    for sentence in underlined_sentence:
        annotated_text(sentence)

with st.echo():
    for word in underlined_words:
        annotated_text(word)



# with st_stdout("code"):
#     print(underlined_text)
#st.write(underlined_text)
# output = st.empty()
# with st_capture(output.code):
#     print(underlined_text)

for word in original_words:
    mistaken_words=[]
    if word not in corrected_words:
        mistaken_words.append(word)        
    #mistaken_words = list(filter(None, mistaken_words))
    #mistaken_words = [s for s in mistaken_words if not mistaken_words == '']
mistaken_words
    # for i in mistaken_words:
    #     if i == '':
    #         mistaken_words.remove(i)
    # st.write(mistaken_words)



# with st.echo():
#     annotated_text(
#         "This ",
#         ("is", "verb", "#8ef"),
#         " some ",
#         ("annotated", "adj", "#faa"),
#         ("text", "noun", "#afa"),
#         " for those of ",
#         ("you", "pronoun", "#fea"),
#         " who ",
#         ("like", "verb", "#8ef"),
#         " this sort of ",
#         ("thing", "noun", "#afa"),
#         "."
#     )


#st.write("find differences")

# splitted sentences
# for word in splitted_text_corrected:
#     corrected_word=[]
#     if word != splitted_text_original(word):
#         corrected_word.append(word)
#     print(f'{word}:{corrected_word}')
#st.write("sentences")




# with st.echo():
#     annotated_text(false_words, "#8ef")




# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')

 

#with st.echo():[false_words, "#faa"]
    




# st.write('---------')





# st.write('---------')


## ----------------------------------------------
# create red underline for the misspelled words:
# def findErrors(dictionaryWords, cleaned_text2):
#     misspelledWords=[]
#     for word in cleaned_text2:
#         if word not in dictionaryWords:
#             misspelledWords.append(word)
#     return misspelledWords
## ----------------------------------------------

#tabs=["Extracted Text", "Check Result"]




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