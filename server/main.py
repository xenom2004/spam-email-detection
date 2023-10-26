from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

import numpy as np
import pandas as pd
import csv
import sklearn
import pickle
import pandas as pd
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV,train_test_split,StratifiedKFold,cross_val_score,learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import nltk

_vectorizer = joblib.load('tfidf_vectorizer.pkl')
loaded_model = joblib.load('multinomialnb_model.pkl')
nltk.download('stopwords')
from nltk.corpus import stopwords
#remove the punctuations and stopwords
import string
def text_process(text):

    text = text.translate(str.maketrans('', '', string.punctuation))
    text = [word for word in text.split() if word.lower() not in stopwords.words('english')]

    return " ".join(text)
def find(x):
    if x == 1:
        return ("Message is SPAM")
    else:
        return ("Message is NOT SPAM")    
def predictR(st,mnb=loaded_model):
  processed= pd.Series(st).apply(text_process)
  z=_vectorizer.transform(processed)
  mnb_predictions = mnb.predict(z)
  return find(mnb_predictions[0])

class Input_Text(BaseModel):
    input_text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def receive_text(item: Input_Text):
    print(predictR(item.input_text))
    return {"message": predictR(item.input_text)}
