from tkinter import *
import qrcode
from PIL import ImageTk, Image


def qr_img(parent, data):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=2,
                       border=1,
                       )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    line = 1
    img.save("qr_image{0}.png".format(line))


def popup(parent, data):
    parent.top = Toplevel()

    frm = Frame(parent.top, bd=2, height=200, width=200, relief="solid")
    frm.grid()
    frm.grid_propagate(True)

    Label(frm,
          foreground="#1e961c",
          text="Filename",
          bd=1,
          relief="solid",
          #   width=27,
          ).grid(row=0, column=0, sticky="news")

    Label(frm,
          text="filename will go here",
          bd=1,
          relief="solid",
          ).grid(row=1, column=0, sticky="news")

    Label(frm,
          text="",
          ).grid(row=2, column=0, sticky="news")

    Label(frm,
          foreground="#1e961c",
          text="Hash",
          bd=1,
          relief="solid",
          ).grid(row=3, column=0, sticky="news")

    Label(frm,
          text="hash will go here",
          bd=1,
          relief="solid",
          ).grid(row=4, column=0, sticky="news")

    qr_img(parent, data)

    parent.img = Image.open("qr_image.png")
    parent.img = ImageTk.PhotoImage(
        parent.img.resize((196, 196), Image.ANTIALIAS))

    Label(frm,
          text="hash will go here",
          image=parent.img,
          bd=1,
          relief="solid",
          ).grid(row=5, column=0, sticky="news")

    Button(frm,
           text='EXIT',
           command=lambda: top_exit(parent),
           bd=1,
           foreground="#FF0000",
           relief="solid",
           ).grid(row=6, column=0, sticky="news")


def top_exit(parent):
    parent.top.destroy()