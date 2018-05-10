from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer



def MakeModel(questions, answers, labels):
    labels = labels
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(questions)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, answers)
    return [clf, labels, count_vect, tfidf_transformer]

def TestModel(model, questions, answers):
    clf = model[0]
    count_vect = model[2]
    tfidf_transformer = model[3]
    docs_new = questions
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    import numpy as np
    predicted = clf.predict(X_new_tfidf)
    my_guessed = []
    theguessee = []
    labels = model[1]
    predictions = []
    right = 0
    for doc, category, thing in zip(docs_new, predicted, answers):
        my_guessed.append(labels[category])
        predictions.append(labels[thing])
        theguessee.append(doc)
        if category == thing:
            right += 1
    return {"plain_text":docs_new,
            "guess":list(map(lambda x: labels[x], predicted)),
            "answer":list(map(lambda x: labels[x], answers)),
            "percent": (right/len(answers)) }







