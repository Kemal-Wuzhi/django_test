# Generated by Django 4.2.11 on 2024-04-09 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]