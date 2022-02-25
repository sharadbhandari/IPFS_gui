#!/bin/python

###########################################
### A simple GUI implementation of IPFS ###
####### Created by: Sharad Bhandari #######
################## 2022 ###################
###########################################

from app_functions import cmd
import app_gui

def main():
    print("App started... ")
    if cmd('ipfs version').returncode == 0:
        app_gui.main()
    else:
        print("Ipfs not found.\n please install ipfs before running this app.")
 
    print("\n... app closed")

if __name__=="__main__":
    main()
