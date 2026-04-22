---
layout: default
title: Andrés Gregori Portfolio
---

# 📊 [Which Pokémon Is Actually the Best?](https://gregolas-poke-pca.streamlit.app/)

- Applied Principal Component Analysis (PCA) to reduce 6 combat stats into 2 interpretable dimensions that capture
"overall battling power"
- Built an interactive Streamlit dashboard where you can visualize all 800+ Pokémon in 2D space
- **PC1 (43.3% of variance)**: Basically "raw power" how much total stats a Pokémon has
- **PC2 (19.1% of variance)**: Captures "stat distribution" balanced vs specialized builds

**The Verdict:**
After crunching the numbers on every Pokémon across all generations. Mewtwo is objectively the best. 

**Why PCA?**
You can't just add up all the stats (a Pokémon with 100 HP and 10 Attack isn't useful).
PCA finds the "directions" in stat-space that matter most for battling effectiveness,
then projects every Pokémon onto those axes. It's like finding the real dimensions that define strength.

**Explore It Yourself:** [Interactive Streamlit App](https://gregolas-poke-pca.streamlit.app/) - 
filter by generation, type, legendary status, and see where your favorite falls.

*** 

# 📈 [Markowitz Model for Optimal Portfolio](https://greg1997-dev.github.io/MyPortfolio/markowitz.html)
**Objective:** To develop a model that helped on trading challenges to select the
optimal portfolio each week to get the best profits in a return-risk trade-off.

- Multiple weeks sitting at top 3 places on best portfolios on Reto Actinver 2022.
- 5th Place National Award for Bloomberg Trading Challenge 2024.
- Worked as advisor for stock buying in Trading challenges.
- The methodology was:
  * Download the stock prices with the yfinance library
  * Clean the data and calculate:
    * Mean Returns
    * Log Returns
    * Portfolio Risk
    * Portfolio Returns
    * Sharpe Ratio
  * Create a function that created random weights for selecting a 10 stock 
  portfolio randomly.
  * Create 100,000 random portfolios.
  * Save the next best portfolio given the return.
 
***

# 🏈 [Finding Hidden NFL Talent: What the Combine Actually Reveals](https://greg1997-dev.github.io/MyPortfolio/nflcombine.html)

- Trained classification models (Logistic Regression vs Random Forest) to predict draft likelihood based purely on
combine measurables, the same data scouts use.
- Identified which physical measurements actually matter most for getting drafted.
- Tested hypothesis: Do different positions have statistically different measurement profiles?
- **Best model**: Logistic Regression with Lasso penalty (AUC = 0.72)
- **Most important features**: 40-yard dash time and weight dominated—speed and size are king

**Real-World Validation:**
The model flagged several undrafted players as "should have been drafted":
- **Cameron Dicker** (K, Chargers) - reliable NFL kicker and statistically the most efficient.  
- **Brock Purdy** (QB, 49ers) - one of the model's strongest recommendations.

***

# 🎲 [Can You Beat the Lottery? Testing the "Jinxed Numbers" Myth](https://greg1997-dev.github.io/MyPortfolio/lottery.html)
- Built 4 probabilistic models to test if Mexican Melate Retro draws show any detectable patterns
(spoiler: they do, but you still shouldn't play)
- Implemented set-likelihood MLE with dynamic programming to efficiently compute combinatorial probabilities over 3.2M
possible outcomes
- Rolling out-of-sample backtest on 100+ draws showed models consistently beat uniform random—suggesting mechanical
biases in lottery equipment
- Found evidence of non-stationarity: recent draws matter more (EWMA model), likely due to ball wear/replacement cycles
- **Bottom line**: Models work way better than random, but nowhere near enough to overcome the house edge.

***
# 🏈 [AI NFL Scout: RAG-Powered Draft Assistant That Actually Watches Tape](link-to-project)

- Developed a Retrieval Augmented Generation (RAG) system using GeminiAPI trained on the entire corpus of 2025 NFL Draft
scouting reports.
- Built an agentic system that doesn't just answer questions, it can run interactive mock drafts, making picks based on
team needs and big board rankings.
- LLM provides detailed player assessments and can compare/contrast prospects at the same position ("Is Marvin Harrison
Jr. or Malik Nabers the better WR1?")

Instead of just memorizing player stats, the RAG architecture lets the AI *retrieve relevant scouting context* before
answering. Ask about a linebacker's coverage skills? It pulls the actual film breakdowns that scouts wrote.
Want to compare two edge rushers' pass-rush moves? It synthesizes multiple expert opinions.

**The Agent Goes Further:**
- Runs interactive mock drafts where you GM your favorite team
- Makes realistic picks based on positional value + team needs (no AI is drafting a kicker in Round 1)
- Justifies every pick with scouting report excerpts—just like real war rooms

**Built for:** [Gen AI Intensive Course Capstone 2025Q1](https://www.kaggle.com/competitions/gen-ai-intensive-course-capstone-2025q1)

***


# 🎲 [Probability and Statistics Course at Universidad Panamericana](https://github.com/greg1997-dev/Prob_and_Stats)
 - Leveraging the R programming language, students were able to have a deeper 
 understanding of Probability and Statistics concepts such as:
    * Conditional Probability
    * Discrete Probability Distributions
    * Continuous Probability Distributions
    * Analysis of Variance
    * Experimental Design
 - **Upcoming term:** On the next term, students will have a reference guide, you can read the
[WIP here](https://github.com/greg1997-dev/MyPortfolio/blob/main/assets/Prob_and_stats_ref_guide.pdf).
 

***

# Predicting NFL Matches with different ML Models and variables
- Using publicly available data like scraping tables from Pro Football Reference,
Sports History Odds and NFLFastR
- Training Data of all games since 1999 to predict the 2023 season
- 72% Accuracy Score
- Variables referenced in
[(Delen,2012)](https://www.researchgate.net/publication/257026772_A_comparative_analysis_of_data_mining_methods_in_predicting_NCAA_bowl_outcomes)
were also relevant for our claim.
- Beats many state-of-the-art algorithms regarding prediction of games.

***

# 📊 [Sankey Report for Laboratory](https://lh3.googleusercontent.com/d/1C3QIvqY0B3pZy9ZgEhw95h5jiw_F4_Ry)
 - Developed an end-to-end data pipeline to provide ad hoc analytics on 
 evaluating Lab Workers to correctly identify blood cells through a specific
 methodology.
 - Whole architecture is hosted on GCP with the final product is delivered
 through Google Data Studio.
 - Participants in this quality program are evaluated in two ways: the monthly
 expert, and an expert consensus to insure an unbiased assessment.

***


# 🏀 [March Madness Kaggle Competition 2022](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/March_Madness.ipynb)

- This project was used in the
[March Machine Learning Mania 2022 - Men’s](https://www.kaggle.com/competitions/mens-march-mania-2022/overview)
competition to predict the bracket
- Logistic Regression with CV was used for predicting the bracket
- Avg. Log Loss of the algorithm 0.68492
- Calculate probability of win for a team
- Beat the auto bracket (all teams have equal probability to win)
- Predicted St. Peter's Peacocks upset over No.2 Seed Kentucky and No. 3 Seed
Purdue

***

# [NLP Project Assignment](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/Big_Data_Project.ipynb)

- Took Amazon Reviews Dataset (you can find the dataset
[here](https://www.kaggle.com/datasets/bittlingmayer/amazonreviews))
- Looked at the most common reviews
- EDA 
- Created a topic classifier with an Latent Dichrilet Allocator (LDA)
- Classified possitive topics into 10 different categories based on their sentiment score


***

# 🚗 [Insurance Project](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/Proyecto_Seguros.ipynb)

- Analyzed a Dataset and predict if a user would renew its insurance policy or
not
- After an EDA we identified that users without a license we the most likely to
not buy an insurance
- Users with older vehicles were more inclined to buy insurance policies
- Decision Tree was the best option for classifying users that were prone to buy
an insurance policy


# 📅 Schedule a Call

If you'd like to chat or collaborate, feel free to book a time with me:


<div style="min-width:320px;height:700px;">
  <iframe src="https://calendly.com/andrew-gregory-a_pb/30min" 
          width="100%" height="100%" frameborder="0" scrolling="no">
  </iframe>
</div>


