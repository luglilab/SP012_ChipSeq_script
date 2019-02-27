import os
# strand shifts at which cross-correlation
command1 = "{Rscript} {phantompeak} -rf -s=-100:5:600 -c={inputfile} -p={thread} -savp -out={output}"
command2 = "{bamcoverage} -b {inputbam} -o {outputbigwig} -p {thread} -of bigwig -bs 10 --effectiveGenomeSize " \
           "{genomesize} --normalizeUsing RPKM -e 200 "


def phantompeak(RscriptPath, spppath, bamfile, thread, pdffile):
    """
    Phantom peak - strand cross-correlation peak / predominant fragment length
    :param RscriptPath:
    :param spppath:
    :param bamfile:
    :param pdffile:
    :return:
    """
    os.system(
        command1.format(Rscript=RscriptPath, phantompeak=spppath, inputfile=bamfile, thread=thread, output=pdffile))


def bam2bigwig(bamcoveragePath, bamfile, bigwipout, thread, gensize):
    """
    Conversion BAM to Big WIG normalized
    :param bamcoveragePath:
    :param bamfile:
    :param bigwipout:
    :param gensize:
    :return:
    """
    os.system(command2.format(bamcoverage=bamcoveragePath, inputbam=bamfile, outputbigwig=bigwipout, thread=thread,
                              genomesize=gensize))


def createdir(dirpath):
    """
    Make directory function
    :param dirpath:
    :return:
    """
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        print(" ".join(["Directory", dirpath.split("/")[-1], "Created"]))
    else:
        print(" ".join(["Directory", dirpath.split("/")[-1], "already exists"]))


if __name__ == "__main__":
    Rscript = "/home/spuccio/miniconda3/envs/chipseq_env/bin/Rscript"
    spp = "/home/spuccio/miniconda3/envs/chipseq_env/bin/run_spp.R"
    BAMfile = {"IRF8_IP_inv": "IRF8_IP_inv_rmdup.bam",
               "IRF8_combo": "IRF8_combo_rmdup.bam",
               "Meox_neb": "Meox_neb_rmdup.bam"}
    inputpath = "/home/spuccio/datadisk2/SP012_ChipSeq_IRF8_MEOX1/Mapping/"
    outputpath = "/home/spuccio/datadisk2/SP012_ChipSeq_IRF8_MEOX1/phantompeak_bigwig_GSE98264/"
    bamcoverage = "/home/spuccio/miniconda3/bin/bamCoverage"
    genomesize = "2747877777"
    thread = "30"
    createdir(outputpath)
    for key, value in BAMfile.items():
        phantompeak(RscriptPath=Rscript, spppath=spp, bamfile="".join([inputpath, value]), thread=thread,
                    pdffile="".join([outputpath, key, ".pdf"]))
        bam2bigwig(bamcoveragePath=bamcoverage, bamfile="".join([inputpath, value]),
                   bigwipout="".join([outputpath, key, ".bw"]), thread=thread, gensize=genomesize)
