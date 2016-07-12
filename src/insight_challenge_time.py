#!/usr/bin/python

from datetime import datetime
import dateutil.parser
import json # This package is called for JSON file formatting
import numpy as np # This package is called for Numerical analyses
import statistics as st # This package is called for Statistical Analyses
import networkx as nx # This package is called for Graph analysis
import sys
if len(sys.argv)<3:
    print "Usage: %s infile" % sys.argv[0]
    sys.exit(1)

infile = sys.argv[1]
print(infile)
outputfile = sys.argv[2]
#outputfile = '/Users/Saeideh/Dropbox/Coursera/Insight/output_test.txt'
G = nx.Graph() # creating an empty graph
window_time = 60 # 60-second window
with open(infile) as inf:
    transactions_all = inf.readlines() # all the lines of the text file read
    num_transactions = len(transactions_all) # how many transacations?
   # print num_transactions
    ct = 'created_time'
    tt = 'target'
    ar = 'actor'
    dict_old = {}
    dict_new = {}
    dict_new = dict_old.fromkeys([ar, tt,ct])
    cnt = 0
    for line in transactions_all:
        cnt = cnt + 1
        curr_trans = eval(line)
        curr_trans_time = dateutil.parser.parse(curr_trans[ct]).replace(microsecond=0)
        curr_trans_target = curr_trans[tt]
        curr_trans_actor = curr_trans[ar]
        if cnt == 1:
            G.add_edge(curr_trans_target, curr_trans_actor)
            med_curr= np.median(list(G.degree().values()))
            fo = open(outputfile, 'w') # openning a file to write in it
            fo.write(str(med_curr)+'\n')
            fo.close()
            dict_old = dict_old.fromkeys([ar, tt,ct])
            dict_old[ar] = [curr_trans_actor]
            dict_old[tt] = [curr_trans_target]
            dict_old[ct] = [curr_trans_time]
        else:
            max_time_new = max([max_timestamp,curr_trans_time])
            G.add_edge(curr_trans_target, curr_trans_actor)
            dict_old[ar].append(curr_trans_actor)
            dict_old[tt].append(curr_trans_target)
            dict_old[ct].append(curr_trans_time)
            #print(dict_old[ct])
            idx_remove = np.where(( np.array([(max_time_new-i).total_seconds() for i in dict_old[ct]]))>window_time)
            idx_keep = np.where(( np.array([(max_time_new-i).total_seconds() for i in dict_old[ct]]))<=window_time)
            
            idx_keep = idx_keep[0]
            idx_remove = idx_remove[0]
            
            G = nx.Graph()
            for ii in idx_keep:
                target_remove = dict_old[tt][ii]
                actor_remove = dict_old[ar][ii]
                G.add_edge(target_remove, actor_remove) # Prunning the graph

            dict_new[ar] = [dict_old[ar][j] for j in idx_keep]
            dict_new[tt] = [dict_old[tt][j] for j in idx_keep]
            dict_new[ct] = [dict_old[ct][j] for j in idx_keep]
            print(list(G.edges()))
            print(list(G.nodes()))
            med_curr= np.median(list(G.degree().values()))
            
            fo = open(outputfile, 'a') # adding a new median to the file 
            fo.write(str(med_curr)+'\n')
            fo.close()
            dict_old = dict_new
        
        max_timestamp = max(dict_old[ct])
