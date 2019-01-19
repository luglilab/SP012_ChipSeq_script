import os
import subprocess
import traceback
import sys
fastqc = "/home/spuccio/miniconda3/envs/chipseq_env/bin/fastqc"
projectdir = "/mnt/datadisk2/spuccio/SP012_ChipSeq_IRF8_MEOX1/"
raw_data_dir = projectdir + "RawReads/"
fastqcout = "".join([projectdir,"fastqc_output/"])
raw_fastq=["ES_4_input_S5_R1_001.fastq.gz"
"IRF8_combo_S3_R1_001.fastq.gz"
"IRF8_IP_inv_S2_R1_001.fastq.gz"
"IRF8_IP_neb_S1_R1_001.fastq.gz"
"Meox_inv_S4_R1_001.fastq.gz"
"Meox_neb_S6_R1_001.fastq.gz"]

os.chdir(projectdir)
os.mkdir(fastqcout)
for i in range(len(raw_fastq)):
    try:
        subprocess.check_call(" ".join([fastqc,"-o",fastqcout,
                                        raw_data_dir+raw_fastq[i]]),
                              shell=True)
    except subprocess.CalledProcessError:
        print ("ERROR.Fastqc analysis failed. Stop execution.")
        sys.exit(1)
    else:
        print ("Fastq analysis complete.")
