#Version 1.0
from io import BytesIO
import re
import time
import tkinter as tk
from tkinter import ttk
import requests as req
from MiDat import socio
from PIL import Image, ImageTk

#Ajustes locales
puerta="01"
url_a="http://www.ceeldense.es/cee_2/qazxsw84/foto/socee/"

#Creación del formulario
ventana=tk.Tk()
ventana.title("CONTROL DE ACCESOS")
ventana.geometry("600x400")
ventana.resizable(False,False)

#Cuadros de texto
res=tk.StringVar()
fecha = ttk.Entry()
nombre=ttk.Entry()
datos=ttk.Entry()
msg=ttk.Entry()
#Cuadro de texto capturar entrada de lector o manual
chip=ttk.Entry(textvariable=res)

# Posicionar cuadros de texto
fecha.place(x=50, y=50)
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
           
      else:
         nombre.insert(0,rsocio.at[0,"torn_nomb"] + " " +rsocio.at[0,"torn_apel"])
         #Estado del socio con respecto a la puerta
         msg.insert(0,estado(str(rsocio.at[0,"torn_pu"+puerta])))
   ventana.after(3000,borrar)

chip.focus_set
chip.bind("<Return>", resultado)
ventana.mainloop() 