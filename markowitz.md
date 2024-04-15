# Markowitz Model in Python

The Markowitz model, also known as Modern Portfolio Theory (MPT), is a framework for building investment portfolios that optimize returns for a given level of risk. 
It emphasizes diversification, the idea that by combining assets with different risk profiles, you can reduce overall portfolio risk without sacrificing returns.

After reading my father in law's thesis about this subject, I decided to reproduce what he made but now on a programming language such as Python but with a twist.
The main issue on the thesis was that the algorithm took all of the assets on [^MXX](https://finance.yahoo.com/quote/%5EMXX?.tsrc=fin-srch) and there was no change at all.
All assets were at least needed to be allocated. 
In my solution, I proposed to randomly select 9 to 10 assets on the portfolio and get the mean returns and risk for that specific selection. 
On each iteration, 100,000 portfolios were generated and an efficient frontier was graphed. 
The assets used were S&P 500 and Nasdaq 100. 
On each iteration I used this strategy on 2022 Reto Actinver. 

![Efficient Frontier in one Iteration](https://storage.googleapis.com/objects-hosted/Screenshot%202024-04-15%20at%208.50.40%20AM.png)

![Portfolio results](https://storage.googleapis.com/objects-hosted/Screenshot%202024-04-15%20at%208.55.31%20AM.png)
![Portfolio results](https://storage.googleapis.com/objects-hosted/Screenshot%202024-04-15%20at%208.56.04%20AM.png)
![Portfolio results](https://storage.googleapis.com/objects-hosted/Screenshot%202024-04-15%20at%208.56.39%20AM.png)
