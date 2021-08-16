#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Checkm-to-OGs.py: filter fasta based on a negative list"""
__author__ = "Luc Cornet"
__copyright__ = "Copyright 2021, Sciensano"
__version__ = "1.0.0"
__maintainer__ = "Luc Cornet"
__email__ = "luc.cornet@uliege.be"
__status__ = "Production"

import click
from collections import defaultdict

@click.command()
###ARGUMENT#####
#main file - Postitive List of Orgs 
@click.argument('main_file', type=click.Path(exists=True,readable=True))
#option
@click.option('--maxdupe', default='5', help='Maximum number of multi hits for an OGs')
@click.option('--fraction', default='0.5', help='minimal fraction of total number of orgs in an OGs')

def main(main_file, maxdupe, fraction):
    #open checkm qa file
    checkmfile = open(main_file)

    #declare
    org = 'NA'
    marker = 'NA'
    org_markers= defaultdict( lambda: defaultdict(lambda: defaultdict( dict )))
    multi_orgs = defaultdict( lambda: defaultdict(lambda: defaultdict( dict )))
    markers_of = {}
    markers_dup = {}
    orgs_of = {}
    markers_org = {}


    for line in checkmfile:
        list_record = line.replace("\n", "")
        if ('>' in list_record):
            split_list = list_record.split(" ")
            org = split_list[0]
            org = org.replace(">", "")
            markerchunks = split_list[3]
            split_list = markerchunks.split(";")
            marker = split_list[0]
            marker = marker.replace("marker=", "")
            markers_of[marker] = 1
            orgs_of[org] = 1
            #register the number of org
            if (marker not in markers_org):
                markers_org[marker] = 1
            else:
                markers_org[marker] += 1

        else:
            sequence = list_record
            #load in nested dict
            if (marker not in org_markers):
                org_markers[marker][org] = sequence
            elif (marker in org_markers):
                temp_dict = org_markers[marker]
                if (org not in temp_dict):
                    org_markers[marker][org] = sequence
                else:
                    #Wrining double hits 
                    #print('Warning double hits for ' + str(org) + ' in ' + str(marker) + ' marker.')
                    if (marker in markers_dup):
                        markers_dup[marker] += 1
                    else:
                        markers_dup[marker] = 1
                    #register org for this marker
                    multi_orgs[marker][org] = 1
                    #delete one count of org 
                    markers_org[marker] = int(markers_org[marker]) - 1
    
    #Print fasta sequence for OGs
    deleteddupe = 0
    deletedfra = 0
    totorgnumber = len(orgs_of)
    for marker in markers_of:
        #number of fupe
        dupe = 0
        if (marker in markers_dup):
            dupe = int(markers_dup[marker])
        else:
            dupe = 0
        #number of org
        orgnumber = markers_org[marker]
        orgfraction = float(orgnumber) / float(totorgnumber)


        #Check if OGs pass the dupe threshold
        if (int(dupe) > int(maxdupe)):
            deleteddupe += 1
        elif(float(orgfraction) < float(fraction)):
            deletedfra += 1
        else:
            #continue with this OG
            markerfile = str(marker) + '.ali'
            out_file = open(markerfile, "w")
            multi_of = multi_orgs[marker]
            sequences_of = org_markers[marker]
            #loop in each org
            for org in sequences_of:
                #check if this org is printable for this marker (no dupe)
                if (org in multi_of):
                    continue
                else:
                    #Print
                    sequence = sequences_of[org]
                    out_file.write('>'+ str(org) + "\n")
                    out_file.write(str(sequence) + "\n")
    
    markernumber = len(markers_of)
    print(str(markernumber) + ' markers.')
    markerdup = len(markers_dup)
    print(str(markerdup) + ' markers with more than one hit for each organism')
    print(str(deleteddupe) + ' deleted markers due to too multiple hits.')
    print(str(deletedfra) + ' deleted markers due to too few orgs.')
    markernumber = markernumber - deleteddupe - deletedfra
    print(str(markernumber) + ' conserved markers.')


if __name__ == '__main__':
    main()
