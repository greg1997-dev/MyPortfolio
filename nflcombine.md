# NFL Combine
The NFL Scouting Combine is an annual, week-long event held normally in February at Lucas Oil Stadium in Indianapolis. 
It's a crucial pre-draft showcase for top college football players hoping to be selected by NFL teams.  
Around 300 athletes are invited to perform a battery of physical and mental tests designed to assess their skills and potential on the field.

The core of the Combine is all about measurables. 
Players run the 40-yard dash, vertical jump, and broad jump to demonstrate speed, explosiveness, and agility. 
They also go through position-specific drills that showcase their technique and ability to perform game-like actions.

![Combine](https://storage.googleapis.com/objects-hosted/combine.jpeg)


However, this event doesn't really show the whole picture of a prospect for the NFL. 
In fact, my main hypothesis was that this specific event proved no impact on whether a CFB player would be selected or not. 
The only drill that could prove a difference would be the 40-yard dash while the other performance drills are not that important. 

## EDA

### Correlation Map
![Correlation map](https://storage.googleapis.com/objects-hosted/corr%20map.png)

At first glance on the variables that were selected, there is no clear correlation on any of the variables for a player to be selected. Being the strongest the 40-yd dash with a 5% correlation.
Note: the variables were already scaled when the correlation map was developed. 

### Identifying Outliers
![Distributions](https://storage.googleapis.com/objects-hosted/continuous%20variables%20combine.png)

When taking a look at the distributions of times and bench presses, we see there are no clear outliers so we can consider the entire dataset for training. 


### Position Distribution
![Positions](https://storage.googleapis.com/objects-hosted/newplot%20(3).png)
WRs are the most common position we can find within prospects for the draft, after that we find CB and RBs on the dataset. 
After that the most players that are noted are Linemen, whether offensive or defensive.

## Modelling
For the modelling we considered 3 different models and compare which is the best approach: 
* Logit
* Logit with L1 Penalization
* Random Forest

Even though the RF was the best performer when evaluating on the train dataset, turned out to be overfitted. This occurs a lot due to the Random Forest nature. 
On the other side, the L1 Penalization turned out to be the best performer when predicting the 2022 class. Also, a good model would be the one that can identify prospects (labeled as 1) without really being drafted, since that player could turn out to be a breakout player that other teams were not interested in. 
On the notable players the model recommends to draft that were not drafted is Cameron Dicker, Kicker for the Los Angeles Chargers and Jaylen Warren, RB for the Pittsburgh Steelers. 
On the other side, the model recommended to draft Brock Purdy. And the model recommended not to draft Tyler Allegier.

The results are presented below. I've only included the final model selected to show the metrics of it. 
Main metrics: On test data
* Score: 72.7%
* ROC AUC: 78.1%
* Precision: 72%
* Recall: 75%

### ROC Curve
![roc_auc](https://storage.googleapis.com/objects-hosted/roc_auc.png)

We see a really good ROC Curve. Meaning that the model is able to detect TP. 
Meaning it recommends slightly more as a scout. However, the model is able to identify undrafted players that can be good prospects.


### Coefficients
![Coefficients](https://storage.googleapis.com/objects-hosted/Screenshot%202024-04-16%20at%201.10.50%20PM.png)

On this summary we see that one of the most important variables is the 40 yd. Which is normally the most talked metric on NFL players, whereas variables such as School do not factor much into whether a player is being drafted or not. The other variables are the weight and the vertical jump. Curiously they work inversely. In a sport like Football one would think that bigger players are prone to be selected. In this case we see that weight works inversely for being drafted. 







