
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
#material = [["Al"]]#,["K","Ti","O","P","O4","C"]]
# =============================================================================
# material = [["Si"],["Si", "O2"], ["Al"], ["Ga", "As"], ["Ge"], 
#             ["In4", "Sn3", "O12"], ["Cu"], ["Zn", "O"], ["Li", "Nb", "O3"], ["K","Ti","O","P","O4"],["Si","C"],["Si", "O2","C"], ["Al","C"], ["Ga", "As","C"], ["Ge","C"], 
#                         ["In4", "Sn3", "O12","C"], ["Cu","C"], ["Zn", "O","C"], ["Li", "Nb", "O3","C"], ["K","Ti","O","P","O4","C"]] 
# =============================================================================
material = [["Si"],["Si", "O2"], ["Al"], ["Ga", "As"], ["Ge"], 
           ["In4", "Sn3", "O12"], ["Cu"], ["Zn", "O"], ["Li", "Nb", "O3"], ["K","Ti","O","P","O4"],["Si","C"],["Si", "O2","C"], ["Al","C"], ["Ga", "As","C"], ["Ge","C"], 
           ["In4", "Sn3", "O12","C"], ["Cu","C"], ["Zn", "O","C"], ["Li", "Nb", "O3","C"], ["K","Ti","O","P","O4","C"]] 
Ns = 400
# =============================================================================
# material = [["Pb"],["Al", "O2"], ["Au"], ["Cd", "S"], ["Cd"], 
#             ["In4", "Sn3", "O12"], ["S"], ["C", "H4"], ["Li", "Nb", "O3"], ["K","Ti","O","P","O4"],
# ["Pb","C"],["Al", "O2","C"], ["Au","C"], ["Cd", "S","C"], ["Cd","C"], 
# ["In4", "Sn3", "O12","C"], ["S","C"], ["C", "H4","C"], ["Li", "Nb", "O3","C"], ["K","Ti","O","P","O4","C"]]  # , ["Ge", " "],["Pb"," "]]
# =============================================================================
par1 = array(range(40, 41)) 
arr = empty([shape(material)[0], size(par1),2048,2])
lists = []
#print(par1[40])
for matnum, mat in tqdm(enumerate(material)):
    path= "/home/nuno/Desktop/fun/outputscat3/{}".format(''.join(mat))
    lists.append("{}".format(''.join(mat)))
    for idx, par in enumerate(par1): 
        path2 = "{}/{}_{}reg1.spc".format(path,''.join(mat),par)
        r = loadtxt(path2)
        arr[matnum,idx] = r
        
save("/home/nuno/Desktop/fun/outputscat2/Mastertestscat2notref", arr)
lists.append("Thickness Range = {}-{}nm".format(min(par1),max(par1)))
lists.append("Array dimensions = {}".format((shape(arr))))
savetxt("/home/nuno/Desktop/fun/outputscat2/Master_listtestscat2notref", lists,fmt='%s')
time.sleep(1)
arr = load("/home/nuno/Desktop/fun/outputscat2/Mastertestscat2notref.npy")
plt.plot(arr[0,0,:,1])
# =============================================================================
# plt.figure(figsize = (15,8))
# plt.xlabel("Energy (eV)")
# plt.ylabel("Counts")
# for i in range(size(par1)):
#     plt.plot(arr[1,i,:,0], arr[1,i,:,1])
# names = ["Thickness = "+str(i)+" nm" for i in par1]
# plt.legend(names)
# =============================================================================

