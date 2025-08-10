from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Post made by ' + self.author.username


class Comment(models.Model):
    post = models.ForeignKey(
            Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} commented something"


class Interaction(models.Model):
    Interaction_type = models.CharField(
            max_length=10, choices=[('LIKE', 'like'), ('SHARE', 'share')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Interaction_type + "on post " + str(self.post.id)


class Follow(models.Model):
    follower = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='followers_set')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
