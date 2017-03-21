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
import time

# TTSA Includes
from ttsa import TTSA


def main():
    #Parse the command line arguments provided at run time.
    parser = argparse.ArgumentParser(description='Traveling Tournament Problem using Simulated Annealing')
    parser.add_argument('-n', '--number_teams', dest='number_teams', metavar='N',
                        type=int, nargs=1 ,help='Provide the number of teams (even) that should be scheduled')
    parser.add_argument('-s', '--seed', dest='seed', metavar='S',
                        type=float, nargs='?', default=0, help='Provide the seed for the PRNG')
    parser.add_argument('-t', '--tau', dest='tau', metavar='T',
                        type=float, nargs='?', default=400, help='Provide the value for Tau, default: 400')
    parser.add_argument('-b', '--beta', dest='beta', metavar='B',
                        type=float, nargs='?', default=0.9999, help='Provide the value for Beta, default: 0.9999')
    parser.add_argument('-o', '--omega', dest='omega', metavar='O',
                        type=float, nargs='?', default=4000, help='Provide the value for Omega, default: 4000')
    parser.add_argument('-d', '--delta', dest='delta', metavar='D',
                        type=float, nargs='?', default=1.04, help='Provide the value for Delta, default: 1.04')
    parser.add_argument('-e', '--theta', dest='theta', metavar='E',
                        type=float, nargs='?', default=1.04, help='Provide the value for Theta, default: 1.04')
    parser.add_argument('-c', '--maxc', dest='maxc', metavar='C',
                        type=int, nargs='?', default=100, help='Provide the value for MaxC, default: 100')
    parser.add_argument('-p', '--maxp', dest='maxp', metavar='P',
                        type=int, nargs='?', default=50, help='Provide the value for MaxP, default: 50')
    parser.add_argument('-r', '--maxr', dest='maxr', metavar='R',
                        type=int, nargs='?', default=3, help='Provide the value for MaxR, default: 3')
    parser.add_argument('-g', '--gamma', dest='gamma', metavar='G',
                        type=float, nargs='?', default=2, help='Provide the value for Gamma, default: 2')

    # Parse the input arguments
    args = parser.parse_args()

    ttsa = TTSA(args.number_teams[0], args.seed, args.tau, args.beta, args.omega, args.delta, args.theta, args.maxc, args.maxp, args.maxr, args.gamma)

if __name__ =='__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
