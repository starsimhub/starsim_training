import sciris as sc
import numpy as np
import pylab as pl
import starsim as ss

data_baseline = np.array([
 1,  1,  1,  1,  2,  4, 10, 15, 22, 31, 45, 59, 75, 83, 90, 89,
85, 83, 79, 74, 64, 53, 46, 44, 43, 45, 51, 55, 57, 57, 61, 53,
51, 48, 40, 34, 29, 27, 22, 18, 16, 13, 11, 12, 12, 12, 13, 13,
14, 12, 13, 13, 13, 15, 17, 18, 19, 22, 24, 29, 38, 40, 44, 50,
53, 55, 58, 56, 53, 52, 48, 42, 37, 31, 28, 19, 16, 15, 13, 13,
12, 14, 13, 11, 13, 11, 13, 14, 15, 15, 13, 14, 16, 21, 21, 28,
36, 40, 42, 48, 49])

data_vaccine = np.array([
 1,  1,  1,  1,  2,  4, 10, 15, 22, 31, 45, 48, 55, 58, 56, 53,
49, 46, 38, 29, 24, 20, 17, 15, 16, 15, 20, 20, 21, 24, 26, 21,
23, 23, 24, 22, 18, 16, 15, 14, 12,  8,  6,  6,  5,  6,  6,  4,
 4,  3,  3,  3,  2,  4,  5,  7,  9, 10, 12, 14, 17, 19, 18, 20,
22, 23, 25, 24, 23, 23, 19, 19, 19, 15, 14, 11, 11, 10,  7,  6,
 6,  5,  3,  3,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
 0,  0,  0,  0,  0])


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


def make_run_sim(beta=0.05, waning=0.05, seed=1, vaccine=False, p=0.5, boost=2.0):
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
    if vaccine:
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


def plot(results, label=''):
    pl.title('Number of people infected')
    pl.plot(results.time, results.n_infected, 'o-', label=label)
    pl.legend()
    sc.figlayout()
    pl.show()
    

# Make, run, and plot the simulation
sc.options(dpi=200)
pars = dict(beta=0.08, waning=0.03, seed=9)
res1 = make_run_sim(**pars)
plot(res1, 'Baseline')
res2 = make_run_sim(**pars, vaccine=True, p=0.7, boost=10)
plot(res2, 'Vaccine')

# Save data
print(res1.n_infected.astype(int))
print(res2.n_infected.astype(int))

