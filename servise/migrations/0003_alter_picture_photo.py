# Generated by Django 4.2.7 on 2024-01-08 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servise', '0002_alter_picture_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='photo',
            field=models.ImageField(upload_to='mysite/static/images'),
        ),
    ]