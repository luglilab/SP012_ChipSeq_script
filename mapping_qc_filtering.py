import os
import subprocess
import sys
import pysam

samtoolspath = "/home/spuccio/miniconda3/envs/chipseq_env/bin/samtools"




def counttotalreads(query):
    with open("test.txt", "w") as t:
        samtools_process = subprocess.Popen([samtoolspath, "view", "-S", query], stdout=subprocess.PIPE)
        cut_process = subprocess.Popen(["cut", "-f", "1", ], stdin=samtools_process.stdout, stdout=subprocess.PIPE)
        # samtools_process.stdout.close()
        sort_process = subprocess.Popen(["sort"], stdin=cut_process.stdout, stdout=subprocess.PIPE)
        # sort_process.stdout.close()
        uniq_process = subprocess.Popen(["uniq"], stdin=sort_process.stdout, stdout=subprocess.PIPE)
        # uniq_process.stdout.close()
        wc_process = subprocess.Popen(["wc", "-l"], stdin=uniq_process.stdout, stdout=t)