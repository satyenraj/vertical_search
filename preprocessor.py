import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("omw-1.4")

nltk.download('stopwords')
nltk.download('punkt')

#preprocess documents or sentences
def preprocess(document):
    stop_words = set(stopwords.words('english'))

    # Remove punctuation
    document_no_punct = document.translate(str.maketrans("", "", string.punctuation))

    #tokenize words in document (sentence)
    tokens = word_tokenize(document.lower())
    
    # Initialize wordnet lemmatizer
    wnl = WordNetLemmatizer()
    words = " ".join(wnl.lemmatize(token, pos="v") for token in tokens if token not in stop_words)

    return words

#generate an inverted index
def inverted_indexer(documents):
    index = {}
    for i, document in enumerate(documents):
        terms = document.split(" ")
        for term in terms:
            if term in index:
                index[term].append(i)
            else:
                index[term] = [i]
    return index


