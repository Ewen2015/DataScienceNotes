# Statistics

- [Hypothesis Test](#Hypothesis-Test)
- [Statistical Tests](#Statistical-Tests)
- [Degree of Freedom](#Degree-of-Freedom)
- [P-value](#P-value)
- [Errors](#Errors)
- [Power Analysis](#Power-Analysis)
- [A/B Testing](#A/B-Testing)
- [References](#References)

## Hypothesis Test

<p align="center">
<img src='https://github.com/Ewen2015/DataScienceNotes/blob/master/stat/Harmonia_Macrocosmica.jpeg'>
</p>

**The main purpose of statistics is to test a hypothesis.**

**A hypothesis** is **an educated guess** about something in the world around you. It should be testable, either by **experiment** or **observation**. For example:

- A new medicine you think might work.
- A way of teaching you think might be better.
- A possible location of new species.
- A fairer way to administer standardized tests.

It can really be anything at all as long as you can put it to the test.

**Hypothesis testing** in statistics is a way for you to test the results of a **survey** or **experiment** to see if you have **meaningful results**. You’re basically testing whether your results are valid by figuring out the odds that your results have happened by chance. If your results may have happened by chance, the experiment won’t be repeatable and so has little use.

## Statistical Tests

<p align="center">
<img src='https://github.com/Ewen2015/DataScienceNotes/blob/master/stat/statistical_tests.jpg'>
</p>

<p align="center">
<img src='https://github.com/Ewen2015/DataScienceNotes/blob/master/stat/xMeanComparisonTable.jpg.pagespeed.ic.ANRLAM5qed.jpg'>
</p>

## Degree of Freedom

## P-value

<p align="center">
<img src='https://github.com/Ewen2015/DataScienceNotes/blob/master/stat/p-value.jpeg'>
</p>

- **P-value (p)**: Probability of obtaining a result equal to or more extreme than was observed in the data.

In interpreting the p-value of a significance test, you must specify **a significance level**, often referred to as the Greek lower case letter **$\alpha$**. A common value for the significance level is 5% written as 0.05.

The p-value is interested in the context of the chosen significance level. A result of a significance test is claimed to be “**statistically significant**” if the p-value is less than the significance level. This means that the null hypothesis (that there is no result) is rejected.

- **$p \le \alpha$**: reject H0, different distribution.
- **$p > \alpha$**: fail to reject H0, same distribution.

Where:

Significance level ($\alpha$): Boundary for specifying a statistically significant finding when interpreting the p-value.

We can see that the p-value is just a probability and that in actuality the result may be different. The test could be wrong. Given the p-value, we could make an error in our interpretation.

## Errors

<p align="center">
<img src='https://github.com/Ewen2015/DataScienceNotes/blob/master/stat/errors.png'>
</p>

There are two types of errors; they are:

- **Type I Error**. Reject the null hypothesis when there is in fact no significant effect (false positive). The p-value is optimistically small.
- **Type II Error**. Not reject the null hypothesis when there is a significant effect (false negative). The p-value is pessimistically large.

## Power Analysis

> Power analysis answers questions like “how much statistical power does my study have?” and “how big a sample size do I need?”.

Statistical power is one piece in a puzzle that has four related parts; they are:

- **Effect Size**. The quantified magnitude of a result present in the population. Effect size is calculated using a specific statistical measure, such as Pearson’s correlation coefficient for the relationship between variables or Cohen’s d for the difference between groups.
- **Sample Size**. The number of observations in the sample.
- **Significance**. The significance level used in the statistical test, e.g. alpha. Often set to 5% or 0.05.
- **Statistical Power**. The probability of accepting the alternative hypothesis if it is true.

All four variables are related. For example, a larger sample size can make an effect easier to detect, and the statistical power can be increased in a test by increasing the significance level.

**A power analysis involves estimating one of these four parameters given values for three other parameters.** This is a powerful tool in both the design and in the analysis of experiments that we wish to interpret using statistical hypothesis tests.

For example, the statistical power can be estimated given an effect size, sample size and significance level. Alternately, the sample size can be estimated given different desired levels of significance.

## A/B Testing

> A/B testing is a way to compare two versions of a single variable, typically by testing a subject’s response to variant A against variant B, and determining which of the two variants is more effective.

### What are the Steps of A/B Testing?
There are 5 main steps for A/B Testing:

#### 1. Make a hypothesis about the change

The first step is exactly what we did in the example above. i.e., We assume that changing the size of the ‘Join Now’ button from 4x3 to 16x9 will affect the number of students enrolled in our online course.

#### 2. Choose the metrics

E.g. We want more students to move from the course menu page to a specific course page, so we choose the ‘click-through probability’ as our metric.

#### 3. Experiments

Design the experiment setups (including the unit of diversion, population, size, and duration), and carry out the test.

#### 4. Analyse the results

Calculate the margin based on the confidence interval, and decide whether it satisfies the practical significance requirements.

#### 5. Make a decision. Communicate the results and risks with stakeholders.

If you feel confused about some of the concepts above, don’t worry. Let’s dive into the details!


## References:

- [Hypothesis Testing](https://www.statisticshowto.com/probability-and-statistics/hypothesis-testing/)
- [A Gentle Introduction to Statistical Power and Power Analysis in Python](https://machinelearningmastery.com/statistical-power-and-power-analysis-in-python/#:~:text=Statistical%20power%2C%20or%20the%20power,the%20null%20hypothesis%20is%20rejected.)
- [A/B Testing 101 with Examples - A Summary of Udacity’s Course](https://towardsdatascience.com/a-b-testing-101-with-examples-a-summary-of-udacitys-course-3f937e8ea31f)
