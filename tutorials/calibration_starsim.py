"""
Solution for tutorial 4.5 part 2
"""

import numpy as np
import sciris as sc
import starsim as ss
import pylab as pl

# Set calibration parameters
beta = 0.25
gamma = 0.1
seed = 4

# Define the colors
colors = sc.objdict(S='darkgreen', I='gold', R='skyblue')

pars = sc.objdict(
    n_agents = 200,
    start = 0,
    end = 20,
    dt = 0.2,
    diseases = dict(
        type = 'sir',
        beta = beta,
        dur_inf = ss.expon(scale=1/gamma),
        init_prev = 5/200,
        p_death = 0,
    ),
    networks = dict(
        type = 'static',
        n_contacts = 5,
    ),
    rand_seed = seed,
)


# Define the data -- from sim.I.astype(int)
data = np.array(
[ 6,  11,  14,  15,  17,  20,  25,  31,  40,  47,  52,  57,  66,
 75,  85,  93,  99, 100, 107, 111, 112, 118, 123, 117, 120, 122,
122, 123, 123, 125, 122, 120, 119, 110, 112, 117, 115, 118, 117,
113, 115, 112, 111, 107, 105, 103, 101,  99, 100,  99,  98,  97,
 94,  93,  92,  91,  89,  88,  88,  87,  86,  83,  81,  80,  78,
 76,  76,  73,  72,  71,  71,  71,  69,  68,  67,  65,  61,  58,
 57,  56,  56,  54,  52,  51,  51,  49,  49,  47,  46,  46,  46,
 46,  45,  45,  45,  43,  43,  40,  37,  36]
)
time = np.arange(len(data))*pars.dt


class check_mismatch(ss.Analyzer):
    def finalize(self, sim):
        self.sim = sim # Used for plotting
        res = sim.diseases.sir.results
        self.mismatch = abs(data - res.n_infected[:len(data)]).mean()
    
    def plot(self):
        """ Plot numbers of S, I, R over time """
        pl.figure()
        res = self.sim.diseases.sir.results
        tvec = self.sim.yearvec
        pl.plot(tvec, res.n_susceptible, label='Susceptible', c=colors.S)
        pl.plot(tvec, res.n_infected, label='Infected', c=colors.I)
        pl.plot(tvec, res.n_recovered, label='Recovered', c=colors.R)
        
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
    np.random.seed(seed)
    check_mismatch = check_mismatch()
    sim = ss.Sim(pars, analyzers=check_mismatch)
    sim.run()
    check_mismatch.plot()