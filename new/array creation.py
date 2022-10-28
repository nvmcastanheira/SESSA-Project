
from numpy import *
from tqdm import tqdm
import os
import time
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# =============================================================================
# material = [["Si"],["Si", "O2"], ["Al"], ["Ga", "As"], ["Ge"], 
#             ["In4", "Sn3", "O12"], ["Cu"], ["Zn", "O"], ["Li", "Nb", "O3"], ["K","Ti","O","P","O4"]] #Append C to the end of each for carbonated ones
# =============================================================================
material = [["K","Ti","O","P","O4"],["K","Ti","O","P","O4","C"]]

par1 = range(5,11)
arr = empty([shape(material)[0], size(par1),2048,2])
lists = []

for matnum, mat in tqdm(enumerate(material)):
    path= "/home/nuno/Desktop/fun/output/{}".format(''.join(mat))
    lists.append("{}".format(''.join(mat)))
    for par in par1: 
        path2 = "{}/{}_{}reg1.spc".format(path,''.join(mat),par)
        r = loadtxt(path2)
        arr[matnum,int(par-min(par1))] = r
        
save("/home/nuno/Desktop/fun/output/Master", arr)
lists.append("Thickness Range = {}-{}nm".format(min(par1),max(par1)))
lists.append("Array dimensions = {}".format((shape(arr))))
savetxt("/home/nuno/Desktop/fun/output/Master_list", lists,fmt='%s')
time.sleep(1)
arr = load("/home/nuno/Desktop/fun/output/Master.npy")
print(shape(arr))
print(arr[-1,-1,-1,-1])
plt.figure(figsize = (15,8))
plt.xlabel("Energy (eV)")
plt.ylabel("Counts")
for i in range(size(par1)):
    plt.plot(arr[1,i,:,0], arr[1,i,:,1])
names = ["Thickness = "+str(i)+" nm" for i in par1]
plt.legend(names)

