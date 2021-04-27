from django.db import models
from django.urls import reverse

class User(models.Model):
    username = models.CharField("User name", max_length=50)
    #username = models.CharField("User name", max_length=50)
    password = models.CharField("User password", max_length=50)

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("post_details", kwargs={"pk": self.pk})
        
    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    your_name = models.CharField(max_length=50)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return "%s -%s" % (self.post.title,  self.your_name)

    