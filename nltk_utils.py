import nltk
import numpy as np

from nltk.stem.porter import PorterStemmer

nltk.download('punkt')

stemmer = PorterStemmer()
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    #sentence = ["hello","how","are","you"]
    #words=["hi","hello","I","you","bye","thank","cool"] #patterns
    #bag = [  0,    1,    0,   1,    0,    0,      0]
    
    tokenized_sentence= [stem(w) for w in tokenized_sentence]
    
    bag= np.zeros(len(all_words), dtype=np.float32) #zeros for each word
    for idx, w, in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag



# Now you can use 'bag_input' as input to your trained model to predict the intent.

#bag_of_words
#sentence = ["hello","how","are","you"]
#words=["hi","hello","I","you","bye","thank","cool"]
#bag = bag_of_words(sentence,words)
#print(bag)

#stemming of words
#words = ["Organize","organizes","Organizing"]
#stemmed_words = [stem(w) for w in words]
#print(stemmed_words)
#a= "Which items do you sell?"

#tokenizing of words

#a = tokenize(a)
#print(a)
