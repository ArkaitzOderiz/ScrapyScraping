import json

jsonsDir = [
    "Scrapy/aemet/datos_aement.json",
    "Scrapy/chcantabrico/datos_nivel_chcantabrico.json",
    "Scrapy/chcantabrico/datos_pluvio_chcantabrico.json",
    "Scrapy/aguaEnNavarra/datos_aguaEnNavarra.json",
    "Scrapy/meteoNavarra/datos_meteoNavarra.json",
]

for dataJSON in jsonsDir:
    formatedJSON = []
    with open(dataJSON, "r", encoding="utf-8") as f:
        file = json.loads(f.read())
        newLine = []
        for line in file:
            data = {}




def checkKey(dic, key):
    if key in dic.keys():
        print("Present, ", end =" ")
        print("value =", dic[key])
    else:
        print("Not present")
precipitacion mm float
nivel m float
caudal m^3/s float
radiacion W/m^2 float
fecha datetime