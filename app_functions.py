# Some system might have to run this command with sudo.
# sysctl -w net.core.rmem_max=2500000
# Please visit the following website to read more about the issue.
# https://github.com/lucas-clemente/quic-go/wiki/UDP-Receive-Buffer-Size

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from app_banner import *
from popup import *
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

    parent.ipfs_status.config(text="IPFS daemon status: Running\nPID: "
                                   + str(cmd('pidof ipfs').stdout.decode())[0:-1],
                              fg="#1e961c",
                              )
    parent.ipfs_status.config()

    parent.button_start.config(state="disable")
    parent.button_stop.config(state="active")


def stop_ipfs(parent):
    pid_ipfs = cmd('pidof ipfs').stdout.decode()
    cmd('kill `pidof ipfs`')

    parent.ipfs_status.config(text="IPFS daemon status: Stopped\n PID: "
                                   + pid_ipfs[0:-1],
                              fg="#FF0000",
                              )

    parent.button_start.config(state="active")
    parent.button_stop.config(state="disable")


def reconsruct_right_frame(parent):
    parent.frame_right.destroy()

    parent.frame_right = LabelFrame(parent.main_frame,
                                    text="Interface",
                                    padx=10,
                                    pady=5,
                                    relief="solid",
                                    width=parent.width*0.70,
                                    height=parent.height*0.65
                                    )
    parent.frame_right.grid(row=0, column=1)
    parent.frame_right.grid_propagate(False)


def add_files(parent):
    reconsruct_right_frame(parent)

    parent.filename = filedialog.askopenfilename(initialdir="./",
                                                 title="Select a File",
                                                 filetypes=(
                                                     ("All files", "*"),)
                                                 )

    if parent.filename:
        parent.ipfs_added = cmd(f'ipfs add {parent.filename}').stdout.decode()

        with open("ipfs_added_list.txt", "a") as f:
            f.write(parent.filename.split("/")[-1] +
                    "  >  " + parent.ipfs_added.split()[1] + "\n")

        Label(parent.frame_right,
              foreground="#1e961c",
              text="File added to IPFS",
              bd=2,
              relief="ridge",
              pady=5,
              ).grid(row=0, column=0, sticky="news")

        Label(parent.frame_right,
              text=parent.filename,
              bd=2,
              relief="ridge",
              pady=5,
              ).grid(row=1, column=0, sticky="news")

        Label(parent.frame_right,
              text="",
              ).grid(row=2, column=0, sticky="news")

        Label(parent.frame_right,
              foreground="#1e961c",
              text="Hash",
              bd=2,
              relief="ridge",
              pady=5,
              ).grid(row=3, column=0, sticky="news")

        Label(parent.frame_right,
              text=parent.ipfs_added.split()[1],
              bd=2,
              relief="ridge",
              pady=5,
              ).grid(row=4, column=0, sticky="news")


def view_files(parent):
    reconsruct_right_frame(parent)

    parent.canvas_frame = LabelFrame(parent.frame_right,
                                     bd=2,
                                     relief="sunken",
                                     width=parent.width*.65,
                                     height=parent.height*0.55,
                                     )
    parent.canvas_frame.grid(row=0, column=0,)

    parent.canvas = Canvas(parent.canvas_frame,
                           width=parent.width*.65,
                           height=parent.height*0.55,
                           )
    parent.canvas.grid(row=0, column=0,)

    parent.x_scroll = ttk.Scrollbar(parent.canvas_frame,
                                    orient=HORIZONTAL,
                                    command=parent.canvas.xview)
    parent.x_scroll.grid(row=1, column=0, sticky="nwse")

    parent.y_scroll = ttk.Scrollbar(parent.canvas_frame,
                                    orient=VERTICAL,
                                    command=parent.canvas.yview)
    parent.y_scroll.grid(row=0, column=1, sticky="nwse")

    parent.canvas.configure(xscrollcommand=parent.x_scroll.set,
                            yscrollcommand=parent.y_scroll.set,
                            )
    parent.canvas.bind('<Configure>', lambda e: parent.canvas.configure(
        scrollregion=parent.canvas.bbox("all")))

    parent.canvas_frame_in = Frame(parent.canvas)

    parent.canvas.create_window(
        (0, 0), window=parent.canvas_frame_in, anchor="nw")

    with open("ipfs_added_list.txt", "r") as f:
        line_count = 0
        for line in f:
            parent.label1 = Label(parent.canvas_frame_in,
                                  cursor="hand2",
                                  text=line.strip(),
                                  foreground="#0000FF",
                                  bd=2,
                                  relief="solid",
                                  padx=10,
                                  pady=5,
                                  )
            parent.label1.grid(row=line_count, column=0, pady=10, sticky="w")
            parent.label1.bind("<Button-1>",
                               lambda event: popup(parent, line))

            line_count += 1
