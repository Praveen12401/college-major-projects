# Generated by Django 4.2.7 on 2024-03-28 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servise', '0017_rename_projects_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_photo',
            field=models.ImageField(default=None, upload_to='photo/'),
        ),
    ]
