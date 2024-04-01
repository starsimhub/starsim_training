"""
Solution for tutorial 4.5
"""

import numpy as np
import sciris as sc
import pylab as pl


# Set default parameters
default_pars = sc.objdict(
    beta = 0.2, # Infection rate per contact per unit time
    gamma = 0.1, # Recovery rate
    n_contacts = 10, # Number of people each person is connected to
    distance = 0.1, # The distance over which people form contacts
    I0 = 1, # Number of people initially infected
    N = 100, # Total population size
    maxtime = 20, # How long to simulate for
    dt = 0.2, # Size of the timestep
    seed = 3495, # Random seed to use -- NB, not all seeds "take off"
    colors = sc.objdict(S='darkgreen', I='gold', R='skyblue'),
    save_movie = False, # Whether to save the movie (slow)
)


# Define the data
data = np.array(
[ 1,  2,  3,  3,  4,  4,  4,  6,  6,  9,  9, 12, 14, 15, 17, 17, 16,
 15, 15, 15, 18, 22, 27, 35, 36, 39, 40, 43, 45, 46, 48, 49, 55, 55,
 58, 58, 58, 54, 54, 54, 55, 53, 50, 48, 45, 45, 42, 43, 42, 41, 41,
 40, 42, 41, 40, 40, 38, 38, 39, 39, 38, 39, 39, 37, 38, 36, 37, 36,
 34, 31, 30, 29, 28, 28, 27, 26, 26, 26, 25, 24, 23, 23, 23, 23, 23,
 23, 23, 23, 22, 21, 20, 18, 18, 18, 18, 18, 18, 18, 19, 19]
)
time = np.arange(len(data))*default_pars.dt

# EXERCISE: Plot the data
fig = pl.figure()
pl.scatter(time, data, c='k')
pl.xlabel('Time')
pl.ylabel('Infections')


class Person(sc.dictobj):
    """
    Define each person (agent) in SimpleABM

    They have three (mutually exclusive) states: susceptible (S), infected (I),
    recovered (R). They also have x,y coordinates for plotting.
    """

    def __init__(self, pars):
        self.pars = pars
        self.S = True # People start off susceptible
        self.I = False
        self.R = False
        self.x = np.random.rand()
        self.y = np.random.rand()

    def infect(self):
        self.S = False
        self.I = True

    def recover(self):
        self.I = False
        self.R = True

    def check_infection(self, other):
        pars = self.pars
        if self.S: # A person must be susceptible to be infected
            if other.I: # The other person must be infectious
                if np.random.rand() < pars.beta*pars.dt: # Infection is probabilistic
                    self.infect()

    def check_recovery(self):
        pars = self.pars
        if self.I: # A person must be infected to recover
            if np.random.rand() < pars.gamma*pars.dt: # Recovery is also probabilistic
                self.recover()


class Sim(sc.dictobj):
    """
    Define the simulation
    """

    def __init__(self, **kwargs):
        pars = sc.mergedicts(default_pars, kwargs) # Parameters to use
        pars.npts = int(pars.maxtime/pars.dt) # Number of points
        self.T = np.arange(pars.npts)
        self.time = self.T*pars.dt
        self.pars = pars
        self.initialize()

    def initialize(self):
        """ Initialize everything (sim can be re-initialized as well) """
        pars = self.pars

        # Initilaize people and the network
        np.random.seed(pars.seed)
        self.people = [Person(pars) for i in range(pars.N)] # Create all the people
        for person in self.people[0:pars.I0]: # Make the first I0 people infectious
            person.infect() # Set the initial conditions
        self.make_network()

        # Initial conditions
        self.S = np.zeros(pars.npts)
        self.I = np.zeros(pars.npts)
        self.R = np.zeros(pars.npts)
        self.S_full = []
        self.I_full = []
        self.R_full = []

    def get_xy(self):
        """ Get the location of each agent """
        x = np.array([p.x for p in self.people])
        y = np.array([p.y for p in self.people])
        return x,y

    def make_network(self):
        """ Create the network by pairing agents who are close to each other """
        pars = self.pars
        x,y = self.get_xy()
        dist = np.zeros((pars.N, pars.N))
        for i in range(pars.N):
            dist[i,:] = 1 + ((x - x[i])**2 + (y - y[i])**2)**0.5/self.pars.distance
            dist[i,i] = np.inf

        rnds = np.random.rand(pars.N, pars.N)
        ratios = dist/rnds
        order = np.argsort(ratios, axis=None)
        inds = order[0:int(pars.N*pars.n_contacts/2)]
        contacts = np.unravel_index(inds, ratios.shape)
        self.contacts = np.vstack(contacts).T

    # EXERCISE: write a method "check_infections" that checks for infections among pairs of people in the contacts
    def check_infections(self):
        """ Check which agents become infected """
        for p1,p2 in self.contacts:
            person1 = self.people[p1]
            person2 = self.people[p2]
            person1.check_infection(person2)
            person2.check_infection(person1)

    def check_recoveries(self):
        """ Check which agents recover """
        for person in self.people:
            person.check_recovery()

    def count(self, t):
        """ Count the number of agents in each state """
        this_S = []
        this_I = []
        this_R = []
        for i,person in enumerate(self.people):
            if person.S: this_S.append(i)
            if person.I: this_I.append(i)
            if person.R: this_R.append(i)

        self.S[t] += len(this_S)
        self.I[t] += len(this_I)
        self.R[t] += len(this_R)

    def run(self):
        """ Run the simulation by integrating over time """
        for t in self.T:
            self.check_infections() # Check which infectious occur
            self.check_recoveries() # Check which recoveries occur
            self.count(t) # Store results

    def plot(self):
        """ Plot numbers of S, I, R over time """
        pl.figure()
        cols = self.pars.colors
        pl.plot(self.time, self.S, label='Susceptible', c=cols.S)
        pl.plot(self.time, self.I, label='Infected', c=cols.I)
        pl.plot(self.time, self.R, label='Recovered', c=cols.R)
        
        # EXERCISE: plot the data
        pl.scatter(time, data, c='k', label='Data')
        
        pl.legend()
        pl.xlabel('Time')
        pl.ylabel('Number of people')
        pl.ylim(bottom=0)
        pl.xlim(left=0)
        pl.show()


if __name__ == '__main__':

    # Create and run the simulation
    sim = Sim()
    sim.run()
    sim.plot()