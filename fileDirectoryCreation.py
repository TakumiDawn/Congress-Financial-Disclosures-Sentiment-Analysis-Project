import os
import platform

osName = platform.system()
global fileDirectory
print(osName)

if(osName == "Windows"):
    fileDirectory = 'S:/Stocks'
    print('This is a Windows Machine.')
else:
    print('OS not Supported!')

def checkFolderIntegrity():
    # Checks to make sure the folders used for saving CSV's are already there.
    global fileDirectory
    fileDirectory = 'S:/Stocks'
    try:
        os.mkdir(fileDirectory+'/')
    except:
        pass

    try:
        os.mkdir(fileDirectory + '/StockHistory/')
    except:
        pass

    try:
        os.mkdir(fileDirectory + '/Congress/')
    except:
        pass
