#!/usr/bin/env python3

"""ttsa.py: Traveling Tournament Problem Using Simulated Annealing"""

__author__ = "Colin Burgin"
__copyright__ = "Copyright 2017, Virginia Tech"
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Colin Burgin"
__email__ = "cburgin@vt.edu"
__status__ = "in progress"

# Standard Python Libraries
import random

class TTSA():
    """Traveling Tournament Simulated Annealing"""

    def __init__(self, number_teams):

        self.number_teams = number_teams

        # Build a starting schedule
        self.S = self.build_schedule(self.number_teams)
        self.print_schedule(self.S)


    # Builds a random starting schedule to build and improve on
    def build_schedule(self, number_teams):
        # Create an empty schedule
        rounds = (2 * number_teams) - 2
        S = [[None for i in range(rounds)] for j in range(number_teams)]

        # Populate the first row (team) with random values (opponents)
        home = lambda x: (x, "home")
        away = lambda x: (x, "away")
        S[0] = [f(x) for x in range(2, number_teams + 1) for f in (home, away)]

        # Populate the rest of the schedule by backtracking from the first row
        for i in range(len(S)):
            for j in range(len(S[i])):
                if S[i][j] is not None:
                    S = self.set_opponent(S, i, j)
                else:
                    S = self.get_opponent(S, i, j)
                    S = self.set_opponent(S, i, j)

        return S

    # Given the schedule and a specfic match, schedule the opponent for that match
    def set_opponent(self, S, i, j):
        match = S[i][j]
        if match[1] is "home":
            S[match[0]-1][j] = (i+1, "away")
        else:
            S[match[0]-1][j] = (i+1, "home")

        return S

    # Given the schedule and an empty slot, schedule a match with an available team
    def set_opponent(self, S, i, j):
        # Create a list of available teams
        rounds = (2 * number_teams) - 2
        home = lambda x: (x, "home")
        away = lambda x: (x, "away")
        available = [f(x) for x in range(2, number_teams + 1) for f in (home, away)]

        # Remove self from list
        available = [l for l in available if l[0] is not i]

        # Remove existing games


    # Prints the schedule in a way that is readable
    def print_schedule(self, S):
        print("\nThe Current Schedule\n")
        rounds = (2 * self.number_teams) - 2
        for row in S:
            print(*row, sep="\t")
