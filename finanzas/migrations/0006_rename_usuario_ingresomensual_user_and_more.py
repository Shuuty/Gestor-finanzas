# Generated by Django 5.2.3 on 2025-06-24 15:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0005_retiroahorro'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingresomensual',
            old_name='usuario',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='saldousuario',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
