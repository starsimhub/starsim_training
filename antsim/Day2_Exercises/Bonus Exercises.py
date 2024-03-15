
"""
BONUS EXERCISE 1:
Modify the antsim model to initialize half of the ants to be red and half to be black. Make sure these colors are shown
on the ‘ants’ in the plot(s).

BONUS EXERCISE 2:
Let’s say we want to incorporate into the model that black ants move 50% faster than red ants. Modify the model to
implement this change in our agents/ants.
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
