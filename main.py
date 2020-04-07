from load_data import x_train, x_test, y_train, y_test
from DecisionTreeClassifier import *

# train and test my_classifier
my_classifier = TreeClassifier()
my_classifier.fit(x_train, y_train)
acc = accuracy_score(y_train, my_classifier.pracdict(x_train))


# draw
lst = [Pick(False, 1), Pick(False, 2), Pick(False, 0)]
my_classifier.tree.display(my_classifier, lst)
