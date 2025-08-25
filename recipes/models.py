from django.db import models
from users.models import *

# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text="Time in minutes", default=0)
    cook_time = models.PositiveIntegerField(help_text="Time in minutes", default=0)
    servings = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='recipe/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_time(self):
        return self.prep_time + self.cook_time

    class Meta:
        db_table = "recipe"

    def __str__(self):
        return self.name