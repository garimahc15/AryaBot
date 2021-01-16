#importing necessary libraries
import nltk
import numpy as np
import string
import warnings

warnings.filterwarnings("ignore")
#import the TFidf vectorizer to convert a collection of raw documents to a matrix of TF-IDF features.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#reading the data
f = open('data.txt','r', errors = 'ignore', encoding = 'utf-8')
paragraph = f.read()
#nltk.download('punkt')   # for first-time use only. Punkt is a Sentence Tokenizer
#nltk.download('wordnet')    # for first-time use only. WordNet is a large lexical database of English.
#sent_tokens = nltk.sent_tokenize(paragraph)
word_tokens = nltk.word_tokenize(paragraph)
sent_tokens = paragraph.split("!!\n\n")



#keyword matching for basic greetings for our very own sophisticated bot :)
greetings = ['Hey', 'Hello', 'Hi', "It's great to see you", 'Nice to see you', 'Good to see you']
bye = ['Bye', 'Bye-Bye', 'Goodbye', 'Have a good day']
thank_you = ['Thanks', 'Thank you', 'Thanks a bunch', 'Thanks a lot.', 'Thank you very much', 'Thanks so much', 'Thank you so much']
thank_response = ["You're welcome." , 'No problem.', 'No worries.', ' My pleasure.' , 'It was the least I could do.', 'Glad to help.']


#pre-processing the raw text
# Lemmitization
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]    # iterate through every token and lemmatize it

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))



#generating responses from our data
def response(user_response):
    bot_response = ''

    sent_tokens.append(user_response)   # Appending the Question user ask to sent_tokens to find the Tf-Idf and cosine_similarity between User query and the content.
    TfidfVec = TfidfVectorizer(tokenizer = Normalize, stop_words='english')    #tokenizer ask about Pre-processing parameter and it will consume the Normalize() function and it will also remove StopWords
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)     # It will do cosine_similarity between last vectors and all the vectors because last vector contain the User query
    idx = vals.argsort()[0][-2]     # argsort() will sort the tf_idf in ascending order. [-2] means second last index i.e. index of second highest value after sorting the cosine_similarity. Index of last element is not taken as query is added at end and it will have the cosine_similarity with itself.
    flat = vals.flatten()    # [[0,...,0.89,1]] -> [0,...,0.89,1] this will make a single list of vals which had list inside a list.
    flat.sort()
    req_tfidf = flat[-2]  # this contains tfid value of second highest cosine_similarity
    print("yess = ", req_tfidf)

    if(req_tfidf == 0):    # 0 means there is no similarity between the question and answer
        bot_response = bot_response + """ I am sorry! I don't understand you. Please rephrase your query.\nIf you require any urgent assistance, please contact Lady Garima at 9588727202"""
        return bot_response
    
    else:
        bot_response = bot_response + sent_tokens[idx]    # return the sentences at index -2 as answer
        return bot_response




#deciding responses from bot to user : FINAL
import random
def bot_response(user_msg):
    flag=True
    while(flag==True):
        user_response = user_msg
        user_response = user_response.capitalize().translate(remove_punct_dict)
        if(user_response not in bye):
            if(user_msg == '/start'):
                bot_response = "Hi! I am Arya and I am NOT going home until I answer all your queries regarding IIT Mandi."
                return bot_response
            elif(user_response in thank_you):
                bot_response = random.choice(thank_response)
                return bot_response
            elif(user_response in greetings):
                bot_response = random.choice(greetings) + ", What information do you want related to IIT Mandi?"
                return bot_response
            else:
                user_response = user_response.lower()
                bot_response = response(user_response)
                sent_tokens.remove(user_response)   # remove user question from sent_token that we added in sent_token in response() to find the Tf-Idf and cosine_similarity
                return bot_response
        else:
            flag = False
            bot_response = random.choice(bye)
            return bot_response