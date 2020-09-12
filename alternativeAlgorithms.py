from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

def vectorizer(data: list) -> list:
    """ Vectorize by some kind of hash (that I don't really know)
    """
    vectorizer = HashingVectorizer()
    vectorized_samples = vectorizer.fit_transform(data).toarray()
    return(vectorized_samples)

def RF(X: list, y: list):
    clf = RandomForestClassifier(n_estimators = 100, warm_start=True) # add verbose = 3 flag to see process
    clf.fit(X, y)
    return(clf)

def SVM(X: list, y: list):
    """ Support Vector Machine \n
    Input is array of samples (A list of Tweets) and a list of tags. Ex: [0, 1, 1, 0, 1]
    """

    clf = svm.SVC(gamma = "scale") # could probs reseach more about the "gamma" flag 
    clf.fit(X, y) 
    return(clf)

def KNN(X: list, y: list):
    clf = KNeighborsClassifier()
    clf.fit(X, y)
    return(clf)