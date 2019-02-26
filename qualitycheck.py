import os
import subprocess
import traceback
import sys
import shutil
# set command
command1="{FASTQC} -o {FASTQOUTPUT} {INPUTRAWREADS}"
command2="{MULTIQC} -o {MULTIQCOUTDIR} -i {MULTIQCNAME} {FASTQCOUTFOLDER}"

# function to create directoryl
def createdir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        print(" ".join(["Directory", dirpath.split("/")[-1], "Created"]))
    else:
        print(" ".join(["Directory", dirpath.split("/")[-1], "already exists"]))


def fastqc(fastqcpath,fastqcfolderout,rawfastq):
    """
    Execute FastQC
    :param fastqcpath:
    :param fastqcfolderout:
    :param rawfastq:
    :return:
    """
    os.system(command1.format(FASTQC=fastqcpath,FASTQOUTPUT=fastqcfolderout,INPUTRAWREADS=rawfastq))


def multiqc(multiqcpath,multiqcfolderout,namemultiqc,fastqcfolderout):
    """
    Multiqc execution
    :param multiqcpath:
    :param multiqcfolderout:
    :param namemultiqc:
    :param fastqcfolderout:
    :return:
    """
    os.system(command2.format(MULTIQC=multiqcpath,MULTIQCOUTDIR=multiqcfolderout,MULTIQCNAME=namemultiqc,
                              FASTQCOUTFOLDER=fastqcfolderout))

if __name__ == "__main__":
    # set variables
    projectdir = "/mnt/datadisk2/spuccio/SP012_ChipSeq_IRF8_MEOX1/"
    raw_data_dir = "".join([projectdir, "RawReads/"])
    fastqcout = "".join([projectdir, "fastqc_output/"])
    multiout = "".join([projectdir, "multiqc_output/"])
    # dictionary with files name
    raw_fastq = {}
    raw_fastq = {"ES_4_input": "ES_4_input_S5_R1_001.fastq",
                 "IRF8_combo": "IRF8_combo_S3_R1_001.fastq",
                 "IRF8_IP_inv": "IRF8_IP_inv_S2_R1_001.fastq",
                 "IRF8_IP_neb": "IRF8_IP_neb_S1_R1_001.fastq",
                 "Meox_inv": "Meox_inv_S4_R1_001.fastq",
                 "Meox_neb": "Meox_neb_S6_R1_001.fastq"}
    # move to project home folder
    os.chdir(projectdir)
    # create fastq output directory
    createdir(fastqcout)
    # create multiqc output directory
    createdir(multiout)
    # execute fastqc
    for key, value in raw_fastq.items():
        try:
            #subprocess.check_call(" ".join([fastqc, "-o", fastqcout, "".join([raw_data_dir, value])]), shell=True)
            fastqc(shutil.which('fastqc'),fastqcout,"".join([raw_data_dir, value]))
        except subprocess.CalledProcessError:
            print("ERROR.Fastqc analysis failed. Stop execution.")
            sys.exit(1)
        else:
            print("Fastq analysis complete.")

    multiqc(shutil.which('multiqc'),multiout,"fastqc_report",fastqcout)

