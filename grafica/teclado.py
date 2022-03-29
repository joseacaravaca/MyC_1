import re
import time
import tkinter as tk
from tkinter import ttk
from xml.sax.handler import feature_validation

from soupsieve import select
from MiDat import socio
puerta="01"

ventana=tk.Tk()
ventana.title("CONTROL DE ACCESOS")
ventana.geometry("600x400")

res=tk.StringVar()
fecha = ttk.Entry()
nombre=ttk.Entry()
datos=ttk.Entry()
msg=ttk.Entry()
chip=ttk.Entry(textvariable=res)


# Posicionar
fecha.place(x=50, y=50)
chip.pack()
nombre.pack()
datos.pack()
msg.pack()
chip.focus_set()




def resultado(event):
   fecha.delete("0","end")
   nombre.delete("0","end")
   datos.delete("0","end")
   msg.delete("0","end")
   numchip=res.get()
   if numchip.isnumeric():   
      p=re.compile("\d")
      fecha.insert(0,time.strftime("%I:%M:%S"))
      nchip="".join(p.findall(numchip))[-6:]
      rsocio=socio(nchip,puerta)
      if rsocio.empty:
            nombre.insert(0,"CHIP:" + nchip + " -> no encontrado")
      else:
         nombre.insert(0,rsocio.at[0,"torn_nomb"] + " " +rsocio.at[0,"torn_apel"])
         chip.delete("0","end")
         #Estado del socio con respecto a la puerta
         msg.insert(0,estado(rsocio.at([0,"torn_pu"+ puerta])))
         


         chip.focus_set


chip.bind("<Return>", resultado)

ventana.mainloop()

def estado(caso):
   estado={
        "00":"no esta dado de alta",
        "11":"correcto",
        "10":"problema cuota",
         "12":"acceso denegado"}
