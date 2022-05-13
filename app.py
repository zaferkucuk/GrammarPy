from tkinter import UNDERLINE
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import language_tool_python
from spellchecker import SpellChecker
import time
from annotated_text import annotated_text, annotation
from PIL import Image

##--------------------------page setup------------------------------##

logo_small=Image.open("logo2.png")
st.set_page_config(page_title='GrammarPy', page_icon=logo_small)
hide_st_style="""
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
col1, col2, col3, col4, col5= st.columns(5)
with col3:
    from PIL import Image
    image = Image.open('GrammarPy_Logo1.png', )
    st.image(image, width=160)
#st.markdown("<h1 style='text-align:center;>Check grammar of your website'</h1>", unsafe_allow_html=True)
#st.title("<h1 style='text-align:center;"""Enter website URL you want to check for grammar recommendations"""</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; '>Grammar Checker for Websites</h4>", unsafe_allow_html=True)

url=st.text_input("", "")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7) #I don`t know to place center the button :(
with col4:
    check_url=st.button('   Let`s go!   ')

##---------------------------------scraping------------------------------##
if check_url==True:
    with st.spinner('Data is analyzing...'):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            def get_html():
                response = requests.get(url)    
                test_html = response.text
                print(test_html)
                return test_html
            get_html()
            
##--------------------------clean text data------------------------------##
        with col2:
            soup = BeautifulSoup(get_html(), 'html.parser')
            text = soup.get_text(separator=' ')
            cleaned_text2 = re.sub("([+#^/|*(){}$~`<>=_])|(\[)|(\])", "", text)

##--------------------------recommendations------------------------------##
        with col3:
            tool = language_tool_python.LanguageTool('en-US')
        with col4:
            corrected_text=tool.correct(cleaned_text2)

##----------------original/corrected/wrong words----------------##
        words_original = cleaned_text2.split()
        words_corrected = corrected_text.split()

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

##---------------------split words------------------------------##
        original_words = cleaned_text2.split()
        corrected_words = corrected_text.split()

##-------------find highlighted sentences/words----------------------##
        
        highlighted_sentence=[]
        for sentence in splitted_sentences_original:
            if sentence not in splitted_sentences_corrected:
                highlighted_sentence.append((sentence," ", "#ffa088"))
            else:
                highlighted_sentence.append(sentence)


        

        def colour_to_word(word, color='black'):
            return f"<text style=color:{color}>{word}</text>"
        wrong_words = []
        for word in cleaned_text2.split():
            if word not in words_corrected:
                wrong_words.append(colour_to_word(word,color='red'))
            else:
                wrong_words.append(word)
        underlined_words = " ".join(wrong_words)

##-------------------original/corrected texts-------------------##
        # with st.expander("See original content"):
        #     st.write(cleaned_text2)
        with st.expander("See original content"):
            for sentence in highlighted_sentence:
                annotated_text(sentence)
        with st.expander("See the possible mistakes"):
            st.markdown(underlined_words,unsafe_allow_html=True )
        with st.expander("See corrected content"):
            st.write(corrected_text)

##------------------------download buttons------------------------------##
        st.write("Download files")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button('Original Text', cleaned_text2, 'original_text/txt')
        with col2:
            st.download_button('Corrected Text', corrected_text, 'corrected_text/txt')
        time.sleep(5)
    #st.success('Done!')
##-------------------end of the code-------------------##

##----following code gives a random word from given URL for wordle game-------##
##----wordle game removed from this project(it requires a wordle.py file)-------##

#wordle = pd.DataFrame(corrected_words)
#wordle.to_csv('word_list.csv', index=False, header=False)
#st.write(corrected_words)
#df=pd.read_csv("word_list.csv", header=None)
#corrected_words=df[0].values
#print(df)
#print(corrected_words)
# word_list_short=[]
# for i in corrected_words:
#     if len(i)==5:
#         word_list_short.append(i)
#     else:
#         pass
#print(word_list_short)
#my_word=random.choice(word_list_short)
#print(my_word)
#exit()

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


## ---------------------alternative way to find corrected words-------------------------##
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

## ---------------------alternative way to find wrong words-------------------------##
        # wrong_words=[]
        # for word in original_words:
        #     #print(word)
        #     if word not in corrected_words:
        #         #print(word)
        #         wrong_words.append((word, "#afa"))
        #     else:
        #         wrong_words.append(word)

## ---------------------alternative way to find wrong sentences-------------------------##
        # wrong_sentences=[]
        # for word in splitted_sentences_original:
        #     if word not in splitted_sentences_corrected:
        #         wrong_sentences.append(word)
        # #wrong_sentences  

##------------display underlined words and highlighted sentences together----------##
        # underlined_sentence2=[]
        # for sentence in splitted_sentences_original:
        #     if sentence not in splitted_sentences_corrected:
        #         #print(sentence)
        #         underlined_words2=[]
        #         for word in sentence.split():
        #             #print(word)
        #             if word not in words_corrected:
        #                 #print(word)
        #                 underlined_words2.append((word, "#8ef"))
        #                 #print(underlined_words2)
        #         underlined_sentence2.extend((sentence, underlined_words2))
        #     else:
        #         underlined_sentence2.append(sentence)
##------------display underlined words and highlighted sentences together----------##

        # with st.echo():
        #     for sentence in underlined_sentence2:
        #         annotated_text(sentence)
        # for word in underlined_words:
        #     annotated_text(word)
        # for sentence in underlined_sentence2:
        #     annotated_text(sentence)
##------------------highlighted words--------------------------##

        # underlined_words=[]
        # for word in words_original:
        #     if word not in words_corrected:
        #         underlined_words.append((word, "#afa"))
        #     else:
        #         underlined_words.append(word)