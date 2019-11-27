# Generated by Django 2.2.7 on 2019-11-26 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='workplace',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='manage_app.Workplace'),
        ),
    ]
