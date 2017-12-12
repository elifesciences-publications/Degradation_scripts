import itertools
import sys
import numpy as np
import pandas as pd
import os
import collections
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('pipeline_dir')  #where mockinbird stores preprocessing files for all factors
parser.add_argument('analysis_dir')  #where new files are stored
parser.add_argument('dir1')   #dir1 is the mockinbird processing directory for factor 1; this script calculates c-localization for this versus all others
args = parser.parse_args()


def occupancy_near_factor(dir_base_factor_table, dir_sec_factor_table, base_range):
    b_qtable = pd.read_table(dir_base_factor_table, sep='\t')
    b_qtable = b_qtable.rename(columns={'seqid': 'chrom'})
    b_qtable = b_qtable.rename(columns={'position': 'start'})
    b_qtable = b_qtable[['chrom', 'start', 'strand', 'occupancy']]

    s_qtable = pd.read_table(dir_sec_factor_table, sep='\t')
    s_qtable = s_qtable.rename(columns={'seqid': 'chrom'})
    s_qtable = s_qtable.rename(columns={'position': 'start'})
    s_qtable.occupancy = 1
    s_qtable = s_qtable[['chrom', 'start', 'strand', 'occupancy']]


    for chrom, chrom_df in b_qtable.groupby('chrom'):
		    
		params = defaultdict(list)
	    for i, f in b_qtable.iterrows():
		params['chrom'].extend([f.chrom] * (base_range*2 + 1))
		params['strand'].extend([f.strand] * (base_range*2 + 1))
		params['occupancy'].extend([1] * (base_range*2 + 1))
		params['id'].extend([i] * (base_range*2 + 1))
		for i in range(-1*base_range, base_range + 1):
		    params['start'].append(f.start + i)

	    d_param = pd.DataFrame(params)     


	    df_merged = d_param.merge(s_qtable, on=['chrom', 'start', 'strand'], how='left').fillna(0)

	    occ_vectors = []
	    for dfid, site_df in df_merged.groupby("id"):
		occ_vectors.append(np.array(site_df['occupancy_y']))

	    occ_vector = np.vstack(occ_vectors).sum(axis=0)
    return occ_vector


direc_names = os.listdir(args.pipeline_dir)


for dir2 in direc_names:
	occ_vector = occupancy_near_factor (os.path.join(args.pipeline_dir , args.dir1, args.dir1 + '.table'), os.path.join(args.pipeline_dir , dir2, dir2 + '.table'), 500)

	with open(os.path.join(args.analysis_dir, args.dir1 + dir2 + '.txt' ), 'w') as f:
		f.write('dir1=%s\tdir2=%s\n'%(args.dir1,dir2))
		print(*occ_vector, sep='\t', file = f)

	print('Finished: ' + dir2)
