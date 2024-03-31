from django.db import models

# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_profile = models.CharField(max_length=1000)
    about_project = models.TextField()

    project_file = models.FileField(upload_to='project/', default=None)
    project_photo = models.ImageField(upload_to='photo/', default=None)

    def __str__(self):
        return self.project_name
     
 
  
