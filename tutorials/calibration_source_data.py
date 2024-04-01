"""
Solution for tutorial 4.5 part 1
"""

import numpy as np
import sciris as sc
import pylab as pl

# EXERCISE: Find parameters that match the data
beta = 0.15
dur_inf = 10
seed = 1

# Set default parameters
default_pars = sc.objdict(
    beta = beta, # Infection rate per contact per unit time
    dur_inf = dur_inf, # Average time of infection
    n_contacts = 5, # Number of people each person is connected to
    I0 = 5, # Number of people initially infected
    N = 200, # Total population size
    maxtime = 20, # How long to simulate for
    dt = 0.2, # Size of the timestep
    seed = seed, # Random seed to use
    colors = sc.objdict(S='darkgreen', I='gold', R='skyblue'),
)


# Define the data -- from sim.I.astype(int)
data = np.array(
[ 7,  10,  16,  22,  26,  29,  35,  39,  48,  53,  59,  68,  77,
 85,  90,  95, 101, 107, 112, 124, 125, 129, 134, 137, 136, 135,
136, 134, 135, 137, 140, 140, 140, 142, 141, 137, 134, 129, 128,
126, 124, 125, 122, 118, 116, 114, 113, 109, 106, 105, 103,  99,
 96,  95,  92,  92,  92,  88,  88,  86,  84,  80,  80,  79,  79,
 76,  75,  72,  69,  68,  66,  66,  66,  66,  64,  61,  61,  61,
 61,  61,  60,  59,  58,  57,  57,  54,  49,  48,  47,  47,  47,
 47,  45,  45,  44,  44,  44,  44,  44,  41]
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
            if np.random.rand() < pars.dt/pars.dur_inf: # Recovery is also probabilistic
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

    def make_network(self):
        """ Create a random network """
        pars = self.pars
        self.contacts = []
        for i in range(pars.N):
            partners = np.random.randint(pars.N, size=pars.n_contacts)
            pairs = [[i,j] for j in partners if i != j]
            self.contacts.extend(pairs)

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
        self.check_mismatch() # Check the mismatch at the end of the run
    
    # EXERCISE: define average mismatch
    def check_mismatch(self):
        self.mismatch = abs(data - self.I).mean()

    def plot(self):
        """ Plot numbers of S, I, R over time """
        pl.figure()
        cols = self.pars.colors
        pl.plot(self.time, self.S, label='Susceptible', c=cols.S)
        pl.plot(self.time, self.I, label='Infected', c=cols.I)
        pl.plot(self.time, self.R, label='Recovered', c=cols.R)
        
        # EXERCISE: add the data to the plot
        pl.scatter(time, data, c='k', label='Data')
        
        pl.legend()
        pl.xlabel('Time')
        pl.ylabel('Number of people')
        
        # EXERCISE: add the goodness of fit/mismatch as a title to the plot
        pl.title(f'Mismatch: {self.mismatch:n}')
        
        pl.ylim(bottom=0)
        pl.xlim(left=0)
        pl.show()


if __name__ == '__main__':

    # Create and run the simulation
    sim = Sim()
    sim.run()
    sim.plot()