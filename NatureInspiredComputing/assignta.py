import pandas as pd
import numpy as np
import evo
import copy
import random as rnd

def conflicts(solution,lab_times):
    '''
    :param lab_times: Schedule time for each lab
    :return: the number of lab assignments for TAs that conflict.
    '''

    # Find the indices where the solution matrix has a 1 (indicating an assignment).
    lab_asgn = np.where(solution == 1)

    # use these indices to find the lab times for TAs when the TA has an assignment
    assigned_times = lab_times[lab_asgn[1]]

    # create a list for each TA
    assigned_times_by_ta = np.split(assigned_times, np.unique(lab_asgn[0], return_index=True)[1][1:])

    # iterate through each TA and check if their have overlapping assignments.
    conflict_counter = 0
    for times in assigned_times_by_ta:
        # If there are duplicates, there's a conflict
        if len(np.unique(times)) < len(times):
            conflict_counter += 1

    return conflict_counter


def overallocation(solution, max_assigned):
    '''
    :param solution: array of solution assignments
    :param max_assigned: max assigned classes for each Ta
    :return: the sum of the differences between assigned labs and max labs where max labs are smaller than assigned.
    '''
    overallocation_penalty = 0
    # Loop through rows
    for i in range(solution.shape[0]):
        # Number of labs assigned per TA
        assigned_labs = np.sum(solution[i])
        if assigned_labs > max_assigned[i]:
            # add to the overallocation penalty based on the difference btwn assigned and max labs.
            overallocation_penalty += assigned_labs - max_assigned[i]
    return overallocation_penalty

def undersupport(solution, min_ta):
    '''

    :param solution: array of solution assignments
    :param min_ta:
    :return:
    '''
    # calculate the number of TAs assigned in each Office Hour.
    num_tas = solution.sum(axis = 0)

    # Calculate how much each lab is undersupported. If a lab has fewer TAs than required, the difference is positive
    undersupported = np.maximum((min_ta - num_tas), 0)
    return undersupported.sum()

def unavailable(solution,availabilities):
    # Create boolean values where 'U' (Unavailable) entries are marked as True.
    unavailabilities = (availabilities == 'U')

    # Count the number of TA assignments that fall into unavailable slots.
    unavailable_count = np.sum(solution[unavailabilities])
    return unavailable_count

def unpreferred(solution,availabilities):
    # Create boolean values where 'W' unpreferred entries are marked as True.
    unpreffered = (availabilities == 'W')

    # use these boolean values to count the number of times TAs are assigned to unpreferred slots
    unpreffered_count = np.sum(solution[unpreffered])
    return unpreffered_count


def one_mutation(solutions):
    # create a function that randomly changes one value from the solution

    # Choose one solution from the list
    solution = solutions[0]

    # Get the dimensions of the solution
    rows, cols = solution.shape

    # Randomly choose one position (row, col) to flip
    row_idx = np.random.randint(0, rows)
    col_idx = np.random.randint(0, cols)

    # Flip the binary value (0 or 1) at that position
    solution[row_idx, col_idx] = 1 - solution[row_idx, col_idx]

    return solution


def crossover_columns(solutions):
    # create a function that takes 2 solutions and merges/stacks the solutions on a random column.
    # Choose two solutions randomly from the pool
    sol1, sol2 = solutions

    # Get the dimensions of the solutions
    rows, cols = sol1.shape

    # Randomly choose a crossover point
    crossover_point = np.random.randint(1, cols)

    # Perform the stack/merge
    answer = np.hstack((sol1[:, :crossover_point], sol2[:, crossover_point:]))
    return answer


def crossover_rows(solutions):
    # create a function that takes 2 solutions and merges/stacks the solutions on a random row.
    # Choose two solutions randomly from the pool
    sol1, sol2 = solutions

    # Get the dimensions of the solutions
    rows, cols = sol1.shape

    # Randomly choose a crossover point
    crossover_point = np.random.randint(1, rows)

    # Perform the merge/stack
    answer = np.vstack((sol1[:crossover_point, :], sol2[crossover_point:, :]))

    return answer

def randomize(solutions):
    # create a function that reshuffles 10% of a solution
    # Choose one solution randomly from the pool
    solution = solutions[0]

    # Get the dimensions of the solution
    rows, cols = solution.shape

    # Randomly choose a portion of the solution to randomize (you could randomize a percentage of the solution)
    num_changes = np.random.randint(1, rows * cols // 10)  # Randomize up to 10% of the solution

    # Randomly select positions to change
    for _ in range(num_changes):
        row = np.random.randint(0, rows)
        col = np.random.randint(0, cols)

        # Flip the value at the selected position (0 becomes 1 and 1 becomes 0)
        solution[row, col] = 1 - solution[row, col]

    return solution

def main():
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
    E.evolve(n=200000, dom=100, status=50000)

    summary_df = E.summarize()
    summary_df.to_csv("ArjunS_summary.csv", index=False)

if __name__ == "__main__":
    main()