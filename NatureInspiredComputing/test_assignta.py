import numpy as np
import pandas as pd
from assignta import overallocation, conflicts, undersupport, unavailable, unpreferred
import pytest
import io
import sys

# import the test csvs
test1 = pd.read_csv("assignta_data/test1.csv",header=None).to_numpy()
test2 = pd.read_csv("assignta_data/test2.csv",header=None).to_numpy()
test3 = pd.read_csv("assignta_data/test3.csv",header=None).to_numpy()

# import the sections and TAs dfs
sections_df = pd.read_csv("assignta_data/sections.csv")
tas_df = pd.read_csv("assignta_data/tas.csv")

# load in the other parameters needed from these dfs.
max_assigned = tas_df['max_assigned']
lab_times = sections_df['daytime']
min_ta = sections_df['min_ta']
availability_matrix = tas_df.drop(columns=['ta_id', 'name', 'max_assigned']).to_numpy()

# create the table of expected values based on the assignment instructions.
expected_values = {
    "Overallocation": [34, 37, 19],
    "Conflicts": [7, 5, 2],
    "Undersupport": [1, 0, 11],
    "Unavailable": [59, 57, 34],
    "Unpreferred": [10, 16, 17]
}

# create tests for each function and test.csv and judge them against the expected values.
def test_overallocation():
    assert overallocation(test1,max_assigned) == expected_values["Overallocation"][0]
    assert overallocation(test2, max_assigned) == expected_values["Overallocation"][1]
    assert overallocation(test3, max_assigned) == expected_values["Overallocation"][2]

def test_conflict():
    assert conflicts(test1,lab_times) == expected_values['Conflicts'][0]
    assert conflicts(test2, lab_times) == expected_values['Conflicts'][1]
    assert conflicts(test3, lab_times) == expected_values['Conflicts'][2]

def test_undersupport():
    assert undersupport(test1,min_ta) == expected_values['Undersupport'][0]
    assert undersupport(test2, min_ta) == expected_values['Undersupport'][1]
    assert undersupport(test3, min_ta) == expected_values['Undersupport'][2]

def test_unavailable():
    assert unavailable(test1,availability_matrix) == expected_values['Unavailable'][0]
    assert unavailable(test2, availability_matrix) == expected_values['Unavailable'][1]
    assert unavailable(test3, availability_matrix) == expected_values['Unavailable'][2]

def test_unpreferred():
    assert unpreferred(test1,availability_matrix) == expected_values['Unpreferred'][0]
    assert unpreferred(test2, availability_matrix) == expected_values['Unpreferred'][1]
    assert unpreferred(test3, availability_matrix) == expected_values['Unpreferred'][2]


def main():
    # Create a StringIO object to capture pytest output
    output = io.StringIO()

    # Run the tests and capture the output
    pytest.main(["-q", "--tb=short", "--maxfail=1"], stdout=output)

    # Write the captured output to a text file on the desktop
    with open("/Users/ArjunShatkin/Desktop/ArjunS_pytest.txt", "w") as f:
        f.write(output.getvalue())

if __name__ == "__main__":
    main()