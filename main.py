#!/usr/bin/env python3

"""main.py: Traveling Tournament Problem Using Simulated Annealing"""

__author__ = "Colin Burgin"
__copyright__ = "Copyright 2017, Virginia Tech"
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Colin Burgin"
__email__ = "cburgin@vt.edu"
__status__ = "in progress"

# Standard Python Libraries
import argparse

# TTSA Includes
from ttsa import TTSA


def main():
    #Parse the command line arguments provided at run time.
    parser = argparse.ArgumentParser(description='Traveling Tournament Problem using Simulated Annealing')
    parser.add_argument('-n', '--number_teams', dest='number_teams', metavar='N',
                        type=int, nargs=1 ,help='Provide the number of teams (even) that should be scheduled')
    parser.add_argument('-s', '--seed', dest='seed', metavar='S',
                        type=int, nargs='?', default=0, help='Provide the seed for the PRNG')

    # Parse the input arguments
    args = parser.parse_args()

    ttsa = TTSA(args.number_teams[0], args.seed)

if __name__ =='__main__':
    main()
