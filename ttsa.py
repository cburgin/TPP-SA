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

    def __init__(self, number_teams, seed, default_schedule):

        # Calculate schedule vars.
        self.number_teams = number_teams
        self.weeks = (2 * self.number_teams) - 2

        # Seed PRNG
        random.seed(seed)

        # Build a starting schedule or use the starting schedule from the paper
        if default_schedule is False:
            self.S = self.build_schedule(self.number_teams)
        else:
            self.S = [[(6, 'home'), (2, 'away'), (4, 'home'), (3, 'home'), (5, 'away'), (4, 'away'), (3, 'away'), (5, 'home'), (2, 'home'), (6, 'away')],
                      [(5, 'home'), (1, 'home'), (3, 'away'), (6, 'away'), (4, 'home'), (3, 'home'), (6, 'home'), (4, 'away'), (1, 'away'), (5, 'away')],
                      [(4, 'away'), (5, 'home'), (2, 'home'), (1, 'away'), (6, 'home'), (2, 'away'), (1, 'home'), (6, 'away'), (5, 'away'), (4, 'home')],
                      [(3, 'home'), (6, 'home'), (1, 'away'), (5, 'away'), (2, 'away'), (1, 'home'), (5, 'home'), (2, 'home'), (6, 'away'), (3, 'away')],
                      [(2, 'away'), (3, 'away'), (6, 'home'), (4, 'home'), (1, 'home'), (6, 'away'), (4, 'away'), (1, 'away'), (3, 'home'), (2, 'home')],
                      [(1, 'away'), (4, 'away'), (5, 'away'), (2, 'home'), (3, 'away'), (5, 'home'), (2, 'away'), (3, 'home'), (4, 'home'), (1, 'home')]]
            self.number_teams = 6
            self.weeks = (2 * self.number_teams) - 2

        self.print_schedule(self.S)
        S = self.swap_teams(self.S)
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

        # Catch all
        return None

    # Check to see if the schedule is full, inefficent
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

    # The move swaps the home and away roles of team T in pos i and j
    # Because this is going to be a random choice everytime the function is called,
    #   the choice is just made inside of the function instead of being passed in.
    def swap_homes(self, S):
        # Choose a team to swap on
        team  = len(S) - 1
        swap_loc = S[team].index(random.choice(S[team]))
        swap_loc_mirror = S[team].index(self.home_away(S[team][swap_loc]))

        # Swap the first game and its opponent
        S[team][swap_loc] = self.home_away(S[team][swap_loc])
        S = self.set_opponent(S, team, swap_loc)

        # Swap the matching game and its opponent
        S[team][swap_loc_mirror] = self.home_away(S[team][swap_loc_mirror])
        S = self.set_opponent(S, team, swap_loc_mirror)

        return S

    # Given a game, swap the home/awayness of that game
    def home_away(self, game):
        if game[1] is 'home':
            return (game[0], 'away')
        else:
            return (game[0], 'home')

    # The move simply swaps rounds k and l
    # Because this is going to be a random choice everytime the function is called,
    #   the choice is just made inside of the function instead of being passed in.
    def swap_rounds(self, S):
        # Choose two different rounds to swap
        choices = random.sample(list(range(len(S[0]))), 2)

        # Iterate through the teams swapping each rounds
        for team in range(len(S)):
            game_one = S[team][choices[0]]
            game_two = S[team][choices[1]]
            S[team][choices[0]] = game_two
            S[team][choices[1]] = game_one

        return S

    # This move swaps the schedule for teams i and j except of course, when they play against each other
    # Because this is going to be a random choice everytime the function is called,
    #   the choice is just made inside of the function instead of being passed in.
    def swap_teams(self, S):
        # Choose two different teams to swap
        choices = random.sample(list(range(len(S)-1)), 2)

        # Swap the teams completely
        team_one = S[choices[0]]
        team_two = S[choices[1]]
        S[choices[0]] = team_two
        S[choices[1]] = team_one

        # Resolve the same team conflicts
        for game in range(len(S[choices[0]])):
            # If the team is playing itself fix it and resolve opponent
            if S[choices[0]][game][0] - 1 is choices[0]:
                S[choices[0]][game] = self.home_away(S[choices[1]][game])
                S = self.set_opponent(S, choices[0], game)

        # Resolve the opponents
        for team in choices:
            for game in range(len(S[team])):
                S = self.set_opponent(S, team, game)

        return S


    # Print Functions for the Schedule
    def str_schedule(self, S):
        return '\n'.join(''.join(['%16s'%(col,) for col in row]) for row in S)+'\n'

    # Prints the schedule in a way that is readable
    def print_schedule(self, S):
        print("\nThe Current Schedule\n")
        for row in S:
            print(*row, sep="\t")
