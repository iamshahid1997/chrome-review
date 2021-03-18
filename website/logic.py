import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import string
from nltk.corpus import stopwords

def incorrect_reviews_df_from_doc(doc):
  classifier = pickle.load(open('website/model.pkl','rb'))
  ##vectorizer = pickle.load(open('website/transform.pkl','rb'))
  df = pd.read_csv(doc)
  df.drop(['Developer Reply','Version'],inplace = True,axis = 1)
  df.dropna(inplace = True)

  def message_cleaning(message):
    Test_punc_removed = [ char for char in message if char not in string.punctuation]
    Test_punc_removed_join = ''.join(Test_punc_removed)
    all_stopwords = stopwords.words('english')
    not_stopwords = {'not', 'no','nor', 'but', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'don', "don't",} 
    final_stop_words = set([word for word in all_stopwords if word not in not_stopwords])
    Test_punc_removed_join_clean = [ word  for word in Test_punc_removed_join.split() if word.lower() not in final_stop_words]
    return Test_punc_removed_join_clean

  chrome_df_1 = df[df['Star'] == 1]
  chrome_df_5 = df[df['Star'] == 5]
  chrome_df_1_5 = pd.concat([chrome_df_1,chrome_df_5])

  vectorizer = CountVectorizer(analyzer= message_cleaning)
  chrome_count_vectorizer = vectorizer.fit_transform(chrome_df_1_5['Text'])

  data_pred = classifier.predict(chrome_count_vectorizer)
  chrome_df_1_5['predicted'] = data_pred

  final = chrome_df_1_5[chrome_df_1_5['Star'] != chrome_df_1_5['predicted']]


  return final
