
# coding: utf-8

# In[1]:


get_ipython().system('pip install --user matplotlib pandas numpy scipy sklearn')


# In[9]:


get_ipython().magic('matplotlib inline')

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import requests
from io import BytesIO

iris_url = 'https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv'
resp = requests.get(iris_url)
print(resp.content)

data = BytesIO(resp.content)


# In[ ]:


import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

data.seek(0) #send program counter to start of file
df = pd.read_csv(data)


# In[42]:


print(df)


# In[44]:


print(df.head())


# In[45]:


print(df.head(10))


# In[46]:


print(df.head()['sepal_length'])


# In[23]:


print(df.iloc[0])


# In[47]:


target = df[df.columns[-1]]
target = target.astype('category')
print(target.head())
# note how it specifies the whole column values


# In[32]:


numeric_data = df._get_numeric_data()
print(numeric_data.head())


# In[35]:


print(target.cat.codes[0:5])
#convert labels literals to numbers (setosa -> 0)


# In[93]:


training_data, testing_data, training_label, testing_label = train_test_split(numeric_data, target.cat.codes)
#train_test_split shuffles the data and selects a subset for testing


# In[61]:


print(len(training_data))
print(training_data.head())
print(training_label.head())


# In[62]:


print(len(testing_data))
print(testing_data.head())
print(testing_label.head())


# In[94]:


tree_model = tree.DecisionTreeClassifier()
tree_model.fit(training_data, training_label)

print(tree_model)


# In[95]:


predict_result = tree_model.predict(testing_data)
score_result = tree_model.predict_proba(testing_data)

print(predict_result[0:5])
print(score_result[0:5])


# In[96]:


matrix = confusion_matrix(testing_label, predict_result)
report = classification_report(testing_label, predict_result, target_names=target.cat.categories)
acc = accuracy_score(testing_label, predict_result)

print(matrix)
print('===')
print(report)
print('===')
print(acc)

#precision -> true to predicted
#recall -> true to actual number


# In[91]:


import itertools
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# In[97]:


# Compute confusion matrix
cnf_matrix = confusion_matrix(testing_label, predict_result)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=target.cat.categories,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=target.cat.categories, normalize=True,
                      title='Normalized confusion matrix')

plt.show()

