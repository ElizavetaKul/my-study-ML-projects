# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ta1Pgy11xCcIcnvf9s7KxZ-klIBMDNCB

ЗАДАНИЕ

- Выберите набор данных для задачи обучения с учителем.
- Разбейте набор данных на тренировочную и тестовую части.
- Постройте график зависимости точности на тестовой и тренировочной части в зависимости от максимальной высоты дерева.
- Не фиксируя высоту дерева поочерёдно перебирайте другие числовые гиперпараметры. Выясните, например построив график, от какого параметра напрямую зависит высота дерева, а от какого зависимость обратная.
- Постройте график зависимости точности Случайного леса на тестовой и тренировочной части в зависимости от числа деревьев в нём.
- Постройте график зависимости точности Бустинга на тестовой и тренировочной части в зависимости от числа деревьев в нём.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Импортируем датасет 
data = pd.read_csv('/content/diabetes_prediction_dataset.csv')

# Уберем колонку с target переменной diabetes
data_X = data.iloc[:, 0:-1]

# В данные есть два категориальных признака
data_X['gender'].value_counts()
data_X['smoking_history'].value_counts()

# С помощью One hot encoding преобразуем категориальные признаки
from sklearn.preprocessing import OneHotEncoder
data_X['gender'] = data_X['gender'].astype('category').cat.codes
data_X['smoking_history'] = data_X['smoking_history'].astype('category').cat.codes

enc = OneHotEncoder()
enc_data = pd.DataFrame(enc.fit_transform(
    data_X[['gender', 'smoking_history']]).toarray())
enc_data.columns = enc.get_feature_names_out()

X = data_X.join(enc_data)
X = X.drop(columns=['gender', 'smoking_history'])

y = data['diabetes']

# Разобьем выборку на train и test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=13)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

# Построим дерево с базовыми параметрами
from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(random_state=13)
dt.fit(X_train, y_train)

# Посчитаем accuracy score
from sklearn.metrics import accuracy_score
accuracy_score(y_test, dt.predict(X_test))

# Глубина получившегося дерева = 36
print('Tree depth = ', dt.get_depth())
print('Number of leaves = ', dt.get_n_leaves())

# Посмотрим, какие признаки оказались наиболее важными
pd.DataFrame({
    'feature': X.columns,
    'importance': dt.feature_importances_
}).sort_values(by='importance', ascending=False).reset_index(drop=True)

# Посмотрим зависимость точности от максимальной высоты дерева на тренировочной выборке
max_depth_array = range(2, 40)
acc_array = []

for max_depth in max_depth_array:
    dt = DecisionTreeClassifier(max_depth=max_depth, random_state=13)
    dt.fit(X_train, y_train)
    acc_array.append(accuracy_score(y_train, dt.predict(X_train)))
plt.plot(max_depth_array, acc_array)
plt.title('Dependence of accuracy on max depth (on X_train)')
plt.xlabel('max depth')
plt.ylabel('accuracy')
plt.show()

# Посмотрим зависимость точности от максимальной высоты дерева на тестовой выборке
max_depth_array = range(2, 40)
acc_array = []

for max_depth in max_depth_array:
    dt = DecisionTreeClassifier(max_depth=max_depth, random_state=13)
    dt.fit(X_train, y_train)
    acc_array.append(accuracy_score(y_test, dt.predict(X_test)))
plt.plot(max_depth_array, acc_array)
plt.title('Dependence of accuracy on max depth (on X_test)')
plt.xlabel('max depth')
plt.ylabel('accuracy')
plt.show()

# Чем больше глубина дерева, тем лучше классифицируются объекты в тренировочной выборке, точность растет,
# но дерево сильно переобучается, подстраиваясь под тренировочные данные,
# поэтому на тестовой выборке при высоких значениях глубины точность падает.

# Зависимость точности от глубины дерева в числовых значениях
pd.DataFrame({
    'max_depth': max_depth_array,
    'accuracy': acc_array
}).sort_values(by='accuracy', ascending=False).reset_index(drop=True)

# Переберем значения min_samples_split и визуализируем зависимость глубины дерева от min_samples_split
min_samples_split_array = range(2, 20)
tree_depth_min_samples = []

for min_samples_split in min_samples_split_array:
    dt = DecisionTreeClassifier(min_samples_split=min_samples_split, random_state=13)
    dt.fit(X_train, y_train)
    tree_depth_min_samples.append(dt.get_depth())

plt.plot(min_samples_split_array, tree_depth_min_samples)
plt.title('Dependence of tree depth on min_samples_split')
plt.xlabel('min_samples_split')
plt.ylabel('tree_depth')
plt.show()

# Зависимость обратная: чем ниже минимальный порог для количества объектов в вершине, тем глубже получается дерево.

# Переберем значения min_samples_leaf
min_samples_leaf_array = range(1, 20)
tree_depth_min_sam_leaf = []

for min_samples_leaf in min_samples_leaf_array:
    dt = DecisionTreeClassifier(min_samples_leaf=min_samples_leaf, random_state=13)
    dt.fit(X_train, y_train)
    tree_depth_min_sam_leaf.append(dt.get_depth())
plt.plot(min_samples_leaf_array, tree_depth_min_sam_leaf)
plt.title('Dependence of tree depth on min_samples_leaf')
plt.xlabel('min_samples_leaf')
plt.ylabel('tree_depth')
plt.show()

# Зависимость обратная: чем ниже число объектов для листовой вершины, тем более глубоким получается дерево.

