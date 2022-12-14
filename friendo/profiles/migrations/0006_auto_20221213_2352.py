# Generated by Django 2.2 on 2022-12-13 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20221213_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hobbies',
            field=models.ManyToManyField(null=True, related_name='profiles', to='profiles.Hobby'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=models.ManyToManyField(null=True, related_name='profiles', to='profiles.Interest'),
        ),
    ]