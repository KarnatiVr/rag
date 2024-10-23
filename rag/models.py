from django.db import models
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=200)
    document=models.FileField(upload_to='uploads/')
    chunks=models.JSONField(blank=True, null=True)
    def __str__(self) -> str:
        return f"{self.id}"

class Chat(models.Model):
    input=models.CharField(max_length=200)
    choice = models.CharField(max_length=200,blank=True,null=True)
    output=models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.id}"

class Chunk(models.Model):
    chunks=models.JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id}"

class chun(models.Model):
    chunks=models.JSONField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id}"