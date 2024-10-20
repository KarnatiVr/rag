from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=200)
    document=models.FileField(upload_to='uploads/')

    def __str__(self) -> str:
        return f"{self.id}"

class Chat(models.Model):
    input=models.CharField(max_length=200)
    output=models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.id}"