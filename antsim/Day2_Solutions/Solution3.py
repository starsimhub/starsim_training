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
            self.update_ant_positions(stepsize)
            pl.scatter(self.x, self.y)
            pl.scatter(self.x_food, self.y_food, color='green', marker='x')
            pl.xlim((-1, 1))
            pl.ylim((-1, 1))
            pl.title('t = %i / %i' % (t + 1, timesteps))
            pl.pause(1e-3)

    def update_ant_positions(self, stepsize):
        ''' Update ant positions based on random walk and attraction towards food sources '''

        # Determine which food source the ant is closest to
        for i in range(self.numants):
            min_distance_to_food = float('inf')
            closest_food_source = None
            for j in range(self.num_food_sources):
                distance_to_food = np.sqrt((self.x[i] - self.x_food[j]) ** 2 + (self.y[i] - self.y_food[j]) ** 2)
                if distance_to_food < min_distance_to_food:
                    min_distance_to_food = distance_to_food
                    closest_food_source = j
            # Move ant towards the closest food source
            if closest_food_source is not None:
                # Calculate the direction towards the food source
                direction_x = self.x_food[closest_food_source] - self.x[i]
                direction_y = self.y_food[closest_food_source] - self.y[i]

                # Normalize the direction vector
                direction_norm = np.sqrt(direction_x ** 2 + direction_y ** 2)
                direction_x /= direction_norm
                direction_y /= direction_norm

                # Update the ant's position towards the food source
                self.x[i] += stepsize * direction_x
                self.y[i] += stepsize * direction_y


# Run the simulation
sim = Antsim()
sim.makeants(numants=100, num_food_sources=2)
sim.plotants()
