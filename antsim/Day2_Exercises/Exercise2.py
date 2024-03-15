
"""
EXERCISE 2:
Modify the antsim model to initialize ‘food sources’ as part of the model. They can be assigned random x,y values in the
space/plot, but make sure they are a different color than the ants so you can see them in the plot(s).
"""

import pylab as pl
import sciris as sc
import numpy as np

sc.options(dpi=200)


class Antsim:
    ''' Simulation of ants randomly walking '''

    def makeants(self, numants=50):
        ''' Initialize the ants '''
        self.numants = numants
        self.x = np.random.uniform(-1,1,100)
        self.y = np.random.uniform(-1,1,100)

    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.x += stepsize * pl.randn(self.numants)
            self.y += stepsize * pl.randn(self.numants)
            pl.scatter(self.x, self.y)
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)


# Run the simulation
sim = Antsim()
sim.makeants(numants=100)
sim.plotants()
