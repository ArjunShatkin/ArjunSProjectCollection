#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:50:40 2021

@author: rachlin
"""
# import needed packages
import copy
from collections import defaultdict
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

class DRV:
    
    def __init__(self, dist=None, **kwargs):
        """ Constructor
         dist: Dictionary of value:probability pairs
         kwargs: misc parameters for other types of distributions """
        # create a dictionary if none is given
        if dist is None:
            self.dist = dict() # Empty distribution
        else:
            self.dist = copy.deepcopy(dist)

        # get the type of distribution from the kwargs parameters, with the distribution type defaulting to discrete.
        dtype = kwargs.get('type', 'discrete')

        # if the dtype is uniform use the min, max, and bins kwargs arguments to calculate the values and probs.
        if dtype == 'uniform':
            minval = kwargs.get('min', 0.0)
            maxval = kwargs.get('max', 1.0)
            bins = kwargs.get('bins', 10)

            self.values = np.linspace(minval, maxval, bins)
            self.probabilities = np.array([1.0 / bins for i in range(bins)])
            self.dist = {v: p for v, p in zip(self.values, self.probabilities)}

        # if the dtype is normal, use the mean, stdev, and bins args to calculate the values and probability dist.
        elif dtype == 'normal':
            self.dist = {}
            mean = kwargs.get('mean', 0.0)
            stdev = kwargs.get('stdev', 1.0)
            bins = kwargs.get('bins', 10)

            # use the Gaussian equation for estimating levels in a normal distribution
            self.values = np.linspace(mean - 3 * stdev, mean + 3 * stdev, bins)
            pdf_vals = np.exp(-0.5 * ((self.values - mean) / stdev) ** 2)
            self.probabilities = pdf_vals / pdf_vals.sum()
            self.dist = {v: p for v, p in zip(self.values, self.probabilities)}

        # if dtype is discrete use the values and probabilities params to create the distribution.
        elif dtype == 'discrete':
            self.values = kwargs.get('values', [])
            self.probabilities = kwargs.get('probabilities', [])
            if len(self.values) != len(self.probabilities):
                print("Values and probabilities must be the same length")

            self.dist = {v: p for v, p in zip(self.values, self.probabilities)}

    def E(self):
        """ Expected value E[X] """
        return sum(v * p for v, p in zip(self.values, self.probabilities))

    def __add__(self, other):
        """ Add two discrete random variables """
        new_probabilities = defaultdict(float)

        # iterate through the values and probabilities and add accordingly
        for v,p in zip(self.values,self.probabilities):
            for v1, p1 in zip(other.values, other.new_probabilities):
                new_val = v + v1
                new_probabilities[new_val] += p*p1

        new_values = list(new_probabilities.keys())
        new_probs = list(new_probabilities.values())

        return DRV(values=new_values, probabilities=new_probs)

    def __radd__(self, a):
        """ Add a scalar, a, by the DRV """
        new_vals = [v+a for v in self.values]
        return DRV(values=new_vals, probabilities=self.probabilities)

    def __sub__(self, other):
        """ Subtract two discrete random variables  """

        sub_probabilities = defaultdict(float)
        # iterate through the values and probabilities and subtract accordingly
        for v,p in zip(self.values,self.probabilities):
            for v1,p1 in zip(other.values,other.probabilities):
                sub_val = v - v1
                sub_probabilities[sub_val] += p*p1
        
        new_values = list(sub_probabilities.keys())
        new_probs = list(sub_probabilities.values())

        return DRV(values=new_values, probabilities=new_probs)

    def __rsub__(self, a):
        """ Subtract scalar - drv """

        new_vals = [a - v for v in self.values]
        return DRV(values=new_vals, probabilities=self.probabilities)

    def __mul__(self, other):
        """ Multiply two discrete random variables  """

        mul_probabilities = defaultdict(float)

        # iterate through the values and probabilities and multiply accordingly
        for v, p in zip(self.values, self.probabilities):
            for v1, p1 in zip(other.values, other.probabilities):
                mul_val = v * v1
                mul_probabilities[mul_val] += p * p1

        new_values = list(mul_probabilities.keys())
        new_probs = list(mul_probabilities.values())

        return DRV(values=new_values, probabilities=new_probs)

    def __rmul__(self, a):
        """ Multiply a scalar, a, by the DRV """
        new_vals = [a * v for v in self.values]
        return DRV(values=new_vals, probabilities=self.probabilities)

    def __repr__(self):
        """ Human-readable string representation of the DRV
        Display each value:probability pair on a separate line.
        Round all probabilities to 5 decimal places. """
        return "\n".join(f"{v}: {round(p, 5)}" for v, p in self.dist.items())

    def plot(self, title=None, xscale=None, yscale=None, show_cumulative=False, discrete=False,
             savefig=None, figsize=(4, 4)):
        """ Display the DRV distribution
        title: The title of the figure
        xscale: If 'log' then log-scale the x axis
        yscale: If 'log' then log-scale the y axis
        show_cummulative: If True, overlay the cummulative distribution line
        savefig: Name of .png file to save plot
        figsize: Default figure size"""

        # separate self.dist into a list of values and probabilities
        values, probabilities = zip(*sorted(self.dist.items()))
        values = np.array(values).flatten()
        probabilities = np.array(probabilities).flatten()

        sns.histplot(x=values, weights=probabilities, discrete=discrete,
                     color="blue",bins=len(values), label="Probability Mass Function (PMF)")

        # rescale the axes if the user called upon this in the function call.
        if xscale:
            plt.xscale('log')
        if yscale:
            plt.yscale('log')

        # show the cumulative probabilities if the user calls upon it in the function call.
        if show_cumulative:
            cumulative_probs = np.cumsum(probabilities)
            plt.step(values, cumulative_probs, label='Cumulative', color="red", where="post")
            #plt.plot(values, cumulative_probs, label='Cumulative', color="red")

        # plot and title accordingly.
        plt.xlabel("Number of Planets")
        plt.ylabel("Probability")
        plt.title(title)
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()