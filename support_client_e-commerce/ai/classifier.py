from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

categories = ["livraison", "remboursement", "produit", "commande", "autre"]

training_data = [
    ("où est ma commande ?", "livraison"),
    ("je veux un remboursement", "remboursement"),
    ("le produit est cassé", "produit"),
    ("je veux modifier ma commande", "commande"),
    ("bonjour j’ai une question", "autre")
]

texts, labels = zip(*training_data)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB().fit(X, labels)

def classify(text):
    return model.predict(vectorizer.transform([text]))[0]