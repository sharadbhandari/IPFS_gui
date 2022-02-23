from app_functions import *
from app_banner import *

def main():
    root = tk.Tk()
    main_gui(root, 900, 600, "IPFS file exchange")
    root.mainloop()

class main_gui:
    def __init__(self, parent, width, height, title):
        self.parent = parent
        self.width = width
        self.height = height
        self.parent.geometry(f"{str(self.width)}x{str(self.height)}")
        
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.grid(padx=self.width*0.022, 
                             pady=self.height*0.05,
                             )
        
        self.frame_left = tk.LabelFrame(self.main_frame, 
                                       text="Menu",
                                       relief="solid",
                                       padx=10,
                                       width=self.width*0.20, 
                                       height=self.height*0.9,
                                       )
        self.frame_left.grid(row=0, column=0, rowspan=2, padx=15)
        self.frame_left.grid_propagate(False) 
        
        self.button_add_files = tk.Button(self.frame_left,
                                         text="Add file",
                                         command=lambda:add_files(self),
                                         borderwidth=1,
                                         width=int(self.width*0.02),
                                         relief="solid",
                                         )
        self.button_add_files.grid(row=0, column=0, )
        
        self.button_view_files = tk.Button(self.frame_left,
                                    text="View files",
                                    command=lambda:view_files(self),
                                    borderwidth=1,
                                    width=int(self.width*0.02),
                                    relief="solid",
                                    )
        self.button_view_files.grid(row=1, column=0)
        
        self.frame_right = tk.LabelFrame(self.main_frame, 
                                    text="Interface", 
                                    padx=10, 
                                    pady=10, 
                                    relief="solid",
                                    width=self.width*0.70, 
                                    height=self.height*0.65)
        self.frame_right.grid(row=0, column=1)
        self.frame_right.grid_propagate(False)

        self.frame_right_bottom = tk.LabelFrame(self.main_frame, 
                                        text="IPFS status",
                                        padx=20,
                                        pady=5,
                                        relief="solid",
                                        width=self.width*0.70, 
                                        height=self.height*0.25)
        self.frame_right_bottom.grid(row=1, column=1)
        self.frame_right_bottom.grid_propagate(False)
        
        self.banner = tk.Label(self.frame_right,
                    text=banner,
                    padx=125, 
                    pady=50,
                    justify="center"
                    )
        self.banner.grid()

        self.button_start = tk.Button(self.frame_right_bottom,
                    text="Start IPFS",
                    command=lambda:start_ipfs(self),
                    borderwidth=2,
                    width=int(self.width*0.023),
                    relief="solid",
                    state="disable" if (cmd('pidof ipfs').returncode == 0) else "active"
                    )
        self.button_start.grid(row=0, column=0)
        
        self.button_stop = tk.Button(self.frame_right_bottom,
                                text="Stop IPFS",
                                command=lambda:stop_ipfs(self),
                                borderwidth=2,
                                width=int(self.width*0.023),
                                relief="solid",
                                state="disable" if (cmd('pidof ipfs').returncode == 1) else "active"
                                )
        self.button_stop.grid(row=1, column=0)
        
        if cmd('pidof ipfs').returncode == 0:
            self.ipfs_status = tk.Label(self.frame_right_bottom,
                                text="IPFS daemon status: Running\nPID: " \
                                + str(cmd('pidof ipfs').stdout.decode())[0:-1],
                                borderwidth=6,
                                padx=25,
                                relief="ridge",
                                fg="#1e961c"
                                )
        else:
            self.ipfs_status = tk.Label(self.frame_right_bottom,
                                text="IPFS daemon status: Stopped",
                                borderwidth=6,
                                padx=25,
                                relief="ridge",
                                fg="#FF0000",
                                )

        self.ipfs_status.grid(row=0, column=1, rowspan=2, padx=20)
            


if __name__ == "__main__":
    main()