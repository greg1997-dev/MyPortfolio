# MyPortfolio
My Data Science Portfolio

***

# [NLP Project Assignment](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/Big_Data_Project.ipynb)
- Took Amazon Reviews Dataset (you can find the dataset [here](https://www.kaggle.com/datasets/bittlingmayer/amazonreviews))
- Looked at the most common reviews
- EDA 
- Created a topic classifier with an Latent Dichrilet Allocator (LDA)
- Classified possitive topics into 10 different categories based on their sentiment score
***

# [Titanic Kaggle Competition](https://github.com/greg1997-dev/Titanic_Kaggle_Competition/blob/main/notebooks/Titanic_Kaggle_Competition.ipynb)
- The most recommended Kaggle competition to get your hands on ML
- Voter Classifier that included distinct methodologies
- Feature engineering on deck in which passenger was assigned
- Filled NULL values in numeric dimensions with average of the column
- This project graded 0.77751 on accuracy
*** 

# [NFL Combine measurements importance](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/NFL_Combine.ipynb)
- This project was to try to identify the most important variables for scouts to Draft a Prospect
- Compared Logistic Regression vs Random Forest Classifier and provide a better example
- Random Forest Classifier with high recall
- RFC with 700 trees
- School from which the prospect comes, 40 yd dash time, and Weight are the most important features
- AUC=0.82
## Next Steps on NFL Combine Model
- We are using merely the Combine to determine if we draft a player or not, further data is required.
- There are great prospects that don't assist to the combine or they do a Pro Day at their campus. That is why names like Derek Stingley Jr, Drake London, Kenny Pickett that the model opts to not draft. The model may have a selection bias due to variable omission.
- Hyperparameter tuning would be a nice to have within the Pipeline. The model is compiled merely "as-is" from SciKit Learn.
- We are interested on the players that are marked as drafted but they weren't. We could find a hidden gem on it.

***
# [March Madness Kaggle Competition 2022](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/March_Madness.ipynb)
- This project was used in the [March Machine Learning Mania 2022 - Men’s](https://www.kaggle.com/competitions/mens-march-mania-2022/overview) competition to predict the bracket
- Logistic Regression with CV was used for predicting the bracket
- Avg. Log Loss of the algorithm 0.68492
- Calculate probability of win for a team
- Beat the auto bracket (all teams have equal probability to win)
- Predicted St. Peter's Peacocks upset over No.2 Seed Kentucky and No. 3 Seed Purdue

***
# [Insurance Project](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/Proyecto_Seguros.ipynb)
- Analyzed a Dataset and predict if a user would renew its insurance policy or not
- After an EDA we identified that users without a license we the most likely to not buy an insurance
- Users with older vehicles were more inclined to buy insurance policies
- Decision Tree was the best option for classifying users that were prone to buy an insurance policy
***

# [Markowitz Model for Optimal Portfolio](https://github.com/greg1997-dev/MyPortfolio/blob/main/notebooks/Markowitz.ipynb)
- Multiple weeks sitting at top 3 places on best portfolios on Trading Challenge called Reto Actinver
- The methodology was:
  * Download the stock prices with the yfinance library
  * Clean the data and calculate:
    * Mean Returns
    * Log Returns
    * Portfolio Risk
    * Portfolio Returns
    * Sharpe Ratio
  * Create a function that created random weights for selecting a 10 stock portfolio randomly
  * Create 100,000 random portfolios 
  * Save the next best portfolio given the return
