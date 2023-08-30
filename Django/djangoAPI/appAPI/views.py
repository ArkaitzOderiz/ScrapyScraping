import json

from django.http import JsonResponse
from .models import Data, Code

# Create your views here.
def storeData(request):
    data = json.loads(request.body.decode("utf-8"))
    for estacion in data:
        for datos in estacion['datos']:
            dato = Data(
                temperatura=datos['temperatura (ºC)'],
                humedad=datos['humedad (%)'],
                precipitacion=datos['precipitacion (mm)'],
                nivel=datos['nivel (m)'],
                caudal=datos['caudal (m^3/s)'],
                radiacion=datos['radiacion (W/m^2)'],
                fecha=datos['fecha y hora'],
                estacion=estacion['estacion']
            )
            dato.save()
    return JsonResponse(data, safe=False)

def storeCode(request):
    data = json.loads(request.body.decode("utf-8"))
    for estacion in data:
        dato = Code(
            estacion=estacion['estacion'],
            codigo=estacion['codigo'],
            coodenadas=estacion['coodenadas'],
            seguimiento=estacion['seguimiento'],
            prealerta=estacion['prealerta'],
            alerta=estacion['alerta'],
        )
        dato.save()
    return JsonResponse(data, safe=False)