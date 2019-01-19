import os
import subprocess
import sys
# set path tool
threads = "40"
GRCh38p12indexpath = "/home/spuccio/AnnotationBowtie2/Homo_sapiens/GencodeGRCh38p12"
bowtiebuild2path = "/home/spuccio/miniconda3/envs/chipseq_env/bin/bowtie2-build"
bowtie2path = "/home/spuccio/miniconda3/envs/chipseq_env/bin/bowtie2"
projectdir = "/mnt/datadisk2/spuccio/SP012_ChipSeq_IRF8_MEOX1/"
mappingout = "".join([projectdir, "mapping"])
raw_data_dir = "".join([projectdir, "RawReads/"])
#
GRCh38p12fasta = "".join([GRCh38p12indexpath, "/GRCh38.p12.chrs.fa"])
raw_fastq = {"ES_4_input": "ES_4_input_S5_R1_001.fastq",
             "IRF8_combo": "IRF8_combo_S3_R1_001.fastq",
             "IRF8_IP_inv": "IRF8_IP_inv_S2_R1_001.fastq",
             "IRF8_IP_neb": "IRF8_IP_neb_S1_R1_001.fastq",
             "Meox_inv": "Meox_inv_S4_R1_001.fastq",
             "Meox_neb": "Meox_neb_S6_R1_001.fastq"}


def createdir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        print(" ".join(["Directory", dirpath.split("/")[-1], "Created"]))
    else:
        print(" ".join(["Directory", dirpath.split("/")[-1], "already exists"]))

# check index function


def checkindex(indexpath, fastafile, indexname):
    for i in range(len(os.listdir(indexpath))):
        if os.listdir(indexpath)[i].split(".")[-1] == "bt2":
            print("Genome index of Fasta file already exists.")
            break
        else:
            try:
                subprocess.check_call(" ".join([bowtiebuild2path, "--threads", threads, fastafile, indexname]),
                                      shell=True)
            except subprocess.CalledProcessError:
                print("ERROR.Fastqc analysis failed. Stop execution.")
                sys.exit(1)
            else:
                print("Fastq analysis complete.")
    return indexname


def bowtie2mapping(indexname, fastqname, samname):
    try:
        subprocess.check_call(" ".join([bowtie2path, "-p", threads, "-q", "--local", "-x", indexname,
                                        "".join([raw_data_dir, fastqname]), "-S", "".join([mappingout, samname])]),
                              shell=True)
    except subprocess.CalledProcessError:
        print("ERROR.Mapping of %s with bowtie2 failed. Stop execution." % fastqname)
        sys.exit(1)
    else:
        print("Mapping of %s with bowtie2 complete." % fastqname)


if __name__ == "__main__":
    index = checkindex(GRCh38p12indexpath, GRCh38p12fasta, "GRCh38p12")
    createdir(mappingout)
    for key, value in raw_fastq.items():
        bowtie2mapping("".join([GRCh38p12indexpath, "/", index]), value, key)
