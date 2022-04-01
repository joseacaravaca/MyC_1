#Version 1.0
from ast import If
import re
import time
import tkinter as tk
import urllib.request
from tkinter import NW, Label, LabelFrame, ttk
from MiDat import socio
from PIL import Image, ImageTk

#Ajustes locales
puerta="01"
url_a="http://www.ceeldense.es/cee_2/qazxsw84/foto/socee/"
hfoto=150 #alto de la foto
wmaxfoto=hfoto/1.4 #Ancho a partir del que la foto se recorta

#Creación del formulario
ventana=tk.Tk()
ventana.title("CONTROL DE ACCESOS")
ventana.geometry("600x400")
ventana.resizable(False,False)
ventana.attributes('-zoomed',False)

# FRAME FOTO
frame = LabelFrame(ventana, text='FOTO SOCIO')
frame.pack(anchor=NW)

#Cuadros de texto
res=tk.StringVar()
fecha = ttk.Entry()
nombre=ttk.Entry()
datos=ttk.Entry()
msg=ttk.Entry()

#Cuadro de texto capturar entrada de lector o manual
chip=ttk.Entry(textvariable=res)

# Posicionar cuadros de texto
fecha.pack()
chip.pack()
nombre.pack()
datos.pack()
msg.pack()

#Foco a entrada de chip
chip.focus_set()   

def borrar():
   fecha.delete("0","end")
   nombre.delete("0","end")
   datos.delete("0","end")
   msg.delete("0","end")
   chip.delete("0","end")
   foto_socio("sin-imagen.jpg")
   
def estado(caso):
   if caso=="00":
     ret="no esta dado de alta"
   elif caso=="11":
      ret="correcto"
   elif caso=="10":
      ret="cuota impagada"
   elif caso=="12":
      ret="bloqueado"
   else:
      ret="desconocido"
   return ret


# IMAGEN POR DEFECTO
PIL_image = Image.open('sin-imagen.jpg')
hpercen = (hfoto / float(PIL_image.size[1]))
w = int((float(PIL_image.size[0]) * float(hpercen)))
PIL_image = PIL_image.resize((w, hfoto),Image.NEAREST)
if PIL_image.width > wmaxfoto:
   l=(PIL_image.width-wmaxfoto)/2
   t=0
   r=l+wmaxfoto
   b=hfoto
   PIL_image=PIL_image.crop(l,t,r,b)

img = ImageTk.PhotoImage(PIL_image)
label2 = Label(frame, image=img)
label2.image = img  # keep a reference!
label2.pack()

#SHOW IMAGE IN FRAME
def foto_socio(rfoto):
    global img
    if rfoto=="sin-imagen.jpg":
      img = Image.open('sin-imagen.jpg')
      hpercen = (hfoto / float(img.size[1]))
      w = int((float(img.size[0]) * float(hpercen)))
      img = img.resize((w, hfoto),Image.NEAREST)
      img = ImageTk.PhotoImage(img)
      label2.config(image=img)
    else:
        try:
            urllib.request.urlretrieve(url_a + rfoto, "tmp.jpg")
            img = Image.open('tmp.jpg')
            hpercen = (hfoto / float(img.size[1]))
            w = int((float(img.size[0]) * float(hpercen)))
            img = img.resize((w, hfoto),Image.NEAREST)
            img = ImageTk.PhotoImage(img)
            label2.config(image=img)
        except:
            foto_socio("sin-imagen.jpg")


#Funcion que se ejecuta al validar la entrada de chip
def resultado(event):
   fecha.insert(0,time.strftime("%I:%M:%S"))
   numchip=res.get()

   if numchip.isnumeric():   
      p=re.compile("\d")
      nchip="".join(p.findall(numchip))[-6:]
      rsocio=socio(nchip,puerta)

      if rsocio.empty:
            nombre.insert(0,"no encontrado")
            foto_socio("sin-imagen.jpg")
           
      else:
         nombre.insert(0,rsocio.at[0,"torn_nomb"] + " " +rsocio.at[0,"torn_apel"])
         #Estado del socio con respecto a la puerta
         msg.insert(0,estado(str(rsocio.at[0,"torn_pu"+puerta])))
         foto_socio(rsocio.at[0,"torn_foto"])
   ventana.after(3000,borrar)

chip.focus_set
chip.bind("<Return>", resultado)
ventana.mainloop() 