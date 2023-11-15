#!/usr/bin/env python3
'''\
Add obsidian tags to all markdown files in folder.
obsidian-add-tags.py

Usage:
  - set these values at the top of the script
    - SrcPathName
      - * the path to the folder with the markdown files you want to tag *
    - DestPathName
      - * the path to the folder where the tagged files should be created) *
    - TagsToAdd
      - * an array of tag names to be added to the files *
  - run the script
    - ```python obsidian-add-tags.py```
  - if the output files look good, you can replace the original files with them
  
  You can also import the ObsidianTagAdder class and use it directly.
    

ToDo:
  - compare tags from body before adding
  - add command-line parameters
  - add a parameter for output control
  - refactor ObsidianTagAdder.addTags() to something prettier
  - unit tests
'''

import glob, re, os, shutil
import frontmatter

SrcPathName = 'E:/jeff/keep/temp/untagged'
DestPathName = 'E:/jeff/keep/temp/tagged'
TagsToAdd = ['fromKeep/2023-11-10', 'fromKeep/asImported']

class ObsidianTagAdder:
    
    def __init__(self, srcPathName, destPathName, filePattern='*.md'):
        self.srcPathName = srcPathName
        self.destPathName = destPathName
        self.filePattern = filePattern
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
            modification_time = os.path.getmtime(srcFilePath)
            fileName = os.path.split(srcFilePath)[1]        
            destFilePath = os.path.join(self.destPathName, fileName)
            with open(srcFilePath, encoding="utf-8-sig") as inFile:
                try: 
                   parser = frontmatter.load(inFile)
                except:
                    shutil.copy2(srcFilePath, destFilePath)
                    print('!!! parsing error: ' + fileName)
                    continue
                docTags = parser.metadata.get('tags', [])
                for newTag in tagNames:
                    if not newTag in docTags:
                        docTags.append(newTag)
                parser.metadata['tags'] = docTags
                with open(destFilePath, 'wb') as outFile:
                    frontmatter.dump(parser, outFile)
                access_time = os.path.getatime(destFilePath)
                os.utime(destFilePath, (access_time, modification_time))
        print('...done')
                    
        
if __name__ == '__main__':
    tagAdder = ObsidianTagAdder(SrcPathName, DestPathName)
    tagAdder.addTags(TagsToAdd);
        

