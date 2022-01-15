# LOB-feature-analysis
Complete dataset available [here](https://drive.google.com/drive/folders/1LP0KT5O1YQT1Vf3692nPeoT5SCsrJtUk?usp=sharing)

##  Setup a working environment (Linux only)
1. Create environment:

    `conda list --explicit > spec-file.txt`
    
    `conda create --name projectenv --file spec-file.txt`

2. Install package: go to `*/anaconda3/envs/projectenv/lib/python3.<version_num>/site-packages` in your file system and paste the .so file and the folder that you can find in `package` folder. 
    For instance:
    
    `cd /opt/anaconda3/envs/projectenv/lib/python3.8/site-packages`
    
    `cp path/db_lob.cpython-39-x86_64-linux-gnu.so .`
    
    `cp -r path/db_lob-0.0.5.dist-info .`
    
3. Work in the new enviroment:
    `conda activate projectenv`
    
4. Create kernel:
    `conda install ipykernel`
    `ipython kernel install --user --name=projectenv`

## What is a limit order book (LOB)?
A LOB is essentially a data structure that contains all the orders sent to the market, with their characteristics: sign of the order (buy or sell), price, volume, timestamp etc. So it contains, at any given point in time, on a given market, the list of all the transactions that one could possibly perform on this market.

<p align="center">
<img src="figures/LOB.png"  width="600"/> </p>

The main idea is that trades occur when orders of different sides match their prices: a side takes on the role of the *aggressor* at a given price, and if there is a resting order on the other side at the same price the trade happens.

Therefore, since bidders want to buy at the lower possible price, the most appealing order for a bidder is the level of the ask side corresponding to the lower price. On the other hand, traders on the ask side want to sell at the highest price, thus the most appealing trades correspond to the highest price on the the bid side.


### Types of orders 
Essentially, three types of orders can be submitted:

* Limit order: to specify a price at which one is willing to buy or sell a certain number of shares, with their corresponding price and quantity, at any point in time;
* Market order: to immediately buy or sell a certain quantity, at the best available opposite quote;
* Cancellation order: to cancel an existing limit order.


## Order flow imbalance

The LOB can be used to see how the shift in orders volumes and prices can give information about the future movement of prices. In particular, the Order flow imbalance (OFI) and its multi-level counterpart Multi Level OFI (MLOFI), may be employed as a price predictor. 
For instance, if we consider the first level of the book informally define the order flow imbalance as the imbalance between demand and supply at the best bid and ask prices. Thus, it has an explanatory power of the traders' intentions.



The formal definition follows:

<p align="center">
<img src="figures/OFI.png"  width="800"/> </p>

Let us now consider as an examples how the LOB evolves if we consider it up to the second level:

<p align="center">
<img src="figures/OFI_ex1.png"  width="800"/> </p>

<p align="center">
<img src="figures/OFI_ex2.png"  width="800"/> </p>


## Probability of Informed Trading

The probability of informed trading (PIN) measures how likely it is that some players engage in informed trading, while the rest simply trade randomly.
Such quantity depends on the following parameters:
* alpha: probability that new information will arrive within the timeframe of the analysis;
* delta: probability 𝛿 that the news will be bad;
* mu: rate of arrival of informed traders;
* epsilon: rate of arrival of uninformed traders.

Once these parameters are known it can be computed by applying a maximum likelihood approach:

<p align="center">
<img src="figures/pin_formula.png"  width="200"/> 
</p>

<p align="center">
<img src="figures/pin_likelihood.png"  width="800"/> 
</p>

## Resources

