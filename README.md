# Script used in the study

Link to BioRx

## anvio_pan-to-OGs.py

Extract orthologous groups (OGs) from the pangenomic fasta file of anvi'o:  
https://merenlab.org/2016/11/08/pangenomics-v2/  

      ./anvio_pan-to-OGs.py < pangenomic fasta file >  

## anvio_OGs-filtration.py

Create a list of OGs after filtration, based on a postive list of genomes.

    ./anvio_OGs-filtration.py Honey-genomes.list
    --pfilter=yes --fraction=0.9 --unwanted=1
    --cfilter=yes --maxcopy=1.5 --hfilter=yes
    --hindex=../LMG_Pan-PAN-homogeneity.txt
    --maxfunctionalindex 0.8 --maxgeometricindex 0.8

    Usage: anvio_OGs-filtration.py [OPTIONS] MAIN_FILE

    Options:
      --mode TEXT                OG inference mode: anvio or OF
      --pfilter TEXT             presence filter: yes or no
      --fraction TEXT            fraction of orgs from the positive list needed
                                 to conserve a file

      --unwanted TEXT            Maximum of unwanted org in a file to be conserved
      --cfilter TEXT             copy filter: yes or no
      --maxcopy TEXT             Mean of maximum of sequence of the same org in a
                                 file to be conserved

      --hfilter TEXT             homogeneity filter (anvio only): yes or no
      --hindex TEXT              homogeneity index (anvio only): path
      --maxfunctionalindex TEXT  Maximum functional index of anvio (1 perfect) for
                                 a file to be conserved

      --maxgeometricindex TEXT   Maximum geometric index of anvio (1 perfect) for
                                 a file to be conserved

      --cogtable TEXT            path to cog table
      --help                     Show this message and exit.

## Checkm-to-OGs.py  

Extract OGs from checkm markers file (qa workflow of Checkm):  
https://github.com/Ecogenomics/CheckM/wiki/Genome-Quality-Commands#qa  

    ./Checkm-to-OGs.py  checkm-qa-9.markers --fraction=0.8  

    Usage: Checkm-to-OGs.py [OPTIONS] MAIN_FILE

    Options:
      --maxdupe TEXT   Maximum number of multi hits for an OGs
      --fraction TEXT  minimal fraction of total number of orgs in an OGs
      --help           Show this message and exit.
