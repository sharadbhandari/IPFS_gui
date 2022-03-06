# Some system might have to run this command with sudo.
# sysctl -w net.core.rmem_max=2500000
# Please visit the following website to read more about the issue.
# https://github.com/lucas-clemente/quic-go/wiki/UDP-Receive-Buffer-Size

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from app_banner import *
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


def draw_qr_image(parent, line_count):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4,
                       )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("qr_image{}.png".format(line_count))


def get_qr_image(line_count):
    with open("ipfs_added_list.txt", "r") as f:
        tracked_line = 0
        for line in f:
            line_count += 1
            if tracked_line == line_count:
                print(line_count)


def view_files(parent):
    reconsruct_right_frame(parent)

    parent.tree_v = ttk.Treeview(parent.frame_right,
                                 columns=("1"),
                                 height=16,
                                 )
    parent.tree_v.grid()
    # parent.tree_v["columns"] = ("1")
    parent.tree_v.column("#0", anchor=CENTER)
    parent.tree_v.column("#1", anchor=CENTER, stretch=NO, width=400)

    parent.tree_v.heading("#0", text="Items", anchor=CENTER)
    parent.tree_v.heading("#1", text="Values", anchor=CENTER)

    with open("ipfs_added_list.txt", "r") as f:
        line_count = 0
        for line in f:
            parent.tree_v.insert("", 0, iid=line_count, text=line.split()[0])

            parent.tree_v.insert(
                line_count, "end", text="File name", values=(line.split()[0]))
            parent.tree_v.insert(
                line_count, "end", text="Hash", values=(line.split()[-1]))
            parent.tree_v.insert(
                line_count, 'end', text="Qr", values=(""))

            line_count += 1
