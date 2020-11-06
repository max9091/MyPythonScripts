# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:46:22 2019

@author: Markus Winklberger
"""

import os
from shutil import copy2
import sys

# Script to change line styles in TpX figures automatically
# Usage to change line styles in all TpX figures of current dir: python ChangeTpXLineStyleAutomatically.py 
# Usage to change line styles in specific TpX figure: python ChangeTpXLineStyleAutomatically.py filename.TpX

# All lines with color
colorSignal = '{rgb}{0.098,0.098,0.439}' #--> midnightblue
# and style
dashPattern = 'dash pattern=on 2.00mm off 1.00mm' #--> dashed (DashSize = 1)
# are replaced by 
newColor = '{rgb}{0,0,0}' #--> black
#'dash pattern=on (24*d)mm off (3*d)mm on (0.5*d)mm off (3*d)mm' #-->Mittellinie laut DIN EN ISO 128-20, Tabellenbuch Metall, Seiten 68 und 69
# e.g.: newDashPattern = getDashPattern(0.25)

# where d is the line width parameter of the current line
def getDashPattern(d):
    return 'dash pattern=on %.2fmm off %.2fmm on %.2fmm off %.2fmm'%(24.0*d,3.0*d,1.0*d,3.0*d)

def getLineWidth(line):
    lineWidthStr = 'line width='
    startIndx = line.find(lineWidthStr) + len(lineWidthStr)
    endIndx = line.find('mm',startIndx)
    return float(line[startIndx:endIndx])
   
#Get all files with ending *.TpX in current folder
def getTpXFiles():
    return [name for name in os.listdir(os.getcwd())
        if os.path.isfile(os.path.join(os.getcwd(), name)) and name.endswith('.TpX')]

#main code
TpXFiles = getTpXFiles()

if len(sys.argv)>1:
	TpXFiles = list(sys.argv[1:])
	
print(TpXFiles)

for TpXFile in TpXFiles:
    #Copy file and add .tikz ending
    newTpXFile = TpXFile+'.tikz'
    copy2(TpXFile, newTpXFile)

    #Open each file and
    with open(os.path.join(os.getcwd(), newTpXFile),'r') as f:
        dataLines = f.read().splitlines()
    
    # ... search if color and style are included in two consecutive lines
    changeFlag = False
    i = 0
    while i < len(dataLines)-1:
        if dataLines[i].count(colorSignal): #check if colorLine is found in line
            colorLineIndex = i
            i = i+1 #check next line(s)
            while not dataLines[i].count(r'\definecolor{L}{rgb}') and not dataLines[i].count(r'\end{tikzpicture}'): #until a new color is defined or file end is reached!
                if dataLines[i].count(dashPattern): #If dash pattern included 1) get line width 2) replace line dash pattern   
                    lineWidth = getLineWidth(dataLines[i])
                    newDashPattern = getDashPattern(lineWidth)
                    dataLines[i] = dataLines[i].replace(dashPattern,newDashPattern)
                    print('LinePattern changed in file <%s> in line <%d>'%(newTpXFile,i))
                    changeFlag = True
                i = i+1
            if changeFlag:
                dataLines[colorLineIndex] = dataLines[colorLineIndex].replace(colorSignal,newColor)
        else:
            i = i+1
    
    if changeFlag:
        with open(os.path.join(os.getcwd(), newTpXFile),'w') as f:
            for line in dataLines:
                f.write('%s\n'%(line))
                
            

