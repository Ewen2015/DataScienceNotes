# Time Series

- [SARIMAX](#SARIMAX)
- [Prophet](#Prophet)
- [NeuralProphet](#NeuralProphet)
- [Evaluation](#Evaluation)
- [References](#References)


## SARIMAX

ARIMA and similar models **assume some sort of causal relationship between past values and past errors and future values** of the time series:

$$ Y_{t+h} = f(Y_t, Y_{t-1}, Y_{t-2}, ..., \epsilon_{t}, \epsilon_{t-1}, \epsilon_{t-2}, ...) $$

e.g. the volatility of a stock today is causally driven by the volatility of that stock yesterday and two days ago, the population of a species this year is a direct function of the population of that same species last year, etc...

## Prophet

### Mathematics

The core model of Prophet is **a structural time series model** (Harvey & Peters 1990).

$$ y(t) = g(t) + s(t) + h(t) + \epsilon_t $$

- $g(t)$ is the trend function which models non-periodic changes in the value of the time series
- $s(t)$ represents periodic changes (e.g., weekly and yearly seasonality)
- $h(t)$ represents the effects of holidays which occur on potentially irregular schedules over one or more days
- $\epsilon_t$, the error term, represents any idiosyncratic changes which are not accommodated by the model; later we will make the parametric assumption that $\epsilon_t$ is normally distributed.

This specification is similar to **a generalized additive model (GAM)** (Hastie & Tibshirani 1987), a class of regression models with potentially non-linear smoothers applied to the regressors.

### Comments

"We are, in effect, framing the forecasting problem as **a curve-fitting exercise**, which is inherently different from time series models that explicitly account for the **temporal dependence** structure in the data. While we give up some important inferential advantages of using **a generative model such as an ARIMA**, this formulation provides a number of practical advantages:

- **Flexibility**: We can easily accommodate seasonality with multiple periods and let the analyst make different assumptions about trends.
- Unlike with ARIMA models, the measurements **do not need to be regularly spaced**, and we **do not need to interpolate missing values** e.g. from removing outliers. 
- **Fitting is very fast**, allowing the analyst to interactively explore many model specifications, for example in a Shiny application (Chang et al. 2015). 
- The forecasting model has **easily interpretable parameters** that can be changed by the analyst to impose assumptions on the forecast. Moreover, analysts typically do have experience with regression and are easily able to extend the model to include new components."

Facebook Prophet **doesn't look for any such causal relationships between past and future**. Instead, it simply tries **to find the best curve to fit to the data (curve-fitting)**, using **a linear or logistic curve**, and **Fourier coefficients for the seasonal components**. There is also a regression component, but that is for external regressors, not for the time series itself (The Prophet model is a special case of **GAM - Generalized Additive Model**).

Theoretically speaking, **the assumptions underlying Prophet are indeed simplistic and weak** - just **fit the best curve to your historical data**. Since fitting a curve to a limited data set over a specific time period doesn't impose any constraints on how the curve behaves outside of your historical data set, it is entirely possible that the best fitting curve will "go off the rails" outside of the historical time interval. For example, I have often noticed that Prophet can go negative in the future, even if the historical data set has only positive values, because the simplistic assumptions mean that it will naively perpetuate a downward trend forever.

This why prophet is **recommended only for time series where the only informative signals are (relatively stable) trend and seasonality, and the residuals are just noise**.

In theory, a more rigorous causal or structural approach is more likely to capture signals that will extrapolate into the future. More importantly, if **the residuals are not just noise**, then an ARIMA model or a Neural Network might be able to capture those relationships...in theory.

**It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.**


## NeuralProphet

### Mathematics

A core concept of the NeuralProphet model is its **modular composability**. The model is composed of modules which each contribute an **additive** component to the forecast. Most components can also be configured to be scaled by the trend for a **multiplicative effect**. Each module has its individual inputs and modelling processes.

$$ y(t) = T(t) + S(t) + E(t) + F(t) + A(t) + L(t) $$

where, 

- $T(t) =$ Trend at time $t$ 
- $S(t) =$ Seasonal effects at time $t$ 
- $E(t) =$ Event and holiday effects at time $t$ 
- $F(t) =$ Regression effects at time $t$ for future-known exogenous variables 
- $A(t) =$ Auto-regression effects at time $t$ based on past observations 
- $L(t) =$ Regression effects at time $t$ for lagged observations of exogenous variables

### Comments

Generally, NeuralProphet is better on **smaller datasets**, but Prophet is better with **lots of training data**.

Neural Prophet是升级版的Prophet。虽然官方PPT写了很多改变，但是其实就是基于两个”巨变“。

- **第一个巨变是分解的分量增加了一个重量级的AR（自回归），这个是超级重量级的**。
  - 因为AR模型本身在经典时序分析里面就独当一面，到了Neural Prophet里面做为辅助，它对于精度的提高是神级的。
  - 相比于传统的AR模型，这里的AR模型借助于神经网络，拟合的更加快捷和精确。
  - 一招鲜，吃遍天，FB把正则用的炉火纯青。对于AR模型也添加了正则项（参数为ar_sparsity）。
  - 通过正则加持，你的AR模型可以看的更远，因为你有能力使用更多的历史数据而不用担心求解。
- **第二个巨变是Pytorch作为backend**。
  - Neural Prophet把所有的分量都用pytorch写了，这才是真正的开源了代码。
  - 趋势项，周期项变化不大，因为他们的算法还是和Prophet一致
  - AR项，外部回归项变化很大，因为有了Pytorch的加持，意味着你不用再局限于线性回归。
  - 从源码看，Neural Prophet采用Relu非线性化了。
  - 而且，神经网络嘛，最适合魔改，看着结果不顺眼，改改层数，说不定就顺眼了。

这两个巨变其实目前还是很有诚意的，但是我还在等它更大的feature: **Global model**. Global model 模型意味着一个模型适配多个时序，比如同时预测iphone11，12，13，甚至未面世的iphone 18的销量（冷启动问题）。 

NeuralPorphet 看起来那么神，其实就是一个全自动的AR，在我看来，它就是**Pytorch版的SARIMAX**。

## Evaluation

**Errors and Residuals**

- An **error** is the difference between  **the observed value and the true value** (very often unobserved, generated by the data generating process, DGP).
- A **residual** is the difference between  **the observed value and the predicted value** (by the model).

**Notes:** In statistics and in empirical sciences, **a data generating process** is a process in the real world that "generates" the data one is interested in. Usually, scholars do not know the real data generating model. However, it is assumed that those real models have observable consequences.

|measures|formula|
|--------|-------|
|scale-dependent errors| mean absolute error (MAE); root mean squared error(RMSE) |
|percentage errors| mean absolute percentage error (MAPE) |
|scaled errors| mean absolute scaled error (MASE) |

$$ MAE = mean(|e_t|)$$

$$ RMSE = \sqrt{mean(e_t^2)} $$

$$ MAPE = mean(|p_t|) $$

$$ MASE = mean(|q_j|) $$

## References

1. [Inference in Time Series: Prophet vs. ARIMA](https://stats.stackexchange.com/questions/472266/inference-in-time-series-prophet-vs-arima)
2. [What is the difference between errors and residuals?](https://stats.stackexchange.com/questions/133389/what-is-the-difference-between-errors-and-residuals)
3. [Evaluating forecast accuracy](https://otexts.com/fpp2/accuracy.html)
4. [为什么NeuralProphet这么准，看这一篇真的就够了](https://mp.weixin.qq.com/s/AJQGZfopVCdpjdyf5bQHqA)
5. [Data generating process](https://en.wikipedia.org/wiki/Data_generating_process#:~:text=In%20statistics%20and%20in%20empirical,real%20models%20have%20observable%20consequences.)
6. [Taylor, Sean J., and Benjamin Letham. “Forecasting at Scale.” PeerJ Inc., September 27, 2017.](https://peerj.com/preprints/3190)
7. [Harvey, A C, and S Peters. “Estimation Procedures for Structural Time Series Models” 9, no. 2 (n.d.): 21.](http://www.stat.yale.edu/~lc436/papers/Harvey_Peters1990.pdf)
8. [Triebe, Oskar, Hansika Hewamalage, Polina Pilyugina, Nikolay Laptev, Christoph Bergmeir, and Ram Rajagopal. “NeuralProphet: Explainable Forecasting at Scale.” arXiv, November 29, 2021.](http://arxiv.org/abs/2111.15397)
