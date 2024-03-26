import pylab as pl
import sciris as sc
import numpy as np

sc.options(dpi=200)


class Antsim:
    ''' Simulation of ants randomly walking '''

    def makeants(self, num_ants=50, num_food_sources=3):
        ''' Initialize the ants and food sources'''
        self.num_ants = num_ants
        self.x = np.random.uniform(-1,1,100)
        self.y = np.random.uniform(-1,1,100)

        ''' Initialize food sources '''
        self.num_food_sources = num_food_sources
        self.x_food = np.random.uniform(-1, 1, num_food_sources)
        self.y_food = np.random.uniform(-1, 1, num_food_sources)

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
            # Plot the ants and food sources
            pl.scatter(self.x, self.y)
            pl.scatter(self.x_food, self.y_food, color='green', marker='x')
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)


# Run the simulation
sim = Antsim()
sim.makeants(num_ants=100, num_food_sources=3)
sim.plotants()
