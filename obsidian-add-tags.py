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

import os, glob, re
import frontmatter

globalSrcPathName = 'E:/jeff/keep/temp'
globalDestPathName = 'E:/jeff/keep/temp/tagged'

#print re.search(r"---\s*\n(.*)\n---", aaa, re.DOTALL).group(0)

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
        for srcFilePath in glob.glob(os.path.join(self.srcPathName, self.filePattern)): #[:10]:
            fileName = os.path.split(srcFilePath)[1]        
            print('* ' + srcFilePath)
            print('** ' + fileName)
            with open(srcFilePath) as inFile:
                parser = frontmatter.load(inFile)
                print('***m')
                print(parser.metadata)
                #print(parser.bodyTags)
                print('***c')
                #print(parser.content[:50])
                print(frontmatter.dumps(parser)[:100])
                destFilePath = os.path.join(self.destPathName, fileName)
                with open(destFilePath, 'wb') as outFile:
                    frontmatter.dump(parser, outFile)
                    print('**** ' + destFilePath)
                    
        
if __name__ == '__main__':
    tagAdder = ObsidianTagAdder(globalSrcPathName, globalDestPathName)
    tagAdder.addTags();
        

