# -*- coding: utf-8 -*-
"""
@author: Abraham Carranza
"""


from __future__ import with_statement
import re
import statistics
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# regex patterns to clean data collection txt file
# regex floating point pattern 
regex_fpp = '[+-]?(?:[0-9]*[.])?[0-9]+'
# regex find coding rate line
regex_cd = '(?i)coding rate'
regex_sf = '(?i)spreading factor'
regex_send_packet_request = '(?i)Sending Packet Request'



# initialize for filedialog popup
root = tk.Tk()
root.withdraw()

# open file popup
with open(str(filedialog.askopenfilename()), "rt") as our_file:
    # arrays to save data collection samples (n = 10)
    rssi_ra = [0]*10
    snr_ra = [0] *10
    
    # create .csv is doesn't already exist in name of .txt file opened
    try:
        file_string = str(Path(str(our_file)).stem) + ".csv"
        with open(file_string, "x") as new_file:
            print(file_string +" created succcessfully.")
    except FileExistsError:
        file_string = str(Path(str(our_file)).stem) + ".csv"
        with open(file_string, "w") as new_file:
            print(file_string + " successfully open in write mode")
            
    # open .csv
    with open(file_string, "w") as new_file:
        # initialize current coding rate and spreading factor determined by .txt file opened and set current spreading factor counter
        current_cr = 0
        current_sp = 0
        sf_counter = 0
        # column names for csv
        new_file.write("Coding Rate,Spreading Factor,RSSI Avg (n=10),SNR Avg (n=10)\n")
        
        # go through txt file line by line
        for line in our_file:
            # w through z create lists of regex expression satisfied
            x = re.findall(regex_fpp, line)
            y = re.findall(regex_cd, line)
            z = re.findall(regex_sf, line)
            w = re.findall(regex_send_packet_request, line)
            
            #if list cr is not empty extract its coding rate
            if y:
                #new_file.write(line)
                extract_cr = re.findall(regex_fpp, line)
                current_cr = extract_cr[1]
            # if list for spreading factor not empty extract sf and initialize counter when found
            elif z:
                #new_file.write(line)
                extract_sf= re.findall(regex_fpp, line)
                current_sp = extract_sf[0]
                sf_counter = 0
            # if send packet request line found continue
            elif w:
                pass
            # if rssi and snr data found
            elif x:
                sf_counter += 1;
                #new_file.write(str(current_cr) + "," + str(current_sp) + ",")
                if len(x) < 3:
                    # for i in x:
                    #     new_file.write(i+",")
                    rssi_ra[sf_counter-1] = x[0]
                    snr_ra[sf_counter-1] = x[1]
                    
                else:
                    # for integer_i in x[1:]:
                    #     new_file.write(integer_i + ",")
                    rssi_ra[sf_counter-1] = x[1]
                    snr_ra[sf_counter-1] = x[2]
                if(sf_counter == 10):
                    sf_counter = 0;       
                    new_file.write(str(current_cr) + "," + str(current_sp) + ",")
                    # for i in x[1:]:
                    #     new_file.write(i + ",")
                    #print(statistics.mean([float(x) for x in rssi_ra]))
                    new_file.write(str(statistics.mean([float(x) for x in rssi_ra])) + "," + str(statistics.mean([float(x) for x in snr_ra]) )+ ",")    
                    new_file.write("\n")
                    
print("done")