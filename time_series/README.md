# Time Series

- [SARIMAX](#SARIMAX)
- [Prophet](#Prophet)
- [NeuralProphet](#NeuralProphet)
- [Evaluation](#Evaluation)


## SARIMAX

ARIMA and similar models assume some sort of causal relationship between past values and past errors and future values of the time series:

$$ Y_{t+h} = f(Y_t, Y_{t-1}, Y_{t-2}, ..., \eps) $$

e.g. the volatility of a stock today is causally driven by the volatility of that stock yesterday and two days ago, the population of a species this year is a direct function of the population of that same species last year, etc...

## Prophet

Prophet is a procedure for forecasting time series data based on **an additive model** where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. **It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.**

Prophet is a special case of the **Generalized Additive Model**. Whereas ARIMA tries to build **a formula for future values as a function of past values**,  Prophet tries **to detect “change points”**; you can think of Prophet as **curve-fitting**.  


## NeuralProphet

Generally, NeuralProphet is better on **smaller datasets**, but Prophet is better with **lots of training data**.

## Evaluation

