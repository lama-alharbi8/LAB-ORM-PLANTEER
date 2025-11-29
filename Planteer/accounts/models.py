from django.db import models
from django.contrib.auth.models import User
from plants.models import Plant

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models. TextField(blank=True)
    profile_image = models.ImageField(upload_to="images/profile_image/", default ="images/profile_image/profile_image.jpg")

    def __str__(self):
        return f'Profile {self.user.username}'
    

class Favorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
