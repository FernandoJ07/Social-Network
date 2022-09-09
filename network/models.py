from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_user')

    def __str__(self):
        return self.content
        
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, blank=True, related_name= "followers")

    def __str__(self):
        return self.user.username