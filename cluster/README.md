# Clustering Algorithms Review

## Mathematical Explainations

### K-Means Clustering

The idea behind K-means clustering is that **a good** clustering is one for which the **within-cluster variation** is as small as possible.(ISL) 

The optimization problem that defines K-means clustering,

$$ minimize_{C_1, ..., C_K} {\sum_{k=1}^K W(C_k)} $$

where $ W(C_k) = \frac{1}{|C_K|} \sum_{i, i'\in C_k \sum_{j=1}^p (x_{ij} -  x_{i'j})^2} $, is the **squared Euclidean distance**.

---
Algorithm K-Means Clustering
---
1. Randomly assign a number, from 1 to K, to each of the observations. These serve as initial cluster assignments for the observations. 
2. Iterate until the cluster assignments stop changing:
    1. For each of the K clusters, compute the cluster centroid. The kth cluster centroid is the vector of the p feature means for the observations in the kth cluster.
    2. Assign each observation to the cluster whose centroid is closest (where closest is defined using Euclidean distance).
---

Because the K-means algorithm finds a **local** rather than a **global optimum**, the results obtained will depend on the initial (random) cluster assignment of each observation in Step 1 of Algorithm.

A good balance is **K-Means++** variant [Arthur and Vassilvitskii, 2006](http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf), whose initialization will still pick random points, but with probability proportional to square distance from the previously assigned centroids. Points that are further away will have higher probability to be selected as starting centroids. (Lovro Iliassich)

### EM Clustering

Expectation-Maximization method. 

With EM Clustering, we can now go a step further and describe each cluster by its centroid (mean), covariance (so that we can have **elliptical clusters**), and weight (the size of the cluster). The probability that a point belongs to a cluster is now given by **a multivariate Gaussian probability distribution** (multivariate - depending on multiple variables). That also means that we can calculate the probability of a point being under **a Gaussian ‘bell’**, i.e. the probability of a point belonging to a cluster.

- **E-step:** Calculate, for each point, the probabilities of it belonging to each of the current clusters (which, again, may be randomly created at the beginning). 
- **M-step:** Recalculate the parameters of each cluster, using the assignments of points to the previous set of clusters. To calculate the new mean, covariance and weight of a cluster, each point data is **weighted by its probability of belonging to the cluster**, as calculated in the previous step.

### Hierarchical Agglomerative Clustering

Or Linkage Clustering, good for when we don’t necessarily have **circular (or hyper-spherical) clusters**, and don’t know the number of clusters in advance. It starts with each point being a separate cluster, and works by joining two closest clusters in each step until everything is in one big cluster. (Lovro Iliassich)



### Affinity Propagation


## Illustrators

**K-Means Clustering**
<p align="center">
    <img width="400" src="https://uploads.toptal.io/blog/image/92528/toptal-blog-image-1463672901961-c86610183bb2ba67f979c421f6748893.gif">
</p>

**EM Clustering**
<p align="center">
    <img width="400" src="https://uploads.toptal.io/blog/image/92523/toptal-blog-image-1463639195822-62ac974368c9d3e4c1501368ae75e321.jpg">
</p>

**Linkage Clustering**
<p align="center">
    <img width="400" src="https://uploads.toptal.io/blog/image/92525/toptal-blog-image-1463639301381-ac46f23d267a0150ea7f3804b456a802.jpg">
</p>




## References:

1. [Brendan J. Frey and Delbert Dueck, “Clustering by Passing Messages Between Data Points”, Science Feb. 2007](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.121.3145)
2. [Hastie, Trevor, Robert Tibshirani, and J. H. Friedman. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2nd ed. Springer Series in Statistics. New York, NY: Springer, 2009.](https://hastie.su.domains/ElemStatLearn/)
3. [James, Gareth, Daniela Witten, Trevor Hastie, and Robert Tibshirani, eds. An Introduction to Statistical Learning: With Applications in R. Springer Texts in Statistics 103. New York: Springer, 2013.](https://www.statlearning.com/)
4. [Clustering Algorithms: From Start To State Of The Art](https://www.toptal.com/machine-learning/clustering-algorithms)
