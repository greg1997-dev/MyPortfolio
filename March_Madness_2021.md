# March Machine Learning Mania 2021 Algorithm 
This algoritm is not public in my Portfolio because the notebook in which I wrote it was lost 😖
However, I made some notes while I was writing the code and I want to state it in a MD document.
The competition in Kaggle, as well as the data can be found [here](https://www.kaggle.com/c/ncaam-march-mania-2021-spread/data)

## Data transformation
- In order to create a unique match identifier, we concatenated the WTeamID with the Season Year, and the Day Played to get a primary ket for the match. That way, we can identify more easily the stage in which the game is being played. 
   - We had a key '2016_1167_136' and this meant that it was the game in which 'CS Bakersfield' won on the First Four in 2016
   - This helped to join the seeds table 
   - Also helped to identify the regular season statistics of a certain team
- Analyze the regular season to make a feature with expected points for each team in the March Madness competitions. This means to create a new table with the TeamID and the Expected Points per game 


## Findings 
Big Correlation made in Offensive Rebounds and Field Goals made. 
Not always a high seed secured the victory, upsets can happen anytime. 
The average points distribution was normalized and the data distribution was pretty close to a Normal behavior.

## Feature Engineering
The variables that were created from different fields were: 
- Point Spread: this was WScore-LScore, also, this was the target for the algorithm realized. 
- Seed Spread: This was achieved by WSeed-LSeed and if the number was <0 it meant that the Winner had a higher seed and if it was greater than 0 the Loser had a higher seed (upset) 
- Region encoded: This was added to view if a region was more prone to win games given the strength of calendar and some regions have better basketball programs
- Expected Score: This was brought from their regular season performance, it was the average points they scored. To avoid a Bias, the data was splitted into two variables 
  - WinExpScore: The average of points scored when a team won
  - LoseExpScore: The average of points scored when a team lost
  - Splitting the data into two new variables was also going to help on the approximations because if a team appears at the Losing Column, the LoseExpScore was taken into consideration. 
- Win Ratio: We prefered to have a ratio instead of a win count because it is a normalized number and it helps the algorithm we will prepare. 
- OT Win Ration: If a game went to OT what is their Win Ratio, this is a disruptive variable and maybe some Teams will have a 0% Win Ratio either because they have never played an overtime or they have never won. 

## The ML Algorithm 


