import subprocess
import os
import time, signal
import tempfile

import tqdm #Install this! Will change your life GUARANTEED: conda install -c conda-forge tqdm

par1 = range(5,16)
material = [["Si","O2/ "], ["C"," "], ["Ge", ""]]
params = [str(a) for a in par1]

td = tempfile.TemporaryDirectory()
print("tempdir is: %s" % td.name)

fb_ps = subprocess.Popen(["/bin/Xvfb", ":2"])
ps = subprocess.Popen("/home/gelb/xps/Sessa-2.2.0-Linux/bin/sessa -c", shell=True,
                      env = {"HOME":td.name, "DISPLAY":":2"},
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE)
time.sleep(0.1) #I found that buffer times between each call for the subprocess ensures nothing sketchy happens.

st = time.time()
#Loop over material
for mat in tqdm.tqdm(material, desc = "Material"):
#loop over params
    for par in tqdm.tqdm(params, desc = "Parameters: /{}/{}".format(mat[0],mat[1])):
        
        spec = ["PROJECT RESET",
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
        
        spec.insert(4, "Sample ADD LAYER /{}/{}THICKNESS {}".format(mat[0],mat[1],par))
        
        path = "/home/gelb/xps/test/{}{}_Thickness_{}".format(mat[0],mat[1][0:2],par)
        os.mkdir(path)
                
        def do(line):
            ps.stdin.write( str.encode(line+"\n") )
            ps.stdin.flush()
            print(bytes.decode(ps.stdout.readline()).strip())
            while True:
                a = bytes.decode(ps.stdout.readline()).strip()
                if a == '[\] Done':
                    break
                else:
                    #print(a)
                    pass
            time.sleep(0.1)
            
        for line in spec:
            do(line)
            
        tstart = time.time()
        do("MODEL SIMULATE")
        tend = time.time()
                
        out = "PROJECT SAVE OUTPUT \"{}/test{}{}_Thickness_{}\"".format(path, mat[0],mat[1][0:2],par)
        do(out)
    
end = time.time()
print("Time is {} seconds".format(str(end-st)))

print("quitting everything")
ps.stdin.write(str.encode( "QUIT\n" ))

os.kill(fb_ps.pid, signal.SIGTERM)

print("cleaning up the tempdir")
td.cleanup()
