# Generated by Django 4.2.7 on 2024-01-14 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servise', '0005_rename_title_picture_job_profile_alter_picture_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='photo',
            field=models.ImageField(default='', upload_to='media/images'),
        ),
    ]
