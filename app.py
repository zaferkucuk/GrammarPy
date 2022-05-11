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

logo_small=Image.open("logo2.png")
st.set_page_config(page_title='GrammarPy', page_icon=logo_small)
hide_st_style="""
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col3:
    from PIL import Image
    image = Image.open('GrammarPy_Logo1.png', )
##page=st.sidebar.radio("Tabs", tabs)
##if page=="input":
    st.image(image, width=160)
#st.markdown("<h1 style='text-align:center;>Check grammar of your website'</h1>", unsafe_allow_html=True)
#st.title("<h1 style='text-align:center;"""Enter website URL you want to check for grammar recommendations"""</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; '>Grammar Checker for Websites</h4>", unsafe_allow_html=True)


url=st.text_input("Enter the web page url (without http://)", "")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7) #I don`t know to place center the button :(
with col4:
    check_url=st.button('   Let`s go!   ')



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
        with col2:
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
        with col3:
           
            #st.write("Result:")
            ## language_tool_python
            
            tool = language_tool_python.LanguageTool('en-US')
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1)
        with col4:
            corrected_text=tool.correct(cleaned_text2)
            #st.write(corrected_text)
                    #progress bar
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1)

##----------------original/corrected/wrong words----------------##
        #st.write("Misspelled words:")
        words_original = cleaned_text2.split()
        #st.write(words_original)
        #st.write("words_corrected")
        words_corrected = corrected_text.split()
        #st.write(words_corrected)

        wrong_words=[]
        for word in words_original:
            if word not in words_corrected:
                wrong_words.append(word)
            else:
                pass
        #st.write(wrong_words)
##----------------original/corrected/wrong words----------------##


##-----------------split sentences------------------------------##
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

        wrong_sentences=[]
        for word in splitted_sentences_original:
            if word not in splitted_sentences_corrected:
                wrong_sentences.append(word)
        #wrong_sentences  


##---------------------split words------------------------------##
        original_words = cleaned_text2.split()
        corrected_words = corrected_text.split()

        wordle = pd.DataFrame(corrected_words)
        wordle.to_csv('file2.csv', index=False, header=False)
        #original_words.to_csv('C:/Users\Guest1\Projects\grammar_checker\wordle_words\"wordle".csv')
        #st.download_button('send words', original_words, 'wordle/csv')

##-------------highlighted sentences/words----------------------##
        #st.write("try")
        list_of_words=[]
        for word in original_words:
            #print(word)
            if word not in corrected_words:
                #print(word)
                list_of_words.append((word, "#afa"))
            else:
                list_of_words.append(word)
        #st.write("this one")
        #for word in list_of_words:
            #annotated_text(word)
        
        underlined_sentence=[]
        for sentence in splitted_sentences_original:
            if sentence not in splitted_sentences_corrected:
                underlined_sentence.append((sentence," ", "#afa"))
            else:
                underlined_sentence.append(sentence)

        underlined_words=[]
        for word in words_original:
            if word not in words_corrected:
                underlined_words.append((word, "#afa"))
            else:
                underlined_words.append(word)
        underlined_sentence2=[]

        #underlined_sentence2=[]
        for sentence in splitted_sentences_original:
            if sentence not in splitted_sentences_corrected:
                #print(sentence)
                underlined_words2=[]
                for word in sentence.split():
                    #print(word)
                    if word not in words_corrected:
                        #print(word)
                        underlined_words2.append((word, "#8ef"))
                        #print(underlined_words2)
                underlined_sentence2.extend((sentence, underlined_words2))
            else:
                underlined_sentence2.append(sentence)

        # with st.echo():
        #     for sentence in underlined_sentence2:
        #         annotated_text(sentence)
        # for word in underlined_words:
        #     annotated_text(word)

        # for sentence in underlined_sentence2:
        #     annotated_text(sentence)
##-------------Carmine----------------------##
        def colour_to_word(word, color='black'):
            return f"<text style=color:{color}>{word}</text>"

        #corrected_words = ['ciao','hello']
        #text = "cia hallo ciao hello"
        text_to_annotated_list = []
        for word in cleaned_text2.split():
            if word not in words_corrected:
                text_to_annotated_list.append(colour_to_word(word,color='red'))
            else:
                text_to_annotated_list.append(word)

        #print(text_to_annotated_list)


        text_to_annoted = " ".join(text_to_annotated_list)
        #print(text_to_annoted)
##------------------------pages------------------------------##
        # from streamlit_option_menu import option_menu
        # selected = option_menu(
        #     menu_title=None,  # required
        #     options=["Original", "Corrected", "Download"],  # required
        #     icons=["house", "book", "envelope"],  # optional
        #     menu_icon="cast",  # optional
        #     default_index=0,  # optional
        #     orientation="horizontal",
        #     styles={
        #         "container": {"padding": "0!important", "background-color": "#FFFFFF"},
        #         "icon": {"color": "#EDDABE", "font-size": "25px"},
        #         "nav-link": {
        #             #"font-size": "25px",
        #             "text-align": "center",
        #             "margin": "0px",
        #             "--hover-color": "#fafafa",
        #         },
        #         "nav-link-selected": {"background-color": "#fafafa"},
        #     },
        # )



        
        # page_names=['Sentences','Words']
        # page=st.radio('Result', page_names)
        # if page is "Sentences":
        #     for sentence in underlined_sentence:
        #         annotated_text(sentence)
        # if page is "Words":
        #     st.markdown(text_to_annoted,unsafe_allow_html=True )
##-------------------original/corrected texts-------------------##
        # with st.expander("See original content"):
        #     st.write(cleaned_text2)
        with st.expander("See original content"):
            for sentence in underlined_sentence:
                annotated_text(sentence)
        with st.expander("See the wrong words"):
            st.markdown(text_to_annoted,unsafe_allow_html=True )
        with st.expander("See corrected content"):
            st.write(corrected_text)
##-------------------download-------------------##
        st.write("Download files")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button('Original Text', cleaned_text2, 'original_text/txt')
        with col2:
            st.download_button('Corrected Text', cleaned_text2, 'corrected_text/txt')
##-------------------original/corrected texts-------------------##





# with st_stdout("code"):
#     print(underlined_text)
#st.write(underlined_text)
# output = st.empty()
# with st_capture(output.code):
#     print(underlined_text)

# for word in original_words:
#     mistaken_words=[]
#     if word not in corrected_words:
#         mistaken_words.append(word)        
    #mistaken_words = list(filter(None, mistaken_words))
    #mistaken_words = [s for s in mistaken_words if not mistaken_words == '']
#mistaken_words
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
#     annotated_text(wrong_sentences, "#8ef")




# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')

 

#with st.echo():[wrong_sentences, "#faa"]
    




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