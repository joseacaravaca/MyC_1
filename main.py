from ntpath import join
from numpy import True_
from MiDat import socio
import re
import requests as req
from PIL import Image
from io import BytesIO

url_a="http://www.ceeldense.es/cee_2/qazxsw84/foto/socee/"

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
            image = Image.open(BytesIO(response.content))
            image.show()
    