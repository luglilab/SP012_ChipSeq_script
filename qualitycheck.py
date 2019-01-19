import os
import subprocess
import traceback
import sys
# set path tool
fastqc = "/home/spuccio/miniconda3/envs/chipseq_env/bin/fastqc"
# set variables
projectdir = "/mnt/datadisk2/spuccio/SP012_ChipSeq_IRF8_MEOX1/"
raw_data_dir = projectdir + "RawReads/"
fastqcout = "".join([projectdir,"fastqc_output/"])
# dictionary with files name
raw_fastq = {}
raw_fastq={"ES_4_input":"ES_4_input_S5_R1_001.fastq",
           "IRF8_combo":"IRF8_combo_S3_R1_001.fastq",
           "IRF8_IP":"IRF8_IP_inv_S2_R1_001.fastq",
           "IRF8_IP":"IRF8_IP_neb_S1_R1_001.fastq",
           "Meox_inv":"Meox_inv_S4_R1_001.fastq",
           "Meox_neb":"Meox_neb_S6_R1_001.fastq"}
# function to create directory
def createdir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        print(" ".join(["Directory", dirpath.split("/")[-1], "Created"]))
    else:
        print(" ".join(["Directory", dirpath.split("/")[-1], "already exists"]))
# move to project home folder
os.chdir(projectdir)
# create fastq output directory
createdir(fastqcout)
# execute fastqc
for key, value in raw_fastq.items():
    try:
        subprocess.check_call(" ".join([fastqc,"-o",fastqcout,"".join([raw_data_dir,value])]),shell=True)
    except (subprocess.CalledProcessError, traceback), e:
        print ("ERROR.Fastqc analysis failed. Stop execution.")
        sys.exit(1)
    else:
        print ("Fastq analysis complete.")





