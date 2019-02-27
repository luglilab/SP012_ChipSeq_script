import os
import subprocess
import sys
import shutil
# set command
command1 = "{BOWTIE2BUILD} --threads {THREADS} {FASTQFILE} {INDEXNAME}"
command2 = "{BOWTIE2ALIGN} -p {THREADS} --mm -k {MULTIMAP} -X {MAXFRAGLEN} " \
           "-x {INDEXNAME} -U {RAWFASTQ} -S {OUTPUTSAM} 2>{LOGFILE} > {EXECUTIONINFO}"
command3 = "{SAMTOOLS} view -@ {THREADS} -hbS {SAMFILE} -o {BAMFILE}"
command4 = "{MULTIQC} -o {MULTIQCOUTDIR} -i {MULTIQCNAME} {FASTQCOUTFOLDER}"

def createdir(dirpath):
    """

    :param dirpath:
    :return:
    """
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        print(" ".join(["Directory", dirpath.split("/")[-1], "Created"]))
    else:
        print(" ".join(["Directory", dirpath.split("/")[-1], "already exists"]))


def checkindex(indexpath, processor, fastafile, indexname):
    """
    Check if the genome index already exist and in case create a new one
    :param indexpath: Output folder
    :param processor:
    :param fastafile: genome fasta file
    :param indexname: index name
    :return:
    """
    for i in range(1, 5):
        if os.path.isfile("".join([indexpath, "/", indexname, ".", str(i), ".bt2"])) is True:
            print("Genome index %s.%d.bt2 already exists." % (indexname, i))
        else:
            try:
                os.chdir(indexpath)
                os.system(command1.format(shutil.which('bowtie2-build'), processor, fastafile, indexname))
            except subprocess.CalledProcessError:
                print("ERROR.Fastqc analysis failed. Stop execution.")
                sys.exit(1)
            else:
                print("Index %d OK" % i)
    return indexname


def bowtie2mapping(pathwbowtie2, processor, multimappar, maxfrag, indexname, fastqname, samname, logfile, secondlog):
    """

    :param pathwbowtie2:
    :param processor:
    :param multimappar:
    :param maxfrag
    :param indexname:
    :param fastqname:
    :param samname:
    :param logfile:
    :param secondlog:
    :return:
    """
    try:
        os.system(command2.format(BOWTIE2ALIGN=pathwbowtie2, THREADS=processor, MULTIMAP=multimappar,
                                  MAXFRAGLEN=maxfrag,
                                  INDEXNAME=indexname, RAWFASTQ=fastqname, OUTPUTSAM=samname,
                                  LOGFILE=logfile, EXECUTIONINFO=secondlog))
    except [IOError, ValueError]:
        print("ERROR.Mapping of %s with bowtie2 failed. Stop execution." % fastqname)
        sys.exit(1)
    else:
        print("Mapping of %s with bowtie2 complete." % fastqname)


def sam2bam(pathsamtools, processor, inputsam, bamfile):
    """

    :param pathsamtools:
    :param inputsam:
    :param processor:
    :param bamfile:
    :return:
    """
    try:
        os.system(command3.format(SAMTOOLS=pathsamtools, THREADS=processor, SAMFILE=inputsam, BAMFILE=bamfile))
    except [IOError, ValueError]:
        print("ERROR.Conversion of %s with samtools failed. Stop execution." % inputsam)
        sys.exit(1)
    else:
        print("Conversion of %s with samtools complete." % inputsam)


def multiqc(multiqcpath, multiqcfolderout, namemultiqc, fastqcfolderout):
    """
    Multiqc execution
    :param multiqcpath:
    :param multiqcfolderout:
    :param namemultiqc:
    :param fastqcfolderout:
    :return:
    """
    os.system(command4.format(MULTIQC=multiqcpath,
                              MULTIQCOUTDIR=multiqcfolderout,
                              MULTIQCNAME=namemultiqc,
                              FASTQCOUTFOLDER=fastqcfolderout))


if __name__ == "__main__":
    # set path tool
    threads = "40"
    multimap = "4"  # the multimapping flag
    fraglen = "2000"
    GRCh38p12indexpath = "/home/spuccio/AnnotationBowtie2/Homo_sapiens/GencodeGRCh38p12"
    projectdir = "/mnt/datadisk2/spuccio/SP012_ChipSeq_IRF8_MEOX1/"
    mappingout = "/mnt/datadisk2/spuccio/SP012_ChipSeq_IRF8_MEOX1/Mapping/"
    multiout = "".join([projectdir, "multiqc_output/"])
    raw_data_dir = "".join([projectdir, "RawReads/"])
    #
    GRCh38p12fasta = "".join([GRCh38p12indexpath, "/GRCh38.p12.chrs.fa"])
    raw_fastq = {"ES_4_input": "ES_4_input_S5_R1_001.fastq",
                 "IRF8_combo": "IRF8_combo_S3_R1_001.fastq",
                 "IRF8_IP_inv": "IRF8_IP_inv_S2_R1_001.fastq",
                 "IRF8_IP_neb": "IRF8_IP_neb_S1_R1_001.fastq",
                 "Meox_inv": "Meox_inv_S4_R1_001.fastq",
                 "Meox_neb": "Meox_neb_S6_R1_001.fastq"}

    index = checkindex(GRCh38p12indexpath, threads, GRCh38p12fasta, "GRCh38p12")
    createdir(mappingout)
    for key, value in raw_fastq.items():
        bowtie2mapping(pathwbowtie2=shutil.which('bowtie2'), processor=threads,
                       multimappar=multimap,
                       maxfrag=fraglen,
                       indexname="".join([GRCh38p12indexpath, "/", index]),
                       fastqname="".join([raw_data_dir, value]),
                       samname="".join([mappingout, key, ".sam"]),
                       logfile="".join([mappingout, key, ".log"]),
                       secondlog="".join([mappingout, key, ".execution.log"]))
        sam2bam(pathsamtools=shutil.which('samtools'),
                processor=threads,
                inputsam="".join([mappingout, key, ".sam"]),
                bamfile="".join([mappingout, key, ".bam"]))

    multiqc(multiqcpath=shutil.which('multiqc'),
            multiqcfolderout=multiout,
            namemultiqc="fastqc_mapping_report",
            fastqcfolderout=mappingout)
