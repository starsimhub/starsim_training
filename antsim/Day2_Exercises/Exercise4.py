
"""
EXERCISE 4:
Now, have the ants (in addition to moving randomly) also move slightly closer to the food based on their
levels of attraction we calculated in Exercise 3. Add this logic to the 'update_ant_positions' function we started
for you below.
"""

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

    def calculate_attraction(self):
        ''' Calculate each ant's attraction toward each food source '''

        # Initialize attraction arrays
        self.attraction_x = np.zeros((self.num_ants, self.num_food_sources))
        self.attraction_y = np.zeros((self.num_ants, self.num_food_sources))

        # Calculate attraction towards each food source
        for i in range(self.num_ants):
            for j in range(self.num_food_sources):
                # Calculate distance between ant and food source
                direction_x = self.x_food[j] - self.x[i]
                direction_y = self.y_food[j] - self.y[i]
                distance_to_food = np.sqrt(direction_x ** 2 + direction_y ** 2)

                # Update attraction arrays (proportional to 1/distance)
                if distance_to_food != 0:
                    self.attraction_x[i, j] = direction_x / distance_to_food
                    self.attraction_y[i, j] = direction_y / distance_to_food

    def plotants(self, timesteps=150, stepsize=0.03):
        ''' Plot the ants '''
        pl.figure()
        for t in range(timesteps):
            pl.clf()
            self.calculate_attraction()
            self.update_ant_positions(stepsize)

            # Plot the ants and food sources
            pl.scatter(self.x, self.y)
            pl.scatter(self.x_food, self.y_food, color='green', marker='x')
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)

    def update_ant_positions(self, stepsize):
        ''' Update ant positions based on random walk and attraction towards food sources '''

        # Move ants randomly
        self.x += stepsize * pl.randn(self.num_ants)
        self.y += stepsize * pl.randn(self.num_ants)

        # Add small additional movement towards food based on attraction

        # Keep ants within bounds
        self.x = pl.clip(self.x, -1, 1)
        self.y = pl.clip(self.y, -1, 1)

# Run the simulation
sim = Antsim()
sim.makeants(num_ants=100, num_food_sources=3)
sim.plotants()