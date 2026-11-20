from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    def __str__(self): return self.user.username
@receiver(post_save, sender=User)
def make_profile(sender, instance, created, **kw):
    if created: Profile.objects.create(user=instance)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=500)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created']
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
