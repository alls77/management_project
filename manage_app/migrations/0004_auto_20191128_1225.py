# Generated by Django 2.2.7 on 2019-11-28 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_app', '0003_auto_20191126_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='workplace',
        ),
        migrations.AddField(
            model_name='workplace',
            name='worker',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workplace', to='manage_app.Worker'),
        ),
    ]