# Переберем значения max_features (всего признаков: 15)
max_features_array = range(1, 16)
tree_depth_max_features = []

for max_features in max_features_array:
    dt = DecisionTreeClassifier(max_features=max_features, random_state=13)
    dt.fit(X_train, y_train)
    tree_depth_max_features.append(dt.get_depth())
plt.plot(max_features_array, tree_depth_max_features)
plt.title('Dependence of tree depth on max number of features')
plt.xlabel('max_features')
plt.ylabel('tree_depth')
plt.show()

# Переберем значения max_leaf_nodes
max_leaf_nodes_array = [10, 100, 1000, 2000, 3000, 3400]
tree_depth_max_l_nodes = []

for max_leaf_nodes in max_leaf_nodes_array:
    dt = DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes, random_state=13)
    dt.fit(X_train, y_train)
    tree_depth_max_l_nodes.append(dt.get_depth())
plt.plot(max_leaf_nodes_array, tree_depth_max_l_nodes)
plt.title('Dependence of tree depth on max_leaf_nodes')
plt.xlabel('max_leaf_nodes')
plt.ylabel('tree_depth')
plt.show()

# Зависимость прямая: чем больше число листьев, тем глубже дерево.

# Random forest
# Зависимость точности от числа деревьев на тренировочной выборке

from sklearn.ensemble import RandomForestClassifier

n_estimators_list = range(5, 200, 10)
acc_score = []

for n_estimators in n_estimators_list:
    rfc = RandomForestClassifier(n_estimators=n_estimators, random_state=0)
    rfc.fit(X_train, y_train)
    acc_score.append(accuracy_score(y_train, rfc.predict(X_train)))

plt.plot(n_estimators_list, acc_score)
plt.title('Dependence of accuracy on n_estimators (on X_train)')
plt.xlabel('n_estimators')
plt.ylabel('acc_score')
plt.show()

# Зависимость точности от числа деревьев на тестовой выборке
n_estimators_list = range(5, 200, 10)
acc_score = []

for n_estimators in n_estimators_list:
    rfc = RandomForestClassifier(n_estimators=n_estimators, random_state=1)
    rfc.fit(X_train, y_train)
    acc_score.append(accuracy_score(y_test, rfc.predict(X_test)))

plt.plot(n_estimators_list, acc_score)
plt.title('Dependence of accuracy on n_estimators (on X_test)')
plt.xlabel('n_estimators')
plt.ylabel('acc_score')
plt.show()

results = pd.DataFrame({
    'n_estimators': n_estimators_list,
    'accuracy': acc_score
}).sort_values(by='accuracy', ascending=False).reset_index(drop=True)

print(f'Best number of estimators for RandomForestClassifier is {results.iloc[0, 0]}\n', \
      f'Best accuracy score is {results.iloc[0, 1]}')

# GradientBoostingClassifier
# Зависимость точности от числа деревьев на тренировочной выборке
from sklearn.ensemble import GradientBoostingClassifier

n_estimators_list = range(5, 200, 10)
acc_score = []

for n_estimators in n_estimators_list:
    gbc = GradientBoostingClassifier(n_estimators=n_estimators, random_state = 13)
    gbc.fit(X_train, y_train)
    acc_score.append(accuracy_score(y_train, gbc.predict(X_train)))

plt.plot(n_estimators_list, acc_score)
plt.title('Dependence of accuracy on n_estimators (on X_train)')
plt.xlabel('n_estimators')
plt.ylabel('acc_score')
plt.show()

# Зависимость точности от числа деревьев на тестовой выборке
n_estimators_list = range(5, 200, 10)
acc_score = []

for n_estimators in n_estimators_list:
    gbc = GradientBoostingClassifier(n_estimators=n_estimators, random_state = 13)
    gbc.fit(X_train, y_train)
    acc_score.append(accuracy_score(y_test, gbc.predict(X_test)))

plt.plot(n_estimators_list, acc_score)
plt.title('Dependence of accuracy on n_estimators (on X_test)')
plt.xlabel('n_estimators')
plt.ylabel('acc_score')
plt.show()

# В бустинге увеличение количества деревьев не обязательно ведет к повышению точности

results = pd.DataFrame({
    'n_estimators': n_estimators_list,
    'accuracy': acc_score
}).sort_values(by='accuracy', ascending=False).reset_index(drop=True)

print(f'Best number of estimators for GradientBoostingClassifier is {results.iloc[0, 0]}\n', \
      f'Best accuracy score is {results.iloc[0, 1]}')

# CatBoost
!pip install catboost

from catboost import CatBoostClassifier

iterations_list = range(10, 300, 50)
acc_score = []

for iterations in iterations_list:
  cat_clf = CatBoostClassifier(iterations=iterations, logging_level='Silent')
  cat_clf.fit(X_train, y_train)
  acc_score.append(accuracy_score(y_test, cat_clf.predict(X_test)))

plt.plot(iterations_list, acc_score)
plt.title('Dependence of accuracy on number of trees (on X_test)')
plt.xlabel('iterations')
plt.ylabel('acc_score')
plt.show()

results = pd.DataFrame({
    'num_iterations': iterations_list,
    'accuracy': acc_score
}).sort_values(by='accuracy', ascending=False).reset_index(drop=True)

print(f'Best number of iterations for CatBoostClassifier is {results.iloc[0, 0]}\n', \
      f'Best accuracy score is {results.iloc[0, 1]}')

"""С небольшим отличием наибольшая точность при изменении числа деревьев получилась при использовании GradientBoostingClassifier (accuracy = 0.97256), число деревьев - 65."""