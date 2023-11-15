#!/usr/bin/env python3
'''\
Add obsidian tags to all markdown files in folder.

ToDo:
 - compare tags from body before adding
 - add command-line parameters
 - refactor ObsidianTagAdder.addTags() to something prettier
 - unit tests
'''

import os, glob, re, shutil
import frontmatter

SrcPathName = 'E:/jeff/keep/temp'
DestPathName = 'E:/jeff/keep/temp/tagged'
TagsToAdd = ['fromKeep/2023-11-11', 'fromKeep/asImported']

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
        print('to ' + self.destPathName)
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
                docTags = parser.metadata.get('tags', [])
                for newTag in tagNames:
                    if not newTag in docTags:
                        docTags.append(newTag)
                parser.metadata['tags'] = docTags
                with open(destFilePath, 'wb') as outFile:
                    frontmatter.dump(parser, outFile)
        print('...done')
                    
        
if __name__ == '__main__':
    tagAdder = ObsidianTagAdder(SrcPathName, DestPathName)
    tagAdder.addTags(TagsToAdd);
        

