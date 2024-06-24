from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=280, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    likes = models.PositiveIntegerField(default=0)

class Follow(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="follower")
    following_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.user} follows {self.following_user}"

class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="user")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name="post")
    
    def __str__(self):
        return f"{self.user} likes {self.post}"