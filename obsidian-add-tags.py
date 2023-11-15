#!/usr/bin/env python3
'''\
Add obsidian tags to all markdown files in folder.

in development
ToDo:
 - frotmatter dumps no header as --- {} ---
 - needs error handler for unicode issues
 - also get tags from body (not sure how to get/set body as text from frontmatter)
 - actually add/replace tags
'''

import os, glob, re, shutil
import frontmatter

SrcPathName = 'E:/jeff/keep/temp'
DestPathName = 'E:/jeff/keep/temp/tagged'

class ObsidianTagAdder:
    
    def __init__(self, srcPathName, destPathName, filePattern='*.md'):
        self.srcPathName = srcPathName
        self.destPathName = destPathName
        self.filePattern = filePattern
        # print('from: ' + srcPathName);
        # print('to: ' + destPathName);
        if not os.path.exists(self.destPathName): 
            os.makedirs(self.destPathName)

    def addTags(self, tagNames=[]):
        if len(tagNames) == 0:
            print('!!! no tags to add')
            return            
        print('adding tags...')
        print('from ' + self.srcPathName)
        print('to ' + self.srcPathName)
        for srcFilePath in glob.glob(os.path.join(self.srcPathName, self.filePattern)): #[:10]:
            fileName = os.path.split(srcFilePath)[1]        
            destFilePath = os.path.join(self.destPathName, fileName)
            with open(srcFilePath, encoding="utf-8-sig") as inFile:
                try: 
                   parser = frontmatter.load(inFile)
                except:
                    print('!!! parsing error: ' + fileName)
                    shutil.copyfile(srcFilePath, destFilePath)
                    continue                    
                with open(destFilePath, 'wb') as outFile:
                    frontmatter.dump(parser, outFile)
        print('...done')
                    
        
if __name__ == '__main__':
    tagAdder = ObsidianTagAdder(SrcPathName, DestPathName)
    tagAdder.addTags();
        

