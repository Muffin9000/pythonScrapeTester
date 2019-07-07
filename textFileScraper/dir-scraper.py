import os
import fnmatch

scrapeDir = 'D:/Users/neutr/Documents/Code/'
outputPath = 'D:/output/'
outputFileName = 'output.txt'
patterns = ['*.ejs','*.css']


result = []

try:
    for dirname, dirnames, filenames in os.walk(scrapeDir):
        # print path to all subdirectories first.
        for filename in filenames:
            for p in patterns: 
                if fnmatch.fnmatch(filename, p):
                    result.append(os.path.join(dirname, filename))
except OSError:
    print('Failed to map directory' + scrapeDir)
print('Scraping done, writing to file...' + outputPath+outputFileName)

if not os.path.exists(outputPath):
    os.makedirs(outputPath)


f = open(outputPath+outputFileName, 'w+')

for line in result:
    f.write(line+"\n")

f.close()


# result = [os.path.join(dp, f) for dp, dn, filenames in os.walk('D:/Users/neutr/Documents/Code/') for f in filenames if os.path.splitext(f)[1] == '.txt']