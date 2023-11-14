#!/usr/bin/env python3
'''\
Add obsidian tags to all markdown files in folder.

in development
ToDo:
 - looks like it chokes on unicode
 - switch to python-fromtmater (instead of parsing directly with yaml)
 - also get tags from body
 - actually add/replace tags
'''

import os, glob, re
import yaml

globalSrcPathName = 'E:/jeff/keep/temp'
globalDestPathName = 'E:/jeff/keep/temp/tagged'

#print re.search(r"---\s*\n(.*)\n---", aaa, re.DOTALL).group(0)

class ObsidianParser:

    headerRe = re.compile(r"---\s*\n(.*?\n)\s*---\s*\n?", re.DOTALL)
    bodyTagRe = re.compile(r"[^|\s](#\w+)[\s|$]", re.MULTILINE)

    def __init__(self, originalBody=''):
        self.originalBody = originalBody
        self.rawHeader = ''
        self.header = {}
        self.body = ''
        self.bodyTags = []
        self._parse()

    def _parse(self):        
        headerMatch = self.headerRe.search(self.originalBody)
        if not headerMatch:
            self.rawHeader = ''
            self.header = {}
            self.body = self.originalBody
            self.bodyTags = []
        else:
            self.rawHeader = headerMatch.group(1)
            self.header = yaml.safe_load(self.rawHeader)
            self.body = self.headerRe.sub('', self.originalBody, 1)
            self.bodyTags = self.bodyTagRe.findall(self.body)


    def getHeaderTag(self, tagName):
        return self.header.get('tags', {}).get(tagName)

        

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
                data = inFile.read()
                parser = ObsidianParser(data)
                if (len(parser.bodyTags) == 0):
                    continue
                if parser.rawHeader:
                    print('***rh')
                    print(parser.rawHeader)
                    print('***h')
                    print(parser.header)
                    print('***bt')
                    print(parser.bodyTags)
                    print('***b')
                    print(parser.body[:50])
                destFilePath = os.path.join(self.destPathName, fileName)
                with open(destFilePath, 'w') as outFile:
                    outFile.write(data)
                    print('**** ' + destFilePath)
                    
    def getContentHeader(self, content):
        match = self.headerRe.search(content)
        if match and len(match.groups()) >0:
            return match.group(0)
        return ''
        
        
        
if __name__ == '__main__':
    tagAdder = ObsidianTagAdder(globalSrcPathName, globalDestPathName)
    tagAdder.addTags();
        

