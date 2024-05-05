from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName
    
class Service(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True ,related_name="services")
    details=models.CharField(max_length=300, null=False, blank=False, default="")
    file = models.FileField(upload_to='create_service',null=True, blank=True)
    # file = models.FileField(upload_to='create_service',null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")

    def __str__(self):
        return str(self.category)
