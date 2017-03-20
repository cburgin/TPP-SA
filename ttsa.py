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

    def __init__(self, number_teams, seed):

        # Calculate schedule vars.
        self.number_teams = number_teams
        self.weeks = (2 * self.number_teams) - 2
        self.current_cost = None

        # Set all the default vars for SA
        self.S = self.build_schedule(self.number_teams)

        # Seed PRNG
        if seed is 0:
            random.seed()
        else:
            random.seed(seed)

        # Read in the cost matrix
        self.cost_matrix = []
        self.cost_matrix = self.get_cost_matrix(self.number_teams)

        # Perform the simulated annealing to solve the schedule
        self.simulated_annealing()

        # Print out the resulting schedule
        self.print_schedule(self.S)

    # The Simulated Annelaing Algorithm TTSA from the TTP paper figure 2
    def simulated_annealing(self):
        pass

    # Builds the cost matrix for the coresponding number of teams
    def get_cost_matrix(self, number_teams):
        file_name = "data/data" + str(number_teams) + ".txt"
        l = []
        with open(file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) > 0:
                    l.append(line.split())

        return l

    # Calculate the cost of the input schedule
    def cost(self, S, cost_m):
        total_cost = 0
        # Loop through the schedule calculating the cost along the way
        for team in S:
            i = S.index(team)
            team.append((None, "home"))
            for game in team:
                j = team.index(game)
                start_loc = None
                dest_loc = None
                # Handle the first game case, get start location
                if j is 0:
                    start_loc = i
                else:
                    if team[j-1][1] is "home":
                        start_loc = i
                    else:
                        start_loc = team[j-1][0] - 1

                # Handle the last game case, get the travel location
                if j is len(team) - 1:
                    dest_loc = i
                else:
                    if team[j][1] is "home":
                        dest_loc = i
                    else:
                        dest_loc = team[j][0] - 1
                # Cost
                total_cost += int(cost_m[start_loc][dest_loc])
            # Pop off the placeholder location
            team.pop()
        return total_cost

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
        choices = random.sample(list(range(len(S))), 2)

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

    # This mode considers team T and swaps its games at round k and l
    # Because this is going to be a random choice everytime the function is called,
    #   the choice is just made inside of the function instead of being passed in.
    def partial_swap_rounds(self, S):
        # Choose a random team and two random rounds to swap
        s_team = random.sample(list(range(len(S))), 1)[0]
        s_rounds = random.sample(list(range(len(S[0]))), 2)

        # Create a starting list
        p_swap = [s_team]

        # Chain ejection until everything is in the list
        while 1:
            # loop through the list adding new teams if necessary
            for item in p_swap:
                if S[item][s_rounds[0]][0]-1 not in p_swap:
                    p_swap.append(S[item][s_rounds[0]][0]-1)

                if S[item][s_rounds[1]][0]-1 not in p_swap:
                    p_swap.append(S[item][s_rounds[1]][0]-1)

            # Check to see if the list is fully inclusive
            if (S[p_swap[-1]][s_rounds[0]][0]-1 in p_swap) and (S[p_swap[-1]][s_rounds[1]][0]-1 in p_swap) and (S[p_swap[-2]][s_rounds[0]][0]-1 in p_swap) and (S[p_swap[-2]][s_rounds[1]][0]-1 in p_swap):
                break

        # Loop through the list for one of the rounds and swap all the games in the list
        for item in p_swap:
            S = self.swap_game_round(S, item, s_rounds[0], s_rounds[1])

        return S

    # Swap games by same team different rounds
    def swap_game_round(self, S, t, rl, rk):
        game_one = S[t][rl]
        game_two = S[t][rk]
        S[t][rl] = game_two
        S[t][rk] = game_one
        return S

    # This move considers round rk and swaps the games of teams Ti and Tj
    # Because this is going to be a random choice everytime the function is called,
    #   the choice is just made inside of the function instead of being passed in.
    def partial_swap_teams(self, S):
        # Choose a random round and two random teams to swap
        s_round = random.sample(list(range(len(S[0]))), 1)[0]
        s_teams = random.sample(list(range(len(S))), 2)

        # Handle case where the games cannot be swapped because it is invalid (cant play yourself)
        if not (set(s_teams) - set([S[s_teams[0]][s_round][0]-1, S[s_teams[1]][s_round][0]-1])):
            return S

        # Create a starting list
        p_swap = [S[s_teams[0]][s_round], S[s_teams[1]][s_round]]

        # Chain ejection until everything is in the list
        while 1:
            # Loop through the list adding new teams if necessary
            for item in p_swap:
                if self.get_concurrent(S, s_teams[0], s_teams[1], item) not in p_swap:
                    p_swap.append(self.get_concurrent(S, s_teams[0], s_teams[1], item))

                if self.get_concurrent(S, s_teams[1], s_teams[0], item) not in p_swap:
                    p_swap.append(self.get_concurrent(S, s_teams[1], s_teams[0], item))

            if( (self.get_concurrent(S, s_teams[0], s_teams[1], p_swap[-1]) in p_swap) and (self.get_concurrent(S, s_teams[1], s_teams[0], p_swap[-1]) in p_swap) and
                (self.get_concurrent(S, s_teams[0], s_teams[1], p_swap[-2]) in p_swap) and (self.get_concurrent(S, s_teams[1], s_teams[0], p_swap[-2]) in p_swap) ):
                break

        # Get the indices of the games found
        p_indices = []
        for item in p_swap:
            p_indices.append(S[s_teams[0]].index(item))

        # Loop through the list for one of the teams and swap all of the games and resolve opponents
        for idx in p_indices:
            S = self.swap_game_team(S, idx, s_teams[0], s_teams[1])

        return S

    # Swap games by same round different teams and resolve opponents
    def swap_game_team(self, S, r, T1, T2):
        game_one = S[T1][r]
        game_two = S[T2][r]
        S[T1][r] = game_two
        S[T2][r] = game_one
        S = self.set_opponent(S, T1, r)
        S = self.set_opponent(S, T2, r)
        return S

    # Given a two teams and a game, find the concurrent game for the other teams
    def get_concurrent(self, S, T1, T2, game):
        for i, j in enumerate(S[T1]):
            if j == game:
                return S[T2][i]

    # Print Functions for the Schedule
    def str_schedule(self, S):
        return '\n'.join(''.join(['%16s'%(col,) for col in row]) for row in S)+'\n'

    # Prints the schedule in a way that is readable
    def print_schedule(self, S):
        print("\nThe Schedule\n")
        for row in S:
            print(*row, sep="\t")

        print("\nCost:", self.cost(self.S, self.cost_matrix))
