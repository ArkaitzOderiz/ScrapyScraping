from django.db import models

# Create your models here.
class Data(models.Model):
    temperatura = models.FloatField(null=True)
    humedad = models.FloatField(null=True)
    precipitacion = models.FloatField(null=True)
    nivel = models.FloatField(null=True)
    caudal = models.FloatField(null=True)
    radiacion = models.FloatField(null=True)
    fecha = models.DateTimeField()
    estacion = models.ForeignKey("Code", on_delete=models.CASCADE)


class Code(models.Model):
    estacion = models.CharField(max_length=50)
    codigo = models.CharField(max_length=20, primary_key=True)
    coodenadas = models.CharField(max_length=50)
    seguimiento = models.FloatField(null=True)
    prealerta = models.FloatField(null=True)
    alerta = models.FloatField(null=True)