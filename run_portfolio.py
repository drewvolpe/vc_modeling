
from collections import Counter
import random
import math

###
# Parameters of assumptions
###

# How many initial investments and avg check size
num_seed_rounds = 50
invested_per_seed_round = 0.5

# Probabilities of different outcomes (prob, outcome multiple)
outcome_probs_seed = [ [0.01, 100],  # N% chance of Mx return
                       [0.03, 20],
                       [0.03, 10],
                       [0.03, 6],
                       [0.25, 1],
                       [0.65, 0]]

follow_on_pct = 0.5 # % of deals in which fund invests in next round
invested_per_follow_on = 1.0 # avg size of follow-on investment
outcome_probs_follow = [ [0.02, 30],
                         [0.06, 15],
                         [0.06, 8],
                         [0.06, 4],
                         [0.30, 1],
                         [0.50, 0]]

# number of simulated portfolios to generate
num_simulations = 10000

# constants
fund_size = (num_seed_rounds * invested_per_seed_round) +\
            (num_seed_rounds * follow_on_pct * invested_per_follow_on)

###
# Classes
###

class Investment:
    def __init__(self, amt_in, outcome, is_seed=True):
        self.is_seed = is_seed
        self.amt_in = amt_in
        self.outcome = outcome

    @property
    def amt_out(self):
        return (self.outcome * self.amt_in)

class Portfolio:
    def __init__(self, investments):
        self.investments = investments

    @property
    def total_invested(self):
        return sum([i.amt_in for i in self.investments])

    @property
    def total_returned(self):
        return sum([i.amt_out for i in self.investments])

    @property
    def return_multiple(self):
        return ((self.total_returned*1.0) / self.total_invested)


    def __str__(self):
        l = ['invested: %s' % self.total_invested,
             'returned: %s' % self.total_returned,
             'return_multiple %s' % self.return_multiple,
             'num_deals_total %s' % len(self.investments),
             'num_deals_seed %s' % len([i for i in self.investments if i.is_seed]),
             'num_deals_follow %s' % len([i for i in self.investments if not i.is_seed]),
            ]
        return '%s' % l


###
# Funcs
##

def validate_params(): 
    if (sum([x[0] for x in outcome_probs_seed]) != 1.0):
        raise Exception("Seed probabilities don't add to 1! ")
    if (sum([x[0] for x in outcome_probs_follow]) != 1.0):
        raise Exception("Follow on probabilities don't add to 1! ")
               

def create_portfolio():
    investments = []

    # Seed rounds
    for i in range(0, num_seed_rounds):
        r = random.random()

        prob_sum = 0
        for (cur_prob, cur_outcome) in outcome_probs_seed:
            prob_sum += cur_prob
            if (r <= prob_sum):
                investments.append(Investment(invested_per_seed_round, cur_outcome))
                break

    # Follow on
    for i in range(0, num_seed_rounds):
        if (random.random() > follow_on_pct):
            continue # did not follow on

        r = random.random()  # for now, make them uncorrelated
        prob_sum = 0
        for (cur_prob, cur_outcome) in outcome_probs_follow:
            prob_sum += cur_prob
            if (r <= prob_sum):
                investments.append(Investment(invested_per_follow_on, cur_outcome, is_seed=False))

    return Portfolio(investments)


def run_simulations(num_iters):

    portfolios = []

    for i in range(0, num_iters):
        cur_portfolio = create_portfolio()
        portfolios.append(cur_portfolio)

    # print a few, for debugging
    print('Sample portfolios:')
    for p in portfolios[0:10]:
        print('    P: %s' % p)

    print('# of portfolios with different multiple returns')
    returns_counter = Counter([math.floor(p.return_multiple) for p in portfolios])
    for (ret, cnt) in sorted(returns_counter.items()):
        pct = 100 * ((cnt*1.0) / num_iters)
        print('  %sx - %s (%0.0f%%)' % (ret, cnt, pct))

    print('# of portfolios with different multiple returns (to 0.1x)')
    returns_counter = Counter([round(p.return_multiple,1) for p in portfolios])
    cum_pct = 0
    for (ret, cnt) in sorted(returns_counter.items()):
        pct = 100 * ((cnt*1.0) / num_iters)
        cum_pct += pct
        stars = '*' * int(pct*10)
        print('  %sx - %s (%0.0f%%) (%0.0f%%) %s' % (ret, cnt, pct, cum_pct, stars))


###
# main()
###

if __name__ == "__main__":

# for dev
#    random.seed(31331)

    print('starting...')
    
    print('validating params...')
    validate_params()    

    print('Parameters')
    print('    $%0.0fm fund which makes %s $%sm seed investments.' %\
        ( fund_size, num_seed_rounds, invested_per_seed_round))
    print('    Follows on with $%sm, %s of the time.' % (invested_per_follow_on, follow_on_pct))

    print('')
    print('Running portfolio simluation...')
    run_simulations(num_simulations)

    print('done.')

