from django.db import models

# Create your models here.
class Picture(models.Model):
    name=models.CharField(max_length=50)
    job_profile=models.CharField(max_length=50)
    about=models.TextField()
    photo=models.ImageField(upload_to='images/',default=None) 

    
 

    def __str__(self):
        return self.name
     
 
  
