#!/usr/bin/env python
'''
Code used to get text files from Perseus XML files for APA 2014 study:
"Distant Reading Alliteration in Latin Literature"
Patrick J. Burns, Fordham University
'''

import os
import re
import libxml2

convertRoot = '../data/convert'

def getPerseusContent(text):
    '''
    For this study, I wanted to use plain text version of Latin literature. This
    script takes Perseus XML files, parses the XML, removes unwanted sections
    by either regex substitutions or libxml2 node unlinks. The file also
    looks for natural breaks in the text (e.g. books, section, poem, etc.) and
    inserts a series of plus signs (i.e., '+') to put distance between unrelated
    text elements. Related, asterisks (i.e., '*'), which are already included in
    the Perseus files to indicate lacunae are converted to match the plus signs.
    
    Input: string; expects a Perseus XML file
    Output: string with all of the XML parsed and non Latin material stripped
    '''
    
    #####
    #####
    ##
    ## Conversion scripts
    ##
    #####
    #####
    
    # Remove empty lines
    # modified based on Regisz 7/12 answer:
    # http://stackoverflow.com/questions/3711856/remove-empty-lines
    text = " ".join([(ll.rstrip()).strip() for ll in text.splitlines() if ll.strip()])
        
    # Remove index (could not figure out a way to use unlink node to do this)
    if text.find('<div1 type="book" n="index">') != -1:
        indexStart = text.find('<div1 type="book" n="index">')
        indexEnd = text.find('</div1>',indexStart)
        text = text[:indexStart] + text[indexEnd+7:]    
    
    # Separate major divisions (using a reasonable gap width)
    # e.g. <div1 type="satire".+?>
    text = re.sub(r'(<div1.+?>)',r'\n++++++++++\n\1',text)
    text = re.sub(r'(<div2 type="Poem".+?>)',r'\n++++++++++\n\1',text)
    text = re.sub(r'(<milestone unit="book".+?>)',r'\n++++++++++\n\1',text)
    text = re.sub(r'(<milestone unit="chapter".+?>)',r'\n++++++++++\n\1',text)
    # <lb.+?>
    text = re.sub(r'(<lb?.*?>)',r'\n\1',text)
    # e.g. <p>
    text = re.sub(r'(<p>)',r'\1\n',text)
    
    # Control for lacuna
    text = re.sub(r'\*+?\s+?',r'***',text)    
    
    # Parse XML document
    doc = libxml2.parseDoc(text)
    
    # Delete non-content text included in the body of file using unlinkNode()
    unlinks = ['teiHeader','front','back','head','argument','bibl','castList','note','speaker']
    
    for unlink in unlinks:
        if unlink in text:
            nodes = doc.xpathEval('//'+unlink)                
            for node in nodes:
                node.unlinkNode()

    content = doc.content # get content from XML file
    doc.freeDoc()
    
    # Remove blank lines & strip initial spaces
    content = [(ll.rstrip()).strip() for ll in content.splitlines() if ll.strip()]
    
    return content
 
def makePerseusTextFile(root,filename):
    '''
    Reads the file given with filename (expects a Perseus XML file) and
    saves the files as a .txt file. 
    
    Input: string with root, string with filename
    Output: nothing
    '''
        
    # Get filename base so it can be saved with next extension later in script
    basename = os.path.splitext(filename)[0]

    # Read file            
    with open(os.path.join(root, filename), 'r') as f:
        text = f.read()
                    
    # Remove/parse unwanted parts of XML file
    content = getPerseusContent(text)
    
    # Output text file
    outFile = root + '/../txt/' + basename + '.txt'
    
    ## Delete file if it already exists.
    try:
        os.remove(outFile)
    except OSError:
        pass
    
    ## Output processed file as text file (.txt).
    for line in content:
        with open(outFile,'a') as f: f.write(line.strip()+'\n')   

def convertDirectory(directory):
    '''
    Iterates through directory converting all .xml files
    with makePerseusTextFile
    
    Input: string with directory name
    Output: None
    '''
    
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith('.xml'):
                makePerseusTextFile(root,f)
                os.rename(root+'/'+f,root+'/../converted/'+f)        
    
if __name__ == '__main__':
    convertDirectory(convertRoot)