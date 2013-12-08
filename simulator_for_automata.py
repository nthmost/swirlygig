#
#
# Presence of NaN (empty vector calculations) in the grid means that no current could be
# calculated in that position.
#
# The question is: what to do about that.
#
# Option 1: impute the missing values. 
#      a. Easy/naive:  assume that, within 3 grid points of a known vector value, 
#                      those 3 points' vectors are the same.
#      b. Hard/better: 
#
# Option 2: ???
#
#
# Problems to solve:
#
# Figure out how much time a dumb agent (like a stick) spends moving between lat/long pts.
#
#

import sys
from lluv import LLUV
from cellular_automata import Floater



def engrid(filename):
    grid = LLUV(filename)
    return grid.to_dataframe() 
     

if __name__=='__main__':
    fname = sys.argv[1]
    df = engrid(fname)
    