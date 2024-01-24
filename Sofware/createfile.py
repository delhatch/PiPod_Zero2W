import vlc
import random
import alsaaudio
import os
import csv
import taglib


fileList = []
print("Updating metadata")
musicPath = "/home/drh/Music/"

for path, dirs, files in os.walk(musicPath):
    for file in files:
        if file.endswith('.mp3') or file.endswith('.m4a') or file.endswith('.wav') or file.endswith('.wma'):
            fileList.append(os.path.join(path, file))
            print(os.path.join(path, file))
        '''
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('.mp3'):
                    fileList.append(filename)
        '''
file = open("info.csv", "w", newline="")
writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# print("Saving metadate")
for i in fileList:
    try:
        audiofile = taglib.File(i)
        tag = audiofile.tags
    except:
        print("Error parsing tags")
        pass

    try:
        # Now check to see if the "ALBUM" field is empty. If so, fill it in with "Not Sure"
        #print(tag["ALBUM"])
        if( tag["ALBUM"] == [] ):
            #print(tag["ALBUM"])
            #print("Found an empty album")
            tag["ALBUM"] = ['Not Sure']
            #print(tag["ALBUM"])
        writer.writerow((i, tag["ARTIST"][0], tag["ALBUM"][0], tag["TITLE"][0]))
    except AttributeError:
        print("Attribute Error", i)
    except:
        print("Unknown error", i)
        #print(i)
print("Done")
file.close()
