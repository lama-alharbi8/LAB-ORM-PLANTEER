from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):

    name = models.CharField(max_length=1024, unique=True)
    flag = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        TREE = 'tree', 'Tree'
        FRUIT = 'fruit', 'Fruit'
        VEGETABLE = 'vegetable', 'Vegetable'
        FLOWER = 'flower', 'Flower'
        HERB = 'herb', 'Herb'
        SUCCULENT = 'succulent', 'Succulent'

    name = models.CharField(max_length=2048)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    category = models.CharField(max_length=20)
    is_edible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.name

    def get_category_display(self):
        for choice_value, choice_label in self.CategoryChoices.choices:
            if self.category.lower() == choice_value:
                return choice_label
        return self.category
    
class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.plant.name}"
