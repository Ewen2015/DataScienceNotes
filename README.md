# Data Sciense Consulting

I generaly work as a data science consultant, which combines the role of data scientist and consultant. Based on my working experience, I established a data science project framework to facilate my daily work. Five aspects are summarized in the framework and can be regarded as a work process to fulfill a data science project; as a result and for esay-memorize, I set it as **One Week Data Science Framework**. 

|Day of Week|Key|Content|
|-----------|---|-------|
|Monday|    Requirement|  Understand the requirements and define your problem.|
|Tuesday|   Solution|     Address a data sciense project solution.|
|Wednesday| Data|         Collect data, explore it, do feature engineering.|
|Thursday|  Algorithm|    Select best machine learning algorithm, build the model, and tune the parameters.|
|Friday|    Presentation| Present your finding, insights. Launch your model.|


## Monday: Requirement 

- Business Understanding
- Design Thinking

## Tuesday: Solution 

- Issue Conversion
  - Target Definition
  - Population Scoping
  - Main Feature Selection

## Wednesday: Data

### Data Processing

- Data Deduplication
  - ``recordlinkage`` ``googletrans``

- DataFrame
  - ``pandas`` ``dask`` for big data

### Exploratory Data Analysis

- Glimpse
  - ``pandas_profiling``
- Visualization
  - ``plotly``

### Feature Engnineering -- Technique-based

**GossipCat**

- Technicly:
  - Highly correlated: difference, LR, AUC
- Bussiness Sense:
  - Groupby
  - Meaningful: ratio
 
 ### Feature Engineering -- Background-based

- Graphic Analysis
- Time Series

 ## Thursday: Algorithm
 
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
 
 ## Friday: Presentation
 
 ### Model interpretation
 
 **GossipCat**
 
 - LIME: `lime` (`matplotlib==2.1.0` required)
 - SHAP: `shap`
 - Others: `skll`, `skopt`, `eli5`, `graphviz`, `pydotplus`, `xgbfir`, `treeinterpreter`, `pycebox`, `pdpbox`

[Interpretable Machine Learning with Python](http://savvastjortjoglou.com/intrepretable-machine-learning-nfl-combine.html#Feature-Importance)

### Launch

- Architectural thinking
- Engineering
- Logging



## Notes:
After almost one year working experience of machine learning project in banking industy, I would like to summary several application advice as following:

1. The problem for you to solve may not be defined. The issues in industry are not always tipical machine learning problems but often appear as consulting issues. You need to communicate with your clients and try to dig out what they want and maybe teach them what they can get from machine learning.
2. The data you got can be dirty. It is, however, a fact so don't waste too much your time complain about the fact. It is what it is. Try to enfront it and solve the problem. That's why they hire you.
3. Generaly, your task is highly related to a engineering problem. Try to learn some skills like Linux OS and big data. 
4. You may not need to spend too much time to machine learning algorithms, like hyperparameter tuning. Try to build a pipeline to apply a general good algorithm, like the gradient boosting decision tree. 
5. Visualization helps you communicate to your clients a lot. Try to sharp your visualization skills. 

Nov 18, 2018
