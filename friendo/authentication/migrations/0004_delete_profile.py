# Generated by Django 2.2 on 2022-12-13 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_profile_handle'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]