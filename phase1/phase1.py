import pandas as pd
import pickle 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report



# Loading Dataset
df = pd.read_csv("spam.csv", encoding='latin-1')
df = df[['v1', 'v2']]
df.columns = ['label', 'message']
df['label'] =  df['label'].map({'ham':0, 'spam': 1})

# Spliting Data
X_train , X_test , Y_train , Y_test = train_test_split(df['message'], df['label'], test_size=0.2 , random_state= 42)

# TF-IDF Vectorizer

vectorizer = TfidfVectorizer(
    stop_words = None,
    ngram_range= (1,2)
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

#model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, Y_train)
probs = model.predict_proba(X_test_vec)
spam_probs = probs[:,1]
threshold = 0.7
y_pred = (spam_probs > threshold).astype(int)
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Accuracy:", accuracy_score(Y_test, y_pred))
print("\nReport:\n", classification_report(Y_test, y_pred))

while True:
    msg = input("\nEnter SMS (or type 'exit'): ")
    if msg.lower() == 'exit':
        break

    msg_vec = vectorizer.transform([msg])
    result = model.predict_proba(msg_vec)[0][1]

    if result > 0.3:
        print("🚨 Spam detected")

    elif result > 0.3:
        print("Suspecious Message")
    else:
        print("✅ Not spam")