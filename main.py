#Version 1.1
import re
from string import ascii_letters
import sys
import time
import tkinter as tk
import urllib.request
from tkinter import Label, ttk
from MiDat import socio
from PIL import Image, ImageTk

#Ajustes locales
puerta="01"
url_a="http://www.ceeldense.es/cee_2/qazxsw84/foto/socee/"
hfoto=180 #alto de la foto
wmax=hfoto/1.4 #Ancho a partir del que la foto se recorta
lico=150 #Medidas de icono informativo

#Creación del formulario
ventana=tk.Tk()
ventana.title("CONTROL DE ACCESOS")
ventana.geometry("800x400")
ventana.resizable(True,True)
ventana.attributes('-fullscreen',True)

#Cuadros de texto
res=tk.StringVar()
fecha = ttk.Label()
nombre=ttk.Label(font=('Arial',36))
apellido=ttk.Label(font=('Arial',36))
datos=ttk.Label()
msg=ttk.Label(font=('Arial',36))
iminf=ttk.Label()

#Cuadro de texto capturar entrada de lector o manual
chip=ttk.Entry(textvariable=res)

# Posicionar cuadros de texto
nombre.place(x=150,y=30)
apellido.place(x=150,y=80)
fecha.place(x=0,y=300)
chip.place(x=10,y=360)
datos.place(x=30,y=300)
msg.place(x=10,y=300)

#Foco a entrada de chip
chip.focus_set()   

def borrar():
   fecha.configure(text="")
   nombre.configure(text="")
   apellido.configure(text="")
   datos.configure(text="")
   msg.configure(text="")
   chip.delete("0","end")
   foto_socio("sin-imagen.jpg")
   icoinfo('borra')

def icoinfo(ep):
   #Icono informativo cambia segun el estado del socio
   global imx
   if ep=="11":
         im=ajustar_imagen(lico,lico,Image.open('verde.jpg'))
         imx = ImageTk.PhotoImage(im)
         iminf.config(image=imx)
   elif ep=="borra":
         im=ajustar_imagen(lico,lico,Image.open('nada.jpg'))
         imx = ImageTk.PhotoImage(im)
         iminf.config(image=imx)
   else:
         im=ajustar_imagen(lico,lico,Image.open('rojo.jpg'))
         imx = ImageTk.PhotoImage(im)
         iminf.config(image=imx)
     
def estado(caso):
   if caso=="00":
     ret="no esta dado de alta"
   elif caso=="11":
      ret="correcto "
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
   imagen = imagen.resize((w, alto),Image.NEAREST)
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
fotosocio.place(x=10,y=10)

im=ajustar_imagen(lico,lico,Image.open('nada.jpg'))
imx = ImageTk.PhotoImage(im)
iminf=Label(ventana, image=imx)
iminf.place(x=250,y=210)

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
            icoinfo("rojo")        
      else:
         rpuerta=str(rsocio.at[0,"torn_pu"+puerta])
         nombre.configure(text=rsocio.at[0,"torn_nomb"])
         apellido.configure(text=rsocio.at[0,"torn_apel"])
         #Estado del socio con respecto a la puerta
         msg.configure(text=estado(rpuerta))
         foto_socio(rsocio.at[0,"torn_foto"])
         icoinfo(rpuerta)
   else:
      if numchip=="v":
         ventana.attributes('-fullscreen',False)
      elif numchip=="q":
         sys.exit()

   
   ventana.after(3000,borrar)

chip.focus_set
chip.bind("<Return>", resultado)
ventana.mainloop() 