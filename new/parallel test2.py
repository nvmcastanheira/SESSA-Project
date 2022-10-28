import subprocess
import os
import time, signal
import tempfile
import threading 
import numpy as np

par1 = range(5,8)
#material = [["Si"," "], ["Ga","As/ "], ["In", "As/ "],["Ge"," "],["Cu"," "],["Al"," "],
            #["Si"," ", "C"], ["Ga","As/ ", "C"], ["In", "As/ ","C"],["Ge"," ","C"],["Cu"," ","C"],["Al"," ","C"]]

material = [["Si"," ", ""], ["Ga","As/ ", ""],
            ["Si"," ", "C"], ["Ga","As/ ", "C"]]

params = [str(a) for a in par1]
threads = np.size(material, 0)
def pr1(material, params):
    fb_ps1 = subprocess.Popen(["/bin/Xvfb", ":2"])

    td1 = tempfile.TemporaryDirectory()
    ps1 = subprocess.Popen("/home/nuno/Desktop/fun/Sessa-2.2.0-Linux/bin/sessa -c", shell=True,
                          env = {"HOME":td1.name, "DISPLAY":":2"},
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    time.sleep(0.1)
    print("tempdir is: %s" % td1.name)
    mat = material
    mn = np.size(material)
    for i, par in enumerate(params):
        spec1 = ["PROJECT RESET",
                "PREFERENCES SET NDIIMFP 1",      # 1 is the fast default, 2 is diff for top two layers.
                "PREFERENCES SET THRESHOLD 1.0e-10",    # doesn't seem to do much?
                "SAMPLE SET MATERIAL Si LAYER 0",  #substrate.
                #"SAMPLE ADD LAYER /Si/O2/ THICKNESS 10", #material
                "PREFERENCES SET OUTPUT SAMPLE true",
                "PREFERENCES SET OUTPUT EXPERIMENT true",
                "PREFERENCES SET OUTPUT PARAMETERS true",
                "PREFERENCES SHOW",
                "SPECTROMETER SET RANGE 500:1500 REGION 1",
                "SPECTROMETER LIST",
                "MODEL SET CONVERGENCE 1.000e-04",   #0.01 is default.  This is in percentage units? 
                "MODEL AUTO NCOL",
                "MODEL SHOW"]  
        
        spec1.insert(4, "Sample ADD LAYER /{}/{}THICKNESS {}".format(mat[0],mat[1],par))
        spec1.insert(4, "Sample ADD LAYER /{}/ THICKNESS {}".format(mat[2],0.5))
        path1 = "/home/nuno/Desktop/fun/output"
                
        def do(line):
            ps1.stdin.write( str.encode(line+"\n") )
            ps1.stdin.flush()
            time.sleep(0.1)
            
        for line in spec1:
            do(line)
            
        do("MODEL SIMULATE")
        time.sleep(8)

        out = "MODEL SAVE SPECTRA \"{}/test{}{}{}_Thickness_{}\"".format(path1, mat[0],mat[1][0:2],"CARB",par)
        do(out)
        time.sleep(11) #Have to add this, or else some threads don't catch up
        if i == int(len(par1)):
            print("quitting everything")
            ps1.stdin.write(str.encode( "QUIT\n" ))
            td1.cleanup()
            os.kill(fb_ps1.pid, signal.SIGTERM)
        
            

for n in range(threads):
    t1=threading.Thread(target=pr1, args = [material[n], params])
    t1.start()
    time.sleep(1.3)



