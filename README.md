# bachelor-thesis
Developing car driving agent in the TORCS virtual environment



Thesis -> https://github.com/Magikis/bachelor-thesis/blob/master/docs/bachelor_thesis.pdf


# Instructions


To run an agent use: `python main.py`
Use --help to look for available arguments.

Agents shortcuts:

* line-follower,
* tree -> Decision Tree single model,
* mlp -> Neural network single model,
* dma -> double agent model,
* dma-sh - >double agent model - shared history,
* sma -> single model agent,
* tma -> triple model agent



To run race without graphics run: `python ruPractice.py`

To run algorithms which learns optimal speed limits fot specific track run: `python speeed_limits_learner.py`


All driving logic is in directory `agents`.
All tracks XML's can be found in directory `tracks`
All models learning was done with jupyter notebooks available in root directory

Trained models can be found in `models directory`
