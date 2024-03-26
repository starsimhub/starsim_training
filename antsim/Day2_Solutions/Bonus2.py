import pylab as pl
import sciris as sc

sc.options(dpi=200)

"""
Exercise: Let’s say we want to incorporate into the model that black ants move 50% faster than red ants. 
Modify Exercise2.py to implement this change in our agents.
"""

class Antsim:
    ''' Simulation of ants randomly walking '''

    def makeants(self, num_ants=50):
        ''' Initialize the ants '''
        self.num_ants = num_ants
        self.x = pl.zeros(num_ants)
        self.y = pl.zeros(num_ants)
        self.colors = ['red' if i < num_ants/2 else 'black' for i in range(num_ants)]
        # Assign speed multiplier for each ant based on its color
        self.speed_multipliers = [1.0 if color == 'red' else 1.5 for color in self.colors]


    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.x += stepsize * pl.randn(self.num_ants) * self.speed_multipliers
            self.y += stepsize * pl.randn(self.num_ants) * self.speed_multipliers
            pl.scatter(self.x, self.y, color=self.colors)
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)


# Run the simulation
sim = Antsim()
sim.makeants(num_ants=100)
sim.plotants()
