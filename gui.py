import cmd
import tkinter as tk
from tkinter import filedialog

def gui():    
    root_width = 800
    root_height = 600

    root = tk.Tk()
    root.geometry(f"{str(root_width)}x{str(root_height)}")
    root.title("IPFS file exchange")    
    
    global banner
    banner = """
                            ░▒█▀▀▄░█▀▀▄░█▀▀░█▀▀▄░▀█▀░█▀▀░█▀▄
                            ░▒█░░░░█▄▄▀░█▀▀░█▄▄█░░█░░█▀▀░█░█
                            ░▒█▄▄▀░▀░▀▀░▀▀▀░▀░░▀░░▀░░▀▀▀░▀▀░


                                                            ░█▀▀▄░█░░█
                                                            ░█▀▀▄░█▄▄█
                                                            ░▀▀▀▀░▄▄▄▀
                
                
                            ░▒█▀▀▀█░█░░░░█▀▀▄░█▀▀▄░█▀▀▄░█▀▄
                            ░░▀▀▀▄▄░█▀▀█░█▄▄█░█▄▄▀░█▄▄█░█░█
                            ░▒█▄▄▄█░▀░░▀░▀░░▀░▀░▀▀░▀░░▀░▀▀░
"""
    
    main_frame = tk.Label(root, text="Menu")
    main_frame.grid(padx=root_width*0.01, 
                    pady=root_height*0.05,
                    )
    
    frame_left = tk.LabelFrame(main_frame, 
                               text="Menu",
                               relief="solid",
                               width=root_width*0.20, 
                               height=root_height*0.9,
                               )
    frame_left.grid(row=0, column=0, rowspan=2, padx=15)
    frame_left.grid_propagate(False) 
    
    button_add_files = tk.Button(frame_left,
                                    text="Add file",
                                    command=add_files,
                                    borderwidth=2,
                                    width=int(root_width*0.020),
                                    relief="solid",
                                    )
    button_add_files.grid(row=0, column=0)
    
    button_view_files = tk.Button(frame_left,
                                    text="View files",
                                    command=view_files,
                                    borderwidth=2,
                                    width=int(root_width*0.020),
                                    relief="solid",
                                    )
    button_view_files.grid(row=1, column=0)
    
    global frame_right
    frame_right = tk.LabelFrame(main_frame, 
                                text="Interface", 
                                padx=10, 
                                pady=10, 
                                relief="solid",
                                width=root_width*0.70, 
                                height=root_height*0.65)
    frame_right.grid(row=0, column=1)
    frame_right.grid_propagate(False)
    global main_label
    
    main_label = tk.Label(frame_right,
                    text=banner,
                    justify="left"
                    # borderwidth=1,
                    # relief="solid",
                    # width=int(root_width*0.092),
                    # height=int(root_height*0.032),
                    )
    main_label.grid()
    main_label.grid_propagate(False)
    
    frame_right_bottom = tk.LabelFrame(main_frame, 
                                       text="IPFS status",
                                       padx=20,
                                       pady=5,
                                       relief="solid",
                                       width=root_width*0.70, 
                                       height=root_height*0.25)
    frame_right_bottom.grid(row=1, column=1)
    frame_right_bottom.grid_propagate(False)

    global button_start
    button_start = tk.Button(frame_right_bottom,
                    text="Start IPFS",
                    command=start_ipfs,
                    borderwidth=2,
                    width=int(root_width*0.020),
                    relief="solid",
                    state="disable" if (cmd.cmd('pidof ipfs').returncode == 0) else "active"
                    )
    button_start.grid(row=0, column=0)
    
    global button_stop
    button_stop = tk.Button(frame_right_bottom,
                    text="Stop IPFS",
                    command=stop_ipfs,
                    borderwidth=2,
                    width=int(root_width*0.020),
                    relief="solid",
                    state="disable" if (cmd.cmd('pidof ipfs').returncode == 1) else "active"
                    )
    button_stop.grid(row=1, column=0)
    
    global ipfs_status
    
    if cmd.cmd('pidof ipfs').returncode == 0:
        ipfs_status = tk.Label(frame_right_bottom,
                               text="IPFS daemon status: Running\nPID: " \
                               + str(cmd.cmd('pidof ipfs').stdout.decode())[0:-1],
                               borderwidth=6,
                               padx=25,
                               relief="ridge",
                               fg="#1e961c"
                               )
    else:
        ipfs_status = tk.Label(frame_right_bottom,
                               text="IPFS daemon status: Stopped",
                               borderwidth=6,
                               padx=25,
                               relief="ridge",
                               fg="#FF0000",
                               )

    ipfs_status.grid(row=0, column=1, rowspan=2, padx=20)
    
    
    root.mainloop()
    
def start_ipfs():
    cmd.cmd('ipfs init &')
    if cmd.cmd('pidof ipfs').returncode != 0:
        cmd.cmd('ipfs daemon > ipfs_start.log &')
    
    ipfs_status.config(text="IPFS daemon status: Running\nPID: " + str(cmd.cmd('pidof ipfs').stdout.decode())[0:-1],
                       borderwidth=6,
                       padx=25,
                       relief="ridge",
                       fg="#1e961c",
                       )
    
    button_start.config(state="disable")
    button_stop.config(state="active")
        
def stop_ipfs():
    pid_ipfs = cmd.cmd('pidof ipfs').stdout.decode()
    cmd.cmd('kill `pidof ipfs`')
    
    ipfs_status.config(text="IPFS daemon status: Stopped\n PID: " + pid_ipfs[0:-1],
                       borderwidth=6,
                       padx=25,
                       relief="ridge",
                       fg="#FF0000",
                       )
    
    button_start.config(state="active")
    button_stop.config(state="disable")

def add_files():
    filename = filedialog.askopenfilename(initialdir = "./",
                                          title = "Select a File",
                                          filetypes = (("All files", "*"),)
                                          )
    
    if filename:
        ipfs_add = cmd.cmd(f'ipfs add {filename}').stdout.decode()
        
        with open ("ipfs_added_list.txt", "a") as f:
            f.write(filename.split("/")[-1] + "  >  " + ipfs_add.split()[1] + "\n")
            
        ipfs_add = f"{filename} added to IPFS\n\n {ipfs_add.split()[1]}"
        
        main_label.config(text = ipfs_add)
        
    # code for browsing directory, if needed
    # filename = filedialog.askdirectory()
    # main_label.config(text=cmd.cmd(f"ls {filename}").stdout
    #                   )

def view_files():
    with open ("ipfs_added_list.txt", "r") as f:
            content = f.read()

    main_label.config(text = content)

if __name__=="__main__":
    gui()
