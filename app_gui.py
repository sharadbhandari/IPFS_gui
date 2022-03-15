from app_functions import *
from app_banner import *


def main():
    root = Tk()
    main_gui(root, 900, 600, "IPFS file exchange")

    stl = ttk.Style()
    stl.theme_use('clam')
    stl.configure('Treeview')

    root.mainloop()


class main_gui:
    def __init__(self, parent, width, height, title):
        self.parent = parent
        self.width = width
        self.height = height
        self.parent.geometry(f"{str(self.width)}x{str(self.height)}")
        self.parent.title("IPFS file share")

        self.main_frame = Frame(self.parent)
        self.main_frame.grid(padx=self.width*0.022,
                             pady=self.height*0.05,
                             )

        self.frame_left = LabelFrame(self.main_frame,
                                     text="Menu",
                                     relief="solid",
                                     padx=10,
                                     width=self.width*0.20,
                                     height=self.height*0.81,
                                     )
        self.frame_left.grid(row=0, column=0, rowspan=2, padx=15)
        self.frame_left.grid_propagate(False)

        self.button_add_files = Button(self.frame_left,
                                       text="Add file",
                                       command=lambda: add_files(self),
                                       borderwidth=3,
                                       width=int(self.width*0.02),
                                       relief="solid",
                                       )
        self.button_add_files.grid(row=0, column=0)

        self.button_fetch_files = Button(self.frame_left,
                                         text="Fetch file",
                                         command=lambda: fetch_file(self),
                                         borderwidth=3,
                                         width=int(self.width*0.02),
                                         relief="solid",
                                         )
        self.button_fetch_files.grid(row=1, column=0)

        self.button_view_files = Button(self.frame_left,
                                        text="View files",
                                        command=lambda: view_files(self),
                                        borderwidth=3,
                                        width=int(self.width*0.02),
                                        relief="solid",
                                        )
        self.button_view_files.grid(row=2, column=0)

        self.button_pin_files = Button(self.frame_left,
                                       text="Pin file",
                                       command=lambda: to_be_added(self),
                                       borderwidth=1,
                                       width=int(self.width*0.02),
                                       relief="solid",
                                       )
        self.button_pin_files.grid(row=3, column=0)

        self.view_peers = Button(self.frame_left,
                                 text="View peers",
                                 command=lambda: to_be_added(self),
                                 borderwidth=1,
                                 width=int(self.width*0.02),
                                 relief="solid",
                                 )
        self.view_peers.grid(row=4, column=0)

        self.frame_right = LabelFrame(self.main_frame,
                                      text="Interface",
                                      relief="solid",
                                      width=self.width*0.70,
                                      height=self.height*0.65,
                                      )
        self.frame_right.grid(row=0, column=1)
        self.frame_right.grid_propagate(False)

        self.banner = Label(self.frame_right,
                            text=banner,
                            padx=125,
                            pady=50,
                            justify="center",
                            )
        self.banner.grid()

        self.frame_bottom = LabelFrame(self.main_frame,
                                       text="IPFS status",
                                       padx=20,
                                       pady=5,
                                       relief="solid",
                                       width=self.width*0.70,
                                       height=self.height*0.16,
                                       )
        self.frame_bottom.grid(row=1, column=1)
        self.frame_bottom.grid_propagate(False)

        self.button_start = Button(self.frame_bottom,
                                   text="Start IPFS",
                                   command=lambda: start_ipfs(self),
                                   borderwidth=2,
                                   width=int(self.width*0.023),
                                   relief="solid",
                                   state="disable" if (
                                       cmd('pidof ipfs').returncode == 0) else "active",
                                   )
        self.button_start.grid(row=0, column=0)

        self.button_stop = Button(self.frame_bottom,
                                  text="Stop IPFS",
                                  command=lambda: stop_ipfs(self),
                                  borderwidth=2,
                                  width=int(self.width*0.023),
                                  relief="solid",
                                  state="disable" if (
                                      cmd('pidof ipfs').returncode == 1) else "active"
                                  )
        self.button_stop.grid(row=1, column=0)

        if cmd('pidof ipfs').returncode == 0:
            self.ipfs_status = Label(self.frame_bottom,
                                     text="IPFS daemon status: Running\nPID: "
                                     + str(cmd('pidof ipfs').stdout.decode())[0:-1],
                                     borderwidth=6,
                                     padx=25,
                                     relief="ridge",
                                     fg="#1e961c"
                                     )
        else:
            self.ipfs_status = Label(self.frame_bottom,
                                     text="IPFS daemon status: Stopped",
                                     borderwidth=6,
                                     padx=25,
                                     relief="ridge",
                                     fg="#FF0000",
                                     )

        self.ipfs_status.grid(row=0, column=1, rowspan=2, padx=20)

        self.button_view_files = Button(self.main_frame,
                                        text="Exit App",
                                        command=exit,
                                        borderwidth=2,
                                        width=int(self.width*0.02),
                                        relief="solid",
                                        )
        self.button_view_files.grid(row=2, column=1, sticky="e", pady=8)


if __name__ == "__main__":
    main()
