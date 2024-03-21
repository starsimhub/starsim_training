
"""
EXERCISE 2:
Modify the antsim model to initialize three ‘food sources’ as part of the model. They can be assigned random x,y values
in the space/plot, but make sure they are a different color than the ants so that you can see them in the plots.
"""

import pylab as pl
import sciris as sc
import numpy as np

sc.options(dpi=200)


class Antsim:
    ''' Simulation of ants randomly walking '''
    #
    def makeants(self, num_ants=50):
        ''' Initialize the ants '''
        self.num_ants = num_ants
        self.x = np.random.uniform(-1,1,100)
        self.y = np.random.uniform(-1,1,100)

        # Initialize food sources. Consider what parameters these food sources need to have (how many? where?)

    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.x += stepsize * pl.randn(self.num_ants)
            self.y += stepsize * pl.randn(self.num_ants)
            # Keep ants within bounds
            self.x = pl.clip(self.x, -1, 1)
            self.y = pl.clip(self.y, -1, 1)
            pl.scatter(self.x, self.y)
            # Plot the food sources
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)


# Run the simulation
sim = Antsim()
sim.makeants(num_ants=100)  # Include the number of food sources as an argument to initialize the sim
sim.plotants()
