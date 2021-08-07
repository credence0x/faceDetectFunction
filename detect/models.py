from django.db import models

class Old_image(models.Model):
    
    image          = models.ImageField(upload_to='old',null=True)
    new_image_file_name = models.CharField(max_length=1000000,null=True)


    

    

