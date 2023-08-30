# Generated by Django 3.2.20 on 2023-08-24 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('estacion', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('coodenadas', models.CharField(max_length=50)),
                ('seguimiento', models.FloatField(null=True)),
                ('prealerta', models.FloatField(null=True)),
                ('alerta', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.FloatField(null=True)),
                ('humedad', models.FloatField(null=True)),
                ('precipitacion', models.FloatField(null=True)),
                ('nivel', models.FloatField(null=True)),
                ('caudal', models.FloatField(null=True)),
                ('radiacion', models.FloatField(null=True)),
                ('fecha', models.DateTimeField()),
                ('estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appAPI.code')),
            ],
        ),
    ]