import cProfile
import pstats
import pandas as pd
import evo
import numpy as np
from assignta import overallocation, conflicts, undersupport, unavailable,unpreferred,one_mutation
from assignta import crossover_columns, crossover_rows, randomize

def profiler():
    # import the dfs.
    sections_df = pd.read_csv("assignta_data/sections.csv")
    tas_df = pd.read_csv("assignta_data/tas.csv")

    # initialize the class framework.
    E = evo.Evo()

    # create/define the 2nd argument for each objective function.
    lab_times = sections_df['daytime']
    max_assigned = tas_df['max_assigned']
    min_ta = sections_df['min_ta']
    availability_matrix = tas_df.drop(columns=['ta_id', 'name', 'max_assigned']).to_numpy()

    # Register the created objectives
    E.add_objective("Overallocation", lambda sol: overallocation(sol, max_assigned))
    E.add_objective("Conflicts", lambda sol: conflicts(sol, lab_times))
    E.add_objective("Undersupport", lambda sol: undersupport(sol, min_ta))
    E.add_objective("Unavailable", lambda sol: unavailable(sol, availability_matrix))
    E.add_objective("Unpreferred", lambda sol: unpreferred(sol, availability_matrix))

    # initialize 10 random starting solutions.
    for _ in range(10):  # Start with 10 random solutions
        sol = np.random.randint(2, size=(40, 17))  # Random TA assignment
        E.add_solution(sol)

    # add the agents I created
    E.add_agent("one_mutation", one_mutation, k=1)
    E.add_agent("crossover_rows", crossover_rows, k=2)
    E.add_agent("randomize", randomize, k=1)
    E.add_agent('crossover_columns', crossover_columns, k=2)

    profiler = cProfile.Profile()
    profiler.enable()

    E.evolve(n=200000, dom=100, status=50000)


    profiler.disable()

    with open("Arjuns_profile.txt", "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.strip_dirs()
        stats.sort_stats("cumtime")
        stats.print_stats()
def main():
    # run the profiler
    profiler()

if __name__ == "__main__":
    main()

