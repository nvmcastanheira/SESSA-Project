import subprocess
import os
import time, signal
import tempfile
import threading
import numpy as np

par1 = np.array(range(40, 41)) #Choose thicknesses. In this case, 40-40 angstroms. 

#Choose materials to iterate over.
material = [["Si"],["Si", "O2"], ["Al"], ["Ga", "As"], ["Ge"], 
            ["In4", "Sn3", "O12"], ["Cu"], ["Zn", "O"], ["Li", "Nb", "O3"], ["K","Ti","O","P","O4"]]  # , ["Ge", " "],["Pb"," "]] 


params = [str(a) for a in par1] #Makes all thicknesses strings.
threads = np.size(material, 0) #How many threads to use. One per material makes the most practical sense.

#We define the spectra-generating function. 
#NOTE that I made it have different functionality for materials with a carbon layer. Modifying this is hell as a result.
def pr1(material, params, mode = 0): #Input "material" string and "params" thicknesses above. Mode 0 is non-carbon mode by default.
    fb_ps1 = subprocess.Popen(["/bin/Xvfb", ":2"]) #Xvfb layer. Necessary.

    td1 = tempfile.TemporaryDirectory() #Make a temp directory to trick this dumb application to open multiple windows.
    ps1 = subprocess.Popen(
        "/home/nuno/Desktop/fun/bin/sessa -c",
        shell=True,
        env={"HOME": td1.name, "DISPLAY": ":2"},
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ) #Open SESSA.
    
    Sleep = 10 #Define a fixed sleep time for spectra generation. HIGHLY specs dependent. 10 works for the UTD PC.
    time.sleep(0.1) #Buffer for threads in time to run them in parallel.    
    print("tempdir is: %s" % td1.name)
    mat = material
    
    if mode == 0: #Non-carbon layer mode.
        for i, par in enumerate(params):
            spec1 = [
                "PROJECT RESET",
                "PREFERENCES SET NDIIMFP 1",  # 1 is the fast default, 2 is diff for top two layers.
                "PREFERENCES SET THRESHOLD 1.0e-10",  # doesn't seem to do much?
                "SAMPLE SET MATERIAL Si LAYER 0",  # substrate.
                "MODEL SET NCOL 1 REGION 1",
                "PREFERENCES SET OUTPUT SAMPLE true",
                "PREFERENCES SET OUTPUT EXPERIMENT true",
                "PREFERENCES SET OUTPUT PARAMETERS true",
                "PREFERENCES SHOW",
                "SPECTROMETER SET RANGE 500:1500 REGION 1",
                "SPECTROMETER LIST",
                "MODEL SET CONVERGENCE 1.000e-04",  # 0.01 is default.  This is in percentage units?
                "MODEL AUTO NCOL",
                "MODEL SHOW",
            ] #SESSA commands. 
    
            spec1.insert(4, "Sample ADD LAYER /{}/ THICKNESS {}".format("/".join(mat), par)) #Add command in the fifth spot to add chosen material layer.
            path1 = "/home/nuno/Desktop/fun/output/{}".format("".join(mat)) #Output path.
            if i == 0:
                os.mkdir(path1) #On first iteration, make a folder to store data (by thickness). You can comment this out.
    
            def do(line): #Performs command.
                ps1.stdin.write(str.encode(line + "\n"))
                ps1.stdin.flush()
                time.sleep(0.1) 
    
            for line in spec1:
                do(line)
    
            do("MODEL SIMULATE") #SIMULATE!!!
            time.sleep(10) #Wait for it to simulate...
    
            out = 'MODEL SAVE SPECTRA "{}/{}_{}"'.format(path1, "".join(mat), par)
            do(out) #Save spectra
            time.sleep(Sleep)  # Have to add this, or else some threads don't catch up
            if i == int(len(par1)): #On last iteration, quit thread.
                print("quitting everything")
                ps1.stdin.write(str.encode("QUIT\n"))
                td1.cleanup()
                os.kill(fb_ps1.pid, signal.SIGTERM)
    else: #Carbon-layer mode. Mostly the same. NOTE: There is obviously a neater way to do this part. I was just too lazy...
        for i, par in enumerate(params):
            spec1 = [
                "PROJECT RESET",
                "PREFERENCES SET NDIIMFP 1",  
                "PREFERENCES SET THRESHOLD 1.0e-10",  
                "SAMPLE SET MATERIAL Si LAYER 0",  
                "SAMPLE ADD LAYER /C/ THICKNESS 0.5", #BIGGEST DIFFERENCE. Here is the carbon layer.
                "PREFERENCES SET OUTPUT SAMPLE true",
                "PREFERENCES SET OUTPUT EXPERIMENT true",
                "PREFERENCES SET OUTPUT PARAMETERS true",
                "PREFERENCES SHOW",
                "SPECTROMETER SET RANGE 500:1500 REGION 1",
                "SPECTROMETER LIST",
                "MODEL SET CONVERGENCE 1.000e-04",  
                "MODEL AUTO NCOL",
                "MODEL SHOW",
            ]
    
            spec1.insert(4, "Sample ADD LAYER /{}/ THICKNESS {}".format("/".join(mat), par))
            path1 = "/home/nuno/Desktop/fun/output5/{}C".format("".join(mat))
            if i == 0:
                os.mkdir(path1)
    
            def do(line):
                ps1.stdin.write(str.encode(line + "\n"))
                ps1.stdin.flush()
                time.sleep(0.1)
    
            for line in spec1:
                do(line)
    
            do("MODEL SIMULATE")
            time.sleep(Sleep)
    
            out = 'MODEL SAVE SPECTRA "{}/{}C_{}"'.format(path1, "".join(mat), par)
            do(out)
            
            time.sleep(Sleep)  
            if i == int(len(par1)):
                print("quitting everything")
                ps1.stdin.write(str.encode("QUIT\n"))
                td1.cleanup()
                os.kill(fb_ps1.pid, signal.SIGTERM)

for n in range(threads): #Perform each thread in parallel.
    t1 = threading.Thread(target=pr1, args=[material[n], params]) #Non-carbon thread.
    t1.start() 
    time.sleep(1) #Buffer time for threads.
    t2 = threading.Thread(target=pr1, args=[material[n], params, 1]) #Carbon thread.
    t2.start()
    time.sleep(1.03) #Silly goofy number buffer.