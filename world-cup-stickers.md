
# World Cup Stickers How much it costs to get the whole collection? 

![World Cup Album](https://i0.wp.com/kupuni.mt/wp-content/uploads/2026/04/Album-and-50.png?w=963&ssl=1)

The World Cup is around the corner and a couple of weeks ago Panini just
announced the pre-sale for the World Cup sticker album. I am incredibly
excited for this collection as I've been collecting all World Cup Sticker
albums since Korea-Japan 2002. I remember my mom arriving from work with
sticker packs for us to open and see which player would show up or if it was
a holo sticker with the logo of a nation. 

As years went by and after opening thousands of sticker packs throughout my
life I wondered: just how much it costs to collect all stickers? I've had the
privilege of collecting them all but now I want to understand the cost as a
whole instead of just buying and trading stickers with my friends. And this is
how this new project came up. 

## The setup: 

Panini announced that this album would contain 980 stickers, the biggest
collection ever. Now it was the moment, how could I model this? 

What we know: 

- 980 stickers
- 25 mxn a pack
- 7 stickers each

## The Collector Coupon Problem

There is something important to note on. If we were making simple math it just
needs to be buying 140 packs and that's it! Collection complete. But that's not
the case, we know that this is random and at first all of our stickers will be
new to us. But as we rip more and more packs we are going to be frustrated. 

This works with the following expectancy:

$$ E[X]=\sum_{k=1}^{N}\frac{N}{N-i+1} $$

Let $k=N-i+1$

$$ E[X]=N\sum_{k=1}^{N}\frac{1}{k}=N\cdot H(N) $$

where $H(N)$ is the Nth harmonic number

$$ H(N)=1+\frac{1}{2}+\frac{1}{3}+...+\frac{1}{N} $$

For large N, this behaves asymptotically as:
 
$$H(N) \approx \ln(N) + \gamma$$
 
where $\gamma \approx 0.5772$ is the Euler-Mascheroni constant.
 
You need roughly $N \cdot \ln(N)$ stickers
to complete a collection of N items **much more than just N**.

## The theoretical Cost

```
N = 980

H(980) =1+ 1/2+ 1/3+...+1/980 = 7.645

Expected stickers needed = 980 × 7.465 = 7,316 stickers
Expected packs needed = 7,316 ÷ 7 = 1,045 packs
Expected cost = 1,045 × 25 MXN = 26,125 MXN
```

But this is just the **expected** cost, you could be way more unlucky.

## Monte Carlo Simulation
To validate these theoretical predictions and explore the full range of outcomes, I ran 10,000 Monte Carlo
simulations, essentially simulating 10,000 different collectors each trying to complete the album through pure random
pack purchasing.

### Basic Strategy No trading
If you wanted to do no trades you would get the following distribution: 

![Histogram of 10,000 collectors](https://lh3.googleusercontent.com/d/15EwFXE3XkmjHOEgMWqu0i1yjHuZXGGdz)

Not that much of efficiency. Understanding that each box of stickers contains
100 packs we are talking about 11 boxes. 

### Buying the last 50 stickers

Some things that Panini always considers is you can buy the last 50 stickers
directly from them. It is a considerable decrease in costs:

![Data for buying stickers](https://lh3.googleusercontent.com/d/1RMnvlcLPWNqQ9idu6pq09B_kLcYs1Qbr)

Our average cost for using a strategy in which we buy the last 50 stickers comes
down to a whooping $10,607 MXN making it a 60% discount! Much better right?

But what about one of the core things of collecting stickers? Trading with your
friends, I remember taking my missing list with my extra stickers to school so
on recess (or sometimes during classes) we would trade and negotiate for
stickers such as the Panini sticker which was extremely rare.

### Trading

I assumed 1 thing here: how much of my stack could I actually trade? 30%? 50%?
I evaluated trading 30, 50, and 70% and the results were: 

| Trade percentage | Mean Cost | Trades made |
|------------------|-----------|-------------|
| 30               | $6,250    | 265         |
| 50               | $5,000    | 327         |
| 70               | $5,000    | 367         |

And comparing the probabilities we get: 

![Cost Distribution and Probability of Completion](https://lh3.googleusercontent.com/d/1jSPepMXRnMn9suQR2FaTUIT4tlC9qJIL)


## What now? 

When I started this analysis, I simply wanted to understand the math behind something I've been doing passionately
since 2002. What I discovered was both shocking and enlightening.
The Numbers Don't Lie
The reality is random purchasing would set you back around 26,125 MXN on average. That's 7.5× more expensive!
But here's the good news: strategy matters enormously.
Key findings:

Pure random (no trading): ~26,125 MXN - financially painful and emotionally frustrating
Buying last 50 stickers: ~10,607 MXN (60% savings!) - smart and accessible
Active trading (50% efficiency): ~5,000 MXN (81% savings!) - the clear winner

The mathematics revealed something I intuitively knew from years of collecting: the social element—trading with friends
is not just fun, it's financially optimal. Those recess trades weren't just about completing our albums; they were about
beating the brutal economics of the Coupon Collector's Problem.

## My Strategy for 2026
Armed with this analysis, here's my plan for this World Cup:

Budget: 6,000-7,000 MXN roughly 2 and a half boxes
Approach:

Buy ~200-250 packs to enjoy the opening experience
Trade actively with friends and online communities (targeting 40-50% efficiency)
Once I hit 900-920 stickers, switch to buying singles for the final stretch


Expected outcome: Complete album for 6,000-7,000 MXN while maximizing the social and emotional experience.

[Back to main page](https://greg1997-dev.github.io/MyPortfolio/)
