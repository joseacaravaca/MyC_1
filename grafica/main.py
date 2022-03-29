from ntpath import join
from numpy import True_
from MiDat import socio
import re
import requests as req
from PIL import Image
from io import BytesIO
from tkinter import END, Entry, Frame,Label, PhotoImage, Tk, mainloop
from PIL import Image, ImageTk


url_a="http://www.ceeldense.es/cee_2/qazxsw84/foto/socee/"

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


if __name__ == '__main__':
    while True:
        cad=input()
        p=re.compile("\d")
        chip ="".join(p.findall(cad))[-6:]
        s=socio(chip,"01")
        if s.empty:
            print ("socio no encontrado")
        else:
            print (s)
            urlx=url_a + s.at[0,"torn_foto"] 
            response = req.get(urlx)
            #image = Image.open(BytesIO(response.content))
            #image.show()
            frm_c()

