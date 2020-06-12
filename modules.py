import numpy as np
import os
import pandas as pd
import math
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import matplotlib.patches as mpatches
from matplotlib import colors

def Rose(directory = "/Users/x53965mb/Python/Fieldwork/Data", filename = "PB_pci_1E.csv", bins = 8, equal_area = True, standard_radius = 'No', tickmarks_interval = 10, save = False):
    # Main user input section
    os.chdir(directory) # Sets working directory
    # Set how many bins the plot should have
    bins=bins
    # Load and assign data
    data = pd.read_csv(filename)
    # Assign data from spreadsheet
    PCI_ddir = data.PCI_ddir
    #PCI_dip = data.PCI_dip
    #PCI_type = data.Type
    logname = data.Location[0]
    
    PC_ddir = np.where(PCI_ddir < 180, PCI_ddir + 180, PCI_ddir - 180) #converts measurements of imbrication to paleocurrent directions
    
    #Conversion to rose-diagram input

    bin_int = 360/bins
    
    bin_classes = []
    binn = []
    counts = []
    counts_perc = []

    for x in range(bins):
        #Define bin limits:
        bin_classes.append(((x*bin_int),((x+1)*bin_int)))
        #Seperate the measurements into bins, using a ≤ x < b :
        binn.append(np.array([(PC_ddir[(PC_ddir >= (x)*bin_int) & (PC_ddir < (x+1)*bin_int)])]))
        #Count how many values in each bin, using a ≤ x < b :
        counts.append(np.count_nonzero((PC_ddir >= (x)*bin_int) & (PC_ddir < (x+1)*bin_int))) 
    
    #Convert number of counts to percentage of total counts in each bin:
    for x in counts:
        counts_perc.append(x/sum(counts)*100)
        
    if equal_area == True or equal_area == 'Yes':
        #Plotting with equal area
        #Ploting with dataset-dependent radius
    
        if type(standard_radius) == int:
            radius = standard_radius
            #Calculate the unit radius (r_1%), depending on input maximum radius:
            r_unit = radius/math.sqrt(radius)
            #Define r or y axis tickmarks:
            r_ticks = [r_unit]
            r_tickslabels = ['1%']
            r_ticksinterval = tickmarks_interval #Sets the spacing between radius ticks
            for x in range(0,int(radius)+r_ticksinterval,r_ticksinterval):
                r_ticks.append(r_unit*math.sqrt(x))
                r_tickslabels.append(x)
        else:
            #Calculate the unit radius (r_1%), depending on largest bin:
            r_unit = max(counts_perc)/math.sqrt(max(counts_perc))
            #Define r or y axis tickmarks:
            r_ticks = [r_unit]
            r_tickslabels = ['1%']
            r_ticksinterval = tickmarks_interval #Sets the spacing between radius ticks
            for x in range(0,int(max(counts_perc))+r_ticksinterval,r_ticksinterval):
                r_ticks.append(r_unit*math.sqrt(x))
                r_tickslabels.append(x)
            
        #Calculate radii corresponding to each bin:
        radii = []
        for x in counts_perc:
            radii.append(r_unit * math.sqrt(x))
          

        theta = np.linspace(0.0, 2 * np.pi, bins, endpoint=False)+(np.pi/bins) #Last bracketed term sets of the bin starting point
        width = (2*np.pi)/bins #Calculates bin width depending on number of bins
        ax = plt.subplot(111, projection='polar')
        ax.bar(theta, radii, width=width, bottom=0.0) #Plots equal-area
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise

        ax.set_yticks(r_ticks)
        ax.set_yticklabels(r_tickslabels)
        ax.set_rlabel_position(-85)  # Move radial labels away from plotted line

        plt.title(('Rose diagram {}'.format(data.Location[0]) + '\n N = {}'.format(len(PC_ddir))))
        if save == False:
            return()
        else:
            plt.savefig('Rose diagram {}.svg'.format(data.Location[0]), bbox_inches='tight')
        plt.show()
    
    else:
        #Plotting non-equal area
        #Plotting dataset dependent maximum radius
  
        theta = np.linspace(0.0, 2 * np.pi, bins, endpoint=False)+(np.pi/bins) #Last bracketed term sets of the binstarting point
        width = (2*np.pi)/bins # Calculates bin width depending on number of bins
        ax = plt.subplot(111, projection='polar')
        ax.bar(theta, counts_perc, width=width, bottom=0.0) #Plots non-equal area
        
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise
        ax.set_rlabel_position(-85)  # Move radial labels away from plotted line
        
        if type(standard_radius) == int:
            plt.ylim(top=standard_radius)
        else:
            pass
        
        plt.title(('Rose diagram {}'.format(data.Location[0]) + '\n N = {}'.format(len(PC_ddir))))
        if save == False:
            return()
        else:
            plt.savefig('Rose diagram {}.svg'.format(data.Location[0]), bbox_inches='tight')
        plt.show()
        
