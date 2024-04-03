import sciris as sc
import numpy as np
import pylab as pl
import starsim as ss

class Vaccine(ss.Intervention):
    def __init__(self, ti=10, p=0.5, boost=2.0):
        super().__init__()
        self.ti = ti
        self.p = p
        self.boost = boost
    
    def apply(self, sim):
        if sim.ti == self.ti:
            sis = sim.diseases.sis
            eligible_ids = sim.people.uid[sis.susceptible]
            n_eligible = len(eligible_ids)
            is_vacc = np.random.rand(n_eligible) < self.p
            vacc_ids = eligible_ids[is_vacc]
            sis.immunity[vacc_ids] += self.boost


def make_run_sim(beta=0.05, waning=0.05, seed=1, vaccinate=False, p=0.5, boost=2.0):
    pars = dict(
        n_agents = 100,
        start = 0,
        end = 100,
        dt = 1.0,
        rand_seed = seed,
        networks = 'random',
        diseases = dict(
            type = 'sis',
            beta = beta,
            waning = waning,
        )
    )
    
    # Define "baseline" and "intervention" sims without and with the vaccine
    if vaccinate:
        vx = Vaccine(p=p, boost=boost)
        sim = ss.Sim(pars, interventions=vx)
    else:
        sim = ss.Sim(pars)
    
    # Run the simulation
    sim.run()
    results = sc.objdict()
    results.time = sim.yearvec
    results.n_infected = sim.results.sis.n_infected
    return results


def plot(results):
    # pl.figure()
    pl.title('Number of people infected')
    pl.plot(results.time, results.n_infected, 'o-', label='Baseline') # Plot baseline
    pl.legend()
    sc.figlayout()
    pl.show()
    
# Make, run, and plot the simulation
sc.options(dpi=200)
for i in range(10):
    results = make_run_sim(beta=0.08, waning=0.03, seed=i)
    plot(results)
    pl.title(i)
    pl.pause(0.5)