
from numpy import *
from tqdm import tqdm
import os
import time
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


material = [["Si"],["Si", "O2"], ["Al"], ["Ga", "As"], ["Ge"], 
           ["In4", "Sn3", "O12"], ["Cu"], ["Zn", "O"], ["Li", "Nb", "O3"], ["K","Ti","O","P","O4"],["Si","C"],["Si", "O2","C"], ["Al","C"], ["Ga", "As","C"], ["Ge","C"], 
           ["In4", "Sn3", "O12","C"], ["Cu","C"], ["Zn", "O","C"], ["Li", "Nb", "O3","C"], ["K","Ti","O","P","O4","C"]] 
#Copy material list in spectra-generating script. Add "C" for carbonated samples.

par1 = array(range(40, 41)) #Same thickness ass spectra-generating script.
arr = empty([shape(material)[0], size(par1),2048,2]) #Array dimensions. First index is # of materials, second is # of thicknesses.
lists = [] #Output text file.

for matnum, mat in tqdm(enumerate(material)):
    path= "/home/nuno/Desktop/fun/output/{}".format(''.join(mat)) #Output path.
    lists.append("{}".format(''.join(mat))) #Appends material iteration to output text.
    for idx, par in enumerate(par1): 
        path2 = "{}/{}_{}reg1.spc".format(path,''.join(mat),par) #Input spectra for array.
        r = loadtxt(path2)
        arr[matnum,idx] = r #"Append" material spectra to matnum index (material) and idx index (thickness).
        
save("/home/nuno/Desktop/fun/outputscat2/Mastertestscat2notref", arr) #Save npy array.
lists.append("Thickness Range = {}-{} angstroms".format(min(par1),max(par1)))
lists.append("Array dimensions = {}".format((shape(arr))))
savetxt("/home/nuno/Desktop/fun/outputscat2/Master_listtestscat2notref", lists,fmt='%s') #Save output text.