###################################################################

def Rose_all(directory = "/Users/x53965mb/Python/Fieldwork/Data", bins = 8, equal_area = True, standard_radius = 'No', tickmarks_interval = 10, save = False):
    # Main user input section
    os.chdir(directory) # Sets working directory
    # Set how many bins the plot should have
    bins=bins
    files = os.listdir()
    files_csv = [f for f in files if f[-3:] == 'csv']
    df = [pd.read_csv(x) for x in files_csv]
    
    all_PCI = [df[x].PCI_ddir for x in range(len(files_csv))]
    flat_all_PCI = np.array([item for sublist in all_PCI for item in sublist])
    
    PC_ddir = np.where(flat_all_PCI < 180, flat_all_PCI + 180, flat_all_PCI - 180) #converts measurements of imbrication to paleocurrent directions

    bin_int = 360/bins
    bin_classes = []
    binn = []
    counts = []
    counts_perc = []

    for x in range(bins):
        #Define bin limits:
        bin_classes.append(((x*bin_int),((x+1)*bin_int)))
        #Seperate the measurements into bins, using a ≤ x < b :
        binn.append(np.array([(PC_ddir[(PC_ddir >= (x)*bin_int) & (PC_ddir < (x+1)*bin_int)])]))
        #Count how many values in each bin, using a ≤ x < b :
        counts.append(np.count_nonzero((PC_ddir >= (x)*bin_int) & (PC_ddir < (x+1)*bin_int))) 
        
    #Convert number of counts to percentage of total counts in each bin:
    for x in counts:
        counts_perc.append(x/sum(counts)*100)
        
    if equal_area == True or equal_area == 'Yes':
        #Plotting with equal area
        #Ploting with dataset-dependent radius
    
        if type(standard_radius) == int:
            radius = standard_radius
            #Calculate the unit radius (r_1%), depending on input maximum radius:
            r_unit = radius/math.sqrt(radius)
            #Define r or y axis tickmarks:
            r_ticks = [r_unit]
            r_tickslabels = ['1%']
            r_ticksinterval = tickmarks_interval #Sets the spacing between radius ticks
            for x in range(0,int(radius)+r_ticksinterval,r_ticksinterval):
                r_ticks.append(r_unit*math.sqrt(x))
                r_tickslabels.append(x)
        else:
            #Calculate the unit radius (r_1%), depending on largest bin:
            r_unit = max(counts_perc)/math.sqrt(max(counts_perc))
            #Define r or y axis tickmarks:
            r_ticks = [r_unit]
            r_tickslabels = ['1%']
            r_ticksinterval = tickmarks_interval #Sets the spacing between radius ticks
            for x in range(0,int(max(counts_perc))+r_ticksinterval,r_ticksinterval):
                r_ticks.append(r_unit*math.sqrt(x))
                r_tickslabels.append(x)
            
        #Calculate radii corresponding to each bin:
        radii = []
        for x in counts_perc:
            radii.append(r_unit * math.sqrt(x))
          

        theta = np.linspace(0.0, 2 * np.pi, bins, endpoint=False)+(np.pi/bins) #Last bracketed term sets of the bin starting point
        width = (2*np.pi)/bins #Calculates bin width depending on number of bins
        ax = plt.subplot(111, projection='polar')
        ax.bar(theta, radii, width=width, bottom=0.0, color=(1.0,0.0,0.0,0.6)) #Plots equal-area
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise

        ax.set_yticks(r_ticks)
        ax.set_yticklabels(r_tickslabels)
        ax.set_rlabel_position(-85)  # Move radial labels away from plotted line

        plt.title(('Rose diagram of all measurements') + '\n N = {}'.format(len(PC_ddir)))
        if save == False:
            return()
        else:
            plt.savefig('Rose diagram all data.svg', bbox_inches='tight')
        plt.show()
    
    else:
        #Plotting non-equal area
        #Plotting dataset dependent maximum radius
  
        theta = np.linspace(0.0, 2 * np.pi, bins, endpoint=False)+(np.pi/bins) #Last bracketed term sets of the binstarting point
        width = (2*np.pi)/bins # Calculates bin width depending on number of bins
        ax = plt.subplot(111, projection='polar')
        ax.bar(theta, counts_perc, width=width, bottom=0.0, color=(1.0,0.0,0.0,0.6)) #Plots non-equal area
        
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise
        ax.set_rlabel_position(-85)  # Move radial labels away from plotted line
        
        if type(standard_radius) == int:
            plt.ylim(top=standard_radius)
        else:
            pass
        
        plt.title(('Rose diagram of all measurements') + '\n N = {}'.format(len(PC_ddir)))
        if save == False:
            return()
        else:
            plt.savefig('Rose diagram all data.svg', bbox_inches='tight')
        plt.show()
        
#######################################################################