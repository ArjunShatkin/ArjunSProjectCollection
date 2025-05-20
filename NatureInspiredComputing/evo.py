"""
File: evo.py
Description: A concise evolutionary computing framework for solving
            multi-objective optimization problems!
"""

import random as rnd
import copy   # doing deep copies of solutions when generating offspring
from functools import reduce  # for discarding dominated (bad) solutions
import numpy as np
import pandas as pd
import time


class Evo:

    def __init__(self):
        """framework constructor"""
        self.pop = {}  # population of solutions: evaluation --> solution
        self.fitness = {}  # objectives:    name --> objective function (f)
        self.agents = {}  # agents:   name --> (operator/function,  num_solutions_input)

    def add_objective(self, name, f):
        """ Register a new objective for evaluating solutions """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Register an agent take works on k input solutions """
        self.agents[name] = (op, k)

    def get_random_solutions(self, k=1):
        """ Picks k random solutions from the population
        and returns them as a list of deep-copies """
        if len(self.pop) == 0:  # No solutions - this shouldn't happen!
            return []
        else:
            solutions = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]


    def add_solution(self, sol):
        """ Adds the solution to the current population.
        Added solutions are evaluated wrt each registered objective. """

        # Create the evaluation key
        # key:  ( (objname1, objvalue1), (objname2, objvalue2), ...... )
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])

        # Add to the dictionary
        self.pop[eval] = sol


    def run_agent(self, name):
        """ Invoking a named agent against the current population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)


    @staticmethod
    def _dominates(p, q):
        """ p = evaluation of solution: ((obj1, score1), (obj2, score2), ... )"""
        pscores = [score for _,score in p]
        qscores = [score for _,score in q]
        score_diffs = list(map(lambda x,y: y-x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p,q)}

    def remove_dominated(self):
        """ Remove solutions from the pop that are dominated (worse) compared
        to other existing solutions. This is what provides selective pressure
        driving the population towards the pareto optimal tradeoff curve. """
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k:self.pop[k] for k in nds}

    
    def evolve(self, n=1, dom=100, status=1000):
        """ Run the framework (start evolving solutions)
        n = # of random agent invocations (# of generations) """
        time_limit = 300
        start_time = time.time()  # Record the start time

        agent_names = list(self.agents.keys())
        for i in range(n):
            # Check if the time limit has been exceeded
            if time.time() - start_time > time_limit:
                print(f"Time limit of {time_limit} seconds reached, stopping evolution.")
                break
            pick = rnd.choice(agent_names)  # pick an agent to run
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()
            if i % status == 0:
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population size: ", len(self.pop))
                print(self)

        self.remove_dominated()


    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval,sol in self.pop.items():
            rslt += str(dict(eval))+":\t"+str(sol)+"\n"
        return rslt

    def summarize(self):
        """ Summarize the non-dominated solutions into a summary table. """

        # First, remove dominated solutions
        self.remove_dominated()

        # Prepare a list to store the rows of the summary table
        summary_data = []

        # Iterate over the non-dominated solution
        for eval, sol in self.pop.items():

            # Extract the objective names and their corresponding values
            objective_values = {name: score for name, score in eval}

            # Convert the solution and its objectives into a dictionary
            solution_summary = {**objective_values, 'Solution': sol, 'Group Name': 'ArjunS'}
            summary_data.append(solution_summary)

        # Convert the summary data to a pandas DataFrame for easy table format
        summary_df = pd.DataFrame(summary_data)

        return summary_df




