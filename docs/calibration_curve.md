# Calibration Curve and Brier Score

## Score function

In decision theory, a **score function**, or **scoring rule**, measures the accuracy of probabilistic predictions. It is applicable to tasks in which predictions must assign probabilities to a set of mutually exclusive outcomes. The set of possible outcomes can be either binary or categorical in nature, and the probabilities assigned to this set of outcomes must sum to one.

A score can be thought of as either a measure of the "calibration" of a set of probabilistic predictions, or as a "cost function" or "loss function". Essentially a scoring rule is a function that caclulates the distance between the true target variable (a probability) and the random variable generated from the forecast schema. 

## Proper scoring rules

A proper scoring rule is one that scores best if the target variable is suggested as the forecast.If a cost is associated in proportion to a proper scoring rule, the minimal expected cost corresponding to reporting the true set of probabilities. Proper scoring rules are used where a forecaster or algorithm will attempt to minimise the average score to yield refined, calibrated probabilities.

A probabilistic forecaster or algorithm will return a probability vector $\mathbf{r}$ with a probability for each of the $i$ outcomes. One useage of a scoring function could be to give a reward of $S(\mathbf{r}, i)$ if the $i$th event occurs. If a *proper* scoring rule is used, then the highest expected reward is obtained by reporting the true probability distribution. The use of a proper scoring rule encourages the forecaster to be honest to maximise the expected reward.

In our case we can think about this as follows: we make predictions based on different decision thresholds, but we want to find a way to evaluate the expected losses with respect to a particular distribution over the decision thresholds, thus the choice of a scoring rule corresponds to an assumption about the probability distribution of the dceision problems for which the predicted probabilities will ultimately be employed.

## Brier score
The Brier score is a [proper score](https://en.wikipedia.org/wiki/Scoring_rule#ProperScoringRules), and originally proposed by Glenn Brier in 1950. It can be obtained by an affine transform from the quadratic scoring rule
$$
Q(\mathbf{r}, i) = 2r_i - \mathbf{r}\cdot\mathbf{r} = 2r_i - \sum_{j=1}^C r_j^2
$$
where $r_i$ is the probability assigned to the correct answer and $C$ is the number of classes.
The Brier score looks like this:
$$
B(\mathbf{r}, i) = \sum_{j=1}^C(y_j-r_j)^2
$$
where $y_j=1$ when the $j$th event is correct and $y_j=0$ otherwise and $C$ is the number of classes. This transformation makes the score much easier to calculate, but we must remember fo minimise the Brier score due to the transformation.

With the Brier score we assume a uniform probability of the decision threshold being anywhere between zero and one.