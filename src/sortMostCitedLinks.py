import pickle
import operator

__author__ = 'dvirdi'

name = "danariely"
website = "danariely.com"

file = pickle.load( open( "/Users/dvirdi/Desktop/Links/"+name+".p", "rb"))


def RemovePrefix(line):
    temp = ["http://www.", "https://www.", "http://", "www.", "https://"]
    if (temp[0] in line):
        line = line.split(temp[0])[1]
    elif (temp[1] in line):
        line = line.split(temp[1])[1]
    elif (temp[2] in line):
        line = line.split(temp[2])[1]
    elif (temp[3] in line):
        line = line.split(temp[3])[1]
    elif (temp[4] in line):
        line = line.split(temp[4])[1]
    return line

listOfLinks = {}


def removeSuffix(line):
    if("/" in line):
        return line.split("/")[0]
    else:
        return line


for line in file:
    if(website not in line):
        line = RemovePrefix(line)
        line = removeSuffix(line)
        if(listOfLinks.has_key(line)):
            listOfLinks[line] = listOfLinks[line]+1;
        else:
            listOfLinks[line] = 1;

sorted_x = sorted(listOfLinks.items(), key=operator.itemgetter(1), reverse=True)
for key, value in sorted_x:
    print key, value



#TODO: get alexa rank using: http://www.alexa.com/siteinfo/hsph.harvard.edu