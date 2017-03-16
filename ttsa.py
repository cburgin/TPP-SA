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
import operator, itertools

class TTSA():
    """Traveling Tournament Simulated Annealing"""

    def __init__(self, number_teams):

        self.number_teams = number_teams
        self.weeks = (2 * self.number_teams) - 2

        # Build a starting schedule
        self.S = self.build_schedule(self.number_teams)
        self.print_schedule(self.S)


    # Builds a random starting schedule to build and improve on
    def build_schedule(self, number_teams):
        # Create an empty schedule
        S = [[None for i in range(self.weeks)] for j in range(number_teams)]

        # Call the recursive build function
        return self.r_build_schedule(S, 0, 0)

    # Recursive part of build schedule
    def r_build_schedule(self, S, team, week):
        # If the schedule is full then return becuase it is complete
        if self.schedule_full(S):
            return S

        # Calculate the next location
        next_week = week + 1
        next_team = team
        if next_week == self.weeks:
            next_week = 0
            next_team += 1

        # If there is already a game scheduled then move forward
        if S[team][week] is not None:
            return self.r_build_schedule(S, next_team, next_week)

        # Find all of the possible games that can be scheduled, return if it isn't schedulable
        possibilities = self.get_game(S, team, week)
        random.shuffle(possibilities)
        if possibilities is None:
            return None

        # Try all the possible games until one works
        for p in possibilities:
            try_S = [[c for c in r] for r in S]
            # Set the game as well as the opponent
            try_S[team][week] = p
            self.set_opponent(try_S, team, week)
            # Move forward with this attempt
            result_S = self.r_build_schedule(try_S, next_team, next_week)
            if result_S is not None:
                return result_S

    # Check to see if the schedule is full
    def schedule_full(self, S):
        for week in S:
            for game in week:
                if game is None:
                    return False
        return True

    # Given the schedule and a specfic match, schedule the opponent for that match
    def set_opponent(self, S, i, j):
        match = S[i][j]
        if match[1] is "home":
            S[match[0]-1][j] = (i+1, "away")
        else:
            S[match[0]-1][j] = (i+1, "home")

        return S

    # Given the schedule and an empty slot, determine the possible games that can be scheduled here
    def get_game(self, S, i, j):
        # Create a list of available teams
        home = lambda x: (x, "home")
        away = lambda x: (x, "away")
        available = [f(x) for x in range(1, self.number_teams+1) for f in (home, away)]

        # Remove self from list
        available = [k for k in available if k[0] is not i+1]

        # Remove games that this team already has on its schedule
        available = [l for l in available if l not in S[i]]

        # Remove opponents that are in concurrent games
        col = [o[0] for o in [row[j] for row in S] if o is not None]
        available = [m for m in available if m[0] not in col]

        return available

    def str_schedule(self, S):
        return '\n'.join(''.join(['%16s'%(col,) for col in row]) for row in S)+'\n'

    # Prints the schedule in a way that is readable
    def print_schedule(self, S):
        print("\nThe Current Schedule\n")
        for row in S:
            print(*row, sep="\t")
