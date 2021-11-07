# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 22:51:54 2020

@author: Anshika Bajpai, Srishti Ginjala

Kindly provide correct path name for imgdivskel.html in line 63
"""

#--------- importing modules ----------------------------
import sys
import getopt
import glob
import bs4    
from pyexiv2 import Image

#--------- Customisable variables ----------------------------
BASE_DIR = "~tag/tmp/Pics"      # Base directory
GALSKEL_DEFAULT = "galskel.html"

#--------- Global variables ----------------------------
galskel = GALSKEL_DEFAULT       # Name of gallery skeleton file
galoutFname = ""                # Name of output gallery
srcdir  = "."                   # Path within BASE_DIR
jpgList =[]                     # Full list of .jpg files
<<< add others >>>

#----------------------------------------------------------
# PrintHelp -- display usage message and exit
#----------------------------------------------------------
def PrintHelp():
    print("Purpose: This script creates a responsive gallery from all the images in a folder.  The description is populated from the filename plus title and/or caption of the image.")
    print("Usage:")
    print("makerespgal [-s <srcDir>] [-i <galskel.html>] [-ftc] <gallery.html>")
    <<< a set of print() stmts, one per line of o/p, is easier to read and edit >>>
    Description\n-----------\n<srcDir> has two subdirectories, thumnails and large.  Each contains all the images in the gallery, in respective sizes.  makerespgal reads the skeleton of the gallery html.  For each image in <srcDir>, it inserts a <div class=\"responsive\">.  The description is taken from the filename/title/caption.  The complete html page is written to <gallery.html>.")
    sys.exit(1)                 # Terminate script

#----------------------------------------------------------
# GetArgs -- <<<insert brief description here>>>
#----------------------------------------------------------
def GetArgs():
    argv = sys.argv[1:] 
    opts , args = getopt.getopt(argv, ":s:i:f:t:ch") 
        for opt, arg in opts:     
            if opt in ['-s']: 
                srcdir=arg

            if opt in ['-i']: 
                galskel = arg 

            if opt in ['-f']: 
                filename = arg 

            if opt in ['-t']: 
                title = arg 

            if opt in ['-c']: 
                caption = arg 

            if ('-h','') in opts: 
                PrintHelp()

    galoutFname = sys.argv[-1]

#---------End of GetArgs() ------------------------------

#----------------------------------------------------------
# ListImages -- <<<insert brief description here>>>
#----------------------------------------------------------
    def ListImages():                        
        for filename in glob.glob(srcdir+"/large/*"):#lists all jpeg files in srcdir/large
            jpgList.append(filename)  

#---------End of ListImages() ------------------------------

#----------------------------------------------------------
# WriteOutput -- <<<insert brief description here>>>
#----------------------------------------------------------
    def WriteOutput():  
        skel=open(galskel,'r')
        galout = open(galoutFname, 'w')

        tempo=[]                # used to collect the img div
        flag=1

        for line in skel:
            #flag==1 implies lines before Image div start
            if line != "<!--  Image div start -->\n" and flag==1:
                galout.write("%s"%line)
                #flag==2 implies lines between Image div start and Image div end
            elif (line == "<!--  Image div start -->\n" and flag==1) or (line !="<!--  Image div end -->\n" and flag==2):
                tempo.append(line)
                flag=2
            elif line =="<!--  Image div end -->\n":
                myfile=open(galskel, 'w+')
<<< Should read galskel and write galout.  Why read and mod? >>>
                #reads and modifies imgdivskel as per the given file
                myfile.writelines(tempo[1:])

                for img in jpgList:
                    myfile.seek(0,0)
                    imgDiv=myfile.read()
                    soup=bs4.BeautifulSoup(imgDiv,features="html.parser")
                    #changing the href attribute
                    soup.a['href']=img #img in jpgList is the path of srcDir/large
                    print(img)
                    #change large to thumbnails for href
                    src=str(img).replace("large","thumbnails")
                    #changing the src attribute
                    soup.img['src']=src 
                    
                    imag = Image(img)
                    iptc = imag.read_iptc()
                    title = iptc['Iptc.Application2.ObjectName']
                    caption = iptc['Iptc.Application2.Caption']
                    imag.close()
                    
                    d=soup.find("div", class_="desc")
                    #s is the name of the file (sliced after last '/' to the last '.')
                    s=str(img)[str(img).rfind('/')+1:str(img).rfind('.')]
                    d.string=s+" : "+title+" - "+caption
                    
                    galout.write(str(soup)) # copying to gallery.html
                    
                myfile.close()
                flag=0
                #flag==0 implies lines after Image div end

            else:
                galout.write("\n%s"%line)
                skel.close()
                galout.close()

#---------End of WriteOutput() ------------------------------

#----------------------------------------------------------
# Main code
#----------------------------------------------------------
try:        
    GetArgs()
except:
    PrintHelp()

ListImages()
WriteOutput()
