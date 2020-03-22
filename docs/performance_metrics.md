# Performance Metrics

## Business Performance

This metric is separate from any model metrics and only be a reflection of the product's success. These metrics are ultimately ones that matter, as they represent the goals of your product or feature. All other metrics should be used as tools to improve product metrics. These do not have to be unique.

In order to compute the metric, the interface should capture whether:

* The number of screeners failed per test has reduced
* The time taken to fulfill a test has decreased/increased
* The number of active testers retained over a period has remained the same / increased

## Model Performance

For most online products, ultimate product metric that determines the success of a model is the proportion of visitors who use the output of a model out of all visitors who could benefit from it. In our case, it is the distribution of people who pick up a test versus those who would have picked up the test under the previous scenario.

When a product is still being built and not deployed yet, it is not possible to measure usage metrics. To still measure progress, it is important to define a separate success metric called an *offline metric* or a *model metric*. A good offline metric should be possible to evaluate without exposing a model to users, and be as correlated as possible with product metrics and goals.

### Other examples of updating an application to make a modeling task easier

* *Changing an interface so that a model's results can be omitted if they are below a confidence threshold*
* *Presenting a few other predictions or heuristics in addition to a model's top prediction*
* *Communicating to users that a model is still in an experimental phase and giving them opportunities to provide feedback*

If we want to always have advice that is relevant, we would want to prioritize the model's *precision* because when a high-precision model classifies a question as good (and thus makes a recommendation), there is a high chance that this question is actually good. High precision means that when we do make a recommendation, it will tend to be correct. 

## Freshness and Distribution Shift

Supervised models draw their predictive power from learning correlations between input features and prediction targets. This means that most models need to have been exposed to training data that is similar to a given input to perform well on it. Depending on your business problem, you should consider how hard it is will be to keep models *fresh*. How often will you need to retrain models, and how much will it cost you each time to do so?

In the case of churn model, features that could change with time are:

- Demographic information distribution of the testers under consideration
- Number of tests available in the previous month
- Number of tests with screeners in the previous month

In our model we have captured all these information as part of the training data - does this mean we won't need to update the model as often?
