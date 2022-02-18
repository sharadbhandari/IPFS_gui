#!/bin/python

####################################
#### Created by Sharad Bhandari ####
############### 2022 ###############
####################################

import cmd
import gui

def main():
    print("App started... ")
    if cmd.cmd('ipfs version').returncode == 0:
        gui.gui()
    else:
        print("Ipfs not found.\n please install ipfs before running this app.")
 
    print("\n... app closed")

if __name__=="__main__":
    main()
