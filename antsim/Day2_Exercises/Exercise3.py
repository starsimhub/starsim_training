
"""
EXERCISE 3:
Now, we want the ants to be drawn toward the food source they are closest to over time. Incorporate this into the model
(Hint: This might be best organized with the creation of a new function)
"""

import pylab as pl
import sciris as sc
import numpy as np

sc.options(dpi=200)


class Antsim:
    ''' Simulation of ants randomly walking '''

    def makeants(self, numants=50, num_food_sources=2):
        ''' Initialize the ants '''
        self.numants = numants
        self.num_food_sources = num_food_sources
        self.x = np.random.uniform(-1,1,100)
        self.y = np.random.uniform(-1,1,100)

        ''' Initialize food sources '''
        self.x_food = np.random.uniform(-1, 1, num_food_sources)
        self.y_food = np.random.uniform(-1, 1, num_food_sources)

    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.x += stepsize * pl.randn(self.numants)
            self.y += stepsize * pl.randn(self.numants)
            pl.scatter(self.x, self.y)
            pl.scatter(self.x_food, self.y_food, color='green', marker='x')
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)


# Run the simulation
sim = Antsim()
sim.makeants(numants=100, num_food_sources=2)
sim.plotants()
