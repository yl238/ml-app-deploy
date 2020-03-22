# Estimate Scope and Challenges

## Leverage Domain Expertise

Heuristic: A good rule of thumb based on knowledge of the problem and the data. The best way to devise heuristics is to see what experts are currently doing. Most practical applications are not entirely novel. How do people currently solve the problem you are trying to solve?

The second best way to devise heuristics is to look at your data. Based on your dataset, how would you solve this task if you were doing it manually?

## Learning From Experts

This is where I go to an expert who understands who the existing model works and what assumptions we can reasonably make. This includes understanding how often the model is being run, and what indicators are showing the efficacy of the model.

## Examine the Data

Although this sounds trivial, it is by no means done effectively. It is crucial to individually label examples in the way you hope a model would. Doing so helps validate assumptions and confirms that you chose models that can appropriately leverage your dataset.

It can often be a good idea to build a convincing proof of concept before committing significant resources to a project. Before using time and money to label data, for example, we need to convince ourselves that we can build a model that will learn from said data.

Some of the things we need to look at for the screener / tester matching problem:

* Which tests have questions that already exist in the demographic information that a tester has already provided?
* What kind of questions are the testers most likely to fail at?

## Open data

Think about what kind of problem our project tackles and whether there are existing dataset that is similar so we can make a start on our own problem.