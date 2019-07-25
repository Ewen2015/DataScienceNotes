# Data Sciense Consulting

I generaly work as a data science consultant, which combines roles of the data scientist and the consultant in IBM. 

As a data scientist, I focus on the machine learning (including deep learning), knowledge graph, and the intersection of them. Based on my working experience, I established a data science project framework to facilate my daily work. Five aspects are summarized in the framework and can be regarded as a work process to fulfill a data science project; as a result and for esay-memorize, I set it as **One Week Data Science Framework**. 

|Day of Week|Key|Content|
|-----------|---|-------|
|Monday|    Requirement|  Understand the requirements and define your problem.|
|Tuesday|   Solution|     Address a data sciense project solution.|
|Wednesday| Data|         Collect data, explore it, do feature engineering.|
|Thursday|  Algorithm|    Select best machine learning algorithm, build the model, and tune the parameters.|
|Friday|    Presentation| Present your finding, insights. Launch your model.|


## Weekends: Preparation

### Hard skills

- Mathematics, statistics
- Machine learning
- Python
- Linux

- Issue based consulting
- Project management

### Soft skills

- Communication
- Leadership

### Industry knowledge

- Banking
- Retails

### Thinking

- Critical thinking
- Desgin thinking
- Architectural thinking

### Work style
- Agile
- DevOps

## Monday: Requirement 

- Business Understanding

“Far better an approximate answer to the right question, which is often vague, than an exact answer to the wrong question, which can always be made precise.”

"To be successful, ML projects need to think big from the start by taking into consideration the company structure, customers, company size and internal workflows."

Machine Learning (a data-driven method) is not suitable for Operational Risk Modeling. Two characteristics of operational risk– that it is 1) exposure-based and that 2) extreme losses cannot be extrapolated from recurring losses. Two approaches to model operational risk: 1) data-driven; 2) the scenario-driven point of view is precisely focused on the potential large future losses.

- Design Thinking


## Tuesday: Solution 

- Issue Conversion
  - Target Definition
  - Population Scoping
  - Main Feature Selection

Data leakage is a very critical issue and can be easily ignored. How to properly define a question and correctly build the test, training, and validation is an essential question in machine learning.

## Wednesday: Data

### Data Processing

In machine learning, your work generally involves building one long pipeline that starts by taking data in, ends with spitting a model (or predictions) out,  which fits in very naturally with functional programming paradigms.

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

To a significant degree, feature engineering is one the most important two progress in a machine learning modeling project, the other one is parameter tuning. Generally speaking, at the later stage of a modeling project, most score improvements are gained from feature engineering.

**GossipCat**

- Technicly:
  - Highly correlated: difference, LR, AUC
- Bussiness Sense:
  - Groupby
  - Meaningful: ratio
 
 ### Feature Engineering -- Background-based

- Graphic Analysis

Two major applications of Graph Theory: 1) network analysis, like Page Rank and Link Predictions; 2) engineering applications, like traversals.

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
 
 ### Model Evaluation
 
 **Mathematics**
 
 `How to choose metric for binary classification in industry(click prediction, credit risk)?`
 
Generaly, we have several metrics to choose from -- **precision, recall, f1-score, ROC AUC score, and PR AUC score**. So the question turns into Why choose average precision than others?

Firstly, we do care about **the precision and recall rate**; however, we do not care any of them singly, since there is a tradeoff between precision and recall according to different thresholds setted. As a result, a metric that considers both precision and recall is required.

**F1-score** is the harmonic mean of precision and recall. A regular mean treats precision and recall equally, while f1-score puts more weights on the lower one. It seems like f1-score finds a balance between precision and recall, however it depends on thresholds as well. What we need is a metric that considers both precision and recall, and does not depend on thresholds. 

Both **ROC AUC score** and **PR AUC score** measure distinguish capacity of a classifier, which is independent from thresholds. The receiver operating curve(ROC) plots recall to (1-specificity); while PR curve plots precision to recall. As a result, PR AUC cares more precision than specificity, compared to ROC AUC.

Assume we care more about precision than specifity, we choose PR AUC score as our metric.

Moreover, considering the imbalanced data, the ROC AUC score may look good, for few positive instances than the negatives; while the PR curve score provides a better metric to show how much we can improve.

Therefore, we choose average precision.

 **Business**
 
Considering your clients or boss, "do NOT use AUC-ROC, PR-Curve Area (Average Precision score), etc for business reporting. Use Derived Metrics since they easily capture the essence of your business easily," like fixing the precision (or recall) according to your business and reporting your recall (or precision).
 
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

Logging is one of the most underrated features. Two things (5&3) to take away from Logging in Python: 1) FIVE levels of importance that logs can contain(debug, info, warning, error, critical); 2) THREE components to configure a logger in Python (a logger, a formatter, and at least one handler).



## Notes:
After almost one year working experience of machine learning project in banking industy, I would like to summary several application advice as following:

1. The problem for you to solve may not be defined. The issues in industry are not always tipical machine learning problems but often appear as consulting issues. You need to communicate with your clients and try to dig out what they want and maybe teach them what they can get from machine learning.
2. The data you got can be dirty. It is, however, a fact so don't waste too much your time complain about the fact. It is what it is. Try to enfront it and solve the problem. That's why they hire you.
3. Generaly, your task is highly related to a engineering problem. Try to learn some skills like Linux OS and big data. 
4. You may not need to spend too much time to machine learning algorithms, like hyperparameter tuning. Try to build a pipeline to apply a general good algorithm, like the gradient boosting decision tree. 
5. Visualization helps you communicate to your clients a lot. Try to sharp your visualization skills. 

Nov 18, 2018
