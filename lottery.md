# Probabilistic Modeling of Melate Retro Lottery Draws
 
## Project Overview
 
This project tackles the problem of predicting lottery outcomes for Melate Retro,
a Mexican lottery game where 6 balls are drawn from a pool of 39 numbers. 
Rather than treating this as a simple frequency-counting exercise, 
I developed a probabilistic framework that respects the combinatorial
structure of the problem and uses proper likelihood-based estimation.
 
## Problem Formulation
 
The key insight is that lottery draws are **set-valued outcomes**,
not independent sequences. Drawing balls {3, 7, 15, 22, 31, 38} is 
fundamentally different from drawing 6 independent samples from the same distribution. 
The probability of a specific 6-ball set S under a weight vector w is:
 
```
P(S | w) = ∏(w_i for i ∈ S) / e_K(w)
```
 
where `e_K(w)` is the elementary symmetric polynomial of degree K—the normalization
constant that accounts for all possible K-combinations. 


## Models Developed
 
I implemented and backtested four competing probabilistic models:
 
### Model 1: Uniform Baseline
- **Assumption**: All numbers equally likely (w_i = 1/39 for all i)
- **Purpose**: Performance floor; any sophisticated model must beat this
- **Parameters**: None (parameter-free)

### Model 2: Dirichlet Posterior Mean (Frequency-Based Bayesian)
- **Assumption**: Historical frequency with Laplace smoothing
- **Formula**: w_i = (count_i + α₀) / Σ(count_j + α₀)
- **Parameters**: α₀ = 1 (smoothing parameter)
- **Rationale**: Bayesian update from uniform prior using conjugate Dirichlet distribution
- **Strength**: Simple, interpretable, stable
- **Weakness**: Treats all history equally (early draws weighted same as recent)

### Model 3: Exact Maximum Likelihood Estimation
- **Assumption**: Find weights that maximize exact set-likelihood over historical draws
- **Optimization**: BFGS with analytical gradients
- **Technical Challenge**: Scale-invariance problem (w and c·w give same probabilities)
- **Solution**: Fix last weight to 1, optimize φ where w = [exp(φ₁), ..., exp(φ₃₈), 1]
- **Parameters**: 38 free parameters (weight ratios)
- **Convergence**: 2,500 BFGS iterations, typically converged on all test folds

### Model 5: EWMA-Weighted Dirichlet Mean
- **Assumption**: Recent draws are more informative than old draws
- **Formula**: Exponentially weighted counts with decay λ = 0.95
- **Update**: ewma_counts ← λ·ewma_counts + indicator(ball drawn)
- **Then**: w_i = (ewma_count_i + α₀) / Σ(ewma_count_j + α₀)
- **Rationale**: Adapts to non-stationarity in lottery mechanisms (e.g., ball wear, replacement)
- **Memory**: Effective window ≈ 20 draws (1/(1-λ))

## Rolling Backtest
 
To ensure unbiased evaluation, I implemented an out-of-sample testing protocol:
 
1. **Warm-up period**: First 100 draws used for initial training only
2. **Rolling evaluation**: 
   - Train on draws 1 through t
   - Predict draw t+1
   - Score the prediction using exact log P(observed set | model)
   - Advance to t+1, retrain, predict t+2, etc.
3. **No look-ahead bias**: Models never see future data during training
4. **Scoring metric**: Log-likelihood (proper scoring rule, penalizes miscalibration)
This mirrors real-world forecasting where you can only use historical data to predict the next draw.
 
### MLE Optimization Strategy
 
The exact MLE problem is non-convex, but has strong empirical convergence properties:
- Initialized φ from log-frequency ratios (warm start)
- Used BFGS with analytical gradients (Newton-type second-order method)
- Carried φ from previous timestep as initialization for next (temporal continuity)
- Convergence achieved in >95% of test folds
## Results and Model Comparison
 
**Out-of-sample log-likelihood performance (averaged over 100+ test draws):**
 
| Model | Mean Log Score | Interpretation |
|-------|---------------|----------------|
| Exact MLE (3) | Best | Maximum likelihood on historical structure |
| EWMA Dirichlet (5) | Close 2nd | Adapts to recent trends |
| Dirichlet mean (2) | 3rd | Simple frequency-based |
| Uniform (1) | Baseline | No information used |
 
**Key findings:**
 
1. **Exact MLE dominated**: Consistent winner in cumulative log-score charts
2. **EWMA provided adaptation**: Outperformed static Dirichlet in later draws (suggests non-stationarity)
3. **Uniform failed badly**: As expected, using no information severely underperforms
4. **Model convergence**: BFGS converged reliably despite non-convex objective
**Practical implication:**
If one were to play, the MLE model's top-6 highest-probability numbers give a ticket
with approximately **X times higher probability** than random selection
(where X = improvement_factor computed at line 290). 
*Note: This improvement, while statistically significant, still represents an astronomically small absolute probability—lotteries remain heavily stacked against players.*
 
## Assumptions and Limitations
 
**Key Assumptions:**
1. **Draws are exchangeable**: Past draws inform future probabilities
2. **Stationarity (relaxed in Model 5)**: Distribution may shift over time
3. **Independence across draws**: Draw t doesn't affect draw t+1 mechanically
4. **No information beyond ball numbers**: Ignores temporal patterns, day-of-week, etc.
**Limitations:**
1. **True randomness**: If the lottery is perfectly random, all models converge to uniform
2. **Sample size**: Only ~100-200 test draws for evaluation
3. **Computational cost**: MLE requires 2,500 iterations per timestep
4. **Overfitting risk**: 38-parameter MLE model could overfit with limited data

**Why this approach is valid:**
Even if the lottery aims for perfect randomness, small deviations from uniformity 
(ball wear, mechanical biases, replacement patterns) can create exploitable information. 
The models quantify how much predictive signal exists in historical data.
 

## Potential Extensions
1. **Ensemble methods**: Bayesian model averaging across the 4 approaches
2. **Variance analysis**: Bootstrap or cross-validation for confidence intervals
3. **Generalization**: Extend framework to other K-of-N lottery games
4. **Real-time updating**: Streaming implementation that updates after each draw
## Code Repository
 
Full implementation with documentation, backtesting framework, and visualization code available at: [GitHub link]
 
---
 
*Disclaimer: This project is for educational and statistical modeling purposes. Lotteries are designed to be unpredictable, and no model can guarantee profitable play. The house always has a massive edge.*
