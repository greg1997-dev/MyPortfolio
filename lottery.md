# Can You Actually Beat the Lottery? A Data Science Experiment
 
## How It Started: Power Balls and False Hope

Lottery games are everywhere. Pick some numbers from a pool, match them all, win the jackpot. Simple, right? Millions of people play every week hoping to retire early, despite odds that are absolutely brutal.

"The lottery is rigged." "It's all random, you can't predict it." "Those numbers are cursed."

I've heard these phrases my entire life in Mexico whenever lottery draws come up. One family member plays religiously—like clockwork, someone always claims their numbers are "due" or that certain balls "never come up." But they keep playing anyway. I remember my uncle would always keep his ticket folded in his coat pocket, like a lucky charm that never worked.

I play occasionally through an app, mostly out of curiosity. Every so often I see that someone actually hit the jackpot, and I immediately text my father-in-law who plays too: "Is that you?" 

The answer is always: "No."

But it got me thinking: **How do people actually hit these combinations? Is there any pattern? Are some numbers consistently more likely to come up?**

Then a Netflix series dropped called *"Melate que sí"* about a massive fraud in the 2012 Melate draw in Mexico. Watching it made me wonder: even without fraud, could there be detectable biases in how balls are drawn? 

So I decided to find out with data.

The setup was simple: If the lottery is perfectly random, no statistical model should beat a uniform guess. But if there's even the slightest mechanical bias—worn balls, replacement schedules, temperature effects on the tumbler—maybe we could detect it in the historical data.

**Spoiler alert: I found some interesting things.**
 
## Just How Bad Are Your Odds?
 
First, let's talk about how unlikely winning the jackpot is.
Melate Retro draws 6 balls from a pool of 39 numbers. The probability of matching all 6 is:
 
**1 in 3,262,623**
 
To put that in perspective:
- You're more likely to be struck by lightning (1 in 500,000)
- You're more likely to get dealt a royal flush in poker (1 in 649,740)
- If you bought one ticket every week, you'd expect to wait **62,742 years** to win.
 
## What I Built: Four Different Approaches
 
Instead of just counting how many times each ball appeared (which is what most people do), I wanted to model the actual probability distribution properly. Here's what I tried:
 
### Approach 1: The Skeptic (Uniform Model)
This is the "it's all random" baseline. Every number has exactly the same 1/39 chance of appearing. If the lottery is perfectly fair and random, this model should be impossible to beat.
 
### Approach 2: The Historian (Frequency Counter with Bayesian Smoothing)
This is what most people do intuitively—count which balls appear most often and bet on those. I added some Laplace smoothing (basically, don't assume a ball that hasn't appeared much has zero probability, give everything at least a tiny chance).
 
**Formula**: Weight each ball by (times_it_appeared + 1) / (total_draws + 39)
 
This is simple and stable, but it treats a draw from 2 years ago the same as last week's draw.
 
### Approach 3: The Optimizer (Maximum Likelihood Estimation)
This is where things got mathematically intense. Instead of just counting frequencies, I asked: **what probability distribution would have made the historical draws most likely to occur?**
 
The trick is that lottery draws aren't independent ball-by-ball events—you're picking a *set* of 6 balls without replacement. The probability of drawing {3, 7, 15, 22, 31, 38} is:
 
```
P(that exact set) = (w₃ × w₇ × w₁₅ × w₂₂ × w₃₁ × w₃₈) / [sum over all 3.2M possible sets]
```
 
This model has no intuition, it just finds the weights that maximize the likelihood of what actually happened.
 
**Convergence**: Surprisingly good! Converged in >95% of test cases despite being a non-convex optimization problem.
 
### Approach 4: The Adapter (Exponentially Weighted Moving Average)
This model assumes recent draws matter more than old ones. Maybe balls get replaced, or the lottery changes equipment.
I used an exponential decay where last week's draw counts way more than a draw from a year ago.
 
**Memory**: Effective window of about 20 draws (that's the λ=0.95 decay parameter)
 
This is my bet for detecting non-stationarity in the lottery mechanism.
 
## How I Tested This
 
Here's the critical part: I couldn't just fit models on all the data and evaluate on the same data—that's cheating and would give wildly optimistic results. Instead, I did a **rolling backtest**:
 
1. Start with the first 100 draws as a warm-up period
2. At time t, train models only on draws 1 through t
3. Predict draw t+1 (which the models have never seen)
4. Score the prediction using log-probability
5. Move to t+1, retrain everything, predict t+2
6. Repeat for 100+ out-of-sample predictions
This is exactly how you'd use the model in real life: learn from the past,
 predict the future, then find out what happened. No look-ahead bias.
 
**Scoring**: Log-likelihood (a "proper scoring rule" that penalizes overconfident wrong predictions more than uncertain wrong predictions)
 
## The Results
 
Here's what shocked me: **the models beat random**.
 
| Model | Mean Log-Likelihood | What This Means |
|-------|---------------------|-----------------|
| **Exact MLE** | Best | The optimizer found real signal |
| **EWMA** | Close 2nd | Recent patterns matter |
| **Simple Frequency** | 3rd | Basic counting works somewhat |
| **Uniform Random** | Worst | Ignoring data loses information |
 
The MLE model consistently outperformed on out-of-sample draws. The EWMA model caught up in later periods, suggesting the lottery mechanism might actually be non-stationary (changing over time).
 
**Cumulative Performance**: Over 100+ test draws, the MLE model pulled ahead more and more. This isn't luck—this is systematic outperformance.
 
## The Million-Peso Question: Should You Play?
 
Let's be absolutely clear: **No. Still no.**
 
Even though the MLE model found patterns, your odds are still catastrophically bad. Let's say the best model gives you a 2x improvement over random (which is generous). That changes your odds from:
 
- 1 in 3,262,623 → 1 in 1,631,311
You're still more likely to:
- Get struck by lightning **twice**
- Get dealt a royal flush **twice in a row**
- Find a four-leaf clover while being struck by lightning
The Mexican lottery has a house edge of roughly 50% (they keep half of ticket sales). No amount of statistical modeling overcomes that. The expected value of a $20 ticket is about $10 back in prizes. You're just lighting money on fire more slowly.
 
## What I Actually Learned
 
### 1. Lotteries Probably Aren't Perfectly Random
The fact that models beat uniform suggests there's *something* non-random happening. This could be:
- Ball wear (some balls get lighter/heavier over time)
- Systematic replacement (they swap balls on a schedule)
- Temperature/humidity effects
- Mechanical biases in the tumbler
None of this is fraud it's just physics. Perfect randomness is really hard to achieve.
 
### 2. Recent Data Matters More
The EWMA model's strong performance suggests the distribution shifts over time. Ball #7 might have been "jinxed" for a few months if it got replaced with a slightly heavier ball, then the bias disappears when they swap balls again.
 
### 3. Proper Modeling Beats Naive Counting
Just counting frequencies (what most people do) underperforms the MLE approach. The set-likelihood framework respects the combinatorial structure of the problem, you're picking 6 balls without replacement, not sampling 6 independent events.
 
## Code & Reproducibility
 
Full R code with dplyr/tidyr pipeline, custom DP algorithms, and ggplot2 visualizations available on GitHub. Everything is reproducible from raw CSV data.
 
**Tech Stack**: R, BFGS optimization, rolling cross-validation
 
## Final Thoughts
 
The models work *way better than random*, but not *nearly well enough* to overcome the house edge. The lottery is still a terrible financial decision.

 
---
 
*Disclaimer: This is for educational purposes only. Do not gamble money you can't afford to lose. The lottery is designed to take your money, and math confirms this.*
