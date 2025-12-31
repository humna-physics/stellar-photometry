import pandas as pd # pandas is a common package for handling data in tables known as DataFrames
import re           # for Regular expressions
 
strFileName = "Measurements_M15_ASCC992597_3.xls" # Save the filename as a string. Ensure you include the file extension (.xls)
ClusterData = pd.read_csv(strFileName, sep = "\t") # Read data from the file into a pandas DataFrame
display(ClusterData)
def isValidCol(colName):                                       # Sets the function name and the input name used within
    if (colName[0:10] == 'rel_flux_T' or colName == 'Label'):  # If statement with two true conditions
        return True                                            # Returns True if either of the above conditions met
    else:
        return False                                           # Returns False if neither condition is met
ClusterData = pd.read_csv(strFileName, sep = '\t', usecols = isValidCol) # Rerun read_csv() only keeping desired columns
 
display(ClusterData) # Display the DataFrame to check it has only included the requested columns
strFilter = r'.*_([BV]).*' # Define a regular expression that will match any strings that contain _B or _V
ClusterData['Label'] = [re.search(strFilter, x).group(1) for x in ClusterData['Label']] # Searching for B or V in label
display(ClusterData) # Display the DataFrame to check the change has occurred.
ClusterData.set_index('Label', inplace = True) # Set the column called 'Label' to be the index for the DataFrame.
ClusterData = ClusterData.transpose()  # Transpose 
 
display(ClusterData)
ClusterData['FluxRatio'] = ClusterData['B']/ClusterData['V'] # Creates a new column called FluxRatio
 
display(ClusterData)
import numpy as np               # Numpy has essential tools for manipulating lists of data
import matplotlib.pyplot as plt  # Matplotlib is the tool for plotting data
REF_B_MAG = 10.928                          # <<<< Enter the apparent B magnitude of the reference star
REF_V_MAG = 10.378    # <<<< Enter the apparent V magnitude of the reference star
ClusterData['Bmag'] = -2.5 * np.log10(ClusterData['B']) + REF_B_MAG               # <<<< Calculate the apparent B magnitude using the rearranged Equation 2.1b
ClusterData = ClusterData[ClusterData['V'] > 0].copy()
ClusterData['Vmag'] = -2.5 * np.log10(ClusterData['V']) + REF_V_MAG                    # <<<< Calculate the apparent V magnitude using the rearranged Equation 2.1b
ClusterData['B_V']  = (ClusterData['Bmag']- ClusterData['Vmag'])
ClusterData['B_V'] = ClusterData['B_V'].round(4)
# <<<< Calculate the colour index B-V by subtracting Vmag from Bmag
display(ClusterData.head(5)) # Display the top 5 lines to check the new columns have been calculated correctly
# Code for your CMD plot
B_V =  ClusterData['B_V']              # <---- Put here the DataFrame column for the B-V colour, e.g. DataFrame['B-V']
V = ClusterData['Vmag']                 # <---- Put here the DataFrame column for the V colour, e.g. DataFrame['Vmag']
 
keep_list = ClusterData['B_V'] < 2.5 # Questions which rows have a value less than 2.0 in the column B-V
ClusterData_red_removed = ClusterData[keep_list] # Save a new DataFrame based on the Boolean operator list
 
plt.rcParams['figure.figsize'] = [12, 8] # Set figure.figsize to be 12 inches wide and 8 inches high.
plt.scatter(                            # pyplot.scatter() function
    ClusterData_red_removed["B_V"],       # Required input - x values
    ClusterData_red_removed["Vmag"],      # Required input - y values
    c = ClusterData_red_removed["B_V"],   # Setting colour based on B-V colour
    cmap = "coolwarm",                  # Setting the colour map to use
    s = 3)                              # Setting datapoint size
 
plt.ylim(16, 9) # Set y axis limits, with the higher number first to invert the axis
plt.xlim(-0.2, 1.6)
plt.title('Colour Magnitude diagram of M15 Cluster') # Set plot title
plt.xlabel('Colour index (B_V)') # Set x axis label
plt.ylabel('Apparent V magnitude') # Set y axis label
plt.text(0.1, 15.5, 'Horizontal branch')
plt.plot([0.0, 0.4], [14.5, 14.5])
plt.text(1.0, 13, 'Giant branch')
plt.plot([0.85, 1.4], [14.8, 12.2])
plt.text(0.5, 12, 'Likely interloper stars')
plt.show() # Show the plot
