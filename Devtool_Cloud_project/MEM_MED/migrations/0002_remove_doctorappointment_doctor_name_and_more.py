# Generated by Django 5.1.2 on 2024-11-01 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MEM_MED', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorappointment',
            name='doctor_name',
        ),
        migrations.AlterField(
            model_name='doctorappointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='MEM_MED.patient'),
        ),
        migrations.AlterField(
            model_name='medicationschedule',
            name='is_eaten',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('birthdate', models.DateField()),
                ('expertise', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='doctorappointment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='MEM_MED.doctor'),
        ),
        migrations.CreateModel(
            name='SideEffect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('detail', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MEM_MED.patient')),
            ],
        ),
    ]
