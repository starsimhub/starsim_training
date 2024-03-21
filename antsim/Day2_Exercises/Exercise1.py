
"""
EXERCISE 1:
Currently, the antsim model initializes all ants to start at (0,0) in our plot. Modify the initialization so that:
    1) the ants are randomly distributed in the plot (which ranges from (-1,1) in both x and y directions)
    2) the ants don't go outside the (-1,1) bound
"""

import pylab as pl
import sciris as sc

sc.options(dpi=200)


class Antsim:
    ''' Simulation of ants randomly walking '''    
    
    def makeants(self, num_ants=50):
        ''' Initialize the ants '''
        self.num_ants = num_ants
        self.x = pl.zeros(num_ants)  # Randomly distribute the x,y coordinates of the ants
        self.y = pl.zeros(num_ants)
    
    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.x += stepsize*pl.randn(self.num_ants)
            self.y += stepsize*pl.randn(self.num_ants)
            # Adjust ant positions if they go beyond the bounds
            pl.scatter(self.x, self.y)
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t+1, timesteps))
            pl.pause(1e-3)
            

# Run the simulation
sim = Antsim()
sim.makeants(num_ants=100)
sim.plotants()
