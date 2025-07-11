# Generated by Django 4.2.7 on 2025-05-29 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dissalinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Dessalinizador',
                'verbose_name_plural': 'Dessalinizadores',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Região',
                'verbose_name_plural': 'Regiões',
            },
        ),
        migrations.CreateModel(
            name='Reservoir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Reservatório',
                'verbose_name_plural': 'Reservatórios',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sensor_type', models.CharField(choices=[('temperature', 'Temperatura'), ('ph', 'pH'), ('salinity', 'Salinidade'), ('flow', 'Fluxo'), ('pressure', 'Pressão'), ('level', 'Nível')], max_length=20)),
                ('unit', models.CharField(max_length=10)),
                ('min_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dissalinator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='monitoring.dissalinator')),
                ('reservoir', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='monitoring.reservoir')),
            ],
            options={
                'verbose_name': 'Sensor',
                'verbose_name_plural': 'Sensores',
            },
        ),
        migrations.CreateModel(
            name='WaterWell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('depth', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Poço de Água',
                'verbose_name_plural': 'Poços de Água',
            },
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='monitoring.sensor')),
            ],
            options={
                'verbose_name': 'Leitura do Sensor',
                'verbose_name_plural': 'Leituras dos Sensores',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='sensor',
            name='water_well',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='monitoring.waterwell'),
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('plant_type', models.CharField(choices=[('small', 'Pequena'), ('medium', 'Média'), ('large', 'Grande')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.address')),
                ('dissalinator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoring.dissalinator')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.region')),
                ('reservoir', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoring.reservoir')),
                ('water_well', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoring.waterwell')),
            ],
            options={
                'verbose_name': 'Planta de Dessalinização',
                'verbose_name_plural': 'Plantas de Dessalinização',
            },
        ),
    ]
