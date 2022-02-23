# Some system might have to run this command with sudo.
# sysctl -w net.core.rmem_max=2500000
# Please visit the following website to read more about the issue.
# https://github.com/lucas-clemente/quic-go/wiki/UDP-Receive-Buffer-Size

import tkinter as tk
from tkinter import filedialog
import subprocess

def cmd(arg):
    shell_output = subprocess.run(arg, stdout=subprocess.PIPE, shell=True)
    return shell_output

def do_nothing():
    pass

def start_ipfs(parent):
    cmd('ipfs init &')
    if cmd('pidof ipfs').returncode != 0:
        cmd('ipfs daemon > ipfs_start.log &')

    parent.ipfs_status.config(text="IPFS daemon status: Running\nPID: " \
                                   + str(cmd('pidof ipfs').stdout.decode())[0:-1],
                              fg="#1e961c",
                              )
    parent.ipfs_status.config()
    
    parent.button_start.config(state="disable")
    parent.button_stop.config(state="active")
        
def stop_ipfs(parent):
    pid_ipfs = cmd('pidof ipfs').stdout.decode()
    cmd('kill `pidof ipfs`')
    
    parent.ipfs_status.config(text="IPFS daemon status: Stopped\n PID: " \
                                   + pid_ipfs[0:-1], 
                              fg="#FF0000",
                              )
    
    parent.button_start.config(state="active")
    parent.button_stop.config(state="disable")

def main_label(parent, count, line):
    parent.main_label = tk.Label(parent.frame_right,
                                 text=line[:-1],
                                 relief="solid",
                                 pady=5,
                                 )
    parent.main_label.grid(row=count, column=0, sticky="w")

def reconstruct_frame_right(parent):
    parent.frame_right.destroy()
    parent.frame_right = tk.LabelFrame(parent.main_frame, 
                                       text="Interface", 
                                       padx=10, 
                                       pady=10, 
                                       relief="solid",
                                       width=parent.width*0.70, 
                                       height=parent.height*0.65,
                                       )
    parent.frame_right.grid(row=0, column=1)
    parent.frame_right.grid_propagate(False)

def add_files(parent):
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("All files", "*"),)
                                          )
    
    if filename:
        reconstruct_frame_right(parent)
        
        ipfs_add = cmd(f'ipfs add {filename}').stdout.decode()
        
        with open ("ipfs_added_list.txt", "a") as f:
            f.write(filename.split("/")[-1] + "  >  " + ipfs_add.split()[1] + "\n")
            
        ipfs_add = f"{filename} added to IPFS\n\n {ipfs_add.split()[1]}"
        
        main_label(parent, 0, ipfs_add)
    
def view_files(parent):
    reconstruct_frame_right(parent)
    
    with open ("ipfs_added_list.txt", "r") as f:
        line_count=0
        for line in f:
            main_label(parent, line_count, line)
            qr_buttons(parent, line_count)
            line_count+=1

def qr_buttons(parent, count):
    parent.button_view_files = tk.Button(parent.frame_right,
                                         text="QR",
                                         command=do_nothing,
                                         borderwidth=1,
                                         relief="solid",
                                         )
    parent.button_view_files.grid(row=count, column=1)
