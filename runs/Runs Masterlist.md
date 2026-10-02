## Run 0
Tested new model architecture to set a baseline. Essentially failed, with the model predicting no pendulum movement.
- 40 trajectories
- 300 epochs
- 300 optimizer updates

## Run 1
Tried to expand the space of training data, sampling an 8x4 grid of initial conditions for training data. *Slight* improvement.
- 40 trajectories
- 300 epochs
- 300 optimizer updates
- Sampled 8x4 grid for training trajectories

## Run 2
Increased trajectory sample size from 40 to 100. Slight improvement on shared tests from 0 and 1, but overall higher error from the aggregate of the tests
- 100 trajectories
- 300 epochs
- 300 optimizer updates

## Run 3
Changed training procedures to have mini-batches and more frequent optimizer updates rather than once per epoch. Also used a learning-rate scheduler (this didn't do anythinga as the improvememtn never slowed). Performed better, started to see predicted oscillation.
- 40 trajectories
- 40 epochs
- 126 batches per epoch, 256 samples per batch
- 5040 optimizer updates

## Run 4
Changed to have even more optimizer updates, and it had VAST improvements.
- 40 trajectories
- 120 epochs
- 126 batches per epoch, 256 samples per batch
- 15120 optimizer updates

## Run 5
Changed to have more optimizer updates but fewer epochs, had slight improvement
- 40 trajectories
- 100 epochs
- 200 batches per epoch, 160 samples per batch
- 20000 optimizer updates

# Agent Instructions
Never edit this file; these are manual notes and should only ever be written by me.