# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:26:16 2019

@author: Johanna Rahm, Research Group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt am Main.
"""

import datetime
import numpy as np
import matplotlib.pyplot as plt

class ExpDisplacement():
    def __init__(self):
        self.mjd = []
        self.file_name = ""
        self.base_name = ""
        self.mjd_histogram = []
        #self.mjd_frequency_max = 0#
        #self.mjd_max_index = 0#
        #self.mjd_max = 0
        self.average_mjd = 0
         
    def load_seg_file(self, file_name):
        """
        If True Create self.mjd (numpy.ndarray) col0 = mjd, col1 = mjd_n else raise error.
        
        :param file_name: Name of the inserted file by widgetExpDisp. 
        """
        if not (file_name == ""):
            self.mjd = np.loadtxt(file_name, usecols = (1, 2)) # col0 = mjd, col1 = mjd_n
        else:
            print("Insert a file name.")
        
    def count_mjd_frequencies(self):
        """
        Create histogram with col0 = bins = mjd and col1 = frequencies as np.ndarray.
        
        """
        max_bin = int(np.ceil(self.mjd[:,0].max()/20)*20)  # max mjd ceiled and divisible by 20
        bin_size = int(np.ceil(self.mjd[:,0].max()/20))  # divides the bin range in sizes -> desired bin = max_bin/bin_size
        hist = np.histogram(self.mjd[:,0],
                                        range = (0, max_bin),
                                        bins = bin_size,
                                        density = True,
                                        weights = self.mjd[:,1])
        self.mjd_histogram = np.zeros([np.size(hist[0]),2])
        self.mjd_histogram [:,0] = hist[1][:-1]  # mjd [nm]
        self.mjd_histogram [:,1] = hist[0][:]  # frequencies
        
    def calc_exp_displacement(self):
        """
        Exp_displacement = average displacement.
        """
        #self.mjd_frequency_max = self.mjd_histogram[:,1].max()
        #self.mjd_max_index = self.mjd_histogram[:,1].argmax()
        #self.mjd_max =  self.mjd_histogram[self.mjd_max_index, 0]
        #print("The expected displacement is %i [nm].\nThe corresponding frequency is %.4e." %(self.mjd_max, self.mjd_frequency_max))
        mjd_no_zeros = np.ma.masked_array(self.mjd[:,0], self.mjd[:,0] == 0)
        self.average_mjd = mjd_no_zeros.mean()

    def save_mjd_frequencies(self, directory, base_name):
        """
        Create a mjd_frequencies.txt file with exp displacement in header, col0 = mjd, col1 = frequencies.
        """
        now = datetime.datetime.now()
        year = str(now.year)
        year = year[2:]
        month = str(now.month)
        if len(month) == 1:
            month = str(0) + month
        day = str(now.day)
        out_file_name = directory + "\ " + year + month + day + "_" + base_name[:-19] + "mjd_frequencies.txt"  # Betriebssystemunabhängig?!?!?!
        #header = "The expected displacement is %i [nm].\nThe corresponding frequency is %.4e.\n" %(self.mjd_max, self.mjd_frequency_max)
        header = "The expected displacement is %.3f [nm].\n" %(self.average_mjd)
        header += "mjd [nm]\t fraction\t"
        np.savetxt(out_file_name, 
                   X=self.mjd_histogram,
                   fmt = ("%i","%.4e"),
                   header = header)
        
    def plot_mjd_frequencies(self, directory, base_name):
        now = datetime.datetime.now()
        year = str(now.year)
        year = year[2:]
        month = str(now.month)
        if len(month) == 1:
            month = str(0) + month
        day = str(now.day)
        out_file_name = directory + "\ " + year + month + day + "_" + base_name[:-19] + "mjd_frequencies.pdf"
        fig = plt.figure()
        sp = fig.add_subplot(1, 1, 1)  # only 1 plot
        sp.bar(self.mjd_histogram [:,0], self.mjd_histogram [:,1], 
               align = "center",
               width = 20,  # width = bin size
               color = "gray",
               edgecolor = "black")
        sp.set_title("PDF of Mean Jump Distance")
        sp.set_xlabel("Mean Jump Distance [nm]")
        sp.set_ylabel("Fraction")
        plt.savefig(out_file_name)
        plt.show()  # print the graph
        print("The expected displacement is %.3f nm." %(self.average_mjd)) 
        
    
def main():
    exp_displacement = ExpDisplacement()
    #exp_displacement.file_name = "F:\\Marburg\\single_colour_tracking\\resting\\160404_CS5_Cell1\\cell_1_MMStack_Pos0.ome.tif.tracked.seg.txt"
    exp_displacement.load_seg_file()
    exp_displacement.count_mjd_frequencies()
    exp_displacement.calc_exp_displacement()
    exp_displacement.save_mjd_frequencies()
    exp_displacement.plot_mjd_frequencies()
    
if __name__ == "__main__":
    main()
 
    