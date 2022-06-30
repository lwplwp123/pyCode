#give me a folder.
#find out all files and folders.
import os
import glob

def findAllSubs(folderP)->list: 
    # return  os.listdir(folderP)
    return glob.glob(folderP+'/*.xcodeproj')

f0 = input('please input a path, I will find out all the files and folders').strip()
if os.path.exists(f0) and  os.path.isdir(f0):
    allSubs = findAllSubs(f0)
    print(allSubs)
else: 
    print ('not a folder or no found the path.')

 

