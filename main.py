#Version 1.1
from ast import If
from cProfile import label
import re
import time
import tkinter as tk
import urllib.request
from tkinter import Label, ttk
from MiDat import socio
from PIL import Image, ImageTk

#Ajustes locales
puerta="01"
url_a="http://www.ceeldense.es/cee_2/qazxsw84/foto/socee/"
hfoto=150 #alto de la foto
wmax=hfoto/1.4 #Ancho a partir del que la foto se recorta

#Creación del formulario
ventana=tk.Tk()
ventana.title("CONTROL DE ACCESOS")
ventana.geometry("600x400")
ventana.resizable(False,False)
#ventana.attributes('-zoomed',False)


#Cuadros de texto
res=tk.StringVar()
fecha = ttk.Label()
nombre=ttk.Label(font=('Arial',20))
datos=ttk.Label()
msg=ttk.Label()
iminf=ttk.Label()

#Cuadro de texto capturar entrada de lector o manual
chip=ttk.Entry(textvariable=res)

# Posicionar cuadros de texto
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=4)

fecha.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
chip.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
nombre.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
datos.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
msg.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

#Foco a entrada de chip
chip.focus_set()   

def borrar():
   fecha.configure(text="")
   nombre.configure(text="")
   datos.configure(text="")
   msg.configure(text="")
   chip.delete("0","end")
   foto_socio("sin-imagen.jpg")

def iconoinformativo():
   img=ImageTk.PhotoImage(Image.open('ok.gif'))
   iminf=Label(ventana)
   iminf.image=img
   iminf(column=0, row=5, sticky=tk.W, padx=5, pady=5)
   
def estado(caso):
   if caso=="00":
     ret="no esta dado de alta"
   elif caso=="11":
      ret="correcto"
      iconoinformativo()
   elif caso=="10":
      ret="cuota impagada"
   elif caso=="12":
      ret="bloqueado"
   else:
      ret="desconocido"
   return ret

def ajustar_imagen(ancho,alto,imagen):
   hpercen = (alto/ float(imagen.size[1]))
   w = int((float(imagen.size[0]) * float(hpercen)))
   imagen = imagen.resize((w, hfoto),Image.NEAREST)
   if imagen.width > ancho:
      l=(imagen.width-ancho)/2
      t=0
      r=l+ancho
      b=alto
      imagen=imagen.crop((l,t,r,b))
      return imagen

# IMAGEN POR DEFECTO
PIL_image = ajustar_imagen(wmax,hfoto,Image.open('sin-imagen.jpg'))
img = ImageTk.PhotoImage(PIL_image)
fotosocio = Label(ventana, image=img)
fotosocio.image = img  # keep a reference!
fotosocio.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

#FOTO DE SOCIO
def foto_socio(rfoto):
    global img
    if rfoto=="sin-imagen.jpg":
      img =  ajustar_imagen(wmax,hfoto,Image.open('sin-imagen.jpg'))
      img = ImageTk.PhotoImage(img)
      fotosocio.config(image=img)
    else:
        try:
            urllib.request.urlretrieve(url_a + rfoto, "tmp.jpg")
            img = ajustar_imagen(wmax,hfoto,Image.open('tmp.jpg'))
            img = ImageTk.PhotoImage(img)
            fotosocio.config(image=img)
        except:
            img = ajustar_imagen(wmax,hfoto,Image.open('sin-imagen.jpg'))
            img = ImageTk.PhotoImage(img)
            fotosocio.config(image=img)


#Funcion que se ejecuta al validar la entrada de chip
def resultado(event):
   fecha.configure(text=time.strftime("%I:%M:%S"))
   numchip=res.get()

   if numchip.isnumeric():   
      p=re.compile("\d")
      nchip="".join(p.findall(numchip))[-6:]
      rsocio=socio(nchip,puerta)

      if rsocio.empty:
            nombre.configure(text="no encontrado")
            foto_socio("sin-imagen.jpg")
           
      else:
         nombre.configure(text=rsocio.at[0,"torn_nomb"] + " " +rsocio.at[0,"torn_apel"])
         #Estado del socio con respecto a la puerta
         msg.configure(text=estado(str(rsocio.at[0,"torn_pu"+puerta])))
         foto_socio(rsocio.at[0,"torn_foto"])
   ventana.after(3000,borrar)

chip.focus_set
chip.bind("<Return>", resultado)
ventana.mainloop() 