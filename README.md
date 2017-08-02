# Notes 

## Table of Contents
1. [Forget `for` Loops](#Forget `for` Loops)
2. [Plot with `Plotly`](#Plot with `Plotly`#)

## Forget `for` Loops

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

## Plot with `Plotly`

August 2, 2017 

Have used `plotly` in r in school, while just find that it has data visualization tool online. I guess it is better than Tableau, easy to use and can do more than the later one.

