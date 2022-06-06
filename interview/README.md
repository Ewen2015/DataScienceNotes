# interview questions

## 1. least squares regression, ridge regression, and lasso regression

1. least squares regression: 

$$ RSS = \sum_{i=1}^n(y_{i} - \beta_{0} - \sum_{j-0}^p\beta_{j}x_{ij})^2 $$

residual sum of squares(RSS)

2. ridge regression:

$$ RSS + \lambda\sum_{j-0}^p\beta_{j}^2 $$

where $ \lambda \geq 0 $ is a *tuning parameter*.

$\sum_{j-0}^p\beta_{j}x_{ij})^2$, *shrinkage penalty*, $ l_{2} $ penalty. 

the ridge includes all **p** predictors in the final model.

3. lasso regression:

$$ RSS + \lambda\sum_{j-0}^p|\beta_{j}| $$

$ l_{1} $ penalty

the lasso performs **variable selection**.

## 2. bagging, ransom forests, booting

1. bagging:

bootstrap

$$ \hat f_{bag}(x) = \frac{1}{B}\sum_{b=1}^B \hat f^{*b}(x) $$

2. random forests

*a random sample of m predictors* is chosen as split candidates from the full set of p predictors. 

Boosting works in a similar way, except that the trees are grown **sequentially**: each tree is grown using information from previously grown trees.
