# Clustering Algorithms Review

## Philosophy

Central to all of the goals of cluster analysis is the notion of the degree of **similarity** (or dissimilarity) between the individual objects being clustered. ... **Fundamental to all clustering techniques is the choice of distance or dissimilarity measure between two objects.** (ESL)

## Mathematical Explainations

### K-Means Clustering

The idea behind K-means clustering is that **a good** clustering is one for which the **within-cluster variation** is as small as possible.(ISL) 

The optimization problem that defines K-means clustering,

$$ minimize_{C_1, ..., C_K} {\sum_{k=1}^K W(C_k)} $$

where $ W(C_k) = \frac{1}{|C_K|} \sum_{i, i'\in C_k \sum_{j=1}^p (x_{ij} -  x_{i'j})^2} $, is the **squared Euclidean distance**.

---
Algorithm K-means Clustering
---
1. Randomly assign a number, from 1 to K, to each of the observations. These serve as initial cluster assignments for the observations. 
2. Iterate until the cluster assignments stop changing:
    1. For each of the K clusters, compute the cluster centroid. The kth cluster centroid is the vector of the p feature means for the observations in the kth cluster.
    2. Assign each observation to the cluster whose centroid is closest (where closest is defined using Euclidean distance).
---

Because the K-means algorithm finds a **local** rather than a **global optimum**, the results obtained will depend on the initial (random) cluster assignment of each observation in Step 1 of Algorithm.

A good balance is **K-Means++** variant [Arthur and Vassilvitskii, 2006](http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf), whose initialization will still pick random points, but with probability proportional to square distance from the previously assigned centroids. Points that are further away will have higher probability to be selected as starting centroids. (Lovro Iliassich)

### Gaussian Mixtures as Soft K-means Clustering: EM (Expectation-Maximization) Method

With EM Clustering, we can now go a step further and describe each cluster by its centroid (mean), covariance (so that we can have **elliptical clusters**), and weight (the size of the cluster). The probability that a point belongs to a cluster is now given by **a multivariate Gaussian probability distribution** (multivariate - depending on multiple variables). That also means that we can calculate the probability of a point being under **a Gaussian ‘bell’**, i.e. the probability of a point belonging to a cluster.

- **E-step:** Calculate, for each point, the probabilities of it belonging to each of the current clusters (which, again, may be randomly created at the beginning). 
- **M-step:** Recalculate the parameters of each cluster, using the assignments of points to the previous set of clusters. To calculate the new mean, covariance and weight of a cluster, each point data is **weighted by its probability of belonging to the cluster**, as calculated in the previous step.

EM is a “soft” version of K-means clustering, making **probabilistic** (rather than **deterministic**) assignments of points to cluster centers. **As the variance $/sigma^2 \rightarrow 0$, these probabilities become 0 and 1, and the two methods coincide.**

### Hierarchical Agglomerative Clustering

Strategies for hierarchical clustering divide into **two basic paradigms: agglomerative (bottom-up) and divisive (top-down)**. Agglomerative strategies start at the bottom and at each level recursively merge a selected pair of clusters into a single cluster. This produces a grouping at the next higher level with one less cluster. The pair chosen for merging consist of the two groups with the smallest intergroup dissimilarity. Divisive methods start at the top and at each level recursively split one of the existing clusters at that level into two new clusters. The split is chosen to produce two new groups with the largest between-group dissimilarity. With both paradigms there are N − 1 levels in the hierarchy.

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


### Evaluation

