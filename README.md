# DataScienceNotes
Just a notebook, nothing more.

## Question Definition 

- Business Understanding
- Issue Conversion
  - Target Definition
  - Population Scoping
  - Main Feature Selection

## Feature Engineering -- Background-based

- Graphic Analysis
- Time Series

## Data Cleaning

- Data Deduplication
  - ``recordlinkage`` ``googletrans``

## Data Loading

- DataFrame
  - ``pandas`` ``dask`` for big data

## Exploratory Data Analysis

- Glimpse
  - ``pandas_profiling``
- Visualization
  - ``plotly``

## Feature Engnineering -- Technique-based

**GossipCat**

- Technicly:
  - Highly correlated: difference, LR, AUC
- Bussiness Sense:
  - Groupby
  - Meaningful: ratio
 
 ## Machine Learning
 
 **GossipCat**
 - Development:
   - Establishment of a machine learning project file system. 
 - Algorithms:
   - ``LightGBM``, ``XGBoost``, ``bayes_opt``
 - Stacking
 - Hyperparameter Tuning:
   - Grid Search
   - Simulated Annealing
   - Bayesian Optimization
 
 ## Model interpretation
 
 **GossipCat**
 
 - LIME: `lime` (`matplotlib==2.1.0` required)
 - SHAP: `shap`
 - Others: `skll`, `skopt`, `eli5`, `graphviz`, `pydotplus`, `xgbfir`, `treeinterpreter`, `pycebox`, `pdpbox`

[Interpretable Machine Learning with Python](http://savvastjortjoglou.com/intrepretable-machine-learning-nfl-combine.html#Feature-Importance)

## Notes:
After almost one year working experience of machine learning project in banking industy, I would like to summary several application advice as following:

1. The problem for you to solve may not be defined. The issues in industry are not always tipical machine learning problems but often appear as consulting issues. You need to communicate with your clients and try to dig out what they want and maybe teach them what they can get from machine learning.
2. The data you got can be dirty. It is, however, a fact so don't waste too much your time complain about the fact. It is what it is. Try to enfront it and solve the problem. That's why they hire you.
3. Generaly, your task is highly related to a engineering problem. Try to learn some skills like Linux OS and big data. 
4. You may not need to spend too much time to machine learning algorithms, like hyperparameter tuning. Try to build a pipeline to apply a general good algorithm, like the gradient boosting decision tree. 
5. Visualization helps you communicate to your clients a lot. Try to sharp your visualization skills. 

Nov 18, 2018
