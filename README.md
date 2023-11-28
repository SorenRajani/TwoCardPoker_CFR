# TwoCardPoker_CFR
An analysis of a simplified 2 card version of poker using monte carlo counterfactual regret minimization. In this game, players are dealt a hand of two cards. The best hand is a pair, then a suit, then a high card. As normal, all ties are decided by high cards. Once cards are dealt and a 1 chip buy in is paid, there is one round of betting where bets are limited to 1 chip. 

Instead of running the algorithm on all possible hands, I chose to instead alias the hands to a score. Since this game is relatively small, I decided to give each strength hand its own score, however if one wanted to expand this game to be larger, for example flexible bet sizes, it would be adviseable to alias similar hands as well (ie pair 2's and pair 3's should be played almost identically).

# Files
cfr.py: This file specifies the counterfactual regret minimisation algorithm
mccfr.py: This file specifices the monte carlo cfr algorithm
train.py: This algorithm imports from either cfr or mccfr and produces a pickled bot
test_game.ipynb: This game goes over a simple method to interact with the bot
save.p: This is the pickled file of the bot, if you want to play against it you can download this and the notebook

# References:
This project is based on the following papers: 
* https://proceedings.neurips.cc/paper/2012/file/3df1d4b96d8976ff5986393e8767f5b2-Paper.pdf
* https://www.science.org/doi/10.1126/science.aay2400


The code is an adaptation of the code provided by Ian Sullivan in their video series on the topic: 
* https://www.youtube.com/watch?v=Wa-fRIBGZZI&t=350s
