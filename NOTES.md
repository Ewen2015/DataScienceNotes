# Notes 


#### August 7, 2017 Time Series `stlf` of `forecast`

In the Walmart sales forecasting competition in Kaggle, 'stlf' works pretty well. To understand how it works, its author wrote answered a qeustion posted on [stackoverflow](https://stackoverflow.com/questions/24991039/stlf-function-in-the-forecast-package). 

```
# STL decomposition
temp <- stl(WeeklyReferral, s.window="periodic", robust=TRUE)
# Seasonally adjusted data
sa <- seasadj(temp)
seascomp <- tail(temp$time.series,52)[,1]
# ETS model
fit <- ets(sa, "ZZN")
# Simulations from ETS model with re-seasonalization
sim <- matrix(0, nrow=52, ncol=1000)
for(i in 1:1000)
  sim[,i] <- simulate(fit, nsim=52) + seascomp
```

#### Plot with `Plotly` 

Have used `plotly` in r in school, while just find that it has data visualization tool online. I guess it is better than Tableau, easy to use and can do more than the later one.


#### August 2, 2017 Forget about `for` Loops

**Nested `for` Loops**

As `for` loops in `R` are extremely slow, it is better to wrap the process into a nested `sapply` function. 

*Note:* To update a global variable inside a function, use `<<-`.

```
# nested for loop
for(i in seq(0.1, 1, 0.1)){
  for(j in seq(1, 10, 1)){
  function(i, j)                                      # any function with parameter i and j
  }
}

# improved version, nested sapply loop
sapply(seq(0.1, 1, 0.1), function(i)       
  sapply(seq(1, 10, 1), function(j)
    function(i, j)))
```
