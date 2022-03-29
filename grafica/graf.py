from tkinter import END, Entry, Frame,Label, PhotoImage, Tk, mainloop
from PIL import Image, ImageTk


def frm_c():
    frm=Tk()
    frm.config(bg='white')
    frm.geometry('600x400')
    frm.resizable(0,0)
    frm.title('CONTROL DE ACCESOS')
    im=Image.open(r'/home/jacv/GitHub/MyC_1/grafica/fresa.jpg')
    h=im.height
    w=im.width
    e=h/w
    nh=85 #altura de la imagen
    im=im.resize([nh,int(nh*e)])
    im_=ImageTk.PhotoImage(im)
    fondo=Label(frm,image=im_).place(x=0,y=0)
    frm.mainloop()