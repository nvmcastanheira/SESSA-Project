import subprocess
import os
import time, signal
import tempfile
import threading 

import tqdm #Install this! Will change your life GUARANTEED: conda install -c conda-forge tqdm

par1 = range(5,15)
material = [["Si","O2/ "], ["C"," "]]
params = [str(a) for a in par1]

fb_ps = subprocess.Popen(["/bin/Xvfb", ":2"])
def pr1():
    td1 = tempfile.TemporaryDirectory()
    ps1 = subprocess.Popen("/home/nuno/Desktop/fun/Sessa-2.2.0-Linux/bin/sessa -c", shell=True,
                          env = {"HOME":td1.name, "DISPLAY":":2"},
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    time.sleep(1)
    print("tempdir is: %s" % td1.name)
    mat = material[0]
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
    
        path1 = "/home/nuno/Desktop/fun/output/{}{}_Thickness_{}".format(mat[0],mat[1][0:2],par)
        os.mkdir(path1)
                
        def do(line):
            ps1.stdin.write( str.encode(line+"\n") )
            ps1.stdin.flush()
            time.sleep(0.1)
            
        for line in spec1:
            do(line)
            
        do("MODEL SIMULATE")
        time.sleep(10)

        out = "PROJECT SAVE OUTPUT \"{}/test\"".format(path1)
        do(out)
        if i == int(len(par1)):
            print("quitting everything")
            ps1.stdin.write(str.encode( "QUIT\n" ))
            td1.cleanup()
            

def pr2():
    td2 = tempfile.TemporaryDirectory()
    ps2 = subprocess.Popen("/home/nuno/Desktop/fun/Sessa-2.2.0-Linux/bin/sessa -c", shell=True,
                          env = {"HOME":td2.name, "DISPLAY":":2"},
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print("tempdir is: %s" % td2.name)
    time.sleep(3)
    mat = material[1]
    for i, par in enumerate(params):
        spec2 = ["PROJECT RESET",
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
        
        spec2.insert(4, "Sample ADD LAYER /{}/{}THICKNESS {}".format(mat[0],mat[1],par))
    
        path2 = "/home/nuno/Desktop/fun/output/{}{}_Thickness_{}".format(mat[0],mat[1][0:2],par)
        os.mkdir(path2)
                
        def do(line):
            ps2.stdin.write( str.encode(line+"\n") )
            ps2.stdin.flush()
            time.sleep(0.1)
            
        for line in spec2:
            do(line)
            
        do("MODEL SIMULATE")
        time.sleep(10)
                
        out = "PROJECT SAVE OUTPUT \"{}/test\"".format(path2)
        do(out)
        
        if i == int(len(par1)):
            print("quitting everything")
            ps2.stdin.write(str.encode( "QUIT\n" ))
            td2.cleanup()


time.sleep(0.1) #I found that buffer times between each call for the subprocess ensures nothing sketchy happens.

st = time.time()
#Loop over material
    
t1=threading.Thread(target=pr1)
t1.start()
t2=threading.Thread(target=pr2)
t2.start()
end = time.time()
print("Time is {} seconds".format(str(end-st)))

os.kill(fb_ps.pid, signal.SIGTERM)