[StakeExchange](https://stats.stackexchange.com/questions/195456/how-to-select-a-clustering-method-how-to-validate-a-cluster-solution-to-warran)

1. **Cluster metaphor.** "I preferred this method because it constitutes clusters such (or such a way) which meets with my concept of a cluster in my particular project". Each clustering algorithm or subalgorithm/method implies its corresponding structure/build/shape of a cluster. In regard to hierarchical methods, I've observed this in one of points here, and also here. I.e. some methods give clusters that are prototypically "types", other give "circles [by interest]", still other "[political] platforms", "classes", "chains", etc. Select that method which cluster metaphor suits you. For example, if I see my customer segments as types - more or less spherical shapes with compaction(s) in the middle I'll choose Ward's linkage method or K-means, but never single linkage method, clearly. If I need a focal representative point I could use medoid method. If I need to screen points for them being core and peripheral representatives I could use DBSCAN approach.

2. **Data/method assumptions.** "I preferred this method because my data nature or format predispose to it". This important and vast point is also mentioned in my link above. Different algorithms/methods may require different kind of data for them or different proximity measure to be applied to the data, and vice versa, different data may require different methods. There are methods for quantitative and methods for qualitative data. Mixture quantitative + qualitative features dramatically narrows the scope of choice among methods. Ward's or K-means are based - explicitly or implicitly - on (squared) euclidean distance proximity measure only and not on arbitrary measure. Binary data may call for special similarity measures which in turn will strongly question using some methods, for example Ward's or K-means, for them. Big data may need special algorithms or special implementations.

3. **Internal validity.** "I preferred this method because it gave me most clear-cut, tight-and-isolated clusters". Choose algorithm/method that shows the best results for your data from this point of view. The more tight, dense are clusters inside and the less density is outside of them (or the wider apart are the clusters) - the greater is the internal validity. Select and use appropriate internal clustering criteria (which are plenty - Calinski-Harabasz, Silhouette, etc etc; sometimes also called "stopping rules") to assess it. [Beware of overfitting: all clustering methods seek to maximize some version of internal validity1 (it's what clustering is about), so high validity may be partly due to random peculiarity of the given dataset; having a test dataset is always beneficial.]

4. **External validity.** "I preferred this method because it gave me clusters which differ by their background or clusters which match with the true ones I know". If a clustering partition presents clusters which are clearly different on some important background (i.e. not participated in the cluster analysis) characteristics then it is an asset for that method which produced the partition. Use any analysis which applies to check the difference; there also exist a number of useful external clustering criteria (Rand, F-measure, etc etc). Another variant of external validation case is when you somehow know the true clusters in your data (know "ground truth"), such as when you generated the clusters yourself. Then how accurately your clustering method is able to uncover the real clusters is the measure of external validity.

5. **Cross-validity.** "I preferred this method because it is giving me very similar clusters on equivalent samples of the data or extrapolates well onto such samples". There are various approaches and their hybrids, some more feasible with some clustering methods while others with other methods. Two main approaches are stability check and generalizability check. Checking stability of a clustering method, one randomly splits or resamples the data in partly intersecting or fully disjoint sets and does the clustering on each; then matches and compares the solutions wrt some emergent cluster characteristic (for example, a cluster's central tendency location) whether it is stable across the sets. Checking generalizability implies doing clustering on a train set and then using its emergent cluster characteristic or rule to assign objects of a test set, plus also doing clustering on the test set. The assignment result's and the clustering result's cluster memberships of the test set objects are compared then.

6. **Interpretation.** "I preferred this method because it gave me clusters which, explained, are most persuasive that there is meaning in the world". It's not statistical - it is your psychological validation. How meaningful are the results for you, the domain and, possibly audience/client. Choose method giving most interpretable, spicy results.

7. **Gregariousness.** Some researches regularly and all researches occasionally would say "I preferred this method because it gave with my data similar results with a number of other methods among all those I probed". This is a heuristic but questionable strategy which assumes that there exist quite universal data or quite universal method.

Points 1 and 2 are theoretical and precede obtaining the result; exclusive relying on these points is the haughty, self-assured exploratory strategy. Points 3, 4 and 5 are empirical and follow the result; exclusive relying on these points is the fidgety, try-all-out exploratory strategy. Point 6 is creative which means that it denies any result in order to try to rejustify it. Point 7 is loyal mauvaise foi.

Points 3 through 7 can also be judges in your selection of the "best" number of clusters.



## References:

1. [Brendan J. Frey and Delbert Dueck, “Clustering by Passing Messages Between Data Points”, Science Feb. 2007](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.121.3145)
2. [Hastie, Trevor, Robert Tibshirani, and J. H. Friedman. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2nd ed. Springer Series in Statistics. New York, NY: Springer, 2009.](https://hastie.su.domains/ElemStatLearn/)
3. [James, Gareth, Daniela Witten, Trevor Hastie, and Robert Tibshirani, eds. An Introduction to Statistical Learning: With Applications in R. Springer Texts in Statistics 103. New York: Springer, 2013.](https://www.statlearning.com/)
4. [Clustering Algorithms: From Start To State Of The Art](https://www.toptal.com/machine-learning/clustering-algorithms)
5. [How to select a clustering method? How to validate a cluster solution (to warrant the method choice)?](https://stats.stackexchange.com/questions/195456/how-to-select-a-clustering-method-how-to-validate-a-cluster-solution-to-warran)
