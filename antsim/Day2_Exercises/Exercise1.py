
"""
EXERCISE 1:
Currently, the antsim model initializes all ants to start at (0,0) in our plot. Modify the initialization so that the
ants are randomly distributed in the plot (which ranges from (-1,1) in both x and y directions).
"""

import pylab as pl
import sciris as sc

sc.options(dpi=200)


class Antsim:
    ''' Simulation of ants randomly walking '''    
    
    def makeants(self, numants=50):
        ''' Initialize the ants '''
        self.numants = numants
        self.x = pl.zeros(numants)
        self.y = pl.zeros(numants)
    
    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.x += stepsize*pl.randn(self.numants)
            self.y += stepsize*pl.randn(self.numants)
            pl.scatter(self.x, self.y, color=self.colors)
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t+1, timesteps))
            pl.pause(1e-3)
            

# Run the simulation
sim = Antsim()
sim.makeants(numants=100)
sim.plotants()
