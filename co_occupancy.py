import pybedtools
import sys
import numpy as np
import pandas as pd
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('all_transcript_bed_dir')
parser.add_argument('factor_table_dir')
parser.add_argument('analysis_dir')
args = parser.parse_args()


def co_occupancy (all_transcript_bed_dir, factor_table_dir, output_file):
    f = pybedtools.BedTool(all_transcript_bed_dir)
    
    qtable = pd.read_table(factor_table_dir, sep='\t')
    qtable = qtable.rename(columns= {'seqid' : 'chrom'})
    qtable = qtable.rename(columns= {'position' : 'start'})
    qtable = qtable[['chrom','start','start','strand','strand','strand','strand', 'occupancy']]
    qpybed = pybedtools.BedTool.from_dataframe(qtable)
    counts = list()

    for i in range(len(f)):
        intersect = qpybed.intersect(f[i:i+1], wa = True)
        counts.append(sum([1 for f in intersect]))
    
    with open(output_file, 'w') as out_file:
        print(*counts, sep='\t', file = out_file)


factor_name = os.path.basename(args.factor_table_dir).split('.')[0]
output_file = os.path.join(args.analysis_dir, factor_name + '_transcript_occ.txt')

co_occupancy(args.all_transcript_bed_dir, args.factor_table_dir, output_file)
